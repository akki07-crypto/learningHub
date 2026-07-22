from django.db import models
from django.contrib.auth.models import User

class ForumPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forum_posts')
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.CharField(max_length=100, default='General Tech')
    is_solved = models.BooleanField(default=False)
    upvotes = models.ManyToManyField(User, related_name='upvoted_posts', blank=True)
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def upvote_count(self):
        return self.upvotes.count()

    def answer_count(self):
        return self.answers.count()

    def __str__(self):
        return self.title

class ForumAnswer(models.Model):
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='answers')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forum_answers')
    content = models.TextField()
    is_accepted = models.BooleanField(default=False)
    upvotes = models.ManyToManyField(User, related_name='upvoted_answers', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_accepted', '-created_at']

    def upvote_count(self):
        return self.upvotes.count()

    def __str__(self):
        return f"Answer by {self.user.username} on {self.post.title}"
