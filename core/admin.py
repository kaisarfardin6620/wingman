from django.contrib import admin
from .models import Tone, Persona, UserSettings, TargetProfile

@admin.register(Tone)
class ToneAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')

@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_active')

@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'language', 'passcode_lock_enabled')

@admin.register(TargetProfile)
class TargetProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')