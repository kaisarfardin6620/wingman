import base64
import json
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from openai import OpenAI
from .models import Message, ChatSession

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def generate_title_task(session_id, user_text):
    try:
        session = ChatSession.objects.get(id=session_id)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Summarize into 3-5 words title (no quotes)."},
                {"role": "user", "content": user_text}
            ],
            max_tokens=15
        )
        session.title = response.choices[0].message.content.strip().replace('"', '')
        session.save()
    except Exception:
        pass

def analyze_screenshot_task(message_id):
    try:
        message = Message.objects.get(id=message_id)
        if not message.image: return
        
        base64_image = encode_image(message.image.path)
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extract text exactly. Analyze emotional tone. JSON: { 'extracted_text': '...', 'tags': ['tag1'] }"},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                    ],
                }
            ],
            response_format={"type": "json_object"}
        )

        ai_content = json.loads(response.choices[0].message.content)
        message.ocr_extracted_text = ai_content.get('extracted_text', '')
        message.analysis_tags = ai_content.get('tags', [])
        message.save()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'chat_{message.session.id}',
            {
                'type': 'chat_message',
                'message': {
                    'id': message.id, 
                    'type': 'analysis_complete', 
                    'ocr_text': message.ocr_extracted_text,
                    'tags': message.analysis_tags
                }
            }
        )
    except Exception as e:
        print(f"OCR Error: {e}")

def generate_ai_reply_task(session_id, user_text):
    try:
        session = ChatSession.objects.get(id=session_id)
        
        all_messages = session.messages.all().order_by('created_at')
        
        conversation_history = []
        for msg in all_messages:
            role = "assistant" if msg.is_ai else "user"
            
            content_part = msg.text if msg.text else ""
            
            if msg.ocr_extracted_text:
                content_part += f"\n\n[SYSTEM: The user uploaded an image with this text: {msg.ocr_extracted_text}]"
            
            if content_part:
                conversation_history.append({"role": role, "content": content_part})

        system_prompt = (
            "You are an expert AI Wingman. Your goal is to help the user with dating.\n"
            "Keep advice confident, charming, and brief.\n"
            "Use the conversation history to understand context."
        )

        messages_to_send = [{"role": "system", "content": system_prompt}]
        messages_to_send.extend(conversation_history)

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages_to_send
        )
        
        ai_reply = response.choices[0].message.content

        ai_msg = Message.objects.create(session=session, is_ai=True, text=ai_reply)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'chat_{session.id}',
            {'type': 'chat_message', 'message': {'id': ai_msg.id, 'text': ai_msg.text, 'is_ai': True}}
        )

    except Exception as e:
        print(f"AI Error: {e}")