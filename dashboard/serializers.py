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
    profile_image_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'email', 'name', 'profile_image', 'profile_image_url',
            'subscription', 'usage_count', 'status',
            'is_active', 'is_premium', 'is_staff', 'date_joined', 'last_login'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']

    def get_status(self, obj):
        """Get user status"""
        return "Active" if obj.is_active else "Inactive"

    def get_usage_count(self, obj):
        """
        Get message count
        ✅ Cached or use annotation if provided
        """
        # Check if already annotated in queryset
        if hasattr(obj, 'msg_count'):
            return obj.msg_count
        
        # Fallback to query
        return Message.objects.filter(sender=obj, is_ai=False).count()

    def get_subscription(self, obj):
        """Get subscription type"""
        return "Premium" if obj.is_premium else "Free"
    
    def get_profile_image_url(self, obj):
        """Get full profile image URL"""
        if obj.profile_image and hasattr(obj.profile_image, 'url'):
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.profile_image.url)
            return obj.profile_image.url
        return None


class AdminToneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tone
        fields = ['id', 'name', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_name(self, value):
        """Validate tone name"""
        if value:
            value = value.strip()
            
            if len(value) < 2:
                raise serializers.ValidationError("Name must be at least 2 characters.")
            if len(value) > 50:
                raise serializers.ValidationError("Name cannot exceed 50 characters.")
            
            # Check uniqueness (exclude current instance on update)
            queryset = Tone.objects.filter(name__iexact=value)
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)
            
            if queryset.exists():
                raise serializers.ValidationError("A tone with this name already exists.")
        
        return value


class AdminPersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = ['id', 'name', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_name(self, value):
        """Validate persona name"""
        if value:
            value = value.strip()
            
            if len(value) < 2:
                raise serializers.ValidationError("Name must be at least 2 characters.")
            if len(value) > 50:
                raise serializers.ValidationError("Name cannot exceed 50 characters.")
            
            # Check uniqueness (exclude current instance on update)
            queryset = Persona.objects.filter(name__iexact=value)
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)
            
            if queryset.exists():
                raise serializers.ValidationError("A persona with this name already exists.")
        
        return value
    
    def validate_description(self, value):
        """Validate description"""
        if value:
            if len(value) < 10:
                raise serializers.ValidationError("Description must be at least 10 characters.")
            if len(value) > 2000:
                raise serializers.ValidationError("Description cannot exceed 2000 characters.")
        
        return value


class GlobalConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalConfig
        fields = ['daily_free_limit', 'max_chat_length', 'ocr_limit', 'updated_at']
        read_only_fields = ['updated_at']
    
    def validate_daily_free_limit(self, value):
        """Validate daily free limit"""
        if value < 1:
            raise serializers.ValidationError("Daily limit must be at least 1.")
        if value > 1000:
            raise serializers.ValidationError("Daily limit cannot exceed 1000.")
        return value
    
    def validate_max_chat_length(self, value):
        """Validate max chat length"""
        if value < 100:
            raise serializers.ValidationError("Max chat length must be at least 100 characters.")
        if value > 50000:
            raise serializers.ValidationError("Max chat length cannot exceed 50,000 characters.")
        return value
    
    def validate_ocr_limit(self, value):
        """Validate OCR limit"""
        if value < 1:
            raise serializers.ValidationError("OCR limit must be at least 1.")
        if value > 100:
            raise serializers.ValidationError("OCR limit cannot exceed 100.")
        return value


class AdminProfileUpdateSerializer(serializers.ModelSerializer):
    profile_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'profile_image', 'profile_image_url']
        read_only_fields = ['id']

    def get_profile_image_url(self, obj):
        """Get full profile image URL"""
        if obj.profile_image and hasattr(obj.profile_image, 'url'):
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.profile_image.url)
            return obj.profile_image.url
        return None

    def validate_email(self, value):
        """Validate email uniqueness"""
        if value:
            value = value.lower().strip()
            
            user = self.context['request'].user
            
            # Check if email is already taken by another user
            if User.objects.exclude(pk=user.pk).filter(email=value).exists():
                raise serializers.ValidationError("This email is already in use.")
        
        return value
    
    def validate_name(self, value):
        """Validate name"""
        if value:
            value = value.strip()
            
            if len(value) < 2:
                raise serializers.ValidationError("Name must be at least 2 characters.")
            if len(value) > 100:
                raise serializers.ValidationError("Name cannot exceed 100 characters.")
        
        return value
    
    def validate_profile_image(self, value):
        """Validate profile image"""
        if value:
            # Check file size (max 5MB)
            max_size = 5 * 1024 * 1024
            if value.size > max_size:
                raise serializers.ValidationError("Image file size cannot exceed 5MB.")
            
            # Check file type
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
            if hasattr(value, 'content_type'):
                if value.content_type not in allowed_types:
                    raise serializers.ValidationError("Only JPEG, PNG, and WebP images are allowed.")
        
        return value


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        min_length=8,
        style={'input_type': 'password'}
    )
    confirm_password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    def validate_old_password(self, value):
        """Verify old password"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def validate(self, attrs):
        """Cross-field validation"""
        # Check if passwords match
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({
                "confirm_password": "Password fields didn't match."
            })
        
        # Validate password strength
        user = self.context['request'].user
        try:
            validate_password(attrs['new_password'], user)
        except Exception as e:
            raise serializers.ValidationError({
                "new_password": list(e.messages)
            })
        
        return attrs