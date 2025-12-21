from rest_framework import serializers
from .models import Tone, Persona, UserSettings, TargetProfile

class ToneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tone
        fields = ['id', 'name', 'icon_url']

class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = ['id', 'name', 'description', 'icon_url']

class UserSettingsSerializer(serializers.ModelSerializer):
    selected_tones_details = ToneSerializer(source='selected_tones', many=True, read_only=True)
    selected_tones_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tone.objects.all(), many=True, source='selected_tones', write_only=True
    )
    
    active_persona_details = PersonaSerializer(source='active_persona', read_only=True)
    active_persona_id = serializers.PrimaryKeyRelatedField(
        queryset=Persona.objects.all(), source='active_persona', write_only=True, allow_null=True
    )

    class Meta:
        model = UserSettings
        fields = [
            'language', 
            'gold_theme', 'premium_logo', 'wingman_persona_active',
            'hide_notifications', 'passcode_lock_enabled', 'passcode',
            'selected_tones_details', 'selected_tones_ids',
            'active_persona_details', 'active_persona_id'
        ]
        extra_kwargs = {
            'passcode': {'write_only': False},
        }

class TargetProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TargetProfile
        fields = ['id', 'name', 'preferences', 'what_she_likes', 'details', 'her_mentions', 'avatar', 'created_at']