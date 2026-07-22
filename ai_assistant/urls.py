from django.urls import path
from .views import gemini_chat_api

urlpatterns = [
    path('', gemini_chat_api, name='ai_chat_api'),
]
