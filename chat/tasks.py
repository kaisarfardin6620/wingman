import json
import base64
import logging
from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.conf import settings
from django.core.cache import cache
from django.db import transaction
from openai import OpenAI, OpenAIError, RateLimitError, APIConnectionError, InternalServerError, BadRequestError
from .models import ChatSession, Message, DetectedEvent
from .services import AIService
from core.models import UserSettings, TargetProfile
from core.utils import send_push_notification
from django.utils import timezone

logger = logging.getLogger(__name__)

MAX_RETRIES = 3
OPENAI_TIMEOUT = 30

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
    autoretry_for=(RateLimitError, APIConnectionError, InternalServerError),
    retry_backoff=True
)
def generate_ai_response(self, session_id, user_text, selected_tone=None):
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    lock_key = f"ai_processing_lock:{session_id}"
    
    try:
        session = ChatSession.objects.select_related('user', 'target_profile').get(id=session_id)
        
        with transaction.atomic():
            ai_msg = Message.objects.create(
                session=session, 
                is_ai=True, 
                text="", 
                processing_status='processing'
            )
        
        send_ws_message(session.conversation_id, {
            'id': ai_msg.id, 
            'text': "", 
            'is_ai': True, 
            'status': 'processing',
            'created_at': str(ai_msg.created_at)
        })

        system_prompt = AIService.build_system_prompt(session.user, session, selected_tone)
        messages_payload = AIService.prepare_context(session, system_prompt)
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages_payload,
            max_tokens=1000,
            timeout=OPENAI_TIMEOUT,
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        
        ai_reply_json = response.choices[0].message.content
        tokens_used = response.usage.total_tokens if hasattr(response, 'usage') else 0
        
        ai_msg.text = ai_reply_json
        ai_msg.tokens_used = tokens_used
        ai_msg.processing_status = 'completed'
        ai_msg.save()
        
        session.update_preview()
        cache.delete(f"chat_history:{session.conversation_id}")
        
        send_ws_message(session.conversation_id, {
            'id': ai_msg.id, 
            'text': ai_msg.text, 
            'is_ai': True, 
            'status': 'completed',
            'created_at': str(ai_msg.created_at)
        })
        
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
        
        user_msg_count = session.messages.filter(is_ai=False).count()
        if user_msg_count == 1:
            generate_chat_title.delay(session.id, user_text)
        
        if any(word in user_text.lower() for word in ['tomorrow', 'tonight', 'meet', 'date', 'clock', 'pm', 'am', 'schedule']):
            intent_engine.delay(session.id, user_text)
        
        if session.target_profile:
            profile_target_engine.delay(session.id, user_text)

        return ai_msg.id

    except BadRequestError as e:
        logger.error(f"OpenAI Bad Request (Non-Retryable): {e}")
        if 'ai_msg' in locals():
            ai_msg.processing_status = 'failed'
            ai_msg.text = "Error: Request too long or invalid."
            ai_msg.save()
            send_ws_message(session_id, {'id': ai_msg.id, 'status': 'failed', 'text': ai_msg.text})
    
    except (RateLimitError, APIConnectionError, InternalServerError) as e:
        logger.warning(f"OpenAI Network/Rate Error (Retrying): {e}")
        raise self.retry(exc=e)
        
    except Exception as e:
        logger.error(f"AI System Error: {e}", exc_info=True)
        if 'ai_msg' in locals():
            ai_msg.processing_status = 'failed'
            ai_msg.text = "System Error."
            ai_msg.save()
            send_ws_message(session_id, {'id': ai_msg.id, 'status': 'failed', 'text': "System Error."})

    finally:
        cache.delete(lock_key)

@shared_task(bind=True, max_retries=2, autoretry_for=(OpenAIError,))
def analyze_screenshot_task(self, message_id):
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    try:
        message = Message.objects.select_related('session').get(id=message_id)
        if not message.image: 
            return
            
        message.processing_status = 'processing'
        message.save(update_fields=['processing_status'])
        send_ws_message(message.session.conversation_id, {
            'id': message.id, 'status': 'processing', 'type': 'analysis_update'
        })

        try:
            with message.image.open('rb') as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e: 
            logger.error(f"Failed to read image for message {message_id}: {e}")
            message.processing_status = 'failed'
            message.save()
            return

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{
                "role": "user", 
                "content": [
                    {"type": "text", "text": "Extract all visible text from this image and return it as JSON with key 'extracted_text'."}, 
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            }],
            max_tokens=1000,
            response_format={"type": "json_object"}
        )
        ai_content = json.loads(response.choices[0].message.content)
        ocr_text = ai_content.get('extracted_text', '')
        
        message.ocr_extracted_text = ocr_text
        message.processing_status = 'completed'
        message.save(update_fields=['ocr_extracted_text', 'processing_status'])
        
        cache.delete(f"chat_history:{message.session.conversation_id}")
        
        send_ws_message(message.session.conversation_id, {
            'id': message.id, 
            'type': 'analysis_complete', 
            'ocr_text': ocr_text,
            'status': 'completed'
        })
        
    except Exception as e: 
        logger.error(f"OCR Error for message {message_id}: {e}")
        message.processing_status = 'failed'
        message.save(update_fields=['processing_status'])
        send_ws_message(message.session.conversation_id, {
            'id': message.id, 'status': 'failed', 'type': 'analysis_failed'
        })

