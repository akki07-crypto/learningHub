from django.db import models
from django.contrib.auth.models import User
import uuid

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(default="Passionate Learner & Tech Enthusiast", blank=True)
    qualification = models.CharField(max_length=150, default="B.Tech Computer Science", blank=True)
    current_study = models.CharField(max_length=200, default="Specializing in Python Full Stack & Databases", blank=True)
    skills_expertise = models.CharField(max_length=255, default="Python, Django, MySQL, SQL, React JS", blank=True)
    github_linkedin = models.URLField(max_length=255, blank=True, null=True)
    points = models.IntegerField(default=100)
    referral_code = models.CharField(max_length=12, unique=True, blank=True)
    referred_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals')
    streak_count = models.IntegerField(default=1)
    last_login_date = models.DateField(auto_now_add=True)
    avatar = models.CharField(max_length=255, default="https://api.dicebear.com/7.x/bottts/svg?seed=learnhub")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = uuid.uuid4().hex[:8].upper()
        super().save(*args, **kwargs)

    def check_daily_streak(self):
        import datetime
        today = datetime.date.today()
        if self.last_login_date:
            delta = (today - self.last_login_date).days
            if delta == 1:
                self.streak_count += 1
                self.points += 10
            elif delta > 1:
                self.streak_count = 1
        self.last_login_date = today
        self.save()

    def get_level(self):
        if self.points >= 1000:
            return "Master Mentor 👑"
        elif self.points >= 500:
            return "Tech Ninja 🥷"
        elif self.points >= 250:
            return "Skill Scholar 🎓"
        return "Beginner Explorer 🚀"

    def __str__(self):
        return f"{self.user.username} - {self.qualification} ({self.points} XP)"

class Badge(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=50, default="🏆")
    points_threshold = models.IntegerField(default=100)

    def __str__(self):
        return self.name

class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    unlocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'badge')

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=150)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    link = models.CharField(max_length=255, default="/dashboard/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.title}"

class SkillOffer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skill_offers')
    title = models.CharField(max_length=200)
    offered_skill = models.CharField(max_length=100)
    wanted_skill = models.CharField(max_length=100)
    description = models.TextField()
    experience_level = models.CharField(max_length=50, default="Intermediate")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} offers {self.offered_skill}"

class SwapRequest(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Declined', 'Declined'),
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_swap_requests')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_swap_requests')
    skill_offer = models.ForeignKey(SkillOffer, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class DirectMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificates')
    certificate_code = models.CharField(max_length=20, unique=True, blank=True)
    title = models.CharField(max_length=255)
    issued_date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.certificate_code:
            self.certificate_code = "CERT-" + str(uuid.uuid4()).hex[:10].upper()
        super().save(*args, **kwargs)
