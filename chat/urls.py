from django.urls import path
from .views import CreateSessionView, ChatHistoryView, ImageUploadView

urlpatterns = [
    path('session/create/', CreateSessionView.as_view(), name='create-session'),
    path('session/<int:session_id>/history/', ChatHistoryView.as_view(), name='chat-history'),
    path('session/<int:session_id>/upload/', ImageUploadView.as_view(), name='image-upload'),
]