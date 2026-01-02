import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.utils import timezone
from core.models import TargetProfile, GlobalConfig
from .models import ChatSession, Message
from .tasks import generate_ai_response, generate_chat_title

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_anonymous:
            await self.close()
            return
        
        self.conversation_id = self.scope['url_route']['kwargs'].get('conversation_id')
        self.room_group_name = None

        if self.conversation_id:
            session = await self.get_session(self.conversation_id)
            if session:
                self.room_group_name = f'chat_{self.conversation_id}'
                await self.channel_layer.group_add(self.room_group_name, self.channel_name)
                await self.accept()
            else:
                await self.close()
        else:
            await self.accept()

    async def disconnect(self, close_code):
        if self.room_group_name:
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_text = data.get('message')
        target_id = data.get('target_id') 

        if not message_text:
            return

        error_message = await self.check_limits(message_text)
        if error_message:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': error_message
            }))
            return

        if self.conversation_id:
            session = await self.get_session(self.conversation_id)
            created = False
        else:
            session, created = await self.create_session(target_id)
            self.conversation_id = str(session.conversation_id)
            self.room_group_name = f'chat_{self.conversation_id}'
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
    def check_limits(self, text):
        if self.user.is_premium:
            return None
        config = GlobalConfig.load()
        if len(text) > config.max_chat_length:
            return f"Message too long. Free limit is {config.max_chat_length} characters."
        today = timezone.now().date()
        msg_count = Message.objects.filter(sender=self.user, created_at__date=today).count()
        if msg_count >= config.daily_free_limit:
            return "Daily free limit reached. Upgrade to Premium."
        return None

    @database_sync_to_async
    def get_session(self, conversation_id):
        try:
            return ChatSession.objects.get(conversation_id=conversation_id, user=self.user)
        except ChatSession.DoesNotExist:
            return None

    @database_sync_to_async
    def create_session(self, target_id=None):
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