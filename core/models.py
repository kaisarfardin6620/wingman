from django.db import models
from django.conf import settings

class Tone(models.Model):
    name = models.CharField(max_length=50)
    icon_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Persona(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    icon_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class UserSettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='settings')
    language = models.CharField(max_length=50, default='English')
    selected_tones = models.ManyToManyField(Tone, blank=True)
    active_persona = models.ForeignKey(Persona, on_delete=models.SET_NULL, null=True, blank=True)
    gold_theme = models.BooleanField(default=False)
    premium_logo = models.BooleanField(default=False)
    wingman_persona_active = models.BooleanField(default=True)
    hide_notifications = models.BooleanField(default=False)
    passcode_lock_enabled = models.BooleanField(default=False)
    passcode = models.CharField(max_length=4, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Settings for {self.user.email}"

class TargetProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='target_profiles')
    name = models.CharField(max_length=100)
    preferences = models.JSONField(default=list, blank=True)
    what_she_likes = models.JSONField(default=list, blank=True)
    details = models.TextField(blank=True)
    her_mentions = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='target_profiles/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name