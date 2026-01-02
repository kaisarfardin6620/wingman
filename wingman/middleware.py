from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth import get_user_model
from django.conf import settings
import urllib.parse
import logging

User = get_user_model()

logger = logging.getLogger(__name__)
@database_sync_to_async
def get_user(token_key):
    try:
        validated_token = UntypedToken(token_key)
        user_id = validated_token.get("user_id")
        if not user_id:
            user_id = validated_token.get("sub")
        if not user_id:
            return AnonymousUser()
        return User.objects.get(id=user_id)
    except (InvalidToken, TokenError, User.DoesNotExist, Exception) as e:
        logger.warning(f"WebSocket Auth Failed: {e}") 
        return AnonymousUser()

class JwtAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode("utf-8")
        query_params = urllib.parse.parse_qs(query_string)
        token = query_params.get("token", [None])[0]

        if token:
            scope["user"] = await get_user(token)
        else:
            scope["user"] = AnonymousUser()
        
        return await super().__call__(scope, receive, send)