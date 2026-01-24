import structlog
from django.core.cache import cache
from django.utils import timezone
from core.models import GlobalConfig
from .models import ChatSession, Message
from .serializers import MessageSerializer
from .tasks import analyze_screenshot_task, transcribe_audio_task
from wingman.constants import CACHE_TTL_CHAT_SESSION, CACHE_TTL_CHAT_HISTORY, CACHE_TTL_CHAT_DETAIL

logger = structlog.get_logger(__name__)

class ChatService:
    
    @staticmethod
    def get_or_create_session(conversation_id, user):
        pass

    @staticmethod
    def delete_session(session, user_id):
        conversation_id = session.conversation_id
        session.delete()
        
        # Invalidate caches
        cache.delete(f"chat_session:{conversation_id}:{user_id}")
        cache.delete(f"chat_session_detail:{conversation_id}:{user_id}")
        cache.delete(f"chat_history:{conversation_id}")
        logger.info("chat_session_deleted", conversation_id=str(conversation_id), user_id=user_id)

    @staticmethod
    def clear_all_sessions(user):
        sessions = ChatSession.objects.filter(user=user)
        count = sessions.count()
        conversation_ids = list(sessions.values_list('conversation_id', flat=True))
        sessions.delete()
        
        for cid in conversation_ids:
            cache.delete(f"chat_session:{cid}:{user.id}")
            cache.delete(f"chat_session_detail:{cid}:{user.id}")
            cache.delete(f"chat_history:{cid}")
            
        logger.info("all_chats_cleared", user_id=user.id, count=count)
        return count

    @staticmethod
    def handle_file_upload(user, session, validated_data, request_context=None):
        if not user.is_premium:
            today = timezone.now().date()
            cache_key = f"upload_count:{user.id}:{today}"
            upload_count = cache.get(cache_key)
            
            if upload_count is None:
                upload_count = Message.objects.filter(
                    sender=user,
                    created_at__date=today,
                    image__isnull=False
                ).count()
                cache.set(cache_key, upload_count, 3600)
            
            config = GlobalConfig.load()
            if upload_count >= config.ocr_limit:
                logger.warning("upload_limit_reached", user_id=user.id)
                return None, f"Daily upload limit reached ({config.ocr_limit}/day). Upgrade to Premium."

        image = validated_data.get('image')
        audio = validated_data.get('audio')
        text = validated_data.get('text', '')

        if not text:
            if image: text = "[Screenshot Uploaded]"
            elif audio: text = "[Audio Uploaded]"

        msg = Message.objects.create(
            session=session,
            sender=user,
            is_ai=False,
            text=text,
            image=image,
            audio=audio
        )
        session.update_preview()
        
        if not user.is_premium:
            cache.set(f"upload_count:{user.id}:{timezone.now().date()}", 
                      (upload_count or 0) + 1, 3600)
        
        if image:
            analyze_screenshot_task.delay(msg.id)
        if audio:
            transcribe_audio_task.delay(msg.id)
            
        cache.delete(f"chat_history:{session.conversation_id}")
        logger.info("chat_file_uploaded", message_id=msg.id, type="image" if image else "audio")
        
        return MessageSerializer(msg, context=request_context).data, None