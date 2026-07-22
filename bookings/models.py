from django.db import models
from django.contrib.auth.models import User
import uuid

class Booking(models.Model):
    MODE_CHOICES = (
        ('Roadmap', '🗺️ Career & Skill Roadmap Guidance'),
        ('MockInterview', '⚡ Mock Technical Interview Practice'),
        ('CodeAudit', '🔍 Pair Programming & Deep Code Audit'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    session_topic = models.CharField(max_length=200)
    session_mode = models.CharField(max_length=50, choices=MODE_CHOICES, default='Roadmap')
    mentor_name = models.CharField(max_length=100, default="Senior Python Architect")
    booking_date = models.DateField()
    time_slot = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default='Confirmed')
    jitsi_room_name = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    rating = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.jitsi_room_name:
            self.jitsi_room_name = "LearnHub-Mentorship-" + str(uuid.uuid4()).hex[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.session_topic} ({self.get_session_mode_display()})"
