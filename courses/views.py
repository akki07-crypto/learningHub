from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Course, Category, Review, CourseBookmark
from users.models import Certificate
from .youtube_service import fetch_and_sync_youtube_courses

def course_list_view(request):
    query = request.GET.get('q', '')
    cat_slug = request.GET.get('category', '')
    difficulty = request.GET.get('difficulty', '')

    fetch_and_sync_youtube_courses(query if query else "Python Programming")

    courses = Course.objects.all()

    if query:
        courses = courses.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) | 
            Q(channel_title__icontains=query)
        )

    if cat_slug:
        courses = courses.filter(category__slug=cat_slug)

    if difficulty:
        courses = courses.filter(difficulty=difficulty)

    categories = Category.objects.all()

    context = {
        'courses': courses,
        'categories': categories,
        'selected_query': query,
        'selected_cat': cat_slug,
        'selected_difficulty': difficulty,
    }
    return render(request, 'courses/list.html', context)

def course_detail_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    reviews = course.reviews.all()
    related_courses = Course.objects.filter(category=course.category).exclude(id=course.id)[:3]
    
    bookmark = None
    if request.user.is_authenticated:
        bookmark = CourseBookmark.objects.filter(user=request.user, course=course).first()

    if request.method == 'POST' and request.user.is_authenticated:
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        if rating and comment:
            Review.objects.create(
                course=course,
                user=request.user,
                rating=int(rating),
                comment=comment
            )
            profile = request.user.profile
            profile.points += 15
            profile.save()
            messages.success(request, "Review submitted! You earned +15 XP points.")
            return redirect('course_detail', course_id=course.id)

    context = {
        'course': course,
        'reviews': reviews,
        'related_courses': related_courses,
        'bookmark': bookmark,
    }
    return render(request, 'courses/detail.html', context)

@login_required
def toggle_course_bookmark(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    bookmark, created = CourseBookmark.objects.get_or_create(user=request.user, course=course)
    
    action = request.GET.get('action', 'bookmark')
    if action == 'complete':
        bookmark.is_completed = True
        bookmark.progress_percent = 100
        bookmark.save()
        
        # Award +50 XP and Issue Certificate
        request.user.profile.points += 50
        request.user.profile.save()
        
        Certificate.objects.get_or_create(
            user=request.user,
            title=f"Course Completion: {course.title}"
        )
        messages.success(request, f"Course Completed! You earned +50 XP and a Completion Certificate. 🎓")
    else:
        if not created:
            bookmark.delete()
            messages.info(request, "Removed from Bookmarks.")
            return redirect('course_detail', course_id=course.id)
        else:
            bookmark.progress_percent = 25
            bookmark.save()
            messages.success(request, "Added to Bookmarks!")
            
    return redirect('course_detail', course_id=course.id)
