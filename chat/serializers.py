from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from .models import ChatSession, Message, DetectedEvent
from core.serializers import TargetProfileSerializer

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            'id', 'is_ai', 'text', 'image', 'audio', 
            'ocr_extracted_text', 'created_at', 'processing_status'
        ]

class DetectedEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetectedEvent
        fields = ['id', 'title', 'description', 'start_time', 'created_at', 'has_conflict']

class ChatSessionListSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    target_profile = TargetProfileSerializer(read_only=True)
    events = DetectedEventSerializer(many=True, read_only=True)

    class Meta:
        model = ChatSession
        fields = ['conversation_id', 'title', 'target_profile', 'last_message', 'events', 'updated_at']

    @extend_schema_field(serializers.CharField(allow_null=True))
    def get_last_message(self, obj):
        return obj.last_message_preview or ""

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
    image = serializers.ImageField(required=False, allow_null=True)
    audio = serializers.FileField(required=False, allow_null=True)
    text = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        if not attrs.get('image') and not attrs.get('audio') and not attrs.get('text'):
            raise serializers.ValidationError("Must provide either image, audio, or text.")
        return attrs