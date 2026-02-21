import structlog
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import transaction
from drf_spectacular.utils import extend_schema, OpenApiParameter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.apple.views import AppleOAuth2Adapter
from allauth.socialaccount.providers.apple.client import AppleOAuth2Client
from allauth.socialaccount.models import SocialLogin
from rest_framework_simplejwt.tokens import RefreshToken
from core.utils import send_push_notification
from .serializers import (
    SignupSerializer, VerifyOTPSerializer, LoginSerializer,
    ResendOTPSerializer, ForgotPasswordSerializer,
    ResetPasswordSerializer, UserProfileSerializer,
    UserChangePasswordSerializer, EmailChangeVerifySerializer,
    DeleteAccountSerializer
)
from .services import AuthService
from .utils import send_otp_via_email
from wingman.constants import CACHE_TTL_USER_PROFILE
import requests
import jwt
from jwt.algorithms import RSAAlgorithm
from google.oauth2 import id_token as google_id_token
from google.auth.transport import requests as google_requests

User = get_user_model()
logger = structlog.get_logger(__name__)

class OTPRateThrottle(AnonRateThrottle):
    scope = 'otp' 

class RegisterView(APIView):
    throttle_classes = [AnonRateThrottle]
    permission_classes = [AllowAny]

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
                logger.error("registration_failed", error=str(e))
                return Response(
                    {"error": "Registration failed. Please try again later."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
    throttle_classes = [OTPRateThrottle]
    permission_classes = [AllowAny]

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
    permission_classes = [AllowAny]

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
    permission_classes = [AllowAny]

    @extend_schema(
        request=ResendOTPSerializer,
        responses={200: dict},
        summary="Resend Verification OTP"
    )
    def post(self, request):
        serializer = ResendOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            if User.objects.filter(email=email).exists():
                send_otp_via_email(email)
            
            return Response(
                {"message": "If the email exists, an OTP has been sent."}, 
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(APIView):
    throttle_classes = [OTPRateThrottle]
    permission_classes = [AllowAny]

    @extend_schema(
        request=ForgotPasswordSerializer,
        responses={200: dict},
        summary="Request Password Reset"
    )
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            AuthService.forgot_password(serializer.validated_data['email'])
            return Response(
                {"message": "If the email exists, an OTP has been sent."}, 
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordConfirmView(APIView):
    throttle_classes = [OTPRateThrottle]
    permission_classes = [AllowAny]

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
        request={"application/json": {"type": "object", "properties": {"id_token": {"type": "string"}}}},
        responses={200: dict},
        summary="Google Login (Mobile)"
    )
    def post(self, request):
        token_str = request.data.get("id_token")
        if not token_str:
            return Response(
                {"detail": "id_token is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            decoded = {}
            
            if token_str.startswith("ya29"):
                user_info_resp = requests.get(
                    f"https://www.googleapis.com/oauth2/v3/userinfo?access_token={token_str}"
                )
                user_info_resp.raise_for_status()
                decoded = user_info_resp.json()
            
            else:
                decoded = google_id_token.verify_oauth2_token(
                    token_str,
                    google_requests.Request(),
                    settings.GOOGLE_CLIENT_ID
                )
                if decoded.get("aud") != settings.GOOGLE_CLIENT_ID:
                    return Response(
                        {"detail": "Invalid token audience"},
                        status=status.HTTP_401_UNAUTHORIZED
                    )

            if not decoded.get("email_verified", False):
                return Response(
                    {"detail": "Google email not verified"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            email = decoded.get("email")
            if not email:
                return Response(
                    {"detail": "Email not provided by Google"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            with transaction.atomic():
                user, created = User.objects.get_or_create(
                    email=email,
                    defaults={"is_active": True}
                )

            if not user.is_active:
                return Response(
                    {"detail": "Account is disabled"},
                    status=status.HTTP_403_FORBIDDEN
                )

            tokens = user.tokens
            send_push_notification(user, "New Login", "Logged in via Google.")
            logger.info("google_login_success", user_id=user.id, created=created)

            return Response({
                "message": "Login successful",
                "access": tokens['access'],
                "refresh": tokens['refresh'],
                "user": UserProfileSerializer(user, context={"request": request}).data
            }, status=status.HTTP_200_OK)

        except ValueError as e:
            logger.warning("google_login_invalid_token", error=str(e))
            return Response(
                {"detail": "Invalid or expired Google token"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        except requests.exceptions.RequestException:
            logger.warning("google_api_request_failed")
            return Response(
                {"detail": "Failed to validate token with Google"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception:
            logger.exception("google_login_failed")
            return Response(
                {"detail": "Google authentication failed"},
                status=status.HTTP_400_BAD_REQUEST
            )


class AppleLoginView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    APPLE_KEYS_CACHE_KEY = "apple_public_keys"
    APPLE_KEYS_URL = "https://appleid.apple.com/auth/keys"

    @extend_schema(
        request={"application/json": {"type": "object", "properties": {
            "id_token": {"type": "string"},
            "email": {"type": "string", "description": "Required on first login only"}
        }}},
        responses={200: dict},
        summary="Apple Login (Mobile)"
    )
    def post(self, request):
        id_token_str = request.data.get("id_token")
        if not id_token_str:
            return Response(
                {"detail": "id_token is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            decoded = self._verify_apple_token(id_token_str)
        except ValueError as e:
            logger.warning("apple_login_invalid_token", error=str(e))
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception:
            logger.exception("apple_login_token_verification_failed")
            return Response(
                {"detail": "Apple authentication failed"},
                status=status.HTTP_400_BAD_REQUEST
            )

        apple_user_id = decoded.get("sub")
        if not apple_user_id:
            return Response(
                {"detail": "Invalid token: missing sub"},
                status=status.HTTP_400_BAD_REQUEST
            )

        email = decoded.get("email") or request.data.get("email")

        try:
            with transaction.atomic():
                user = self._get_or_create_user(apple_user_id, email)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            logger.exception("apple_login_user_creation_failed")
            return Response(
                {"detail": "Apple authentication failed"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not user.is_active:
            return Response(
                {"detail": "Account is disabled"},
                status=status.HTTP_403_FORBIDDEN
            )

        tokens = user.tokens
        send_push_notification(user, "New Login", "Logged in via Apple.")
        logger.info("apple_login_success", user_id=user.id, apple_sub=apple_user_id)

        return Response({
            "message": "Login successful",
            "access": tokens['access'],
            "refresh": tokens['refresh'],
            "user": UserProfileSerializer(user, context={"request": request}).data
        }, status=status.HTTP_200_OK)

    def _verify_apple_token(self, id_token_str: str) -> dict:
        apple_keys = cache.get(self.APPLE_KEYS_CACHE_KEY)
        if not apple_keys:
            response = requests.get(self.APPLE_KEYS_URL, timeout=5)
            response.raise_for_status()
            apple_keys = response.json()
            cache.set(self.APPLE_KEYS_CACHE_KEY, apple_keys, timeout=3600)

        headers = jwt.get_unverified_header(id_token_str)
        kid = headers.get("kid")

        matching_key = next(
            (k for k in apple_keys["keys"] if k["kid"] == kid), None
        )
        if not matching_key:
            cache.delete(self.APPLE_KEYS_CACHE_KEY)
            raise ValueError("Apple public key not found — please retry")

        public_key = RSAAlgorithm.from_jwk(matching_key)

        decoded = jwt.decode(
            id_token_str,
            public_key,
            algorithms=["RS256"],
            audience=settings.APPLE_CLIENT_ID,
            issuer="https://appleid.apple.com"
        )
        return decoded

    def _get_or_create_user(self, apple_user_id: str, email: str | None):
        user = User.objects.filter(social_id=apple_user_id).first()
        if user:
            return user

        if not email:
            raise ValueError("Email is required on first Apple login")

        user = User.objects.filter(email=email).first()
        if user:
            user.social_id = apple_user_id
            user.save(update_fields=["social_id"])
            return user

        return User.objects.create(
            email=email,
            social_id=apple_user_id,
            is_active=True,
        )
        
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