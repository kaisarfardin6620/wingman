from django.contrib import admin
from .models import Tone, Persona, UserSettings, TargetProfile, GlobalConfig

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