import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import UserProfile

print("="*60)
print(" REGISTERED USERS IN YOUR MYSQL DATABASE ('elearn_db')")
print("="*60)

users = User.objects.all().order_by('-date_joined')
for u in users:
    p = u.profile
    print(f"Username       : {u.username}")
    print(f"User ID        : {u.id}")
    print(f"Email          : {u.email if u.email else 'None provided'}")
    print(f"XP Points      : {p.points}")
    print(f"Daily Streak   : {p.streak_count} Days")
    print(f"Referral Code  : {p.referral_code}")
    print(f"Joined Date    : {u.date_joined.strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)
