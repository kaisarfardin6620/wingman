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
from core.models import UserSettings

client = OpenAI(api_key=settings.OPENAI_API_KEY)
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
def generate_ai_response(self, session_id, user_text):
    try:
        session = ChatSession.objects.select_related(
            'user', 'target_profile'
        ).get(id=session_id)
        
        rate_limit_key = f"ai_response_rate:{session.user.id}"
        request_count = cache.get(rate_limit_key, 0)
        
        if not session.user.is_premium and request_count >= 10:
            send_ws_message(session.conversation_id, {
                'id': None,
                'text': "You're sending messages too quickly. Please wait a moment.",
                'is_ai': True,
                'type': 'rate_limit'
            })
            return
        
        cache.set(rate_limit_key, request_count + 1, 60)
        
        user_settings = UserSettings.objects.select_related(
            'active_persona'
        ).prefetch_related(
            'active_tones'
        ).filter(user=session.user).first()
        
        if not user_settings:
            user_settings, _ = UserSettings.objects.get_or_create(user=session.user)
        
        if user_settings.active_persona:
            persona_prompt = f"You are {user_settings.active_persona.name}. {user_settings.active_persona.description}"
        else:
            persona_prompt = "You are a helpful Wingman AI dating coach."

        user_style_prompt = ""
        if user_settings.linguistic_style:
            user_style_prompt = f"\nUSER STYLE FINGERPRINT: {user_settings.linguistic_style}"

        active_tones = list(user_settings.active_tones.values_list('name', flat=True))
        if active_tones:
            tone_prompt = f"Respond using these tones: {', '.join(active_tones)}."
        else:
            tone_prompt = "Keep the tone confident and supportive."

        target_prompt = ""
        if session.target_profile:
            tp = session.target_profile
            target_prompt = (
                f"CONTEXT: User is asking about '{tp.name}'.\n"
                f"She likes: {tp.what_she_likes or 'Unknown'}\n"
                f"Notes: {tp.details or ''} {tp.her_mentions or ''}"
            )

        system_prompt = (
            f"{persona_prompt}\n"
            f"{user_style_prompt}\n"
            f"{tone_prompt}\n"
            f"{target_prompt}\n"
            "Help the user with dating advice. If drafting texts, use their style."
        )

        recent_messages = session.messages.only(
            'is_ai', 'text', 'ocr_extracted_text'
        ).order_by('-created_at')[:MAX_HISTORY_MESSAGES]
        
        history = []
        for msg in reversed(list(recent_messages)):
            role = "assistant" if msg.is_ai else "user"
            content = msg.text or ""
            if msg.ocr_extracted_text:
                content += f"\n[IMAGE CONTEXT: {msg.ocr_extracted_text}]"
            history.append({"role": role, "content": content})

        messages_payload = [{"role": "system", "content": system_prompt}] + history
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages_payload,
            max_tokens=MAX_TOKENS_GPT4,
            timeout=OPENAI_TIMEOUT,
            temperature=0.7
        )
        
        ai_reply = response.choices[0].message.content
        tokens_used = response.usage.total_tokens if hasattr(response, 'usage') else 0
        
        with transaction.atomic():
            ai_msg = Message.objects.create(
                session=session,
                is_ai=True,
                text=ai_reply,
                tokens_used=tokens_used
            )
            
            session.update_preview()
        
        send_ws_message(session.conversation_id, {
            'id': ai_msg.id,
            'text': ai_msg.text,
            'is_ai': True,
            'created_at': str(ai_msg.created_at)
        })
        
        cache.delete(f"chat_history:{session.conversation_id}")
        
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
        logger.error(f"OpenAI API Error (session {session_id}): {e}")
        send_ws_message(session.conversation_id, {
            'id': None,
            'text': "I'm experiencing technical difficulties. Please try again in a moment.",
            'is_ai': True,
            'type': 'error'
        })
        raise self.retry(exc=e)
    
    except Exception as e:
        logger.error(f"AI Generation Error (session {session_id}): {e}", exc_info=True)
        send_ws_message(session.conversation_id, {
            'id': None,
            'text': "Sorry, something went wrong. Please try again.",
            'is_ai': True,
            'type': 'error'
        })

@shared_task(
    bind=True,
    max_retries=2,
    autoretry_for=(OpenAIError,)
)
def analyze_screenshot_task(self, message_id):
    try:
        message = Message.objects.select_related('session').get(id=message_id)
        
        if not message.image:
            return
        
        try:
            with message.image.open('rb') as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            logger.error(f"Failed to read image file for message {message_id}: {e}")
            return

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Extract all visible text from this image. Return JSON format: {\"extracted_text\": \"...\"}"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                                "detail": "high"
                            }
                        },
                    ],
                }
            ],
            max_tokens=1000,
            timeout=OPENAI_TIMEOUT,
            response_format={"type": "json_object"}
        )

        ai_content = json.loads(response.choices[0].message.content)
        ocr_text = ai_content.get('extracted_text', '')
        
        message.ocr_extracted_text = ocr_text
        message.save(update_fields=['ocr_extracted_text'])
        
        cache.delete(f"chat_history:{message.session.conversation_id}")
        
        send_ws_message(message.session.conversation_id, {
            'id': message.id,
            'type': 'analysis_complete',
            'ocr_text': ocr_text
        })
        
    except OpenAIError as e:
        logger.error(f"OpenAI OCR Error (message {message_id}): {e}")
        raise self.retry(exc=e)
    
    except Exception as e:
        logger.error(f"Screenshot Analysis Error (message {message_id}): {e}", exc_info=True)

