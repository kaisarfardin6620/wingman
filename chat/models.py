import uuid
from django.db import models
from django.conf import settings
from core.models import TargetProfile

class ChatSession(models.Model):
    conversation_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_sessions')
    target_profile = models.ForeignKey(TargetProfile, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255, default="New Chat")
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
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

class DetectedEvent(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_time = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title