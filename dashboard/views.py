from django.utils import timezone
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action

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

User = get_user_model()

class DashboardAnalyticsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_users = User.objects.count()
        today = timezone.now().date()
        active_today = User.objects.filter(last_login__date=today).count()
        
        premium_users = User.objects.filter(is_premium=True).count()
        free_users = total_users - premium_users
        
        conversion_rate = 0.0
        if total_users > 0:
            conversion_rate = round((premium_users / total_users) * 100, 2)

        monthly_data = (
            User.objects.annotate(month=TruncMonth('date_joined'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
        )

        graph_data = []
        for entry in monthly_data:
            if entry['month']:
                graph_data.append({
                    "month": entry['month'].strftime('%b'),
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
        return Response(data)

class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = AdminUserListSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = User.objects.all().order_by('-date_joined')
        search = self.request.query_params.get('search', None)
        status_filter = self.request.query_params.get('status', None)
        
        if search:
            queryset = queryset.filter(email__icontains=search)
        
        if status_filter:
            if status_filter.lower() == 'active':
                queryset = queryset.filter(is_active=True)
            elif status_filter.lower() == 'inactive':
                queryset = queryset.filter(is_active=False)
                
        return queryset

    @action(detail=True, methods=['patch'])
    def toggle_status(self, request, pk=None):
        user = self.get_object()
        user.is_active = not user.is_active
        user.save()
        return Response({"status": "Active" if user.is_active else "Inactive"})
    
    @action(detail=True, methods=['patch'])
    def toggle_premium(self, request, pk=None):
        user = self.get_object()
        user.is_premium = not user.is_premium
        user.save()
        return Response({"subscription": "Premium" if user.is_premium else "Free"})

class AdminToneViewSet(viewsets.ModelViewSet):
    queryset = Tone.objects.all()
    serializer_class = AdminToneSerializer
    permission_classes = [IsAdminUser]

class AdminPersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = AdminPersonaSerializer
    permission_classes = [IsAdminUser]

class GlobalConfigView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        config = GlobalConfig.load()
        serializer = GlobalConfigSerializer(config)
        return Response(serializer.data)

    def post(self, request):
        config = GlobalConfig.load()
        serializer = GlobalConfigSerializer(config, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminProfileView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        serializer = AdminProfileUpdateSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = AdminProfileUpdateSerializer(request.user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminChangePasswordView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)