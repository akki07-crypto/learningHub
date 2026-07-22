from django.urls import path
from .views import course_list_view, course_detail_view, toggle_course_bookmark

urlpatterns = [
    path('', course_list_view, name='course_list'),
    path('<int:course_id>/', course_detail_view, name='course_detail'),
    path('bookmark/<int:course_id>/', toggle_course_bookmark, name='toggle_course_bookmark'),
]