@shared_task(bind=True, max_retries=2, autoretry_for=(OpenAIError,))
def transcribe_audio_task(self, message_id):
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    try:
        message = Message.objects.select_related('session').get(id=message_id)
        if not message.audio: 
            return
            
        message.processing_status = 'processing'
        message.save(update_fields=['processing_status'])
        send_ws_message(message.session.conversation_id, {
            'id': message.id, 'status': 'processing', 'type': 'transcription_update'
        })
            
        with message.audio.open('rb') as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file,
                response_format="text"
            )
        
        message.text = transcript.strip()
        message.processing_status = 'completed'
        message.save(update_fields=['text', 'processing_status'])
        
        cache.delete(f"chat_history:{message.session.conversation_id}")
        
        send_ws_message(message.session.conversation_id, {
            'id': message.id, 
            'text': message.text, 
            'is_ai': False, 
            'type': 'transcription_complete',
            'status': 'completed'
        })
        
        generate_ai_response.delay(message.session.id, message.text)
        
    except Exception as e:
        logger.error(f"Transcription Error for message {message_id}: {e}")
        message.processing_status = 'failed'
        message.save(update_fields=['processing_status'])
        send_ws_message(message.session.conversation_id, {
            'id': message.id, 'status': 'failed', 'type': 'transcription_failed'
        })

@shared_task(bind=True, max_retries=2, autoretry_for=(OpenAIError,))
def profile_target_engine(self, session_id, latest_text):
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    try:
        with transaction.atomic():
            session = ChatSession.objects.select_related('target_profile').select_for_update().get(id=session_id)
            if not session.target_profile: return
            tp = TargetProfile.objects.select_for_update().get(id=session.target_profile.id)
            
            prompt = (
                f"Analyze text about {tp.name}: {latest_text}\n"
                f"Extract new likes, preferences, mentions. Return JSON."
            )
            response = client.chat.completions.create(
                model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}], response_format={"type": "json_object"}
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

            if data.get('new_likes') and add_if_new(tp.what_she_likes, data['new_likes']): updated = True
            if data.get('new_preferences') and add_if_new(tp.preferences, data['new_preferences']): updated = True
            if data.get('new_mentions'):
                if not tp.her_mentions: tp.her_mentions = data['new_mentions']; updated = True
                elif data['new_mentions'] not in tp.her_mentions: tp.her_mentions += f" | {data['new_mentions']}"; updated = True
                    
            if updated: tp.save()
                
    except Exception as e: 
        logger.error(f"Profile Engine Error: {e}")

@shared_task(bind=True, max_retries=2, autoretry_for=(OpenAIError,))
def linguistic_engine(self, user_id, session_id):
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    try:
        user_settings, _ = UserSettings.objects.get_or_create(user_id=user_id)
        user_msgs = Message.objects.filter(sender_id=user_id, is_ai=False).only('text').order_by('-created_at')[:10]
        full_sample = "\n".join([m.text for m in user_msgs if m.text])
        if not full_sample: return
        
        response = client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[{"role": "user", "content": f"Analyze style: {full_sample[:2000]}"}], 
            max_tokens=150
        )
        user_settings.linguistic_style = response.choices[0].message.content.strip()
        user_settings.save()
    except Exception as e: 
        logger.error(f"Linguistic Engine Error: {e}")

@shared_task(bind=True, max_retries=2, autoretry_for=(OpenAIError,))
def intent_engine(self, session_id, user_text):
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    try:
        session = ChatSession.objects.get(id=session_id)
        prompt = f"Detect event in: {user_text}. Return JSON: is_event, title, start_time_iso, description, has_conflict."
        response = client.chat.completions.create(
            model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}], response_format={"type": "json_object"}
        )
        data = json.loads(response.choices[0].message.content)
        
        if data.get('is_event'):
            from dateutil import parser
            reminder_dt = None
            if data.get('start_time_iso'):
                try: reminder_dt = parser.parse(data['start_time_iso'])
                except: pass

            DetectedEvent.objects.create(
                session=session, 
                title=data.get('title', 'Event')[:255], 
                description=data.get('description', '')[:500], 
                start_time=data.get('start_time', '')[:100],
                has_conflict=data.get('has_conflict', False),
                reminder_datetime=reminder_dt
            )
            send_push_notification(session.user, "Event Detected", f"Added '{data.get('title')}' to your plan.")
    except Exception as e: 
        logger.error(f"Intent Engine Error: {e}")

@shared_task(bind=True, max_retries=2, autoretry_for=(OpenAIError,))
def generate_chat_title(self, session_id, first_message):
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    try:
        session = ChatSession.objects.get(id=session_id)
        response = client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[{"role": "system", "content": "Generate 3-5 word title."}, {"role": "user", "content": first_message[:200]}], 
            max_tokens=20
        )
        session.title = response.choices[0].message.content.strip().replace('"', '')[:252]
        session.save(update_fields=['title'])
    except Exception as e: 
        logger.error(f"Title Gen Error: {e}")

@shared_task
def send_reminder_push(event_id):
    try:
        event = DetectedEvent.objects.select_related('session__user').get(id=event_id)
        send_push_notification(event.session.user, "Upcoming Event", f"{event.title} is starting soon.")
        event.reminder_sent = True
        event.save(update_fields=['reminder_sent'])
    except Exception as e:
        logger.error(f"Failed to send reminder for event {event_id}: {e}")

@shared_task
def check_reminders_task():
    from datetime import timedelta
    now = timezone.now()
    event_ids = DetectedEvent.objects.filter(
        reminder_datetime__gte=now,
        reminder_datetime__lte=now + timedelta(minutes=15),
        reminder_sent=False, is_cancelled=False
    ).values_list('id', flat=True)
    
    for eid in event_ids:
        send_reminder_push.delay(eid)