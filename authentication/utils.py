import secrets
import logging
from django.utils import timezone
from datetime import timedelta
from .models import User, OneTimePassword
from .tasks import send_otp_email_task

logger = logging.getLogger(__name__)

def generate_otp():
    return ''.join([str(secrets.randbelow(10)) for _ in range(6)])

def send_otp_via_email(email):
    otp_code = generate_otp()
    try:
        user = User.objects.get(email=email)
        OneTimePassword.objects.update_or_create(
            user=user,
            defaults={
                'otp': otp_code,
                'created_at': timezone.now()
            }
        )
        
        send_otp_email_task.delay(email, otp_code)
        
        return True, "OTP sent successfully"
    except User.DoesNotExist:
        logger.warning(f"Attempted to send OTP to non-existent user: {email}")
        return False, "User not found"
    except Exception as e:
        logger.error(f"Error in send_otp_via_email: {str(e)}")
        return False, "Failed to generate OTP"

def verify_otp_via_email(email, otp_input):
    try:
        user = User.objects.get(email=email)
        otp_record = OneTimePassword.objects.get(user=user)
        
        expiry_time = otp_record.created_at + timedelta(minutes=5)
        if timezone.now() > expiry_time:
            return False, "OTP expired"

        if otp_record.otp == otp_input:
            otp_record.delete()
            return True, "Verification successful"
            
        return False, "Invalid OTP"
    except (User.DoesNotExist, OneTimePassword.DoesNotExist):
        return False, "Invalid request"