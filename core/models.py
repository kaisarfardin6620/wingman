from django.db import models
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password

class Tone(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, blank=True, null=True) 
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Persona(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class GlobalConfig(models.Model):
    daily_free_limit = models.IntegerField(default=10)
    max_chat_length = models.IntegerField(default=1000)
    ocr_limit = models.IntegerField(default=5)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.pk = 1
        super(GlobalConfig, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "System Configuration"

class UserSettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='settings')
    language = models.CharField(max_length=50, default='English')
    active_persona = models.ForeignKey(Persona, on_delete=models.SET_NULL, null=True, blank=True)
    active_tones = models.ManyToManyField(Tone, blank=True)
    
    linguistic_style = models.TextField(blank=True, null=True)
    
    passcode_lock_enabled = models.BooleanField(default=False)
    passcode = models.CharField(max_length=128, blank=True, null=True)
    gold_theme = models.BooleanField(default=False)
    premium_logo = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Settings for {self.user.email}"

    def set_passcode(self, raw_passcode):
        self.passcode = make_password(raw_passcode)
        self.save()

    def check_passcode(self, raw_passcode):
        return check_password(raw_passcode, self.passcode)

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