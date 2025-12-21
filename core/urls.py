from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConfigDataView, UserSettingsView, TargetProfileViewSet

router = DefaultRouter()
router.register(r'profiles', TargetProfileViewSet, basename='target-profile')

urlpatterns = [
    path('config/', ConfigDataView.as_view(), name='core-config'),
    path('settings/', UserSettingsView.as_view(), name='user-settings'),
    path('', include(router.urls)),
]