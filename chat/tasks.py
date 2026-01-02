import json
import base64
import os
from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.conf import settings
from openai import OpenAI
from .models import ChatSession, Message, DetectedEvent
from core.models import UserSettings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def encode_image(image_path):
    if not os.path.exists(image_path):
        return None
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

@shared_task
def generate_ai_response(session_id, user_text):
    try:
        session = ChatSession.objects.get(id=session_id)
        user_settings, _ = UserSettings.objects.get_or_create(user=session.user)
        
        if user_settings.active_persona:
            persona_prompt = f"You are {user_settings.active_persona.name}. {user_settings.active_persona.description}"
        else:
            persona_prompt = "You are a helpful Wingman AI dating coach."

        user_style_prompt = ""
        if user_settings.linguistic_style:
            user_style_prompt = f"\nUSER STYLE FINGERPRINT (Mimic this style for draft texts): {user_settings.linguistic_style}"

        active_tones = user_settings.active_tones.all()
        if active_tones:
            tone_names = ", ".join([t.name for t in active_tones])
            tone_prompt = f"Respond using these tones: {tone_names}."
        else:
            tone_prompt = "Keep the tone confident."

        target_prompt = ""
        if session.target_profile:
            tp = session.target_profile
            target_prompt = (
                f"CONTEXT: The user is asking about '{tp.name}'.\n"
                f"She likes: {tp.what_she_likes}\n"
                f"Notes: {tp.details} {tp.her_mentions}"
            )

        system_prompt = (
            f"{persona_prompt}\n"
            f"{user_style_prompt}\n"
            f"{tone_prompt}\n"
            f"{target_prompt}\n"
            "Your goal is to help the user. If drafting a text, use the User Style Fingerprint."
        )

        recent_messages = session.messages.all().order_by('-created_at')[:20]
        history = []
        for msg in reversed(recent_messages):
            role = "assistant" if msg.is_ai else "user"
            content = msg.text
            if msg.ocr_extracted_text:
                content += f"\n[IMAGE CONTEXT: {msg.ocr_extracted_text}]"
            history.append({"role": role, "content": content or ""})

        messages_payload = [{"role": "system", "content": system_prompt}] + history
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages_payload
        )
        ai_reply = response.choices[0].message.content

        ai_msg = Message.objects.create(session=session, is_ai=True, text=ai_reply)
        
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'chat_{session.conversation_id}',
            {
                'type': 'chat_message',
                'conversation_id': str(session.conversation_id),
                'message': {
                    'id': ai_msg.id,
                    'text': ai_msg.text,
                    'is_ai': True,
                    'created_at': str(ai_msg.created_at)
                }
            }
        )

        profile_target_engine.delay(session.id, user_text)
        intent_engine.delay(session.id, user_text)
        linguistic_engine.delay(session.user.id, session.id)

    except Exception as e:
        print(f"AI Generation Error: {e}")

@shared_task
def analyze_screenshot_task(message_id):
    try:
        message = Message.objects.get(id=message_id)
        if not message.image: return
        
        base64_image = encode_image(message.image.path)
        if not base64_image: return 
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extract text exactly. JSON: { 'extracted_text': '...' }"},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                    ],
                }
            ],
            response_format={"type": "json_object"}
        )

        ai_content = json.loads(response.choices[0].message.content)
        message.ocr_extracted_text = ai_content.get('extracted_text', '')
        message.save()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'chat_{message.session.id}',
            {
                'type': 'chat_message',
                'conversation_id': str(message.session.conversation_id),
                'message': {
                    'id': message.id, 
                    'type': 'analysis_complete', 
                    'ocr_text': message.ocr_extracted_text
                }
            }
        )
    except Exception as e:
        print(f"OCR Error: {e}")

@shared_task
def profile_target_engine(session_id, latest_text):
    try:
        session = ChatSession.objects.get(id=session_id)
        if not session.target_profile:
            return

        tp = session.target_profile
        
        prompt = (
            f"Analyze this message regarding '{tp.name}'. Extract any NEW specific likes, dislikes, or preferences mentioned.\n"
            f"Current Likes: {tp.what_she_likes}\n"
            f"Message: \"{latest_text}\"\n"
            "Return JSON only: {\"new_likes\": [], \"new_preferences\": []}"
        )

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        data = json.loads(response.choices[0].message.content)
        
        updated = False
        if data.get('new_likes'):
            for item in data['new_likes']:
                if item not in tp.what_she_likes:
                    tp.what_she_likes.append(item)
                    updated = True
        
        if data.get('new_preferences'):
            for item in data['new_preferences']:
                if item not in tp.preferences:
                    tp.preferences.append(item)
                    updated = True

        if updated:
            tp.save()
            print(f"AUTO-PROFILING: Updated {tp.name} with new data.")

    except Exception as e:
        print(f"Profiling Error: {e}")

@shared_task
def linguistic_engine(user_id, session_id):
    try:
        session = ChatSession.objects.get(id=session_id)
        user_settings, _ = UserSettings.objects.get_or_create(user_id=user_id)
        
        user_msgs = Message.objects.filter(sender_id=user_id, is_ai=False).order_by('-created_at')[:10]
        if not user_msgs:
            return

        text_sample = "\n".join([m.text for m in user_msgs if m.text])

        prompt = (
            "Analyze the writing style of this user based on their messages.\n"
            "Describe: Sentence length, capitalization, emoji usage, tone, and slang.\n"
            "Keep it concise (1-2 sentences).\n"
            f"Messages:\n{text_sample}"
        )

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=60
        )
        
        style_desc = response.choices[0].message.content.strip()
        user_settings.linguistic_style = style_desc
        user_settings.save()
        print(f"LINGUISTIC ENGINE: Updated User Style to: {style_desc}")

    except Exception as e:
        print(f"Linguistic Error: {e}")

@shared_task
def intent_engine(session_id, user_text):
    try:
        session = ChatSession.objects.get(id=session_id)
        
        prompt = (
            "Does this message contain a concrete plan, date, or meeting time?\n"
            f"Message: \"{user_text}\"\n"
            "If yes, extract: Title, Start Time. If no, return empty JSON.\n"
            "Return JSON: {\"is_event\": boolean, \"title\": string, \"start_time\": string}"
        )

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        data = json.loads(response.choices[0].message.content)
        
        if data.get('is_event'):
            DetectedEvent.objects.create(
                session=session,
                title=data.get('title', 'New Event'),
                start_time=data.get('start_time', '')
            )
            print(f"INTENT ENGINE: Detected Event - {data.get('title')}")

    except Exception as e:
        print(f"Intent Error: {e}")

@shared_task
def generate_chat_title(session_id, first_message):
    try:
        session = ChatSession.objects.get(id=session_id)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Generate a concise 3-4 word title for this chat. No quotes."},
                {"role": "user", "content": first_message}
            ],
            max_tokens=20
        )
        session.title = response.choices[0].message.content.strip().replace('"', '')
        session.save()
    except Exception:
        pass