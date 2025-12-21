from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import logging
import traceback

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_kwargs={'max_retries': 3, 'countdown': 5},
    retry_backoff=True,
    retry_jitter=True,
)
def send_otp_email_task(self, email, otp_code):
    try:
        send_mail(
            subject="Your Verification Code",
            message=f"Your OTP code is {otp_code}. It expires in 5 minutes.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )
        logger.info(f"OTP email sent successfully to {email}")

    except Exception:
        logger.error(traceback.format_exc())
        raise
