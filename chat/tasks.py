import json
import base64
import logging
from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.conf import settings
from django.core.cache import cache
from django.db import transaction
from openai import OpenAI, OpenAIError
from .models import ChatSession, Message, DetectedEvent
from core.models import UserSettings, TargetProfile
from core.utils import send_push_notification

logger = logging.getLogger(__name__)

MAX_RETRIES = 3
OPENAI_TIMEOUT = 30
MAX_HISTORY_MESSAGES = 20
MAX_TOKENS_GPT4 = 4000
MAX_TOKENS_MINI = 500

def send_ws_message(session_id, data):
    try:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'chat_{session_id}',
            {
                'type': 'chat_message',
                'conversation_id': str(session_id),
                'message': data
            }
        )
    except Exception as e:
        logger.error(f"Error sending WebSocket message: {e}")

@shared_task(
    bind=True,
    max_retries=MAX_RETRIES,
    default_retry_delay=5,
    autoretry_for=(OpenAIError,),
    retry_backoff=True
)
def generate_ai_response(self, session_id, user_text, selected_tone=None):
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    try:
        session = ChatSession.objects.select_related('user', 'target_profile').get(id=session_id)
        rate_limit_key = f"ai_response_rate:{session.user.id}"
        request_count = cache.get(rate_limit_key, 0)
        if not session.user.is_premium and request_count >= 10:
            send_ws_message(session.conversation_id, {'id': None, 'text': "Too fast. Please wait a moment.", 'is_ai': True, 'type': 'rate_limit'})
            return
        cache.set(rate_limit_key, request_count + 1, 60)
        user_settings = UserSettings.objects.select_related('active_persona').prefetch_related('active_tones').filter(user=session.user).first()
        if not user_settings:
            user_settings, _ = UserSettings.objects.get_or_create(user=session.user)
            
        lang_code = user_settings.language
        lang_name = dict(settings.LANGUAGES).get(lang_code, 'English')
        
        lang_instruction = f"Respond in {lang_name}."
        if lang_code == 'hi':
            lang_instruction = "Respond in Hinglish mixed with English where natural."

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
        if session.user.is_premium:
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

        recent_messages = session.messages.only('is_ai', 'text', 'ocr_extracted_text').order_by('-created_at')[:MAX_HISTORY_MESSAGES]
        history = []
        for msg in reversed(list(recent_messages)):
            role = "assistant" if msg.is_ai else "user"
            content = msg.text or ""
            if msg.ocr_extracted_text: content += f"\n[IMAGE: {msg.ocr_extracted_text}]"
            history.append({"role": role, "content": content})

        messages_payload = [{"role": "system", "content": system_prompt}] + history
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages_payload,
            max_tokens=MAX_TOKENS_GPT4,
            timeout=OPENAI_TIMEOUT,
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        
        ai_reply_json = response.choices[0].message.content
        tokens_used = response.usage.total_tokens if hasattr(response, 'usage') else 0
        
        with transaction.atomic():
            ai_msg = Message.objects.create(session=session, is_ai=True, text=ai_reply_json, tokens_used=tokens_used)
            session.update_preview()
        
        send_ws_message(session.conversation_id, {'id': ai_msg.id, 'text': ai_msg.text, 'is_ai': True, 'created_at': str(ai_msg.created_at)})
        cache.delete(f"chat_history:{session.conversation_id}")
        
        try:
            parsed_reply = json.loads(ai_reply_json)
            notification_body = parsed_reply.get('content', '')
            if isinstance(notification_body, list):
                notification_body = "Here are some suggestions for you."
        except:
            notification_body = "New message received"

        send_push_notification(
            session.user, 
            "AI Wingman Replied", 
            str(notification_body)[:100] + "...", 
            data={"conversation_id": str(session.conversation_id)}
        )
        
        time_keywords = ['tomorrow', 'tonight', 'meet', 'date', 'clock', 'pm', 'am', 'schedule']
        if any(word in user_text.lower() for word in time_keywords):
            intent_engine.delay(session.id, user_text)
        
        if session.target_profile:
            profile_target_engine.delay(session.id, user_text)

        user_msg_count = session.messages.filter(sender=session.user).count()
        if user_msg_count % 10 == 0:
            linguistic_engine.delay(session.user.id, session.id)
        
        return ai_msg.id

    except OpenAIError as e:
        logger.error(f"OpenAI API Error: {e}")
        send_ws_message(session.conversation_id, {'id': None, 'text': "AI Error.", 'is_ai': True, 'type': 'error'})
        raise self.retry(exc=e)
    except Exception as e:
        logger.error(f"AI Error: {e}", exc_info=True)
        send_ws_message(session.conversation_id, {'id': None, 'text': "System Error.", 'is_ai': True, 'type': 'error'})

