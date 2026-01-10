from django.db import models
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.core.cache import cache


class Tone(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Tone"
        verbose_name_plural = "Tones"
        ordering = ['name']
        indexes = [
            models.Index(fields=['is_active', 'name']),
        ]

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # ✅ Invalidate config cache when tones change
        cache.delete('active_tones')
        cache.delete('global_config')


class Persona(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"
        ordering = ['name']
        indexes = [
            models.Index(fields=['is_active', 'name']),
        ]

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # ✅ Invalidate config cache when personas change
        cache.delete('active_personas')
        cache.delete('global_config')


class GlobalConfig(models.Model):
    daily_free_limit = models.IntegerField(
        default=10,
        help_text="Daily message limit for free users"
    )
    max_chat_length = models.IntegerField(
        default=1000,
        help_text="Maximum message length for free users"
    )
    ocr_limit = models.IntegerField(
        default=5,
        help_text="Daily OCR/image upload limit for free users"
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Global Configuration"
        verbose_name_plural = "Global Configurations"

    def save(self, *args, **kwargs):
        # ✅ Singleton pattern - only one config
        self.pk = 1
        super().save(*args, **kwargs)
        
        # ✅ Clear cache when config changes
        cache.delete('global_config')

    @classmethod
    def load(cls):
        """
        Load global config with caching
        ✅ Cache for 1 hour
        """
        cache_key = 'global_config'
        config = cache.get(cache_key)
        
        if config is None:
            config, created = cls.objects.get_or_create(pk=1)
            cache.set(cache_key, config, 3600)  # 1 hour
        
        return config
    
    def delete(self, *args, **kwargs):
        """Prevent deletion of singleton"""
        pass

    def __str__(self):
        return "System Configuration"


class UserSettings(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='settings',
        db_index=True
    )
    language = models.CharField(max_length=50, default='English')
    active_persona = models.ForeignKey(
        Persona,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_settings'
    )
    active_tones = models.ManyToManyField(Tone, blank=True, related_name='user_settings')
    linguistic_style = models.TextField(
        blank=True,
        null=True,
        help_text="Auto-generated user writing style"
    )
    
    # Security settings
    passcode_lock_enabled = models.BooleanField(default=False)
    passcode = models.CharField(max_length=128, blank=True, null=True)
    
    # Theme settings
    gold_theme = models.BooleanField(default=False)
    premium_logo = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User Settings"
        verbose_name_plural = "User Settings"

    def __str__(self):
        return f"Settings for {self.user.email}"

    def set_passcode(self, raw_passcode):
        """
        Hash and save passcode
        ✅ Validate passcode format
        """
        if not raw_passcode or len(raw_passcode) != 4 or not raw_passcode.isdigit():
            raise ValueError("Passcode must be exactly 4 digits")
        
        self.passcode = make_password(raw_passcode)
        self.save(update_fields=['passcode'])

    def check_passcode(self, raw_passcode):
        """Verify passcode"""
        if not self.passcode:
            return False
        return check_password(raw_passcode, self.passcode)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # ✅ Invalidate user settings cache
        cache.delete(f"user_settings:{self.user.id}")


class TargetProfile(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='target_profiles',
        db_index=True
    )
    name = models.CharField(max_length=100, db_index=True)
    preferences = models.JSONField(
        default=list,
        blank=True,
        help_text="List of preferences"
    )
    what_she_likes = models.JSONField(
        default=list,
        blank=True,
        help_text="Things she likes"
    )
    details = models.TextField(blank=True, help_text="Additional details")
    her_mentions = models.TextField(blank=True, help_text="Her mentions")
    avatar = models.ImageField(upload_to='target_profiles/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Target Profile"
        verbose_name_plural = "Target Profiles"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['user', 'name']),
        ]
        # ✅ Add unique constraint
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'name'],
                name='unique_user_target_name'
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.user.email})"
    
    def clean(self):
        """Validate model"""
        from django.core.exceptions import ValidationError
        
        # ✅ Validate name
        if len(self.name.strip()) < 2:
            raise ValidationError("Name must be at least 2 characters")
        
        # ✅ Validate JSON fields are actually lists
        if not isinstance(self.preferences, list):
            self.preferences = []
        if not isinstance(self.what_she_likes, list):
            self.what_she_likes = []