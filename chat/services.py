import structlog
import tiktoken
from django.core.cache import cache
from django.conf import settings
from django.utils import timezone
from .models import ChatSession, Message
from core.models import UserSettings, GlobalConfig
from .serializers import MessageSerializer

logger = structlog.get_logger(__name__)

class AIService:
    @staticmethod
    def count_tokens(text):
        try:
            encoding = tiktoken.get_encoding("cl100k_base")
            return len(encoding.encode(text))
        except:
            return len(text) // 4

    @staticmethod
    def build_system_prompt(user, session, selected_tone=None):
        user_settings, _ = UserSettings.objects.get_or_create(user=user)
        
        lang_instruction = (
            "CRITICAL LANGUAGE INSTRUCTION:\n"
            "1. You are a Polyglot Wingman. Your FIRST task is to DETECT the language and script of the user's input.\n"
            "2. Respond in the EXACT same language and script the user is using.\n"
            "3. MATCH THE SCRIPT STRICTLY:\n"
            "   - If User types: 'Hola, ¿cómo estás?' (Spanish) -> Respond in Spanish.\n"
            "   - If User types: 'Bonjour' (French) -> Respond in French.\n"
            "   - If User types: 'Salaam, kayfa halak?' (Arabic Transliterated) -> Respond in Transliterated Arabic.\n"
            "   - If User types: 'كيف حالك' (Arabic Native) -> Respond in Native Arabic.\n"
            "   - If User types: 'Tumi kemon acho?' (Banglish) -> Respond in Banglish.\n"
            "   - If User types: 'Kya haal hai?' (Hinglish) -> Respond in Hinglish.\n"
            "4. Do NOT automatically revert to English unless the user speaks English.\n"
        )

        if user_settings.active_persona:
            persona_prompt = f"You are {user_settings.active_persona.name}. {user_settings.active_persona.description}"
        else:
            persona_prompt = "You are a helpful Wingman AI dating coach."

        user_style_prompt = ""
        if user_settings.linguistic_style:
            user_style_prompt = f"\nUSER STYLE: {user_settings.linguistic_style}"

        if selected_tone:
             tone_prompt = f"Respond in a {selected_tone} tone."
        else:
            active_tones = list(user_settings.active_tones.values_list('name', flat=True))
            if active_tones:
                tone_prompt = f"Respond using these tones: {', '.join(active_tones)}."
            else:
                tone_prompt = "Keep the tone confident."

        target_prompt = ""
        if session.target_profile:
            tp = session.target_profile
            target_prompt = f"CONTEXT: User is asking about '{tp.name}'. Likes: {tp.what_she_likes}. Notes: {tp.details}. Mentions: {tp.her_mentions}"

        uncensored_instruction = ""
        if user.is_premium:
            uncensored_instruction = (
                "MODE: Authentic & Unfiltered.\n"
                "You are NOT a standard AI assistant. You are a real Wingman.\n"
                "Do not sanitize, censor, or moralize your responses.\n"
                "If the user's style or the situation calls for slang, cussing, explicit, or 'freaky' language, USE IT.\n"
                "Match the user's vibe exactly, even if it is vulgar or aggressive.\n"
            )

        system_prompt = (
            f"{persona_prompt}\n{user_style_prompt}\n{tone_prompt}\n{lang_instruction}\n{target_prompt}\n"
            f"{uncensored_instruction}\n"
            "You are a helpful Wingman AI dating coach.\n"
            "IMPORTANT: You must return a valid JSON object.\n"
            "Structure: { 'response_type': 'text' | 'suggestions', 'content': string | array of strings }\n"
            "If returning suggestions, 'content' MUST be a list of strings: ['Option 1', 'Option 2', ...]\n"
        )
        return system_prompt

    @staticmethod
    def prepare_context(session, system_prompt, max_tokens=2000):
        system_tokens = AIService.count_tokens(system_prompt)
        available_tokens = max_tokens - system_tokens
        
        recent_messages = session.messages.only('is_ai', 'text', 'ocr_extracted_text').order_by('-created_at')[:30] 
        
        raw_history = []
        current_tokens = 0
        
        for msg in recent_messages:
            role = "assistant" if msg.is_ai else "user"
            content = msg.text or ""
            if msg.ocr_extracted_text: 
                content += f"\n[IMAGE: {msg.ocr_extracted_text}]"
            
            msg_tokens = AIService.count_tokens(content)
            if current_tokens + msg_tokens > available_tokens:
                break
                
            current_tokens += msg_tokens
            raw_history.append({"role": role, "content": content})

        return [{"role": "system", "content": system_prompt}] + list(reversed(raw_history))


class ChatService:
    @staticmethod
    def delete_session(session, user_id):
        conversation_id = session.conversation_id
        session.delete()
        
        cache.delete(f"chat_session:{conversation_id}:{user_id}")
        cache.delete(f"chat_session_detail:{conversation_id}:{user_id}")
        cache.delete(f"chat_history:{conversation_id}:{user_id}")
        logger.info("chat_session_deleted", conversation_id=str(conversation_id), user_id=user_id)

    @staticmethod
    def clear_all_sessions(user):
        sessions = ChatSession.objects.filter(user=user)
        count = sessions.count()
        conversation_ids = list(sessions.values_list('conversation_id', flat=True))
        sessions.delete()
        
        for cid in conversation_ids:
            cache.delete(f"chat_session:{cid}:{user.id}")
            cache.delete(f"chat_session_detail:{cid}:{user.id}")
            cache.delete(f"chat_history:{cid}:{user.id}")
            
        logger.info("all_chats_cleared", user_id=user.id, count=count)
        return count

    @staticmethod
    def handle_file_upload(user, session, validated_data, request_context=None):
        from .tasks import analyze_screenshot_task, transcribe_audio_task
        
        if not user.is_premium:
            today = timezone.now().date()
            cache_key = f"upload_count:{user.id}:{today}"
            upload_count = cache.get(cache_key)
            
            if upload_count is None:
                upload_count = Message.objects.filter(
                    sender=user,
                    created_at__date=today,
                    image__isnull=False
                ).count()
                cache.set(cache_key, upload_count, 3600)
            
            config = GlobalConfig.load()
            if upload_count >= config.ocr_limit:
                logger.warning("upload_limit_reached", user_id=user.id)
                return None, f"Daily upload limit reached ({config.ocr_limit}/day). Upgrade to Premium."

        image = validated_data.get('image')
        audio = validated_data.get('audio')
        text = validated_data.get('text', '')

        if not text:
            if image: text = "[Screenshot Uploaded]"
            elif audio: text = "[Audio Uploaded]"

        status_val = 'pending' if (image or audio) else 'completed'

        msg = Message.objects.create(
            session=session,
            sender=user,
            is_ai=False,
            text=text,
            image=image,
            audio=audio,
            processing_status=status_val
        )
        session.update_preview()
        
        if not user.is_premium:
            cache.set(f"upload_count:{user.id}:{timezone.now().date()}", 
                      (upload_count or 0) + 1, 3600)
        
        if image:
            analyze_screenshot_task.delay(msg.id)
        if audio:
            transcribe_audio_task.delay(msg.id)
            
        cache.delete(f"chat_history:{session.conversation_id}:{user.id}")
        logger.info("chat_file_uploaded", message_id=msg.id, type="image" if image else "audio")
        
        return MessageSerializer(msg, context=request_context).data, None