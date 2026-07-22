import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import UserProfile, Badge, UserBadge

try:
    # Create or update akki in MySQL
    akki_user, created = User.objects.get_or_create(username='akki')
    if created:
        akki_user.set_password('password123')
        akki_user.save()
        print("[SUCCESS] User 'akki' synced to MySQL database ('elearn_db')!")
    else:
        print("[INFO] User 'akki' already exists in MySQL database!")

    p = akki_user.profile
    p.points = 100
    p.save()
except Exception as e:
    print(f"[ERROR] Sync failed: {e}")
