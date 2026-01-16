from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ConfigDataView, UserSettingsView, TargetProfileViewSet,
    VerifyPasscodeView, ForgotPasscodeRequestView, ResetPasscodeConfirmView,
    ChangePasscodeView, FCMTokenView, NotificationViewSet
)

router = DefaultRouter()
router.register(r'profiles', TargetProfileViewSet, basename='target-profile')
router.register(r'notifications', NotificationViewSet, basename='notifications')

urlpatterns = [
    path('config/', ConfigDataView.as_view(), name='core-config'),
    path('settings/', UserSettingsView.as_view(), name='user-settings'),
    path('passcode/verify/', VerifyPasscodeView.as_view(), name='passcode-verify'),
    path('passcode/forgot/', ForgotPasscodeRequestView.as_view(), name='passcode-forgot'),
    path('passcode/reset/', ResetPasscodeConfirmView.as_view(), name='passcode-reset'),
    path('passcode/change/', ChangePasscodeView.as_view(), name='passcode-change'),
    path('fcm/register/', FCMTokenView.as_view(), name='fcm-register'),
    path('', include(router.urls)),
]