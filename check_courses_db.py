import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from courses.models import Course

print("="*60)
print("COURSES IN MYSQL DATABASE:")
print("="*60)

courses = Course.objects.all()
for c in courses:
    print(f"ID: {c.id} | Title: {c.title}")
    print(f"YouTube ID: '{c.youtube_id}'")
    print(f"Embed URL : https://www.youtube.com/embed/{c.youtube_id}")
    print("-" * 60)
