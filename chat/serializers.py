from rest_framework import serializers
from .models import ChatSession, Message, DetectedEvent
from core.serializers import TargetProfileSerializer

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'is_ai', 'text', 'image', 'ocr_extracted_text', 'created_at']

class DetectedEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetectedEvent
        fields = ['id', 'title', 'description', 'start_time', 'created_at']

class ChatSessionListSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    target_profile = TargetProfileSerializer(read_only=True)
    events = DetectedEventSerializer(many=True, read_only=True)

    class Meta:
        model = ChatSession
        fields = ['conversation_id', 'title', 'target_profile', 'last_message', 'events', 'updated_at']

    def get_last_message(self, obj):
        last_msg = obj.messages.last()
        if last_msg:
            return last_msg.text[:50] + "..." if last_msg.text else "[Image]"
        return ""

class ChatSessionDetailSerializer(serializers.ModelSerializer):
    target_profile = TargetProfileSerializer(read_only=True)
    events = DetectedEventSerializer(many=True, read_only=True)

    class Meta:
        model = ChatSession
        fields = ['conversation_id', 'title', 'target_profile', 'events', 'created_at', 'updated_at']

class ChatSessionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatSession
        fields = ['title']

class MessageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()
    text = serializers.CharField(required=False, allow_blank=True)