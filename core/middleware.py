from django.utils import translation

class UserLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', None)
        
        if user and user.is_authenticated and hasattr(user, 'settings'):
            language = user.settings.language
            if language:
                translation.activate(language)
                request.LANGUAGE_CODE = translation.get_language()
        
        response = self.get_response(request)
        
        translation.deactivate()
        
        return response