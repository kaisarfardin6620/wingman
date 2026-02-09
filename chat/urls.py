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
    path(
        'sessions/<uuid:conversation_id>/upload/',
        ChatSessionImageUploadView.as_view(),
        name='session-upload'
    ),
    
    path(
        'stats/',
        ChatStatsView.as_view(),
        name='chat-stats'
    ),
    
    path('', include(router.urls)),
]