from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ChatSessionViewSet,
    ChatSessionImageUploadView,
    ChatStatsView
)

router = DefaultRouter()
router.register(r'sessions', ChatSessionViewSet, basename='chat-sessions')

urlpatterns = [
    # Image upload endpoint
    path(
        'sessions/<uuid:conversation_id>/upload/',
        ChatSessionImageUploadView.as_view(),
        name='session-upload'
    ),
    
    # Stats endpoint
    path(
        'stats/',
        ChatStatsView.as_view(),
        name='chat-stats'
    ),
    
    # Router URLs
    path('', include(router.urls)),
]