import secrets
import logging
from django.utils import timezone
from django.db import transaction
from datetime import timedelta
from .models import User, OneTimePassword
from .tasks import send_otp_email_task
from wingman.constants import OTP_LENGTH

logger = logging.getLogger(__name__)

def generate_otp():
    return ''.join([str(secrets.randbelow(10)) for _ in range(OTP_LENGTH)])

def send_otp_via_email(email):
    try:
        otp_code = generate_otp()
        user = User.objects.get(email=email)
        
        OneTimePassword.objects.update_or_create(
            user=user,
            defaults={
                'otp': otp_code,
                'created_at': timezone.now()
            }
        )
        transaction.on_commit(lambda: send_otp_email_task.delay(email, otp_code))
        return True, "OTP sent successfully"
    except User.DoesNotExist:
        return True, "OTP sent successfully" 
    except Exception as e:
        logger.error(f"Error in send_otp_via_email: {str(e)}")
        return False, "Failed to generate OTP"

def verify_otp_via_email(email, otp_input):
    try:
        user = User.objects.get(email=email)
        otp_record = OneTimePassword.objects.get(user=user)
        
        if otp_record.is_expired():
            return False, "OTP expired"

        if otp_record.otp == otp_input:
            otp_record.delete()
            return True, "Verification successful"
            
        return False, "Invalid OTP"
    except (User.DoesNotExist, OneTimePassword.DoesNotExist):
        return False, "Invalid request"