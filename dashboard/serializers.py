from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from core.models import Tone, Persona, GlobalConfig
from chat.models import Message

User = get_user_model()

class DashboardStatsSerializer(serializers.Serializer):
    total_users = serializers.IntegerField()
    active_today = serializers.IntegerField()
    premium_users = serializers.IntegerField()
    conversion_rate = serializers.FloatField()
    free_users = serializers.IntegerField()
    graph_data = serializers.ListField()

class AdminUserListSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    usage_count = serializers.SerializerMethodField()
    subscription = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'profile_image', 'subscription', 'usage_count', 'status', 'is_active', 'date_joined']

    def get_status(self, obj):
        return "Active" if obj.is_active else "Inactive"

    def get_usage_count(self, obj):
        return Message.objects.filter(sender=obj).count()

    def get_subscription(self, obj):
        return "Premium" if obj.is_premium else "Free"

class AdminToneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tone
        fields = ['id', 'name', 'details', 'is_active']

class AdminPersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = ['id', 'name', 'description', 'is_active']

class GlobalConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalConfig
        fields = ['daily_free_limit', 'max_chat_length', 'ocr_limit']

class AdminProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'profile_image']

    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        
        user = self.context['request'].user
        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError({"old_password": "Old password is not correct."})
        
        validate_password(attrs['new_password'], user)
        return attrs