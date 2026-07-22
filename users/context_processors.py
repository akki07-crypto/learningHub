from .models import Notification

def user_notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user)
        unread_count = notifications.filter(is_read=False).count()
        return {
            'nav_notifications': notifications[:5],
            'unread_notifications_count': unread_count,
        }
    return {
        'nav_notifications': [],
        'unread_notifications_count': 0,
    }
