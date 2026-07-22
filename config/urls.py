from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from courses.models import Course
from forum.models import ForumPost
from users.models import UserProfile, Badge, SkillOffer
from users.views import (
    skills_index_view, send_swap_request, respond_swap_request, 
    direct_messages_view, view_certificate, leaderboard_view
)

def home_view(request):
    featured_courses = Course.objects.all()[:6]
    recent_forum_posts = ForumPost.objects.all()[:4]
    top_learners = UserProfile.objects.order_by('-points')[:5]
    all_badges = Badge.objects.all()[:4]
    latest_skills = SkillOffer.objects.all()[:3]
    
    context = {
        'featured_courses': featured_courses,
        'recent_forum_posts': recent_forum_posts,
        'top_learners': top_learners,
        'all_badges': all_badges,
        'latest_skills': latest_skills,
    }
    return render(request, 'home.html', context)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    
    # Users & Dashboard
    path('users/', include('users.urls')),
    path('dashboard/', include('users.urls_dashboard')),
    
    # Feature 1: Skill Swap
    path('skills/', skills_index_view, name='skills_index'),
    path('skills/request/<int:offer_id>/', send_swap_request, name='send_swap_request'),
    path('swap-request/<int:req_id>/<str:action>/', respond_swap_request, name='respond_swap_request'),
    
    # Feature 2: Direct Messaging
    path('messages/', direct_messages_view, name='direct_messages'),
    
    # Feature 3: Certificates
    path('certificates/<str:cert_code>/', view_certificate, name='view_certificate'),
    
    # Feature 4: Leaderboard
    path('leaderboard/', leaderboard_view, name='leaderboard'),
    
    # Courses
    path('courses/', include('courses.urls')),
    
    # Bookings & Video Call
    path('bookings/', include('bookings.urls')),
    path('video-call/<str:room_name>/', include('bookings.urls_video')),
    
    # Forum
    path('forum/', include('forum.urls')),
    
    # AI Assistant API
    path('api/ai-chat/', include('ai_assistant.urls')),
]
