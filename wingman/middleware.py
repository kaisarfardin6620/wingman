from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.tokens import AccessToken, UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth import get_user_model
from urllib.parse import parse_qs
import logging

User = get_user_model()
logger = logging.getLogger(__name__)

@database_sync_to_async
def get_user(token_key):
    try:
        UntypedToken(token_key)
        token = AccessToken(token_key)
        user_id = token.payload.get('user_id')
        if not user_id:
            return AnonymousUser()
        return User.objects.get(id=user_id)
    except (InvalidToken, TokenError, User.DoesNotExist):
        return AnonymousUser()
    except Exception as e:
        logger.error(f"WebSocket Auth Error: {str(e)}")
        return AnonymousUser()

class JwtAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        token = None
        
        headers = dict(scope.get("headers", []))
        if b"authorization" in headers:
            try:
                auth_header = headers[b"authorization"].decode("latin1")
                if auth_header.startswith("Bearer "):
                    token = auth_header.split(" ")[1]
            except Exception:
                pass
        
        if not token:
            query_string = scope.get("query_string", b"").decode("utf-8")
            query_params = parse_qs(query_string)
            token = query_params.get("token", [None])[0]

        if token:
            scope["user"] = await get_user(token)
        else:
            scope["user"] = AnonymousUser()
        
        return await super().__call__(scope, receive, send)