@shared_task(bind=True, max_retries=2, autoretry_for=(OpenAIError,))
def analyze_screenshot_task(self, message_id):
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    try:
        message = Message.objects.select_related('session').get(id=message_id)
        if not message.image: return
        try:
            with message.image.open('rb') as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e: return

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": [{"type": "text", "text": "Extract text JSON"}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}]}] ,
            max_tokens=1000,
            response_format={"type": "json_object"}
        )
        ai_content = json.loads(response.choices[0].message.content)
        ocr_text = ai_content.get('extracted_text', '')
        message.ocr_extracted_text = ocr_text
        message.save(update_fields=['ocr_extracted_text'])
        cache.delete(f"chat_history:{message.session.conversation_id}")
        send_ws_message(message.session.conversation_id, {'id': message.id, 'type': 'analysis_complete', 'ocr_text': ocr_text})
        
    except Exception as e: logger.error(f"OCR Error: {e}")

@shared_task(bind=True, max_retries=2, autoretry_for=(OpenAIError,))
def profile_target_engine(self, session_id, latest_text):
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    try:
        with transaction.atomic():
            session = ChatSession.objects.select_related('target_profile').select_for_update().get(id=session_id)
            if not session.target_profile: 
                return
            
            tp = TargetProfile.objects.select_for_update().get(id=session.target_profile.id)
            prompt = f"Analyze about {tp.name}. New text from conversation: {latest_text}. Return JSON {{new_likes:[], new_preferences:[], new_mentions: string}}"
            response = client.chat.completions.create(
                model="gpt-4o-mini", 
                messages=[{"role": "user", "content": prompt}], 
                response_format={"type": "json_object"}
            )
            
            data = json.loads(response.choices[0].message.content)
            updated = False
            
            def add_if_new(source_list, new_items):
                has_change = False
                for item in new_items:
                    if item not in source_list:
                        source_list.append(item)
                        has_change = True
                return has_change

            if data.get('new_likes'):
                if add_if_new(tp.what_she_likes, data['new_likes']):
                    updated = True
                    
            if data.get('new_preferences'):
                if add_if_new(tp.preferences, data['new_preferences']):
                    updated = True
            
            if data.get('new_mentions'):
                if not tp.her_mentions:
                    tp.her_mentions = data['new_mentions']
                    updated = True
                elif data['new_mentions'] not in tp.her_mentions:
                    tp.her_mentions += f" | {data['new_mentions']}"
                    updated = True
                    
            if updated:
                tp.save()
                
    except Exception as e: 
        logger.error(f"Profile Error: {e}")

@shared_task(bind=True, max_retries=2, autoretry_for=(OpenAIError,))
def linguistic_engine(self, user_id, session_id):
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    try:
        user_settings, _ = UserSettings.objects.get_or_create(user_id=user_id)
        user_msgs = Message.objects.filter(sender_id=user_id, is_ai=False).only('text', 'ocr_extracted_text').order_by('-created_at')[:10]
        
        text_samples = []
        for m in user_msgs:
            if m.text: text_samples.append(m.text)
            if m.ocr_extracted_text: text_samples.append(f"[OCR]: {m.ocr_extracted_text}")
            
        full_sample = "\n".join(text_samples)
        if not full_sample: return
        
        prompt = f"Analyze style concisely (under 100 words): {full_sample[:2000]}"
        response = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}], max_tokens=150)
        user_settings.linguistic_style = response.choices[0].message.content.strip()
        user_settings.save()
    except Exception as e: logger.error(f"Linguistic Error: {e}")

@shared_task(bind=True, max_retries=2, autoretry_for=(OpenAIError,))
def intent_engine(self, session_id, user_text):
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    try:
        session = ChatSession.objects.select_related('user').get(id=session_id)
        existing_events = DetectedEvent.objects.filter(
            session__user=session.user, 
            is_cancelled=False
        ).order_by('-created_at')[:5]
        
        existing_list = []
        for e in existing_events:
            existing_list.append(f"- {e.title} at {e.start_time}")
        
        existing_context = "\n".join(existing_list)
        prompt = (
            f"User input: \"{user_text}\"\n"
            f"Existing Schedule:\n{existing_context}\n\n"
            "Task: Detect if this is a new plan/event.\n"
            "If yes, extract details and check if it conflicts/overlaps with the Existing Schedule.\n"
            "Return JSON: { \"is_event\": bool, \"title\": string, \"start_time\": string, \"description\": string, \"has_conflict\": bool, \"conflicting_with\": string }"
        )

        response = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}], response_format={"type": "json_object"})
        data = json.loads(response.choices[0].message.content)
        
        if data.get('is_event'):
            DetectedEvent.objects.create(
                session=session, 
                title=data.get('title', 'Event')[:255], 
                description=data.get('description', '')[:500], 
                start_time=data.get('start_time', '')[:100],
                has_conflict=data.get('has_conflict', False)
            )
            
            msg = f"Added {data.get('title')} to plan."
            if data.get('has_conflict'):
                msg += f" Warning: Double booking detected with {data.get('conflicting_with')}."
                
            send_push_notification(session.user, "Event Detected", msg)
            
    except Exception as e: logger.error(f"Intent Error: {e}")

@shared_task(bind=True, max_retries=2, autoretry_for=(OpenAIError,))
def generate_chat_title(self, session_id, first_message):
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    try:
        session = ChatSession.objects.get(id=session_id)
        response = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "system", "content": "3-5 word title"}, {"role": "user", "content": first_message[:200]}], max_tokens=20)
        title = response.choices[0].message.content.strip().replace('"', '')
        session.title = title[:252]
        session.save(update_fields=['title'])
    except Exception as e: pass