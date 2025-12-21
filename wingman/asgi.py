import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wingman.settings')
django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from wingman.middleware import JwtAuthMiddleware
import chat.routing

websocket_urlpatterns = chat.routing.websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JwtAuthMiddleware(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})