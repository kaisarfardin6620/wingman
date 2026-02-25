from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from .models import ChatSession, Message, DetectedEvent, MessageImage
from core.serializers import TargetProfileSerializer

class MessageImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = MessageImage
        fields =['id', 'image_url']
        
    @extend_schema_field(serializers.CharField())
    def get_image_url(self, obj):
        request = self.context.get('request')
        if request and obj.image:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url if obj.image else None

class MessageSerializer(serializers.ModelSerializer):
    images = MessageImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Message
        fields =[
            'id', 'is_ai', 'text', 'images', 'audio', 
            'ocr_extracted_text', 'created_at', 'processing_status'
        ]

class DetectedEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetectedEvent
        fields =['id', 'title', 'description', 'start_time', 'created_at', 'has_conflict']

class ChatSessionListSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    target_profile = TargetProfileSerializer(read_only=True)
    events = DetectedEventSerializer(many=True, read_only=True)

    class Meta:
        model = ChatSession
        fields =['conversation_id', 'title', 'target_profile', 'last_message', 'events', 'updated_at']

    @extend_schema_field(serializers.CharField(allow_null=True))
    def get_last_message(self, obj):
        return obj.last_message_preview or ""

class ChatSessionDetailSerializer(serializers.ModelSerializer):
    target_profile = TargetProfileSerializer(read_only=True)
    events = DetectedEventSerializer(many=True, read_only=True)

    class Meta:
        model = ChatSession
        fields =['conversation_id', 'title', 'target_profile', 'events', 'created_at', 'updated_at']

class ChatSessionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatSession
        fields = ['title']

class MessageUploadSerializer(serializers.Serializer):
    images = serializers.ListField(
        child=serializers.ImageField(), 
        required=False,
        allow_empty=True
    )
    audio = serializers.FileField(required=False, allow_null=True)
    text = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        if not attrs.get('images') and not attrs.get('audio') and not attrs.get('text'):
            raise serializers.ValidationError("Must provide either images, audio, or text.")
        return attrs