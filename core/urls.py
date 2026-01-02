from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ConfigDataView, UserSettingsView, TargetProfileViewSet,
    VerifyPasscodeView, ForgotPasscodeRequestView, ResetPasscodeConfirmView
)

router = DefaultRouter()
router.register(r'profiles', TargetProfileViewSet, basename='target-profile')

urlpatterns = [
    path('config/', ConfigDataView.as_view(), name='core-config'),
    path('settings/', UserSettingsView.as_view(), name='user-settings'),
    path('passcode/verify/', VerifyPasscodeView.as_view(), name='passcode-verify'),
    path('passcode/forgot/', ForgotPasscodeRequestView.as_view(), name='passcode-forgot'),
    path('passcode/reset/', ResetPasscodeConfirmView.as_view(), name='passcode-reset'),
    
    path('', include(router.urls)),
]