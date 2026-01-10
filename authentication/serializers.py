from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.validators import EmailValidator
from django.core.cache import cache
import re

User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        max_length=128,
        style={'input_type': 'password'},
        error_messages={
            'min_length': 'Password must be at least 8 characters long.',
            'max_length': 'Password cannot exceed 128 characters.',
        }
    )
    confirm_password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    email = serializers.EmailField(
        validators=[EmailValidator(message="Enter a valid email address.")],
        error_messages={
            'required': 'Email is required.',
            'invalid': 'Enter a valid email address.',
        }
    )

    class Meta:
        model = User
        fields = ['email', 'password', 'confirm_password']
        
    def validate_email(self, value):
        email = value.lower().strip()
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        disposable_domains = ['tempmail.com', 'guerrillamail.com', '10minutemail.com']
        domain = email.split('@')[-1]
        if domain in disposable_domains:
            raise serializers.ValidationError("Disposable email addresses are not allowed.")
        return email

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        
        if password != confirm_password:
            raise serializers.ValidationError({
                "confirm_password": "Password fields didn't match."
            })
        
        try:
            validate_password(password)
        except Exception as e:
            raise serializers.ValidationError({
                "password": list(e.messages)
            })
        
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        validated_data['email'] = validated_data['email'].lower().strip()
        return User.objects.create_user(**validated_data)


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(
        required=True,
        min_length=4,
        max_length=4,
        error_messages={'min_length': 'OTP must be 4 digits.', 'max_length': 'OTP must be 4 digits.'}
    )
    
    def validate_email(self, value):
        return value.lower().strip()
    
    def validate_otp(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("OTP must contain only numbers.")
        return value


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    
    def validate_email(self, value):
        return value.lower().strip()


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    
    def validate_email(self, value):
        return value.lower().strip()


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(
        required=True,
        min_length=4,
        max_length=4
    )
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        min_length=8
    )
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate_email(self, value):
        return value.lower().strip()
    
    def validate_otp(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("OTP must contain only numbers.")
        return value

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')
        
        if new_password != confirm_password:
            raise serializers.ValidationError({
                "confirm_password": "Passwords do not match."
            })
        
        try:
            validate_password(new_password)
        except Exception as e:
            raise serializers.ValidationError({
                "new_password": list(e.messages)
            })
        return attrs


class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    def validate_email(self, value):
        return value.lower().strip()


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)
    def validate_refresh(self, value):
        if not value or len(value) < 20:
            raise serializers.ValidationError("Invalid refresh token format.")
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    profile_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'profile_image', 'profile_image_url', 'is_premium', 'date_joined']
        read_only_fields = ['id', 'email', 'is_premium', 'date_joined']
        
    def get_profile_image_url(self, obj):
        request = self.context.get('request')
        if obj.profile_image and hasattr(obj.profile_image, 'url'):
            if request:
                return request.build_absolute_uri(obj.profile_image.url)
            return obj.profile_image.url
        return None
    
    def validate_name(self, value):
        if value:
            value = value.strip()
            if len(value) < 2:
                raise serializers.ValidationError("Name must be at least 2 characters long.")
            if len(value) > 100:
                raise serializers.ValidationError("Name cannot exceed 100 characters.")
        return value
    
    def validate_profile_image(self, value):
        if value:
            max_size = 5 * 1024 * 1024
            if value.size > max_size:
                raise serializers.ValidationError("Image file size cannot exceed 5MB.")
        return value
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save(update_fields=validated_data.keys())
        cache_key = f"user_profile:{instance.id}"
        cache.delete(cache_key)
        return instance


class UserPublicSerializer(serializers.ModelSerializer):
    profile_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'name', 'profile_image_url']
        read_only_fields = ['id', 'name', 'profile_image_url']
    
    def get_profile_image_url(self, obj):
        request = self.context.get('request')
        if obj.profile_image and hasattr(obj.profile_image, 'url'):
            if request:
                return request.build_absolute_uri(obj.profile_image.url)
            return obj.profile_image.url
        return None