from django.utils import timezone
from django.db import transaction
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.throttling import UserRateThrottle
from drf_spectacular.utils import extend_schema

from core.models import Tone, Persona, GlobalConfig
from core.utils import send_push_notification
from .serializers import (
    DashboardStatsSerializer, AdminUserListSerializer,
    AdminToneSerializer, AdminPersonaSerializer,
    GlobalConfigSerializer, AdminProfileUpdateSerializer,
    ChangePasswordSerializer
)
from .services import DashboardService
from authentication.tasks import send_otp_email_task
from authentication.utils import generate_otp
from wingman.constants import CACHE_TTL_GLOBAL_CONFIG

User = get_user_model()

class AdminThrottle(UserRateThrottle):
    scope = 'user'

class DashboardAnalyticsView(APIView):
    permission_classes = [IsAdminUser]
    throttle_classes = [AdminThrottle]

    @extend_schema(summary="Get Dashboard Analytics", responses={200: DashboardStatsSerializer})
    def get(self, request):
        cache_key = "admin_dashboard_stats"
        cached = cache.get(cache_key)
        if cached: return Response(cached)
        
        data = DashboardService.get_analytics(request)
        serializer = DashboardStatsSerializer(data)
        cache.set(cache_key, serializer.data, 60)
        return Response(serializer.data)

class AdminUserViewSet(viewsets.ModelViewSet):
    serializer_class = AdminUserListSerializer
    permission_classes = [IsAdminUser]
    throttle_classes = [AdminThrottle]

    def get_queryset(self):
        queryset = User.objects.select_related('settings').order_by('-date_joined')
        search = self.request.query_params.get('search')
        if search: queryset = queryset.filter(Q(email__icontains=search) | Q(name__icontains=search))
        status_filter = self.request.query_params.get('status')
        if status_filter:
            if status_filter.lower() == 'active': queryset = queryset.filter(is_active=True)
            elif status_filter.lower() == 'inactive': queryset = queryset.filter(is_active=False)
        sub_filter = self.request.query_params.get('subscription')
        if sub_filter:
            if sub_filter.lower() == 'premium': queryset = queryset.filter(is_premium=True)
            elif sub_filter.lower() == 'free': queryset = queryset.filter(is_premium=False)
        return queryset

    @action(detail=True, methods=['patch'])
    def toggle_status(self, request, pk=None):
        user = self.get_object()
        if user.id == request.user.id: return Response({"error": "Cannot disable self"}, status=400)
        user.is_active = not user.is_active
        user.save(update_fields=['is_active'])
        return Response({"status": "Active" if user.is_active else "Inactive"})
    
    @action(detail=True, methods=['patch'])
    def toggle_premium(self, request, pk=None):
        user = self.get_object()
        user.is_premium = not user.is_premium
        user.save(update_fields=['is_premium'])
        return Response({"subscription": "Premium" if user.is_premium else "Free"})
    
    @action(detail=True, methods=['post'])
    def reset_user_password(self, request, pk=None):
        import secrets
        from authentication.tasks import send_admin_reset_password_email_task
        user = self.get_object()
        new_pass = secrets.token_urlsafe(10) 
        try:
            with transaction.atomic():
                user.set_password(new_pass)
                user.save(update_fields=['password'])
                send_admin_reset_password_email_task.delay(user.email, user.name, new_pass)
        except Exception as e:
            return Response({"error": f"Failed to reset password: {str(e)}"}, status=500)
        send_push_notification(user, "Security Alert", "Admin reset your password. Check your email.")
        return Response({"message": f"Password reset. Email sent to {user.email}"})

class AdminToneViewSet(viewsets.ModelViewSet):
    queryset = Tone.objects.all().order_by('name')
    serializer_class = AdminToneSerializer
    permission_classes = [IsAdminUser]
    throttle_classes = [AdminThrottle]
    
    def perform_create(self, serializer): serializer.save(); cache.delete('active_tones'); cache.delete('global_config')
    def perform_update(self, serializer): serializer.save(); cache.delete('active_tones'); cache.delete('global_config')
    def perform_destroy(self, instance): instance.delete(); cache.delete('active_tones'); cache.delete('global_config')
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"message": "Tone created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        self.perform_destroy(instance)
        return Response({"message": "Tone deleted successfully", "data": data}, status=status.HTTP_200_OK)

class AdminPersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all().order_by('name')
    serializer_class = AdminPersonaSerializer
    permission_classes = [IsAdminUser]
    throttle_classes = [AdminThrottle]
    
    def perform_create(self, serializer): serializer.save(); cache.delete('active_personas'); cache.delete('global_config')
    def perform_update(self, serializer): serializer.save(); cache.delete('active_personas'); cache.delete('global_config')
    def perform_destroy(self, instance): instance.delete(); cache.delete('active_personas'); cache.delete('global_config')
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"message": "Persona created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        self.perform_destroy(instance)
        return Response({"message": "Persona deleted successfully", "data": data}, status=status.HTTP_200_OK)

class GlobalConfigView(APIView):
    permission_classes = [IsAdminUser]
    throttle_classes = [AdminThrottle]

    @extend_schema(summary="Get System Limits", responses={200: GlobalConfigSerializer})
    def get(self, request):
        return Response(GlobalConfigSerializer(GlobalConfig.load()).data)

    @extend_schema(summary="Update System Limits", request=GlobalConfigSerializer, responses={200: GlobalConfigSerializer})
    def post(self, request):
        config = GlobalConfig.load()
        serializer = GlobalConfigSerializer(config, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Updated", "data": serializer.data})
        return Response(serializer.errors, status=400)

class AdminProfileView(APIView):
    permission_classes = [IsAdminUser]
    throttle_classes = [UserRateThrottle]

    @extend_schema(summary="Get Admin Profile", responses={200: AdminProfileUpdateSerializer})
    def get(self, request):
        cache_key = f"user_profile:{request.user.id}"
        cached_data = cache.get(cache_key)
        if cached_data: return Response(cached_data)
        serializer = AdminProfileUpdateSerializer(request.user, context={'request': request})
        cache.set(cache_key, serializer.data, 300)
        return Response(serializer.data)

    @extend_schema(
        summary="Update Admin Profile",
        request={'multipart/form-data': AdminProfileUpdateSerializer},
        responses={200: AdminProfileUpdateSerializer},
    )
    def patch(self, request):
        user = request.user
        data = request.data.copy()
        new_email = data.get('email', '').strip().lower()
        email_changed = False
        if new_email and new_email != user.email:
            if User.objects.exclude(pk=user.pk).filter(email=new_email).exists():
                return Response({"email": ["This email is already in use."]}, status=status.HTTP_400_BAD_REQUEST)
            email_changed = True
            if 'email' in data: del data['email']
        serializer = AdminProfileUpdateSerializer(user, data=data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            cache.delete(f"user_profile:{user.id}")
            response_data = {"message": "Updated successfully", "data": serializer.data}
            if email_changed:
                otp_code = generate_otp()
                cache.set(f"email_change_request:{user.id}", {'new_email': new_email, 'otp': otp_code}, 600)
                send_otp_email_task.delay(new_email, otp_code)
                response_data['message'] = "Profile updated. Please verify the OTP sent to your new email."
                response_data['email_verification_required'] = True
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminChangePasswordView(APIView):
    permission_classes = [IsAdminUser]
    throttle_classes = [UserRateThrottle]
    
    @extend_schema(summary="Admin Change Password", request=ChangePasswordSerializer, responses={200: dict})
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(request, user)
            return Response({"message": "Password changed"}, status=200)
        return Response(serializer.errors, status=400)