from django.contrib import admin
from .models import Category, Course, Review, CourseBookmark

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'difficulty', 'average_rating', 'views', 'created_at')
    list_filter = ('category', 'difficulty', 'created_at')
    search_fields = ('title', 'description', 'channel_title', 'youtube_id')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('course', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('course__title', 'user__username', 'comment')

@admin.register(CourseBookmark)
class CourseBookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'is_completed', 'progress_percent', 'updated_at')
    list_filter = ('is_completed', 'updated_at')
    search_fields = ('user__username', 'course__title')
