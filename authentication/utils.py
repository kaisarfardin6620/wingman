import random
import logging
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from .models import User, OneTimePassword

logger = logging.getLogger(__name__)

def generate_otp():
    return str(random.randint(1000, 9999))

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
        
        send_mail(
            subject="Your Verification Code",
            message=f"Your OTP code is {otp_code}. It expires in 5 minutes.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )
        
        return True
    except User.DoesNotExist:
        logger.warning(f"Attempted to send OTP to non-existent user: {email}")
        return False
    except Exception as e:
        logger.error(f"Error in send_otp_via_email: {str(e)}")
        return False

def verify_otp_via_email(email, otp_input):
    try:
        user = User.objects.get(email=email)
        otp_record = OneTimePassword.objects.get(user=user)
        
        expiry_time = otp_record.created_at + timedelta(minutes=5)
        if timezone.now() > expiry_time:
            logger.info(f"Expired OTP attempt for {email}")
            return False

        if otp_record.otp == otp_input:
            otp_record.delete()
            return True
            
        return False
    except (User.DoesNotExist, OneTimePassword.DoesNotExist):
        return False