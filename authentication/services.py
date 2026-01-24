import structlog
from django.contrib.auth import get_user_model
from django.db import transaction
from django.core.cache import cache
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from .utils import send_otp_via_email, verify_otp_via_email, generate_otp
from .tasks import send_otp_email_task
from core.utils import send_push_notification
from wingman.constants import CACHE_TTL_USER_PROFILE, CACHE_TTL_LOGIN_ATTEMPTS, MAX_LOGIN_ATTEMPTS, CACHE_TTL_OTP_REQUEST

User = get_user_model()
logger = structlog.get_logger(__name__)

class AuthService:
    
    @staticmethod
    def register_user(validated_data):
        email = validated_data['email']
        try:
            with transaction.atomic():
                validated_data.pop('confirm_password', None)
                
                user = User.objects.create_user(**validated_data)
                success, message = send_otp_via_email(user.email)
                
                if success:
                    logger.info("user_registered", email=email)
                    return {"message": "Account created. OTP sent to your email.", "email": user.email}
                else:
                    logger.error("registration_otp_failed", email=email, error=message)
                    raise Exception(message)
        except Exception as e:
            logger.error("registration_failed", email=email, error=str(e))
            raise e

    @staticmethod
    def verify_otp(email, otp):
        success, message = verify_otp_via_email(email, otp)
        if success:
            try:
                user = User.objects.get(email=email)
                if not user.is_active:
                    user.is_active = True
                    user.save(update_fields=['is_active'])
                    logger.info("user_activated", email=email)
                return True, "Verification successful"
            except User.DoesNotExist:
                return False, "User not found"
        return False, message

    @staticmethod
    def login_user(email, password):
        cache_key = f"login_attempts:{email}"
        attempts = cache.get(cache_key, 0)

        if attempts >= MAX_LOGIN_ATTEMPTS:
            logger.warning("account_locked", email=email, attempts=attempts)
            return None, "Account temporarily locked. Try again in 15 minutes.", 429

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            cache.set(cache_key, attempts + 1, CACHE_TTL_LOGIN_ATTEMPTS)
            return None, "Invalid credentials.", 401

        if not user.check_password(password):
            cache.set(cache_key, attempts + 1, CACHE_TTL_LOGIN_ATTEMPTS)
            logger.warning("login_failed_password", email=email)
            return None, "Invalid credentials.", 401

        if not user.is_active:
            send_otp_via_email(email)
            return None, "Account not active. OTP sent to email.", 403

        cache.delete(cache_key)
        send_push_notification(user, "New Login", "Your account was just accessed.")
        logger.info("login_successful", user_id=user.id)

        tokens = user.tokens
        return {
            "message": "Successfully logged in.",
            "token": tokens['access'],
            "refresh_token": tokens['refresh'],
            "user_id": user.id,
        }, None, 200

    @staticmethod
    def forgot_password(email):
        try:
            user = User.objects.get(email=email)
            success, message = send_otp_via_email(email)
            if success:
                send_push_notification(user, "Password Reset", "An OTP was sent to reset your password.")
                logger.info("forgot_password_otp_sent", email=email)
                return True, "OTP sent for password reset."
            return False, message
        except User.DoesNotExist:
            return True, "If the email exists, an OTP has been sent."

    @staticmethod
    def reset_password(email, otp, new_password):
        success, message = verify_otp_via_email(email, otp)
        if success:
            try:
                with transaction.atomic():
                    user = User.objects.get(email=email)
                    user.set_password(new_password)
                    user.save(update_fields=['password'])
                    tokens = OutstandingToken.objects.filter(user=user)
                    for token in tokens:
                        BlacklistedToken.objects.get_or_create(token=token)

                send_push_notification(user, "Security Alert", "Your password has been changed successfully.")
                logger.info("password_reset_success", user_id=user.id)
                return True, "Password reset successfully. All sessions logged out."
            except User.DoesNotExist:
                return False, "User not found"
        return False, message

    @staticmethod
    def update_profile(user, data, request=None):
        new_email = data.get('email', '').strip().lower()
        email_changed = False
        
        if new_email and new_email != user.email:
            if User.objects.exclude(pk=user.pk).filter(email=new_email).exists():
                return None, "This email is already in use."
            
            email_changed = True
            if 'email' in data:
                del data['email']

        for attr, value in data.items():
            setattr(user, attr, value)
        user.save()
        
        cache.delete(f"user_profile:{user.id}")
        
        response_data = {
            "message": "Profile updated successfully",
            "user": user 
        }

        if email_changed:
            otp_code = generate_otp()
            cache_key = f"email_change_request:{user.id}"
            cache.set(cache_key, {'new_email': new_email, 'otp': otp_code}, CACHE_TTL_OTP_REQUEST)
            send_otp_email_task.delay(new_email, otp_code)
            
            response_data['message'] = "Profile updated. Please verify the OTP sent to your new email to complete the change."
            response_data['email_verification_required'] = True
            logger.info("email_change_requested", user_id=user.id, new_email=new_email)

        send_push_notification(user, "Profile Updated", "Your profile details have been updated.")
        return response_data, None