from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('session_topic', 'user', 'mentor_name', 'booking_date', 'time_slot', 'status', 'jitsi_room_name')
    list_filter = ('status', 'booking_date')
    search_fields = ('session_topic', 'user__username', 'mentor_name', 'jitsi_room_name')
