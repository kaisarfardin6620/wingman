from django.contrib import admin
from .models import ChatSession, Message

class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('sender', 'is_ai', 'text', 'image', 'analysis_tags', 'created_at')

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('conversation_id', 'user', 'title', 'message_count', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('conversation_id', 'user__email', 'title', 'target_profile__name')
    readonly_fields = ('conversation_id', 'created_at', 'updated_at')
    inlines = [MessageInline]

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'session', 'sender', 'is_ai', 'short_text', 'created_at')
    list_filter = ('is_ai', 'created_at', 'processing_status')
    search_fields = ('text', 'session__conversation_id', 'session__user__email')
    readonly_fields = ('created_at',)

    def short_text(self, obj):
        return obj.text[:50] + "..." if obj.text and len(obj.text) > 50 else obj.text