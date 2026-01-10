from django.utils import timezone
from django.db.models.functions import TruncMonth, TruncDate
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
from .serializers import (
    DashboardStatsSerializer,
    AdminUserListSerializer,
    AdminToneSerializer,
    AdminPersonaSerializer,
    GlobalConfigSerializer,
    AdminProfileUpdateSerializer,
    ChangePasswordSerializer
)
import logging

User = get_user_model()
logger = logging.getLogger(__name__)


class AdminThrottle(UserRateThrottle):
    """Throttle for admin endpoints"""
    rate = '100/minute'


class DashboardAnalyticsView(APIView):
    """
    Admin analytics dashboard
    ✅ Cached aggregations
    ✅ Optimized queries
    """
    permission_classes = [IsAdminUser]
    throttle_classes = [AdminThrottle]

    @method_decorator(cache_page(60))  # Cache for 1 minute
    def get(self, request):
        """
        Get dashboard analytics
        ✅ All queries optimized with aggregation
        """
        # ✅ Single query for user stats
        user_stats = User.objects.aggregate(
            total=Count('id'),
            premium=Count('id', filter=Q(is_premium=True)),
            active=Count('id', filter=Q(is_active=True))
        )
        
        total_users = user_stats['total']
        premium_users = user_stats['premium']
        free_users = total_users - premium_users
        
        # ✅ Active today count
        today = timezone.now().date()
        active_today = User.objects.filter(
            last_login__date=today
        ).count()
        
        # ✅ Conversion rate
        conversion_rate = 0.0
        if total_users > 0:
            conversion_rate = round((premium_users / total_users) * 100, 2)

        # ✅ Monthly growth data (last 12 months)
        twelve_months_ago = timezone.now() - timezone.timedelta(days=365)
        monthly_data = (
            User.objects.filter(date_joined__gte=twelve_months_ago)
            .annotate(month=TruncMonth('date_joined'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
        )

        graph_data = []
        for entry in monthly_data:
            if entry['month']:
                graph_data.append({
                    "month": entry['month'].strftime('%b %Y'),
                    "count": entry['count']
                })

        data = {
            "total_users": total_users,
            "active_today": active_today,
            "premium_users": premium_users,
            "free_users": free_users,
            "conversion_rate": conversion_rate,
            "graph_data": graph_data
        }
        
        serializer = DashboardStatsSerializer(data)
        return Response(serializer.data)


class AdminUserViewSet(viewsets.ModelViewSet):
    """
    Admin user management
    ✅ Search, filter, pagination
    ✅ Bulk operations
    """
    serializer_class = AdminUserListSerializer
    permission_classes = [IsAdminUser]
    throttle_classes = [AdminThrottle]

    def get_queryset(self):
        """
        Get users with search and filters
        ✅ Optimized with select_related
        """
        queryset = User.objects.select_related('settings').order_by('-date_joined')
        
        # ✅ Search by email or name
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(email__icontains=search) |
                Q(name__icontains=search)
            )
        
        # ✅ Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            if status_filter.lower() == 'active':
                queryset = queryset.filter(is_active=True)
            elif status_filter.lower() == 'inactive':
                queryset = queryset.filter(is_active=False)
        
        # ✅ Filter by subscription
        subscription_filter = self.request.query_params.get('subscription', None)
        if subscription_filter:
            if subscription_filter.lower() == 'premium':
                queryset = queryset.filter(is_premium=True)
            elif subscription_filter.lower() == 'free':
                queryset = queryset.filter(is_premium=False)
        
        return queryset

    @action(detail=True, methods=['patch'])
    def toggle_status(self, request, pk=None):
        """Toggle user active status"""
        user = self.get_object()
        
        # ✅ Prevent admin from disabling themselves
        if user.id == request.user.id:
            return Response({
                "error": "You cannot disable your own account."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user.is_active = not user.is_active
        user.save(update_fields=['is_active'])
        
        logger.info(f"Admin {request.user.email} toggled status for user {user.email}")
        
        return Response({
            "status": "Active" if user.is_active else "Inactive"
        })
    
    @action(detail=True, methods=['patch'])
    def toggle_premium(self, request, pk=None):
        """Toggle user premium status"""
        user = self.get_object()
        user.is_premium = not user.is_premium
        user.save(update_fields=['is_premium'])
        
        logger.info(f"Admin {request.user.email} toggled premium for user {user.email}")
        
        return Response({
            "subscription": "Premium" if user.is_premium else "Free"
        })
    
    @action(detail=False, methods=['post'])
    def bulk_toggle_status(self, request):
        """Bulk toggle user status"""
        user_ids = request.data.get('user_ids', [])
        
        if not user_ids:
            return Response({
                "error": "No user IDs provided."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # ✅ Prevent admin from disabling themselves
        if request.user.id in user_ids:
            return Response({
                "error": "You cannot disable your own account."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Toggle status
        users = User.objects.filter(id__in=user_ids)
        updated_count = 0
        
        for user in users:
            user.is_active = not user.is_active
            user.save(update_fields=['is_active'])
            updated_count += 1
        
        return Response({
            "message": f"Updated {updated_count} users."
        })


class AdminToneViewSet(viewsets.ModelViewSet):
    """
    Admin tone management
    ✅ CRUD operations with cache invalidation
    """
    queryset = Tone.objects.all().order_by('name')
    serializer_class = AdminToneSerializer
    permission_classes = [IsAdminUser]
    throttle_classes = [AdminThrottle]
    
    def perform_create(self, serializer):
        """Create tone and invalidate cache"""
        serializer.save()
        cache.delete('active_tones')
        cache.delete('global_config')
    
    def perform_update(self, serializer):
        """Update tone and invalidate cache"""
        serializer.save()
        cache.delete('active_tones')
        cache.delete('global_config')
    
    def perform_destroy(self, instance):
        """Delete tone and invalidate cache"""
        instance.delete()
        cache.delete('active_tones')
        cache.delete('global_config')


class AdminPersonaViewSet(viewsets.ModelViewSet):
    """
    Admin persona management
    ✅ CRUD operations with cache invalidation
    """
    queryset = Persona.objects.all().order_by('name')
    serializer_class = AdminPersonaSerializer
    permission_classes = [IsAdminUser]
    throttle_classes = [AdminThrottle]
    
    def perform_create(self, serializer):
        """Create persona and invalidate cache"""
        serializer.save()
        cache.delete('active_personas')
        cache.delete('global_config')
    
    def perform_update(self, serializer):
        """Update persona and invalidate cache"""
        serializer.save()
        cache.delete('active_personas')
        cache.delete('global_config')
    
    def perform_destroy(self, instance):
        """Delete persona and invalidate cache"""
        instance.delete()
        cache.delete('active_personas')
        cache.delete('global_config')


class GlobalConfigView(APIView):
    """
    Global configuration management
    ✅ Singleton pattern with cache
    """
    permission_classes = [IsAdminUser]
    throttle_classes = [AdminThrottle]

    def get(self, request):
        """Get global configuration"""
        config = GlobalConfig.load()  # ✅ Uses cached load method
        serializer = GlobalConfigSerializer(config)
        return Response(serializer.data)

    def post(self, request):
        """Update global configuration"""
        config = GlobalConfig.load()
        serializer = GlobalConfigSerializer(config, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            
            logger.info(f"Admin {request.user.email} updated global config")
            
            return Response({
                "message": "Configuration updated successfully",
                "data": serializer.data
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminProfileView(APIView):
    """
    Admin profile management
    ✅ Update own profile
    """
    permission_classes = [IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def get(self, request):
        """Get admin profile"""
        serializer = AdminProfileUpdateSerializer(
            request.user,
            context={'request': request}
        )
        return Response(serializer.data)

    def patch(self, request):
        """Update admin profile"""
        serializer = AdminProfileUpdateSerializer(
            request.user,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save()
            
            # ✅ Invalidate profile cache
            cache.delete(f"user_profile:{request.user.id}")
            
            return Response({
                "message": "Profile updated successfully",
                "data": serializer.data
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminChangePasswordView(APIView):
    """
    Admin password change
    ✅ Secure password update
    """
    permission_classes = [IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        """Change admin password"""
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            logger.info(f"Admin {user.email} changed password")
            
            return Response({
                "message": "Password changed successfully. Please log in again."
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)