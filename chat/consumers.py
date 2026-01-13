import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.cache import cache
from core.models import TargetProfile, GlobalConfig
from .models import ChatSession, Message
from .tasks import generate_ai_response, generate_chat_title

User = get_user_model()
logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope.get("user")
        
        if not self.user or self.user.is_anonymous:
            await self.accept()
            await self.close(code=4001)
            return
        
        self.conversation_id = self.scope['url_route']['kwargs'].get('conversation_id')
        self.room_group_name = None

        if self.conversation_id:
            session = await self.get_session_cached(self.conversation_id)
            if session:
                self.room_group_name = f'chat_{self.conversation_id}'
                await self.channel_layer.group_add(self.room_group_name, self.channel_name)
                await self.accept()
                
                history = await self.get_chat_history_cached(session)
                await self.send(text_data=json.dumps({
                    'type': 'chat_history',
                    'conversation_id': self.conversation_id,
                    'messages': history
                }))
            else:
                await self.accept()
                await self.close(code=4004)
        else:
            await self.accept()

    async def disconnect(self, close_code):
        if self.room_group_name:
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            return

        message_text = data.get('message', '').strip()
        target_id = data.get('target_id')
        incoming_conversation_id = data.get('conversation_id')
        selected_tone = data.get('tone', None)

        if not message_text:
            return

        error_message = await self.check_limits_cached(message_text)
        if error_message:
            await self.send(text_data=json.dumps({'type': 'error', 'message': error_message}))
            return

        session = None
        created = False
        send_history_flag = False

        if self.conversation_id:
            session = await self.get_session_cached(self.conversation_id)
        elif incoming_conversation_id:
            session = await self.get_session_cached(incoming_conversation_id)
            if session:
                self.conversation_id = str(session.conversation_id)
                self.room_group_name = f'chat_{self.conversation_id}'
                await self.channel_layer.group_add(self.room_group_name, self.channel_name)
                send_history_flag = True

        if not session:
            session, created = await self.create_session(target_id)
            self.conversation_id = str(session.conversation_id)
            self.room_group_name = f'chat_{self.conversation_id}'
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        if send_history_flag:
            history = await self.get_chat_history_cached(session)
            await self.send(text_data=json.dumps({
                'type': 'chat_history',
                'conversation_id': self.conversation_id,
                'messages': history
            }))

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

        generate_ai_response.delay(session.id, message_text, selected_tone)
        
        if created:
            generate_chat_title.delay(session.id, message_text)
        
        await self.invalidate_session_cache(session.conversation_id)

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'new_message',
            'conversation_id': event['conversation_id'],
            'message': event['message']
        }))

    @database_sync_to_async
    def get_session_cached(self, conversation_id):
        cache_key = f"chat_session:{conversation_id}:{self.user.id}"
        cached = cache.get(cache_key)
        if cached: return cached
        try:
            session = ChatSession.objects.select_related('user', 'target_profile').get(conversation_id=conversation_id, user=self.user)
            cache.set(cache_key, session, 300)
            return session
        except ChatSession.DoesNotExist: return None

    @database_sync_to_async
    def get_chat_history_cached(self, session):
        cache_key = f"chat_history:{session.conversation_id}"
        cached = cache.get(cache_key)
        if cached: return cached
        messages = session.messages.only('id', 'text', 'is_ai', 'image', 'ocr_extracted_text', 'created_at').order_by('created_at')
        history_data = []
        for msg in messages:
            history_data.append({
                'id': msg.id,
                'text': msg.text,
                'is_ai': msg.is_ai,
                'image': msg.image.url if msg.image else None,
                'ocr_text': msg.ocr_extracted_text,
                'created_at': str(msg.created_at)
            })
        cache.set(cache_key, history_data, 120)
        return history_data

    @database_sync_to_async
    def check_limits_cached(self, text):
        if self.user.is_premium: return None
        cache_key = "global_config"
        config = cache.get(cache_key)
        if not config:
            config = GlobalConfig.load()
            cache.set(cache_key, config, 3600)
        
        if len(text) > config.max_chat_length:
            return f"Message too long. Free limit is {config.max_chat_length} characters."
        
        today = timezone.now().date()
        count_cache_key = f"msg_count:{self.user.id}:{today}"
        
        try:
            current_count = cache.incr(count_cache_key)
        except ValueError:
            cache.set(count_cache_key, 1, timeout=86400)
            current_count = 1
            
        if current_count > config.daily_free_limit:
            return "Daily free limit reached. Upgrade to Premium."
        return None

    @database_sync_to_async
    def create_session(self, target_id=None):
        target = None
        if target_id:
            try: target = TargetProfile.objects.get(id=target_id, user=self.user)
            except TargetProfile.DoesNotExist: pass
        session = ChatSession.objects.create(user=self.user, target_profile=target)
        return session, True

    @database_sync_to_async
    def save_message(self, session, text):
        message = Message.objects.create(session=session, sender=self.user, text=text, is_ai=False)
        session.update_preview()
        return message

    @database_sync_to_async
    def invalidate_session_cache(self, conversation_id):
        cache.delete(f"chat_session:{conversation_id}:{self.user.id}")
        cache.delete(f"chat_history:{conversation_id}")