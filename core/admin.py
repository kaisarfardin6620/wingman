from django.contrib import admin
from .models import Tone, Persona, UserSettings, TargetProfile, GlobalConfig, FCMDevice, Notification

@admin.register(Tone)
class ToneAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')

@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_active')

@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'language', 'active_persona', 'passcode_lock_enabled')

@admin.register(TargetProfile)
class TargetProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')

@admin.register(GlobalConfig)
class GlobalConfigAdmin(admin.ModelAdmin):
    list_display = ('daily_free_limit', 'max_chat_length', 'ocr_limit')

    def has_add_permission(self, request):
        return not GlobalConfig.objects.exists()
        
    def has_delete_permission(self, request, obj=None):
        return False
    
@admin.register(FCMDevice)
class FCMDeviceAdmin(admin.ModelAdmin):
    list_display = ('user', 'device_type', 'token_preview', 'created_at')
    search_fields = ('user__email',)
    list_filter = ('device_type', 'created_at')

    def token_preview(self, obj):
        return obj.token[:20] + "..." if obj.token else ""

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__email', 'title', 'body')