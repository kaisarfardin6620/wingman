from django.urls import path
from .views import (
    RegisterView, VerifyEmailChangeView, VerifyOTPView, LoginView, LogoutView, 
    ResendOTPView, ForgotPasswordView, ResetPasswordConfirmView, 
    UserProfileView, GoogleLoginView, AppleLoginView,ChangePasswordView  
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend-otp'),
    path('password-reset/', ForgotPasswordView.as_view(), name='password-reset'),
    path('password-reset-confirm/', ResetPasswordConfirmView.as_view(), name='password-reset-confirm'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('google/', GoogleLoginView.as_view(), name='google_login'),
    path('apple/', AppleLoginView.as_view(), name='apple_login'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('profile/verify-email/', VerifyEmailChangeView.as_view(), name='verify-email-change'),
]