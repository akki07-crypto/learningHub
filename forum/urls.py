from django.urls import path
from .views import forum_index_view, forum_detail_view, upvote_post, accept_answer

urlpatterns = [
    path('', forum_index_view, name='forum_index'),
    path('<int:post_id>/', forum_detail_view, name='forum_detail'),
    path('<int:post_id>/upvote/', upvote_post, name='upvote_post'),
    path('answer/<int:answer_id>/accept/', accept_answer, name='accept_answer'),
]
