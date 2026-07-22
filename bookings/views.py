from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Booking
from users.models import Notification, UserProfile, Badge, UserBadge
import datetime

@login_required
def booking_calendar_view(request):
    today = datetime.date.today().strftime('%Y-%m-%d')
    peers = User.objects.exclude(id=request.user.id).select_related('profile')
    
    if request.method == 'POST':
        topic = request.POST.get('topic')
        session_mode = request.POST.get('session_mode', 'Roadmap')
        mentor_id = request.POST.get('mentor_user_id')
        mentor_custom = request.POST.get('mentor')
        date_str = request.POST.get('date')
        time_slot = request.POST.get('time_slot')
        notes = request.POST.get('notes', '')

        # Determine peer mentor name
        peer_user = None
        if mentor_id:
            peer_user = User.objects.filter(id=mentor_id).first()
            mentor_name = peer_user.username if peer_user else "Peer Student Mentor"
        else:
            mentor_name = mentor_custom or "Peer Student Mentor"

        if topic and date_str and time_slot:
            booking = Booking.objects.create(
                user=request.user,
                session_topic=topic,
                session_mode=session_mode,
                mentor_name=mentor_name,
                booking_date=date_str,
                time_slot=time_slot,
                notes=notes
            )
            
            # Award +25 XP Points
            profile, _ = UserProfile.objects.get_or_create(user=request.user)
            profile.points += 25
            profile.save()

            # Unlock Badge
            mentor_badge, _ = Badge.objects.get_or_create(
                slug='mentorship-guide',
                defaults={
                    'name': 'Mentorship Guide 🎓',
                    'description': 'Scheduled a 1-on-1 private mentorship session',
                    'icon': '🎓',
                    'points_threshold': 125
                }
            )
            UserBadge.objects.get_or_create(user=request.user, badge=mentor_badge)

            # Send In-App Notification to Peer Mentor
            if peer_user:
                mode_label = dict(Booking.MODE_CHOICES).get(session_mode, 'Mentorship Session')
                Notification.objects.create(
                    user=peer_user,
                    title=f"📅 Private {mode_label} Booked!",
                    message=f"{request.user.username} booked a private 1-on-1 {mode_label} session with you on '{topic}' ({date_str} at {time_slot})!",
                    link="/bookings/"
                )

            messages.success(request, f"Private 1-on-1 Mentorship session scheduled with {mentor_name}! (+25 XP Points)")
            return redirect('booking_calendar')

    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    
    context = {
        'today': today,
        'bookings': bookings,
        'peers': peers,
    }
    return render(request, 'bookings/calendar.html', context)

def video_call_room_view(request, room_name):
    booking = Booking.objects.filter(jitsi_room_name=room_name).first()
    context = {
        'room_name': room_name,
        'booking': booking,
    }
    return render(request, 'video_call/room.html', context)
