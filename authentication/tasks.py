from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import OneTimePassword

@shared_task
def cleanup_expired_otps():
    expiration_time = timezone.now() - timedelta(minutes=10)
    OneTimePassword.objects.filter(created_at__lt=expiration_time).delete()