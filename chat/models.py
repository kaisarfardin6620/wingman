import uuid
import json
from django.db import models
from django.db.models import F
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
            preview_text = last_msg.text
            if not preview_text:
                if last_msg.images.exists(): preview_text = "[Image]"
                elif last_msg.audio: preview_text = "[Voice Note]"
                else: preview_text = ""
            
            if last_msg.is_ai and preview_text.strip().startswith('{'):
                try:
                    data = json.loads(preview_text)
                    if 'content' in data:
                        content = data['content']
                        if isinstance(content, list) and content:
                            preview_text = content[0]
                        elif isinstance(content, str):
                            preview_text = content
                except (json.JSONDecodeError, AttributeError, TypeError):
                    pass

            self.last_message_preview = (preview_text[:97] + "...") if len(preview_text) > 100 else preview_text
            self.updated_at = last_msg.created_at
            
            ChatSession.objects.filter(pk=self.pk).update(
                last_message_preview=self.last_message_preview,
                updated_at=self.updated_at,
                message_count=models.Subquery(
                    Message.objects.filter(session_id=self.pk).values('session_id').annotate(count=models.Count('id')).values('count')
                )
            )

class Message(models.Model):
    STATUS_CHOICES =[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

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
    audio = models.FileField(upload_to='chat_audio/', null=True, blank=True)
    ocr_extracted_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    tokens_used = models.PositiveIntegerField(default=0, null=True, blank=True)
    analysis_tags = models.JSONField(
        default=list, 
        blank=True,
        help_text="AI-generated tags/metadata for this message"
    )
    processing_status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='completed',
        db_index=True
    )

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering =['created_at']
        indexes = [
            models.Index(fields=['session', 'created_at']),
            models.Index(fields=['sender', 'is_ai', '-created_at']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f"Message {self.id} - {'AI' if self.is_ai else 'User'} ({self.processing_status})"

class MessageImage(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='chat_uploads/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Message Image"
        verbose_name_plural = "Message Images"
        ordering = ['created_at']

    def __str__(self):
        return f"Image for Message {self.message.id}"

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
    has_conflict = models.BooleanField(default=False)
    reminder_datetime = models.DateTimeField(null=True, blank=True, db_index=True)
    reminder_sent = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Detected Event"
        verbose_name_plural = "Detected Events"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['session', '-created_at']),
            models.Index(fields=['reminder_datetime', 'reminder_sent']),
        ]

    def __str__(self):
        return self.title