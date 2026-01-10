from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth import get_user_model
from django.conf import settings
import urllib.parse
import logging
import hashlib

User = get_user_model()
logger = logging.getLogger(__name__)

# Cache timeout for user lookups (5 minutes)
USER_CACHE_TIMEOUT = getattr(settings, 'WS_USER_CACHE_TIMEOUT', 300)


def get_token_cache_key(token_key):
    """Generate cache key for token"""
    token_hash = hashlib.sha256(token_key.encode()).hexdigest()[:16]
    return f"ws_user:{token_hash}"


@database_sync_to_async
def get_user_from_db(user_id):
    """Fetch user from database"""
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()


async def get_user(token_key):
    """
    Get user from token with caching.
    Cache structure: token_hash -> user_id for faster lookups
    """
    cache_key = get_token_cache_key(token_key)
    
    # Try to get user_id from cache
    cached_user_id = cache.get(cache_key)
    
    if cached_user_id:
        # User ID found in cache, fetch user
        try:
            return await get_user_from_db(cached_user_id)
        except Exception as e:
            logger.warning(f"Cached user lookup failed: {e}")
            # If cache is stale, continue to validate token
    
    # Validate token and cache result
    try:
        validated_token = UntypedToken(token_key)
        user_id = validated_token.get("user_id") or validated_token.get("sub")
        
        if not user_id:
            logger.warning("Token missing user_id claim")
            return AnonymousUser()
        
        # Cache the user_id for future lookups
        cache.set(cache_key, user_id, USER_CACHE_TIMEOUT)
        
        return await get_user_from_db(user_id)
        
    except (InvalidToken, TokenError) as e:
        logger.warning(f"WebSocket Auth Failed - Invalid Token: {e}")
        return AnonymousUser()
    except Exception as e:
        logger.error(f"WebSocket Auth Error: {e}", exc_info=True)
        return AnonymousUser()


class JwtAuthMiddleware(BaseMiddleware):
    """
    Custom JWT authentication middleware for Django Channels WebSocket connections.
    Extracts token from query parameters and authenticates user.
    """
    
    async def __call__(self, scope, receive, send):
        # Parse query string for token
        query_string = scope.get("query_string", b"").decode("utf-8")
        query_params = urllib.parse.parse_qs(query_string)
        token = query_params.get("token", [None])[0]
        
        # Authenticate user
        if token:
            scope["user"] = await get_user(token)
        else:
            scope["user"] = AnonymousUser()
            logger.debug("WebSocket connection without token")
        
        return await super().__call__(scope, receive, send)