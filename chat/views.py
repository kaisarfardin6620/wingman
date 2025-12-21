import threading # <--- IMPORT THREADING
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, parsers
from rest_framework.permissions import IsAuthenticated
from .models import ChatSession, Message
from .serializers import ChatSessionSerializer, MessageSerializer
from core.models import TargetProfile
from .tasks import analyze_screenshot_task, generate_ai_reply_task, generate_title_task

class ChatHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, session_id):
        try:
            session = ChatSession.objects.get(id=session_id, user=request.user)
            messages = session.messages.all().order_by('created_at')
            return Response(MessageSerializer(messages, many=True).data)
        except ChatSession.DoesNotExist:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)

class CreateSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        chat_type = request.data.get('chat_type', 'general')
        target_id = request.data.get('target_profile_id')
        first_message = request.data.get('message')
        
        target = None
        session_title = "New Chat"

        if chat_type == 'target':
            if not target_id:
                return Response({"error": "target_profile_id is required for target chat"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                target = TargetProfile.objects.get(id=target_id, user=request.user)
                session_title = f"Chat about {target.name}"
            except TargetProfile.DoesNotExist:
                return Response({"error": "Target Profile not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            session_title = "General Wingman"

        session = ChatSession.objects.create(
            user=request.user, 
            chat_type=chat_type,
            target_profile=target,
            title=session_title
        )

        if first_message:
            Message.objects.create(
                session=session,
                sender=request.user,
                is_ai=False,
                text=first_message
            )
            # FIX: Use Threading instead of Celery .delay()
            threading.Thread(target=generate_title_task, args=(session.id, first_message)).start()
            threading.Thread(target=generate_ai_reply_task, args=(session.id, first_message)).start()

        return Response(ChatSessionSerializer(session).data)

class ImageUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def post(self, request, session_id):
        try:
            session = ChatSession.objects.get(id=session_id, user=request.user)
        except ChatSession.DoesNotExist:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)
            
        file_obj = request.data.get('image')
        if not file_obj:
            return Response({"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST)

        message = Message.objects.create(
            session=session,
            sender=request.user,
            is_ai=False,
            image=file_obj,
            text="[Screenshot Uploaded]"
        )

        # FIX: Use Threading instead of Celery .delay()
        threading.Thread(target=analyze_screenshot_task, args=(message.id,)).start()

        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)