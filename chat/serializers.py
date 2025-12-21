from rest_framework import serializers
from .models import ChatSession, Message
from core.serializers import TargetProfileSerializer

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'session', 'is_ai', 'text', 'image', 'ocr_extracted_text', 'analysis_tags', 'created_at']

class ChatSessionSerializer(serializers.ModelSerializer):
    target_profile = TargetProfileSerializer(read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = ChatSession
        fields = ['id', 'title', 'chat_type', 'target_profile', 'last_message', 'updated_at']

    def get_last_message(self, obj):
        last_msg = obj.messages.order_by('-created_at').first()
        if last_msg:
            return MessageSerializer(last_msg).data
        return None