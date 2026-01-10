from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.shortcuts import get_object_or_404
from authentication.utils import send_otp_via_email, verify_otp_via_email
from .models import Tone, Persona, UserSettings, TargetProfile, FCMDevice
from .serializers import (
    ToneSerializer, PersonaSerializer,
    UserSettingsSerializer, TargetProfileSerializer,
    PasscodeVerifySerializer, ResetPasscodeSerializer
)
import logging

User = get_user_model()
logger = logging.getLogger(__name__)

class ConfigThrottle(UserRateThrottle):
    rate = '30/minute'

class ConfigDataView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [ConfigThrottle]

    @method_decorator(cache_page(300))
    def get(self, request):
        cache_key_tones = 'active_tones'
        cache_key_personas = 'active_personas'
        
        tones_data = cache.get(cache_key_tones)
        personas_data = cache.get(cache_key_personas)
        
        if tones_data is None:
            tones = Tone.objects.filter(is_active=True).only('id', 'name', 'description')
            tones_data = ToneSerializer(tones, many=True).data
            cache.set(cache_key_tones, tones_data, 300)
        
        if personas_data is None:
            personas = Persona.objects.filter(is_active=True).only('id', 'name', 'description')
            personas_data = PersonaSerializer(personas, many=True).data
            cache.set(cache_key_personas, personas_data, 300)
        
        return Response({
            "tones": tones_data,
            "personas": personas_data
        })

class UserSettingsView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get(self, request):
        cache_key = f"user_settings:{request.user.id}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data)
        
        settings, created = UserSettings.objects.select_related(
            'active_persona'
        ).prefetch_related(
            'active_tones'
        ).get_or_create(user=request.user)
        
        serializer = UserSettingsSerializer(settings)
        cache.set(cache_key, serializer.data, 300)
        return Response(serializer.data)

    def patch(self, request):
        settings, created = UserSettings.objects.get_or_create(user=request.user)
        
        serializer = UserSettingsSerializer(
            settings,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save()
            cache.delete(f"user_settings:{request.user.id}")
            return Response({
                "message": "Settings updated successfully",
                "data": serializer.data
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TargetProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    serializer_class = TargetProfileSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return TargetProfile.objects.filter(
            user=self.request.user
        ).order_by('-created_at')
    
    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(
            TargetProfile,
            pk=pk,
            user=self.request.user
        )
        return obj

    def perform_create(self, serializer):
        if not self.request.user.is_premium:
            profile_count = TargetProfile.objects.filter(user=self.request.user).count()
            if profile_count >= 10:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied("Free limit reached.")
        serializer.save(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class VerifyPasscodeView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        serializer = PasscodeVerifySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        passcode_input = serializer.validated_data['passcode']
        cache_key = f"passcode_attempts:{request.user.id}"
        attempts = cache.get(cache_key, 0)
        
        if attempts >= 5:
            return Response({"error": "Too many attempts"}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        try:
            user_settings = request.user.settings
        except UserSettings.DoesNotExist:
            user_settings, _ = UserSettings.objects.get_or_create(user=request.user)
        
        if not user_settings.passcode_lock_enabled:
            return Response({"message": "Passcode not enabled"}, status=status.HTTP_200_OK)

        if user_settings.check_passcode(passcode_input):
            cache.delete(cache_key)
            return Response({"success": True}, status=status.HTTP_200_OK)
        else:
            cache.set(cache_key, attempts + 1, 900)
            return Response({"success": False, "error": "Incorrect passcode"}, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasscodeRequestView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        success, message = send_otp_via_email(request.user.email)
        if success:
            return Response({"message": "OTP sent"}, status=status.HTTP_200_OK)
        return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)

class ResetPasscodeConfirmView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        serializer = ResetPasscodeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = request.user.email
        otp = serializer.validated_data['otp']
        new_passcode = serializer.validated_data['new_passcode']

        success, message = verify_otp_via_email(email, otp)
        
        if success:
            settings, _ = UserSettings.objects.get_or_create(user=request.user)
            settings.set_passcode(new_passcode)
            settings.passcode_lock_enabled = True
            settings.save()
            cache.delete(f"passcode_attempts:{request.user.id}")
            return Response({"message": "Passcode reset"}, status=status.HTTP_200_OK)
        return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)

class FCMTokenView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        token = request.data.get('token')
        device_type = request.data.get('device_type', 'android')
        
        if token:
            FCMDevice.objects.update_or_create(
                user=request.user,
                token=token,
                defaults={'device_type': device_type}
            )
            return Response({"message": "Token registered"})
        return Response({"error": "Token required"}, status=400)