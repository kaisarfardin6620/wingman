import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.throttling import AnonRateThrottle
from django.utils.translation import gettext_lazy as _
from django.db import transaction

from .serializers import *
from .models import User
from .utils import send_otp_via_email, verify_otp_via_email

logger = logging.getLogger(__name__)

try:
    from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
    from allauth.socialaccount.providers.oauth2.client import OAuth2Client
    from allauth.socialaccount.providers.apple.views import AppleOAuth2Adapter
    from allauth.socialaccount.providers.apple.client import AppleOAuth2Client
except ImportError:
    pass

class RegisterView(APIView):
    throttle_classes = [AnonRateThrottle]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    user = serializer.save()
                    if send_otp_via_email(user.email):
                        return Response({
                            "message": "Account created. OTP sent.",
                            "email": user.email
                        }, status=status.HTTP_201_CREATED)
                    else:
                        raise Exception("Failed to send OTP email service error.")
            except Exception as e:
                logger.error(f"Registration failed: {str(e)}")
                return Response(
                    {"error": "Failed to send OTP. Please try again later."}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
    throttle_classes = [AnonRateThrottle]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            otp = serializer.data['otp']
            
            if verify_otp_via_email(email, otp):
                try:
                    user = User.objects.get(email=email)
                    if not user.is_active:
                        user.is_active = True
                        user.save()
                    
                    tokens = user.tokens
                    return Response({
                        "message": "Verification Successful",
                        "token": tokens['access'],
                        "refresh_token": tokens['refresh'],
                        "user": UserProfileSerializer(user, context={'request': request}).data
                    }, status=status.HTTP_200_OK)
                except User.DoesNotExist:
                    return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            return Response({"error": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    throttle_classes = [AnonRateThrottle]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.data['email']
        password = serializer.data['password']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            send_otp_via_email(email)
            return Response({"error": "Account not active. OTP sent to email."}, status=status.HTTP_403_FORBIDDEN)

        tokens = user.tokens
        return Response({
            "message": "Successfully Logged in.",
            "token": tokens['access'],
            "refresh_token": tokens['refresh'],
            "user_id": user.id,
        }, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            try:
                refresh_token = serializer.data['refresh']
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
            except TokenError:
                return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResendOTPView(APIView):
    throttle_classes = [AnonRateThrottle]

    def post(self, request):
        serializer = ResendOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            if not User.objects.filter(email=email).exists():
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

            if send_otp_via_email(email):
                return Response({"message": "OTP resent successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Failed to send SMS."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(APIView):
    throttle_classes = [AnonRateThrottle]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            if User.objects.filter(email=email).exists():
                send_otp_via_email(email)
                return Response({"message": "OTP sent for password reset."}, status=status.HTTP_200_OK)
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordConfirmView(APIView):
    throttle_classes = [AnonRateThrottle]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            otp = serializer.data['otp']
            new_pass = serializer.data['new_password']

            if verify_otp_via_email(email, otp):
                try:
                    user = User.objects.get(email=email)
                    user.set_password(new_pass)
                    user.save()
                    return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
                except User.DoesNotExist:
                    return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"error": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        serializer = UserProfileSerializer(request.user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Profile updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GoogleLoginView(APIView):
    permission_classes = [AllowAny]
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
            login = adapter.complete_login(request, app, social_token)
            login.state = {} 
            login.save(request)
            
            tokens = login.user.tokens
            return Response({
                "message": "Login Successful",
                "token": tokens['access'],
                "refresh_token": tokens['refresh'],
                "user": UserProfileSerializer(login.user, context={'request': request}).data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Google Login Failed: {str(e)}")
            return Response({"detail": "Google authentication failed"}, status=status.HTTP_400_BAD_REQUEST)

class AppleLoginView(APIView):
    permission_classes = [AllowAny]
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
            login = adapter.complete_login(request, app, social_token)
            login.state = {} 
            login.save(request)
            
            tokens = login.user.tokens
            return Response({
                "message": "Login Successful",
                "token": tokens['access'],
                "refresh_token": tokens['refresh'],
                "user": UserProfileSerializer(login.user, context={'request': request}).data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Apple Login Failed: {str(e)}")
            return Response({"detail": "Apple authentication failed"}, status=status.HTTP_400_BAD_REQUEST)