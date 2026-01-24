import structlog
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
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from authentication.utils import send_otp_via_email, verify_otp_via_email
from .models import Tone, Persona, UserSettings, TargetProfile, FCMDevice, Notification
from .serializers import (
    ToneSerializer, PersonaSerializer,
    UserSettingsSerializer, TargetProfileSerializer,
    PasscodeVerifySerializer, ResetPasscodeSerializer,
    ChangePasscodeSerializer, NotificationSerializer
)
from .services import CoreService
from wingman.constants import CACHE_TTL_CONFIG_DATA, CACHE_TTL_USER_SETTINGS

User = get_user_model()
logger = structlog.get_logger(__name__)

class ConfigThrottle(UserRateThrottle):
    scope = 'anon'

class ConfigDataView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [ConfigThrottle]

    @method_decorator(cache_page(300))
    @extend_schema(summary="Get Global Config (Tones/Personas)", responses={200: dict})
    def get(self, request):
        data = CoreService.get_config_data()
        return Response(data)

class UserSettingsView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    @extend_schema(summary="Get User Settings", responses={200: UserSettingsSerializer})
    def get(self, request):
        settings_obj = CoreService.get_user_settings(request.user)
        if isinstance(settings_obj, dict):
             return Response(settings_obj)
        serializer = UserSettingsSerializer(settings_obj)
        cache.set(f"user_settings:{request.user.id}", serializer.data, CACHE_TTL_USER_SETTINGS)
        return Response(serializer.data)

    @extend_schema(summary="Update User Settings", request=UserSettingsSerializer, responses={200: UserSettingsSerializer})
    def patch(self, request):
        settings, _ = UserSettings.objects.get_or_create(user=request.user)
        serializer = UserSettingsSerializer(
            settings,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            cache.delete(f"user_settings:{request.user.id}")
            return Response({"message": "Settings updated successfully", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema_view(
    create=extend_schema(request={'multipart/form-data': TargetProfileSerializer}),
    update=extend_schema(request={'multipart/form-data': TargetProfileSerializer}),
    partial_update=extend_schema(request={'multipart/form-data': TargetProfileSerializer}),
)
class TargetProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    serializer_class = TargetProfileSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return TargetProfile.objects.none()
            
        return TargetProfile.objects.filter(user=self.request.user).order_by('-created_at')
    
    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(TargetProfile, pk=pk, user=self.request.user)
        return obj

    def perform_create(self, serializer):
        success, error = CoreService.create_target_profile(self.request.user, None)
        if error:
            raise PermissionDenied(error)
        serializer.save(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class VerifyPasscodeView(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(summary="Verify Passcode", request=PasscodeVerifySerializer, responses={200: dict})
    def post(self, request):
        serializer = PasscodeVerifySerializer(data=request.data)
        if not serializer.is_valid(): return Response(serializer.errors, status=400)
        
        user_settings = CoreService.get_user_settings(request.user)
        if isinstance(user_settings, dict):
            user_settings, _ = UserSettings.objects.get_or_create(user=request.user)

        if not user_settings.passcode_lock_enabled:
            return Response({"message": "Passcode not enabled"}, status=200)

        if user_settings.check_passcode(serializer.validated_data['passcode']):
            return Response({"success": True})
        return Response({"success": False, "error": "Incorrect passcode"}, status=400)

class ForgotPasscodeRequestView(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Request Passcode Reset OTP", 
        request=None,
        responses={200: dict}
    )
    def post(self, request):
        send_otp_via_email(request.user.email)
        return Response({"message": "OTP sent"})

class ResetPasscodeConfirmView(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(summary="Reset Passcode with OTP", request=ResetPasscodeSerializer, responses={200: dict})
    def post(self, request):
        serializer = ResetPasscodeSerializer(data=request.data)
        if serializer.is_valid():
            success, msg = verify_otp_via_email(request.user.email, serializer.validated_data['otp'])
            if success:
                settings, _ = UserSettings.objects.get_or_create(user=request.user)
                settings.set_passcode(serializer.validated_data['new_passcode'])
                settings.passcode_lock_enabled = True
                settings.save()
                return Response({"message": "Passcode reset"})
            return Response({"error": msg}, status=400)
        return Response(serializer.errors, status=400)

class ChangePasscodeView(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(summary="Change Passcode", request=ChangePasscodeSerializer, responses={200: dict})
    def post(self, request):
        serializer = ChangePasscodeSerializer(data=request.data)
        if serializer.is_valid():
            settings, _ = UserSettings.objects.get_or_create(user=request.user)
            if settings.passcode_lock_enabled:
                if not settings.check_passcode(serializer.validated_data['old_passcode']):
                    return Response({"error": "Incorrect old passcode"}, status=400)
            settings.set_passcode(serializer.validated_data['new_passcode'])
            settings.passcode_lock_enabled = True
            settings.save()
            return Response({"message": "Passcode changed"})
        return Response(serializer.errors, status=400)

class FCMTokenView(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(summary="Register FCM Token", request=dict, responses={200: dict})
    def post(self, request):
        token = request.data.get('token')
        if token:
            FCMDevice.objects.update_or_create(user=request.user, token=token)
            return Response({"message": "Token registered"})
        return Response({"error": "Token required"}, status=400)

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Notification.objects.none()
        return Notification.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['patch'])
    def mark_read(self, request, pk=None):
        n = self.get_object()
        n.is_read=True
        n.save()
        return Response({'status': 'marked as read'})
        
    @action(detail=False, methods=['patch'])
    def mark_all_read(self, request):
        self.get_queryset().update(is_read=True)
        return Response({'status': 'all marked as read'})