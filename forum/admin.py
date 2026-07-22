from django.contrib import admin
from .models import ForumPost, ForumAnswer

@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'upvote_count', 'is_solved', 'created_at')
    list_filter = ('is_solved', 'created_at')
    search_fields = ('title', 'content', 'user__username')

@admin.register(ForumAnswer)
class ForumAnswerAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'upvote_count', 'is_accepted', 'created_at')
    list_filter = ('is_accepted', 'created_at')
    search_fields = ('post__title', 'user__username', 'content')
