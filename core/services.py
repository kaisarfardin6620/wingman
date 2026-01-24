import structlog
from django.core.cache import cache
from .models import Tone, Persona, UserSettings, TargetProfile
from .serializers import ToneSerializer, PersonaSerializer
from wingman.constants import CACHE_TTL_CONFIG_DATA, CACHE_TTL_USER_SETTINGS, MAX_FREE_TARGET_PROFILES

logger = structlog.get_logger(__name__)

class CoreService:
    @staticmethod
    def get_config_data():
        cache_key_tones = 'active_tones'
        cache_key_personas = 'active_personas'
        
        tones_data = cache.get(cache_key_tones)
        personas_data = cache.get(cache_key_personas)
        
        if tones_data is None:
            tones = Tone.objects.filter(is_active=True).only('id', 'name', 'description')
            tones_data = ToneSerializer(tones, many=True).data
            cache.set(cache_key_tones, tones_data, CACHE_TTL_CONFIG_DATA)
        
        if personas_data is None:
            personas = Persona.objects.filter(is_active=True).only('id', 'name', 'description')
            personas_data = PersonaSerializer(personas, many=True).data
            cache.set(cache_key_personas, personas_data, CACHE_TTL_CONFIG_DATA)
            
        return {"tones": tones_data, "personas": personas_data}

    @staticmethod
    def get_user_settings(user):
        cache_key = f"user_settings:{user.id}"
        cached_data = cache.get(cache_key)
        if cached_data: return cached_data
        
        settings, _ = UserSettings.objects.select_related('active_persona').prefetch_related('active_tones').get_or_create(user=user)
        return settings 

    @staticmethod
    def create_target_profile(user, data):
        if not user.is_premium:
            profile_count = TargetProfile.objects.filter(user=user).count()
            if profile_count >= MAX_FREE_TARGET_PROFILES:
                logger.warning("target_profile_limit", user_id=user.id)
                return None, "Free limit reached."
        return True, None