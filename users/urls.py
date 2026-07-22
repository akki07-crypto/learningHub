from django.urls import path
from .views import register_view, login_view, logout_view, mark_notification_read

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('notification/read/<int:notif_id>/', mark_notification_read, name='mark_notification_read'),
]
