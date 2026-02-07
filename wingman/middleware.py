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
        
    except (InvalidToken, TokenError, User.DoesNotExist) as e:
        logger.warning(f"WebSocket Auth Failed: {str(e)}")
        return AnonymousUser()
    except Exception as e:
        logger.error(f"Unexpected WebSocket Auth Error: {str(e)}")
        return AnonymousUser()

class JwtAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode("utf-8")
        query_params = parse_qs(query_string)
        token = query_params.get("token", [None])[0]

        if token:
            scope["user"] = await get_user(token)
        else:
            scope["user"] = AnonymousUser()
            logger.debug("WebSocket connection attempted without token")
        
        return await super().__call__(scope, receive, send)