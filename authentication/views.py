import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from django.db import transaction
from django.core.cache import cache
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.apple.views import AppleOAuth2Adapter
from allauth.socialaccount.providers.apple.client import AppleOAuth2Client
from allauth.socialaccount.models import SocialLogin
from core.utils import send_push_notification
from .serializers import *
from .models import User
from .utils import generate_otp, send_otp_via_email, verify_otp_via_email, send_otp_email_task

logger = logging.getLogger(__name__)

class OTPRateThrottle(AnonRateThrottle):
    scope = 'otp' 

class RegisterView(APIView):
    throttle_classes = [AnonRateThrottle]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    user = serializer.save()
                    success, message = send_otp_via_email(user.email)
                    
                    if success:
                        return Response({
                            "message": "Account created. OTP sent to your email.",
                            "email": user.email
                        }, status=status.HTTP_201_CREATED)
                    else:
                        raise Exception(message)
                        
            except Exception as e:
                logger.error(f"Registration failed for {request.data.get('email')}: {str(e)}")
                return Response(
                    {"error": "Registration failed. Please try again later."}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
    throttle_classes = [OTPRateThrottle]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            
            success, message = verify_otp_via_email(email, otp)
            
            if success:
                try:
                    user = User.objects.get(email=email)
                    if not user.is_active:
                        user.is_active = True
                        user.save(update_fields=['is_active'])
                    
                    tokens = user.tokens
                    
                    return Response({
                        "message": "Verification successful",
                    }, status=status.HTTP_200_OK)
                    
                except User.DoesNotExist:
                    return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    throttle_classes = [AnonRateThrottle]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        cache_key = f"login_attempts:{email}"
        attempts = cache.get(cache_key, 0)
        
        if attempts >= 5:
            return Response(
                {"error": "Account temporarily locked. Try again in 15 minutes."},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            cache.set(cache_key, attempts + 1, 900)
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            cache.set(cache_key, attempts + 1, 900)
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            success, message = send_otp_via_email(email)
            return Response({"error": "Account not active. OTP sent to email."}, status=status.HTTP_403_FORBIDDEN)
        
        cache.delete(cache_key)
        send_push_notification(user, "New Login", "Your account was just accessed.")

        tokens = user.tokens
        return Response({
            "message": "Successfully logged in.",
            "token": tokens['access'],
            "refresh_token": tokens['refresh'],
            "user_id": user.id,
        }, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            try:
                refresh_token = serializer.validated_data['refresh']
                token = RefreshToken(refresh_token)
                token.blacklist()
                
                fcm_token = serializer.validated_data.get('fcm_token')
                if fcm_token:
                    request.user.fcm_devices.filter(token=fcm_token).delete()
                
                return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
            except TokenError:
                return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResendOTPView(APIView):
    throttle_classes = [OTPRateThrottle]

    def post(self, request):
        serializer = ResendOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            if not User.objects.filter(email=email).exists():
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

            success, message = send_otp_via_email(email)
            
            if success:
                return Response({"message": message}, status=status.HTTP_200_OK)
            else:
                return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(APIView):
    throttle_classes = [OTPRateThrottle]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            try:
                user = User.objects.get(email=email)
                success, message = send_otp_via_email(email)
                
                if success:
                    send_push_notification(user, "Password Reset", "An OTP was sent to reset your password.")
                    
                    return Response({"message": "OTP sent for password reset."}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({"message": "If the email exists, an OTP has been sent."}, status=status.HTTP_200_OK)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordConfirmView(APIView):
    throttle_classes = [OTPRateThrottle]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            new_pass = serializer.validated_data['new_password']

            success, message = verify_otp_via_email(email, otp)
            
            if success:
                try:
                    with transaction.atomic():
                        user = User.objects.get(email=email)
                        user.set_password(new_pass)
                        user.save(update_fields=['password'])
                        tokens = OutstandingToken.objects.filter(user=user)
                        for token in tokens:
                            BlacklistedToken.objects.get_or_create(token=token)

                    send_push_notification(user, "Security Alert", "Your password has been changed successfully.")

                    return Response({"message": "Password reset successfully. All sessions logged out."}, status=status.HTTP_200_OK)
                    
                except User.DoesNotExist:
                    return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    throttle_classes = [UserRateThrottle]

    def get(self, request):
        cache_key = f"user_profile:{request.user.id}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)
        
        serializer = UserProfileSerializer(request.user, context={'request': request})
        cache.set(cache_key, serializer.data, 300)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = request.user
        data = request.data.copy()
        
        new_email = data.get('email', '').strip().lower()
        email_changed = False
        
        if new_email and new_email != user.email:
            if User.objects.filter(email=new_email).exists():
                return Response({"email": ["This email is already in use."]}, status=status.HTTP_400_BAD_REQUEST)
            
            email_changed = True
            if 'email' in data:
                del data['email']

        serializer = UserProfileSerializer(
            user, 
            data=data, 
            partial=True, 
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save()
            
            cache.delete(f"user_profile:{user.id}")
            
            response_data = {
                "message": "Profile updated successfully",
                "data": serializer.data
            }

            if email_changed:
                otp_code = generate_otp()
                
                cache_key = f"email_change_request:{user.id}"
                cache.set(cache_key, {'new_email': new_email, 'otp': otp_code}, 600)
                
                send_otp_email_task.delay(new_email, otp_code)
                
                response_data['message'] = "Profile updated. Please verify the OTP sent to your new email to complete the change."
                response_data['email_verification_required'] = True

            send_push_notification(request.user, "Profile Updated", "Your profile details have been updated.")
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GoogleLoginView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]
    
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
            
            tokens = user.tokens
            return Response({
                "message": "Login successful",
                "token": tokens['access'],
                "refresh_token": tokens['refresh'],
                "user": UserProfileSerializer(user, context={'request': request}).data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Google Login Failed: {str(e)}", exc_info=True)
            return Response({"detail": "Google authentication failed"}, status=status.HTTP_400_BAD_REQUEST)

class AppleLoginView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]
    
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
            
            tokens = user.tokens
            return Response({
                "message": "Login successful",
                "token": tokens['access'],
                "refresh_token": tokens['refresh'],
                "user": UserProfileSerializer(user, context={'request': request}).data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Apple Login Failed: {str(e)}", exc_info=True)
            return Response({"detail": "Apple authentication failed"}, status=status.HTTP_400_BAD_REQUEST)
        
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        serializer = UserChangePasswordSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(request, user)
            
            send_push_notification(user, "Security Alert", "Your password was changed.")
            
            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VerifyEmailChangeView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

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
            
            return Response({"message": "Email updated successfully."}, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  