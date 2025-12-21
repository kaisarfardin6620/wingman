from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DashboardAnalyticsView, 
    AdminUserViewSet, 
    AdminToneViewSet, 
    AdminPersonaViewSet,
    GlobalConfigView,
    AdminProfileView,
    AdminChangePasswordView
)

router = DefaultRouter()
router.register(r'users', AdminUserViewSet, basename='admin-users')
router.register(r'tones', AdminToneViewSet, basename='admin-tones')
router.register(r'personas', AdminPersonaViewSet, basename='admin-personas')

urlpatterns = [
    path('analytics/', DashboardAnalyticsView.as_view(), name='admin-analytics'),
    path('limits/', GlobalConfigView.as_view(), name='admin-limits'),
    path('settings/profile/', AdminProfileView.as_view(), name='admin-profile'),
    path('settings/password/', AdminChangePasswordView.as_view(), name='admin-password'),
    path('', include(router.urls)),
]