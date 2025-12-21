from rest_framework import serializers
from .models import ChatSession, Message
from core.serializers import TargetProfileSerializer

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'is_ai', 'text', 'image', 'created_at']

class ChatSessionListSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    target_profile = TargetProfileSerializer(read_only=True)

    class Meta:
        model = ChatSession
        fields = ['conversation_id', 'title', 'target_profile', 'last_message', 'updated_at']

    def get_last_message(self, obj):
        last_msg = obj.messages.last()
        if last_msg:
            return last_msg.text[:50] + "..."
        return ""