import uuid
from django.db import models
from django.conf import settings
from core.models import TargetProfile

class ChatSession(models.Model):
    TYPE_CHOICES = (
        ('general', 'General Chatbot'),
        ('target', 'Target Specific Chat'),
    )

    conversation_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_sessions')
    chat_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='general')
    target_profile = models.ForeignKey(TargetProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='sessions')
    title = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.conversation_id})"

class Message(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    is_ai = models.BooleanField(default=False)
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='chat_uploads/', null=True, blank=True)
    ocr_extracted_text = models.TextField(blank=True, null=True)
    analysis_tags = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)