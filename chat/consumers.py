import json
import urllib.parse
import threading
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import ChatSession, Message
from .tasks import generate_ai_reply_task, generate_title_task

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.session_id_param = self.scope['url_route']['kwargs']['session_id']
        self.user = self.scope["user"]

        if self.user.is_anonymous:
            await self.close()
            return

        if self.session_id_param == "new":
            # Auto-create session on connect
            self.session = await self.create_session(self.user)
            self.session_id = str(self.session.id)
            self.room_group_name = f'chat_{self.session_id}'
            
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()

            # Tell Frontend the new ID immediately
            await self.send(text_data=json.dumps({
                'type': 'session_created',
                'session_id': self.session.id,
                'title': self.session.title
            }))

        else:
            # Connect to existing
            self.session_id = self.session_id_param
            self.room_group_name = f'chat_{self.session_id}'
            
            if await self.check_session_exists(self.session_id, self.user):
                await self.channel_layer.group_add(self.room_group_name, self.channel_name)
                await self.accept()
            else:
                await self.close()

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        if not text_data: return

        # Safe JSON parsing
        try:
            data = json.loads(text_data)
            if isinstance(data, dict):
                message_text = data.get('message')
            else:
                message_text = str(data)
        except json.JSONDecodeError:
            message_text = text_data.strip()
        
        if message_text:
            # 1. Save User Message
            user_msg = await self.save_message(self.session_id, self.user, message_text)
            
            # 2. Echo to UI
            await self.send(text_data=json.dumps({
                'type': 'new_message',
                'message': self.message_to_json(user_msg)
            }))

            # 3. Generate Title (if first message)
            if await self.is_first_message(self.session_id):
                threading.Thread(target=generate_title_task, args=(self.session_id, message_text)).start()
            
            # 4. Generate AI Reply (with history)
            threading.Thread(target=generate_ai_reply_task, args=(self.session_id, message_text)).start()

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'new_message',
            'message': event['message']
        }))

    @database_sync_to_async
    def create_session(self, user):
        return ChatSession.objects.create(user=user, title="New Chat")

    @database_sync_to_async
    def check_session_exists(self, session_id, user):
        return ChatSession.objects.filter(id=session_id, user=user).exists()

    @database_sync_to_async
    def save_message(self, session_id, user, text):
        session = ChatSession.objects.get(id=session_id)
        return Message.objects.create(session=session, sender=user, is_ai=False, text=text)
    
    @database_sync_to_async
    def is_first_message(self, session_id):
        return Message.objects.filter(session_id=session_id).count() == 1

    def message_to_json(self, message):
        return {
            'id': message.id,
            'text': message.text,
            'is_ai': message.is_ai,
            'image': message.image.url if message.image else None,
            'ocr_text': message.ocr_extracted_text,
            'created_at': str(message.created_at)
        }