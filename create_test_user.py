import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import UserProfile, Badge, UserBadge
from users.views import send_signup_email_notification

test_username = "test_learner_2026"
test_email = "student2026@gmail.com"
test_phone = "+91 9876543210"
test_password = "Password@123"

print("="*60)
print(" EXECUTING TEST USER REGISTRATION SIMULATION")
print("="*60)

# Check if user exists, delete first for clean test
User.objects.filter(username=test_username).delete()

# Create User in MySQL DB
user = User.objects.create_user(
    username=test_username,
    email=test_email,
    password=test_password
)

profile, _ = UserProfile.objects.get_or_create(user=user)
profile.phone_number = test_phone
profile.points = 100
profile.save()

welcome_badge, _ = Badge.objects.get_or_create(
    slug='pioneer',
    defaults={
        'name': 'Pioneer Learner',
        'description': 'Joined the LearnHub platform',
        'icon': '🌟',
        'points_threshold': 100
    }
)
UserBadge.objects.get_or_create(user=user, badge=welcome_badge)

print(f"[SUCCESS] User '{user.username}' created in MySQL database ('elearn_db')!")
print(f" -> User ID        : {user.id}")
print(f" -> Email          : {user.email}")
print(f" -> Mobile Number  : {profile.phone_number}")
print(f" -> XP Points      : {profile.points}")
print(f" -> Referral Code  : {profile.referral_code}")
print("-" * 60)

print("[INFO] Dispatching Formspree Email Notification to akki28869@gmail.com...")
send_signup_email_notification(user.username, user.email, profile.phone_number, ref_code='')
print("="*60)
print(" TEST REGISTRATION COMPLETED SUCCESSFULLY!")
print("="*60)
