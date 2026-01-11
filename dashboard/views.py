from django.utils import timezone
from django.db.models.functions import TruncMonth
from django.db.models import Count, Q
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.throttling import UserRateThrottle
from core.models import Tone, Persona, GlobalConfig
from core.utils import send_push_notification
from .serializers import (
    DashboardStatsSerializer, AdminUserListSerializer,
    AdminToneSerializer, AdminPersonaSerializer,
    GlobalConfigSerializer, AdminProfileUpdateSerializer,
    ChangePasswordSerializer
)
import logging

User = get_user_model()
logger = logging.getLogger(__name__)

class AdminThrottle(UserRateThrottle):
    rate = '100/minute'

class DashboardAnalyticsView(APIView):
    permission_classes = [IsAdminUser]
    throttle_classes = [AdminThrottle]

    @method_decorator(cache_page(60))
    def get(self, request):
        user_stats = User.objects.aggregate(
            total=Count('id'),
            premium=Count('id', filter=Q(is_premium=True)),
            active=Count('id', filter=Q(is_active=True))
        )
        total_users = user_stats['total']
        premium_users = user_stats['premium']
        free_users = total_users - premium_users
        active_today = User.objects.filter(last_login__date=timezone.now().date()).count()
        conversion_rate = round((premium_users / total_users * 100), 2) if total_users > 0 else 0
        
        twelve_months_ago = timezone.now() - timezone.timedelta(days=365)
        monthly_data = (
            User.objects.filter(date_joined__gte=twelve_months_ago)
            .annotate(month=TruncMonth('date_joined'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
        )
        graph_data = [{"month": e['month'].strftime('%b %Y'), "count": e['count']} for e in monthly_data if e['month']]

        data = {
            "total_users": total_users, "active_today": active_today,
            "premium_users": premium_users, "free_users": free_users,
            "conversion_rate": conversion_rate, "graph_data": graph_data
        }
        return Response(DashboardStatsSerializer(data).data)

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
        from django.core.mail import send_mail
        from django.conf import settings

        user = self.get_object()
        
        new_pass = secrets.token_urlsafe(10) 
        user.set_password(new_pass)
        user.save()
        
        try:
            send_mail(
                subject="Your Password has been Reset by Admin",
                message=f"Hello {user.name or 'User'},\n\nYour Admin has reset your password.\n\nTemporary Password: {new_pass}\n\nPlease log in and change this immediately.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )
        except Exception as e:
            return Response({"error": f"Password reset, but failed to email user: {str(e)}"}, status=500)
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

class AdminPersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all().order_by('name')
    serializer_class = AdminPersonaSerializer
    permission_classes = [IsAdminUser]
    throttle_classes = [AdminThrottle]
    
    def perform_create(self, serializer): serializer.save(); cache.delete('active_personas'); cache.delete('global_config')
    def perform_update(self, serializer): serializer.save(); cache.delete('active_personas'); cache.delete('global_config')
    def perform_destroy(self, instance): instance.delete(); cache.delete('active_personas'); cache.delete('global_config')

class GlobalConfigView(APIView):
    permission_classes = [IsAdminUser]
    throttle_classes = [AdminThrottle]

    def get(self, request):
        return Response(GlobalConfigSerializer(GlobalConfig.load()).data)

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

    def get(self, request):
        return Response(AdminProfileUpdateSerializer(request.user, context={'request': request}).data)

    def patch(self, request):
        serializer = AdminProfileUpdateSerializer(request.user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            cache.delete(f"user_profile:{request.user.id}")
            return Response({"message": "Updated", "data": serializer.data})
        return Response(serializer.errors, status=400)

class AdminChangePasswordView(APIView):
    permission_classes = [IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"message": "Password changed"}, status=200)
        return Response(serializer.errors, status=400)