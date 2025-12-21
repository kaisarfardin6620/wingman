import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from core.models import TargetProfile
from .models import ChatSession, Message
from .tasks import generate_ai_response, generate_chat_title

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_anonymous:
            await self.close()
            return
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        conversation_id = data.get('conversation_id')
        message_text = data.get('message')
        target_id = data.get('target_id')

        if not message_text:
            return

        session, created = await self.get_or_create_session(conversation_id, target_id)
        
        self.room_group_name = f'chat_{session.conversation_id}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        user_msg = await self.save_message(session, message_text)

        await self.send(text_data=json.dumps({
            'type': 'new_message',
            'conversation_id': str(session.conversation_id),
            'message': {
                'id': user_msg.id,
                'text': user_msg.text,
                'is_ai': False,
                'created_at': str(user_msg.created_at)
            }
        }))

        generate_ai_response.delay(session.id, message_text)
        
        if created:
            generate_chat_title.delay(session.id, message_text)

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'new_message',
            'conversation_id': event['conversation_id'],
            'message': event['message']
        }))

    @database_sync_to_async
    def get_or_create_session(self, conversation_id, target_id=None):
        if conversation_id:
            try:
                return ChatSession.objects.get(conversation_id=conversation_id, user=self.user), False
            except ChatSession.DoesNotExist:
                pass
        
        target = None
        if target_id:
            try:
                target = TargetProfile.objects.get(id=target_id, user=self.user)
            except TargetProfile.DoesNotExist:
                pass

        session = ChatSession.objects.create(user=self.user, target_profile=target)
        return session, True

    @database_sync_to_async
    def save_message(self, session, text):
        return Message.objects.create(session=session, sender=self.user, text=text, is_ai=False)