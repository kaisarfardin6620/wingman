import os
import firebase_admin
from firebase_admin import credentials, messaging
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def initialize_firebase():
    try:
        if not firebase_admin._apps:
            cred_path = os.environ.get('FIREBASE_CREDENTIALS_PATH')
            if cred_path and os.path.exists(cred_path):
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
            else:
                logger.warning("Firebase credentials not found or path not set")
    except Exception as e:
        logger.error(f"Firebase initialization error: {e}")

def send_push_notification(user, title, body, data=None):
    try:
        from .models import Notification
        Notification.objects.create(user=user, title=title, body=body, data=data or {})
    except Exception as e:
        logger.error(f"Failed to save notification to DB for user {user.id}: {e}")

    if not user.is_active: return

    try:
        if hasattr(user, 'settings') and user.settings.hide_notifications: return

        devices = list(user.fcm_devices.all())
        if not devices: return
        tokens = [d.token for d in devices]
        if not tokens: return
        
        safe_data = {str(k): str(v) for k, v in (data or {}).items()}

        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            android=messaging.AndroidConfig(
                priority='high',
                notification=messaging.AndroidNotification(
                    sound='default',
                    channel_id='high_importance_channel', 
                    click_action='FLUTTER_NOTIFICATION_CLICK',
                )
            ),
            apns=messaging.APNSConfig(
                payload=messaging.APNSPayload(
                    aps=messaging.Aps(
                        sound='default',
                        content_available=True,
                        mutable_content=True,
                    )
                )
            ),
            data=safe_data,
            tokens=tokens,
        )
        
        response = messaging.send_each_for_multicast(message)
        logger.info(f"Sent push notification to {user.email}: {response.success_count} success")
        
        if response.failure_count > 0:
            from .models import FCMDevice
            for idx, resp in enumerate(response.responses):
                if not resp.success:
                    logger.error(f"FCM Error for token {tokens[idx][:15]}...: {resp.exception}")
                    if resp.exception.code in ('NOT_FOUND', 'UNREGISTERED', 'INVALID_ARGUMENT'):
                        failed_token = tokens[idx]
                        FCMDevice.objects.filter(token=failed_token).delete()
                        
    except Exception as e:
        logger.error(f"Push notification error for {user.email}: {e}")