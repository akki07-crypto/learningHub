from django.urls import path
from .views import booking_calendar_view

urlpatterns = [
    path('', booking_calendar_view, name='booking_calendar'),
]
