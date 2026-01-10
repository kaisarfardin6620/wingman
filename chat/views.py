from rest_framework import viewsets, mixins, parsers, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django.core.cache import cache
from django.db.models import Prefetch, Count
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.shortcuts import get_object_or_404
import logging

from .models import ChatSession, Message
from .serializers import (
    ChatSessionListSerializer,
    ChatSessionDetailSerializer,
    ChatSessionUpdateSerializer,
    MessageSerializer,
    MessageUploadSerializer
)
from .tasks import analyze_screenshot_task

logger = logging.getLogger(__name__)


class ChatThrottle(UserRateThrottle):
    rate = '60/minute'


class UploadThrottle(UserRateThrottle):
    rate = '10/minute'


class ChatSessionViewSet(viewsets.GenericViewSet,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    throttle_classes = [ChatThrottle]
    serializer_class = ChatSessionListSerializer
    lookup_field = 'conversation_id'

    def get_queryset(self):
        return ChatSession.objects.filter(
            user=self.request.user
        ).select_related(
            'target_profile'
        ).prefetch_related(
            'events'
        ).order_by('-updated_at')
    
    def get_object(self):
        conversation_id = self.kwargs.get('conversation_id')
        obj = get_object_or_404(
            ChatSession,
            conversation_id=conversation_id,
            user=self.request.user
        )
        return obj

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'history':
            return ChatSessionDetailSerializer
        elif self.action == 'rename':
            return ChatSessionUpdateSerializer
        return ChatSessionListSerializer

    @method_decorator(cache_page(60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        conversation_id = kwargs.get('conversation_id')
        cache_key = f"chat_session_detail:{conversation_id}:{request.user.id}"
        
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        cache.set(cache_key, serializer.data, 120)
        
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        conversation_id = instance.conversation_id
        
        instance.delete()
        
        cache.delete(f"chat_session:{conversation_id}:{request.user.id}")
        cache.delete(f"chat_session_detail:{conversation_id}:{request.user.id}")
        cache.delete(f"chat_history:{conversation_id}")
        
        return Response(
            {"message": "Chat session deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=True, methods=['get'])
    def history(self, request, conversation_id=None):
        cache_key = f"chat_history:{conversation_id}"
        
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        
        session = self.get_object()
        
        messages = session.messages.only(
            'id', 'is_ai', 'text', 'image',
            'ocr_extracted_text', 'tokens_used', 'created_at'
        ).order_by('created_at')
        
        serializer = MessageSerializer(
            messages,
            many=True,
            context={'request': request}
        )
        
        cache.set(cache_key, serializer.data, 120)
        
        return Response(serializer.data)

    @action(detail=True, methods=['patch'], throttle_classes=[ChatThrottle])
    def rename(self, request, conversation_id=None):
        session = self.get_object()
        serializer = self.get_serializer(session, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            
            cache.delete(f"chat_session:{conversation_id}:{request.user.id}")
            cache.delete(f"chat_session_detail:{conversation_id}:{request.user.id}")
            
            return Response({
                "message": "Chat renamed successfully",
                "title": serializer.data['title']
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'])
    def clear_all(self, request):
        user_sessions = ChatSession.objects.filter(user=request.user)
        
        conversation_ids = list(user_sessions.values_list('conversation_id', flat=True))
        
        deleted_count, _ = user_sessions.delete()
        
        for conv_id in conversation_ids:
            cache.delete(f"chat_session:{conv_id}:{request.user.id}")
            cache.delete(f"chat_session_detail:{conv_id}:{request.user.id}")
            cache.delete(f"chat_history:{conv_id}")
        
        return Response({
            "message": f"Deleted {deleted_count} chat sessions"
        }, status=status.HTTP_200_OK)


class ChatSessionImageUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    throttle_classes = [UploadThrottle]

    def post(self, request, conversation_id):
        try:
            session = ChatSession.objects.get(
                conversation_id=conversation_id,
                user=request.user
            )
        except ChatSession.DoesNotExist:
            return Response(
                {"error": "Session not found or access denied"},
                status=status.HTTP_404_NOT_FOUND
            )

        if not request.user.is_premium:
            from django.utils import timezone
            
            today = timezone.now().date()
            cache_key = f"upload_count:{request.user.id}:{today}"
            upload_count = cache.get(cache_key)
            
            if upload_count is None:
                upload_count = Message.objects.filter(
                    sender=request.user,
                    created_at__date=today,
                    image__isnull=False
                ).count()
                cache.set(cache_key, upload_count, 3600)
            
            if upload_count >= 10:
                return Response(
                    {"error": "Daily upload limit reached (10/day). Upgrade to Premium for unlimited uploads."},
                    status=status.HTTP_429_TOO_MANY_REQUESTS
                )

        serializer = MessageUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        image = serializer.validated_data['image']
        text = serializer.validated_data.get('text', '[Screenshot Uploaded]')

        try:
            msg = Message.objects.create(
                session=session,
                sender=request.user,
                is_ai=False,
                text=text,
                image=image
            )
            
            session.update_preview()
            
            if not request.user.is_premium:
                cache.set(cache_key, upload_count + 1, 3600)
            
            analyze_screenshot_task.delay(msg.id)
            
            cache.delete(f"chat_history:{conversation_id}")
            
            return Response(
                {
                    "message": "Image uploaded successfully",
                    "data": MessageSerializer(msg, context={'request': request}).data
                },
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            logger.error(f"Image upload error for user {request.user.id}: {e}", exc_info=True)
            return Response(
                {"error": "Failed to upload image. Please try again."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ChatStatsView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    @method_decorator(cache_page(300))
    def get(self, request):
        user = request.user
        
        stats = ChatSession.objects.filter(user=user).aggregate(
            total_sessions=Count('id'),
            total_messages=Count('messages')
        )
        
        user_messages = Message.objects.filter(
            sender=user,
            is_ai=False
        ).count()
        
        ai_messages = Message.objects.filter(
            session__user=user,
            is_ai=True
        ).count()
        
        total_tokens = 0
        if user.is_premium:
            from django.db.models import Sum
            total_tokens = Message.objects.filter(
                session__user=user,
                is_ai=True
            ).aggregate(
                total=Sum('tokens_used')
            )['total'] or 0
        
        return Response({
            "total_sessions": stats['total_sessions'],
            "total_messages": stats['total_messages'],
            "user_messages": user_messages,
            "ai_messages": ai_messages,
            "total_tokens_used": total_tokens,
        })