from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Tone, Persona, UserSettings, TargetProfile
from .models import Notification

class ToneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tone
        fields = ['id', 'name', 'description']

class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = ['id', 'name', 'description']

class UserSettingsSerializer(serializers.ModelSerializer):
    selected_tones_details = ToneSerializer(source='active_tones', many=True, read_only=True)
    active_tones_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tone.objects.all(), many=True, source='active_tones', write_only=True
    )
    
    active_persona_details = PersonaSerializer(source='active_persona', read_only=True)
    active_persona_id = serializers.PrimaryKeyRelatedField(
        queryset=Persona.objects.all(), source='active_persona', write_only=True, allow_null=True
    )

    class Meta:
        model = UserSettings
        fields = [
            'language', 'gold_theme', 'premium_logo', 
            'passcode_lock_enabled', 'passcode',
            'hide_notifications',
            'selected_tones_details', 'active_tones_ids',
            'active_persona_details', 'active_persona_id',
            'linguistic_style', 'goal'
        ]
        extra_kwargs = {
            'passcode': {'write_only': True},
            'linguistic_style': {'read_only': True}
        }

    def update(self, instance, validated_data):
        if 'passcode' in validated_data:
            validated_data['passcode'] = make_password(validated_data['passcode'])
        return super().update(instance, validated_data)

class TargetProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TargetProfile
        fields = ['id', 'name', 'birthday', 'preferences', 'what_she_likes', 'details', 'her_mentions', 'avatar', 'created_at']

class PasscodeVerifySerializer(serializers.Serializer):
    passcode = serializers.CharField(max_length=4)

class ForgotPasscodeSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ResetPasscodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=4)
    new_passcode = serializers.CharField(max_length=4)
    confirm_passcode = serializers.CharField(max_length=4)

    def validate(self, attrs):
        if attrs['new_passcode'] != attrs['confirm_passcode']:
            raise serializers.ValidationError({"new_passcode": "Passcodes do not match."})
        return attrs

class ChangePasscodeSerializer(serializers.Serializer):
    old_passcode = serializers.CharField(max_length=4)
    new_passcode = serializers.CharField(max_length=4)
    confirm_passcode = serializers.CharField(max_length=4)

    def validate(self, attrs):
        if attrs['new_passcode'] != attrs['confirm_passcode']:
            raise serializers.ValidationError({"new_passcode": "Passcodes do not match."})
        return attrs
    
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'body', 'data', 'is_read', 'created_at']
        read_only_fields = ['id', 'title', 'body', 'data', 'created_at']    