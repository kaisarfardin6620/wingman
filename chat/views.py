from rest_framework import viewsets, mixins, parsers, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ChatSession, Message
from .serializers import ChatSessionListSerializer, MessageSerializer
from .tasks import analyze_screenshot_task

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

class ChatSessionImageUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def post(self, request, conversation_id):
        try:
            session = ChatSession.objects.get(conversation_id=conversation_id, user=request.user)
        except ChatSession.DoesNotExist:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)

        file_obj = request.data.get('image')
        if not file_obj:
            return Response({"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST)

        msg = Message.objects.create(
            session=session,
            sender=request.user,
            is_ai=False,
            text="[Screenshot Uploaded]",
            image=file_obj
        )

        analyze_screenshot_task.delay(msg.id)

        return Response(MessageSerializer(msg).data, status=status.HTTP_201_CREATED)