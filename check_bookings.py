import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from bookings.models import Booking

print("="*60)
print(" MENTORSHIP BOOKED SESSIONS IN MYSQL DATABASE ('elearn_db')")
print("="*60)

bookings = Booking.objects.all().order_by('-booking_date')
for b in bookings:
    print(f"Topic        : {b.session_topic}")
    print(f"Booked By    : {b.user.username}")
    print(f"Mentor Name  : {b.mentor_name}")
    print(f"Date & Slot  : {b.booking_date} ({b.time_slot})")
    print(f"Jitsi Room   : {b.jitsi_room_name}")
    print(f"Video Call   : http://127.0.0.1:8000/video-call/{b.jitsi_room_name}/")
    print("-" * 60)
