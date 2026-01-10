import uuid
from django.db import models
from django.conf import settings
from core.models import TargetProfile


class ChatSession(models.Model):
    conversation_id = models.UUIDField(
        default=uuid.uuid4, 
        editable=False, 
        unique=True,
        db_index=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='chat_sessions',
        db_index=True
    )
    target_profile = models.ForeignKey(
        TargetProfile, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        db_index=True
    )
    title = models.CharField(max_length=255, default="New Chat")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    message_count = models.PositiveIntegerField(default=0)
    last_message_preview = models.CharField(max_length=100, blank=True, default="")

    class Meta:
        verbose_name = "Chat Session"
        verbose_name_plural = "Chat Sessions"
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['user', '-updated_at']),
            models.Index(fields=['conversation_id']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f"{self.title} ({self.conversation_id})"
    
    def update_preview(self):
        last_msg = self.messages.order_by('-created_at').first()
        if last_msg:
            self.last_message_preview = (last_msg.text[:97] + "...") if last_msg.text and len(last_msg.text) > 100 else (last_msg.text or "[Image]")
            self.message_count = self.messages.count()
            self.save(update_fields=['last_message_preview', 'message_count', 'updated_at'])


class Message(models.Model):
    session = models.ForeignKey(
        ChatSession, 
        on_delete=models.CASCADE, 
        related_name='messages',
        db_index=True
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        db_index=True
    )
    is_ai = models.BooleanField(default=False, db_index=True)
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='chat_uploads/', null=True, blank=True)
    ocr_extracted_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    tokens_used = models.PositiveIntegerField(default=0, null=True, blank=True)

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['session', 'created_at']),
            models.Index(fields=['sender', 'is_ai', '-created_at']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f"Message {self.id} - {'AI' if self.is_ai else 'User'}"


class DetectedEvent(models.Model):
    session = models.ForeignKey(
        ChatSession, 
        on_delete=models.CASCADE, 
        related_name='events',
        db_index=True
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_time = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    is_confirmed = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Detected Event"
        verbose_name_plural = "Detected Events"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['session', '-created_at']),
        ]

    def __str__(self):
        return self.title