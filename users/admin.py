from django.contrib import admin
from .models import UserProfile, Badge, UserBadge, Notification, SkillOffer, SwapRequest, DirectMessage, Certificate

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'points', 'streak_count', 'referral_code', 'get_level', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone_number', 'referral_code')
    list_filter = ('streak_count', 'created_at')

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'slug', 'points_threshold')
    search_fields = ('name', 'slug')

@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ('user', 'badge', 'unlocked_at')
    search_fields = ('user__username', 'badge__name')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username', 'title', 'message')

@admin.register(SkillOffer)
class SkillOfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'offered_skill', 'wanted_skill', 'experience_level', 'created_at')
    search_fields = ('title', 'offered_skill', 'wanted_skill', 'user__username')
    list_filter = ('experience_level', 'created_at')

@admin.register(SwapRequest)
class SwapRequestAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'skill_offer', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('sender__username', 'receiver__username', 'skill_offer__title')

@admin.register(DirectMessage)
class DirectMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'content', 'is_read', 'timestamp')
    list_filter = ('is_read', 'timestamp')
    search_fields = ('sender__username', 'receiver__username', 'content')

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('certificate_code', 'user', 'title', 'issued_date')
    search_fields = ('certificate_code', 'user__username', 'title')
