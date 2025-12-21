from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.conf import settings
from openai import OpenAI
from .models import ChatSession, Message
from core.models import UserSettings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

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

@shared_task
def generate_ai_response(session_id, user_text):
    try:
        session = ChatSession.objects.get(id=session_id)
        user_settings, _ = UserSettings.objects.get_or_create(user=session.user)
        
        if user_settings.active_persona:
            persona_prompt = f"You are {user_settings.active_persona.name}. {user_settings.active_persona.description}"
        else:
            persona_prompt = "You are a helpful Wingman AI dating coach."

        active_tones = user_settings.active_tones.all()
        if active_tones:
            tone_names = ", ".join([t.name for t in active_tones])
            tone_prompt = f"Respond using these tones: {tone_names}."
        else:
            tone_prompt = "Keep the tone confident and helpful."

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
            f"{tone_prompt}\n"
            f"{target_prompt}\n"
            "Your goal is to help the user. Keep it short and engaging."
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

    except Exception as e:
        print(f"AI Generation Error: {e}")