from django.urls import path
from .views import video_call_room_view

urlpatterns = [
    path('', video_call_room_view, name='video_call_room'),
]
