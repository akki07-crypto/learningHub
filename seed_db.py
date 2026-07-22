import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import UserProfile, Badge, UserBadge, Notification, SkillOffer, SwapRequest, DirectMessage, Certificate
from courses.models import Course, Category, Review, CourseBookmark
from bookings.models import Booking
from forum.models import ForumPost, ForumAnswer
from courses.youtube_service import seed_mock_courses
import datetime

def seed():
    print("[INFO] Seeding database with initial data...")

    # Seed Badges
    badges_data = [
        {'name': 'Pioneer Learner 🌟', 'slug': 'pioneer', 'description': 'Joined LearnHub Platform', 'icon': '🌟', 'points_threshold': 100},
        {'name': 'Code Ninja 🥷', 'slug': 'code-ninja', 'description': 'Earned over 200 XP Points', 'icon': '🥷', 'points_threshold': 200},
        {'name': 'Forum Contributor 💬', 'slug': 'forum-star', 'description': 'Active Q&A poster and answerer', 'icon': '💬', 'points_threshold': 300},
        {'name': 'Tech Master 🎓', 'slug': 'tech-master', 'description': 'Earned 500+ XP Points', 'icon': '🎓', 'points_threshold': 500},
    ]

    for bdata in badges_data:
        Badge.objects.get_or_create(slug=bdata['slug'], defaults=bdata)

    # Seed Courses
    seed_mock_courses()

    # Seed Demo Users
    user1, created1 = User.objects.get_or_create(username='demouser', defaults={'email': 'demo@example.com'})
    if created1:
        user1.set_password('demo1234')
        user1.save()
        user1.profile.points = 350
        user1.profile.streak_count = 5
        user1.profile.save()

    user2, created2 = User.objects.get_or_create(username='alex_coder', defaults={'email': 'alex@example.com'})
    if created2:
        user2.set_password('demo1234')
        user2.save()
        user2.profile.points = 620
        user2.profile.streak_count = 12
        user2.profile.save()

    # Seed Skill Offers
    SkillOffer.objects.get_or_create(
        user=user2,
        offered_skill='Python & Django',
        defaults={
            'title': 'Teaching Python & Django in exchange for React JS',
            'wanted_skill': 'React JS & Frontend',
            'description': 'Senior Backend developer offering 1-on-1 Python tutoring in exchange for modern React JS state management techniques.',
            'experience_level': 'Expert'
        }
    )

    SkillOffer.objects.get_or_create(
        user=user1,
        offered_skill='MySQL Database Design',
        defaults={
            'title': 'Offering MySQL Optimization for UI/UX Design',
            'wanted_skill': 'Figma & UI/UX Design',
            'description': 'Want to learn Figma wireframing and design systems. I can teach relational database normalization and SQL queries.',
            'experience_level': 'Intermediate'
        }
    )

    # Seed Certificate
    Certificate.objects.get_or_create(
        user=user1,
        title='Python Full Stack Web Architecture Masterclass',
        defaults={'certificate_code': 'LH-CERT-DEMO101'}
    )

    # Seed Direct Message
    DirectMessage.objects.get_or_create(
        sender=user2,
        receiver=user1,
        content="Hey! I saw your request for Figma UI/UX design. Let's schedule a skill swap call!",
        defaults={'is_read': False}
    )

    print("[SUCCESS] Database seeding complete!")

if __name__ == '__main__':
    seed()
