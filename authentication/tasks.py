from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def send_otp_email_task(self, email, otp_code):
    try:
        send_mail(
            subject="Your Verification Code",
            message=f"Your OTP code is {otp_code}. It expires in 5 minutes.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )
        return f"OTP sent to {email}"
    except Exception as e:
        logger.error(f"Failed to send OTP to {email}: {e}")
        raise self.retry(exc=e, countdown=10)