@shared_task(
    bind=True,
    max_retries=2,
    autoretry_for=(OpenAIError,)
)
def profile_target_engine(self, session_id, latest_text):
    try:
        session = ChatSession.objects.select_related('target_profile').get(id=session_id)
        
        if not session.target_profile:
            return
        
        tp = session.target_profile
        
        prompt = (
            f"Analyze this message about '{tp.name}'. Extract NEW likes/preferences not already mentioned.\n"
            f"Current Likes: {tp.what_she_likes or 'None'}\n"
            f"User Message: \"{latest_text}\"\n"
            "Return JSON only: {\"new_likes\": [\"item1\", \"item2\"], \"new_preferences\": [\"pref1\"]}"
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=MAX_TOKENS_MINI,
            timeout=OPENAI_TIMEOUT,
            response_format={"type": "json_object"}
        )
        
        data = json.loads(response.choices[0].message.content)
        
        updated = False
        
        if data.get('new_likes') and isinstance(data['new_likes'], list):
            for item in data['new_likes']:
                if item and item not in (tp.what_she_likes or []):
                    if not tp.what_she_likes:
                        tp.what_she_likes = []
                    tp.what_she_likes.append(item)
                    updated = True
        
        if data.get('new_preferences') and isinstance(data['new_preferences'], list):
            for item in data['new_preferences']:
                if item and item not in (tp.preferences or []):
                    if not tp.preferences:
                        tp.preferences = []
                    tp.preferences.append(item)
                    updated = True

        if updated:
            tp.save(update_fields=['what_she_likes', 'preferences'])

    except OpenAIError as e:
        logger.error(f"OpenAI Profiling Error (session {session_id}): {e}")
        raise self.retry(exc=e)
    
    except Exception as e:
        logger.error(f"Profile Engine Error (session {session_id}): {e}", exc_info=True)

@shared_task(
    bind=True,
    max_retries=2,
    autoretry_for=(OpenAIError,)
)
def linguistic_engine(self, user_id, session_id):
    try:
        user_settings, _ = UserSettings.objects.get_or_create(user_id=user_id)
        user_msgs = Message.objects.filter(
            sender_id=user_id,
            is_ai=False
        ).only('text').order_by('-created_at')[:10]
        
        if not user_msgs:
            return
        
        text_sample = "\n".join([m.text for m in user_msgs if m.text])
        
        if not text_sample:
            return

        prompt = (
            "Analyze this person's texting style. Describe concisely:\n"
            "- Sentence length (short/long)\n"
            "- Capitalization patterns\n"
            "- Emoji usage\n"
            "- Tone (casual/formal/flirty)\n"
            "- Slang or unique phrases\n"
            "Keep response under 100 words.\n\n"
            f"Messages:\n{text_sample[:1000]}"
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            timeout=OPENAI_TIMEOUT,
            temperature=0.3
        )
        
        style_desc = response.choices[0].message.content.strip()
        user_settings.linguistic_style = style_desc
        user_settings.save(update_fields=['linguistic_style'])

    except OpenAIError as e:
        logger.error(f"OpenAI Linguistic Error (user {user_id}): {e}")
        raise self.retry(exc=e)
    
    except Exception as e:
        logger.error(f"Linguistic Engine Error (user {user_id}): {e}", exc_info=True)

@shared_task(
    bind=True,
    max_retries=2,
    autoretry_for=(OpenAIError,)
)
def intent_engine(self, session_id, user_text):
    try:
        session = ChatSession.objects.get(id=session_id)
        
        prompt = (
            "Does this message contain a concrete plan, meeting, or date?\n"
            f"Message: \"{user_text}\"\n"
            "Return JSON: {\"is_event\": true/false, \"title\": \"string\", \"start_time\": \"string\", \"description\": \"string\"}"
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            timeout=OPENAI_TIMEOUT,
            response_format={"type": "json_object"}
        )
        
        data = json.loads(response.choices[0].message.content)
        
        if data.get('is_event'):
            DetectedEvent.objects.create(
                session=session,
                title=data.get('title', 'New Event')[:255],
                description=data.get('description', '')[:500],
                start_time=data.get('start_time', '')[:100]
            )

    except OpenAIError as e:
        logger.error(f"OpenAI Intent Error (session {session_id}): {e}")
        raise self.retry(exc=e)
    
    except Exception as e:
        logger.error(f"Intent Engine Error (session {session_id}): {e}", exc_info=True)

@shared_task(
    bind=True,
    max_retries=2,
    autoretry_for=(OpenAIError,)
)
def generate_chat_title(self, session_id, first_message):
    try:
        session = ChatSession.objects.get(id=session_id)
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Generate a 3-5 word chat title. No quotes. Be concise and descriptive."
                },
                {
                    "role": "user",
                    "content": first_message[:200]
                }
            ],
            max_tokens=20,
            timeout=10,
            temperature=0.7
        )
        
        title = response.choices[0].message.content.strip().replace('"', '').replace("'", "")
        
        if len(title) > 255:
            title = title[:252] + "..."
        
        session.title = title
        session.save(update_fields=['title'])
        
    except OpenAIError as e:
        logger.warning(f"OpenAI Title Error (session {session_id}): {e}")
    
    except Exception as e:
        logger.error(f"Title Generation Error (session {session_id}): {e}")