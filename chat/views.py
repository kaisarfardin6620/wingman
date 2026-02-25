import structlog
from rest_framework import viewsets, mixins, parsers, status, filters
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema

from .models import ChatSession
from .serializers import (
    ChatSessionListSerializer,
    ChatSessionDetailSerializer,
    ChatSessionUpdateSerializer,
    MessageSerializer,
    MessageUploadSerializer
)
from .services import ChatService
from wingman.constants import CACHE_TTL_CHAT_DETAIL, CACHE_TTL_CHAT_HISTORY

logger = structlog.get_logger(__name__)

class ChatThrottle(UserRateThrottle):
    scope = 'chat'

class UploadThrottle(UserRateThrottle):
    scope = 'user'

class ChatSessionViewSet(viewsets.GenericViewSet,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    throttle_classes = [ChatThrottle]
    serializer_class = ChatSessionListSerializer
    lookup_field = 'conversation_id'
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return ChatSession.objects.none()
            
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

    def retrieve(self, request, *args, **kwargs):
        conversation_id = kwargs.get('conversation_id')
        cache_key = f"chat_session_detail:{conversation_id}:{request.user.id}"
        
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        cache.set(cache_key, serializer.data, CACHE_TTL_CHAT_DETAIL)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        ChatService.delete_session(instance, request.user.id)
        return Response(
            {"message": "Chat session deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=True, methods=['get'])
    def history(self, request, conversation_id=None):
        cache_key = f"chat_history:{conversation_id}:{request.user.id}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        
        session = self.get_object()
        messages = session.messages.prefetch_related('images').only(
            'id', 'is_ai', 'text', 'audio',
            'ocr_extracted_text', 'tokens_used', 'created_at', 'processing_status'
        ).order_by('created_at')
        
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        cache.set(cache_key, serializer.data, CACHE_TTL_CHAT_HISTORY)
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
        count = ChatService.clear_all_sessions(request.user)
        return Response({"message": f"Deleted {count} chat sessions"}, status=status.HTTP_200_OK)


class ChatSessionImageUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    throttle_classes = [UploadThrottle]

    @extend_schema(
        summary="Upload Media to Chat",
        request={'multipart/form-data': MessageUploadSerializer},
        responses={201: MessageSerializer},
    )
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

        data = request.data.copy()
        if hasattr(request, 'FILES'):
            images = request.FILES.getlist('images')
            if images:
                data.setlist('images', images)

        serializer = MessageUploadSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        response_data, error = ChatService.handle_file_upload(
            request.user, 
            session, 
            serializer.validated_data, 
            request_context={'request': request}
        )
        
        if error:
            return Response({"error": error}, status=status.HTTP_429_TOO_MANY_REQUESTS)
            
        return Response({"message": "Files uploaded successfully", "data": response_data}, status=status.HTTP_201_CREATED)


class ChatStatsView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes =[UserRateThrottle]

    @extend_schema(summary="Get User Chat Stats", responses={200: dict})
    def get(self, request):
        user = request.user
        
        cache_key = f"chat_stats:{user.id}"
        cached = cache.get(cache_key)
        if cached: return Response(cached)
        
        total_sessions = ChatSession.objects.filter(user=user).count()
        user_messages = user.msg_count
        ai_messages = 0
        
        stats = {
            "total_sessions": total_sessions,
            "total_messages": user_messages,
            "user_messages": user_messages,
            "ai_messages": ai_messages,
            "total_tokens_used": user.tokens_used,
        }
        cache.set(cache_key, stats, 300)
        return Response(stats)