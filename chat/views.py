from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ChatSession
from .serializers import ChatSessionListSerializer, MessageSerializer

class ChatSessionViewSet(viewsets.GenericViewSet, 
                         mixins.ListModelMixin, 
                         mixins.DestroyModelMixin):
    
    permission_classes = [IsAuthenticated]
    serializer_class = ChatSessionListSerializer
    lookup_field = 'conversation_id'

    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user).order_by('-updated_at')

    @action(detail=True, methods=['get'])
    def history(self, request, conversation_id=None):
        session = self.get_object()
        messages = session.messages.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def rename(self, request, conversation_id=None):
        session = self.get_object()
        new_title = request.data.get('title')
        if new_title:
            session.title = new_title
            session.save()
            return Response({"title": session.title})
        return Response({"error": "Title required"}, status=400)    