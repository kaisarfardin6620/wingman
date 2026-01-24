import structlog
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from django.core.cache import cache
from drf_spectacular.utils import extend_schema, OpenApiParameter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.apple.views import AppleOAuth2Adapter
from allauth.socialaccount.providers.apple.client import AppleOAuth2Client
from allauth.socialaccount.models import SocialLogin
from core.utils import send_push_notification
from .serializers import *
from .services import AuthService
from .utils import send_otp_via_email
from wingman.constants import CACHE_TTL_USER_PROFILE
from django.db import transaction

logger = structlog.get_logger(__name__)

class OTPRateThrottle(AnonRateThrottle):
    scope = 'otp' 

class RegisterView(APIView):
    throttle_classes = [AnonRateThrottle]

    @extend_schema(
        request=SignupSerializer,
        responses={201: dict},
        summary="Register New User"
    )
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            try:
                result = AuthService.register_user(serializer.validated_data)
                return Response(result, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(
                    {"error": "Registration failed. Please try again later."}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
    throttle_classes = [OTPRateThrottle]

    @extend_schema(
        request=VerifyOTPSerializer,
        responses={200: dict},
        summary="Verify Account OTP"
    )
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            success, message = AuthService.verify_otp(
                serializer.validated_data['email'], 
                serializer.validated_data['otp']
            )
            if success:
                return Response({"message": message}, status=status.HTTP_200_OK)
            return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    throttle_classes = [AnonRateThrottle]

    @extend_schema(
        request=LoginSerializer,
        responses={200: dict},
        summary="Login User"
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data, error_msg, status_code = AuthService.login_user(
            serializer.validated_data['email'], 
            serializer.validated_data['password']
        )
        
        if error_msg:
            return Response({"error": error_msg}, status=status_code)
            
        return Response(data, status=status.HTTP_200_OK)

class ResendOTPView(APIView):
    throttle_classes = [OTPRateThrottle]

    @extend_schema(
        request=ResendOTPSerializer,
        responses={200: dict},
        summary="Resend Verification OTP"
    )
    def post(self, request):
        serializer = ResendOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            if not User.objects.filter(email=email).exists():
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

            success, message = send_otp_via_email(email)
            if success:
                return Response({"message": message}, status=status.HTTP_200_OK)
            return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(APIView):
    throttle_classes = [OTPRateThrottle]

    @extend_schema(
        request=ForgotPasswordSerializer,
        responses={200: dict},
        summary="Request Password Reset"
    )
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            success, message = AuthService.forgot_password(serializer.validated_data['email'])
            if success:
                return Response({"message": message}, status=status.HTTP_200_OK)
            return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordConfirmView(APIView):
    throttle_classes = [OTPRateThrottle]

    @extend_schema(
        request=ResetPasswordSerializer,
        responses={200: dict},
        summary="Confirm Password Reset"
    )
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            success, message = AuthService.reset_password(
                serializer.validated_data['email'],
                serializer.validated_data['otp'],
                serializer.validated_data['new_password']
            )
            if success:
                return Response({"message": message}, status=status.HTTP_200_OK)
            return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    throttle_classes = [UserRateThrottle]

    @extend_schema(
        responses={200: UserProfileSerializer},
        summary="Get User Profile"
    )
    def get(self, request):
        cache_key = f"user_profile:{request.user.id}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)
        
        serializer = UserProfileSerializer(request.user, context={'request': request})
        cache.set(cache_key, serializer.data, CACHE_TTL_USER_PROFILE)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Update User Profile",
        request={'multipart/form-data': UserProfileSerializer},
        responses={200: UserProfileSerializer},
    )
    def patch(self, request):
        serializer = UserProfileSerializer(
            request.user, 
            data=request.data, 
            partial=True, 
            context={'request': request}
        )
        
        if serializer.is_valid():
            result, error = AuthService.update_profile(request.user, serializer.validated_data)
            
            if error:
                 return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)
            
            response_serializer = UserProfileSerializer(request.user, context={'request': request})
            
            response_data = result
            response_data['data'] = response_serializer.data
            if 'user' in response_data: del response_data['user']

            return Response(response_data, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GoogleLoginView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]
    
    @extend_schema(
        request=dict,
        responses={200: dict},
        summary="Google Login"
    )
    def post(self, request):
        try:
            access_token = request.data.get("access_token")
            if not access_token:
                return Response({"detail": "Access token required"}, status=status.HTTP_400_BAD_REQUEST)
            
            adapter = GoogleOAuth2Adapter(request)
            app = adapter.get_provider().get_app(request)
            client = OAuth2Client(
                request, app.client_id, app.secret,
                adapter.access_token_method, adapter.access_token_url,
                adapter.callback_url, adapter.scope
            )
            
            social_token = client.parse_token({"access_token": access_token})
            social_token.app = app
            
            login = adapter.complete_login(request, app, social_token, response_kwargs={})
            login.token = social_token
            
            if not isinstance(login, SocialLogin):
                return Response({"detail": "Error processing login"}, status=status.HTTP_400_BAD_REQUEST)

            login.state = SocialLogin.state_from_request(request)
            adapter.save_user(request, login, form=None)
            
            user = login.user
            send_push_notification(user, "New Login", "Logged in via Google.")
            logger.info("google_login_success", user_id=user.id)
            
            tokens = user.tokens
            return Response({
                "message": "Login successful",
                "token": tokens['access'],
                "refresh_token": tokens['refresh'],
                "user": UserProfileSerializer(user, context={'request': request}).data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error("google_login_failed", error=str(e))
            return Response({"detail": "Google authentication failed"}, status=status.HTTP_400_BAD_REQUEST)

class AppleLoginView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]
    
    @extend_schema(
        request=dict,
        responses={200: dict},
        summary="Apple Login"
    )
    def post(self, request):
        try:
            access_token = request.data.get("access_token")
            id_token = request.data.get("id_token")
            
            if not access_token and not id_token:
                return Response({"detail": "Token required"}, status=status.HTTP_400_BAD_REQUEST)
                
            adapter = AppleOAuth2Adapter(request)
            app = adapter.get_provider().get_app(request)
            client = AppleOAuth2Client(
                request, app.client_id, app.secret,
                adapter.access_token_method, adapter.access_token_url,
                adapter.callback_url, adapter.scope
            )
            
            token_payload = {}
            if access_token: token_payload["code"] = access_token
            if id_token: token_payload["id_token"] = id_token
                
            social_token = client.parse_token(token_payload)
            social_token.app = app
            
            login = adapter.complete_login(request, app, social_token, response_kwargs={})
            login.token = social_token
            
            if not isinstance(login, SocialLogin):
                return Response({"detail": "Error processing login"}, status=status.HTTP_400_BAD_REQUEST)

            login.state = SocialLogin.state_from_request(request)
            adapter.save_user(request, login, form=None)
            
            user = login.user
            send_push_notification(user, "New Login", "Logged in via Apple.")
            logger.info("apple_login_success", user_id=user.id)
            
            tokens = user.tokens
            return Response({
                "message": "Login successful",
                "token": tokens['access'],
                "refresh_token": tokens['refresh'],
                "user": UserProfileSerializer(user, context={'request': request}).data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error("apple_login_failed", error=str(e))
            return Response({"detail": "Apple authentication failed"}, status=status.HTTP_400_BAD_REQUEST)
        
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    @extend_schema(
        request=UserChangePasswordSerializer,
        responses={200: dict},
        summary="Change Password"
    )
    def post(self, request):
        serializer = UserChangePasswordSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(request, user)
            
            send_push_notification(user, "Security Alert", "Your password was changed.")
            logger.info("password_change_success", user_id=user.id)
            
            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VerifyEmailChangeView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    @extend_schema(
        request=EmailChangeVerifySerializer,
        responses={200: dict},
        summary="Verify Email Change OTP"
    )
    def post(self, request):
        serializer = EmailChangeVerifySerializer(data=request.data)
        if serializer.is_valid():
            otp_input = serializer.validated_data['otp']
            cache_key = f"email_change_request:{request.user.id}"
            cached_data = cache.get(cache_key)
            
            if not cached_data:
                return Response({"error": "OTP expired or no email change requested."}, status=status.HTTP_400_BAD_REQUEST)
            
            if str(cached_data['otp']) != str(otp_input):
                return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)
            user = request.user
            user.email = cached_data['new_email']
            user.save(update_fields=['email'])
            cache.delete(cache_key)
            cache.delete(f"user_profile:{user.id}")
            
            logger.info("email_change_verified", user_id=user.id)
            return Response({"message": "Email updated successfully."}, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    
class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    @extend_schema(
        request=DeleteAccountSerializer,
        responses={200: dict},
        summary="Delete Account"
    )
    def delete(self, request):
        serializer = DeleteAccountSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            user = request.user
            try:
                with transaction.atomic():
                    cache.delete(f"user_profile:{user.id}")
                    cache.delete(f"user_settings:{user.id}")
                    user.delete()

                logger.info("account_deleted", user_id=user.id)
                return Response({"message": "Account permanently deleted."}, status=status.HTTP_200_OK)
                
            except Exception as e:
                logger.error("delete_account_failed", user_id=user.id, error=str(e))
                return Response({"error": "Something went wrong."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)