from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from .models import ForumPost, ForumAnswer
from users.models import Notification, UserProfile, Badge, UserBadge
import uuid

def forum_index_view(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    posts = ForumPost.objects.all()

    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))
    if category:
        posts = posts.filter(category=category)

    if request.method == 'POST' and request.user.is_authenticated:
        title = request.POST.get('title')
        content = request.POST.get('content')
        cat = request.POST.get('category', 'General Tech')

        if title and content:
            # Generate unique video call room name for this doubt safely
            room_code = "DOUBT-" + uuid.uuid4().hex[:8].upper()
            
            post = ForumPost.objects.create(
                user=request.user,
                title=title,
                content=content,
                category=cat,
            )
            
            # 🔔 BROADCAST NOTIFICATION TO ALL OTHER REGISTERED STUDENTS!
            all_other_students = User.objects.exclude(id=request.user.id)
            notifications_to_create = [
                Notification(
                    user=student,
                    title="🚨 Live Student Doubt Raised!",
                    message=f"{request.user.username} raised a doubt: '{title[:45]}...'. Click to solve via Video Call or Chat!",
                    link=f"/forum/{post.id}/"
                ) for student in all_other_students
            ]
            if notifications_to_create:
                Notification.objects.bulk_create(notifications_to_create)

            # Award +15 XP for raising a question
            profile, _ = UserProfile.objects.get_or_create(user=request.user)
            profile.points += 15
            profile.save()

            messages.success(request, f"Doubt raised successfully & broadcasted to {len(all_other_students)} students! (+15 XP)")
            return redirect('forum_detail', post_id=post.id)

    context = {
        'posts': posts,
        'selected_query': query,
        'selected_category': category,
    }
    return render(request, 'forum/index.html', context)

def forum_detail_view(request, post_id):
    post = get_object_or_404(ForumPost, id=post_id)
    post.views += 1
    post.save()

    # Generate Jitsi room name for this post
    jitsi_room = f"LearnHub-DoubtRoom-{post.id}"

    if request.method == 'POST' and request.user.is_authenticated:
        content = request.POST.get('content')
        if content:
            ForumAnswer.objects.create(
                post=post,
                user=request.user,
                content=content
            )
            
            # Reward Helper Student +20 XP
            helper_profile, _ = UserProfile.objects.get_or_create(user=request.user)
            helper_profile.points += 20
            helper_profile.save()

            # Unlock 'Peer Solver 🦸' Badge
            solver_badge, _ = Badge.objects.get_or_create(
                slug='peer-solver',
                defaults={
                    'name': 'Peer Solver 🦸',
                    'description': 'Helped solve a fellow student doubt',
                    'icon': '🦸',
                    'points_threshold': 120
                }
            )
            UserBadge.objects.get_or_create(user=request.user, badge=solver_badge)

            # Notify the doubt author
            if post.user != request.user:
                Notification.objects.create(
                    user=post.user,
                    title="💡 New Answer on your Doubt!",
                    message=f"{request.user.username} answered your doubt: '{post.title[:40]}...'",
                    link=f"/forum/{post.id}/"
                )

            messages.success(request, "Your solution has been posted! (+20 XP Points)")
            return redirect('forum_detail', post_id=post.id)

    answers = post.answers.all()
    context = {
        'post': post,
        'answers': answers,
        'jitsi_room': jitsi_room,
    }
    return render(request, 'forum/detail.html', context)

@login_required
def accept_answer(request, answer_id):
    answer = get_object_or_404(ForumAnswer, id=answer_id)
    post = answer.post

    # Verify that ONLY the doubt author can verify/accept the answer!
    if post.user == request.user:
        # Reset any previously accepted answer on this post
        post.answers.update(is_accepted=False)
        
        answer.is_accepted = True
        answer.save()
        
        post.is_solved = True
        post.save()

        # Award BIG +50 XP Reward to the Helper Student!
        helper_profile, _ = UserProfile.objects.get_or_create(user=answer.user)
        helper_profile.points += 50
        helper_profile.save()

        # Unlock 'Verified Solution Master 🏅' Badge
        verified_badge, _ = Badge.objects.get_or_create(
            slug='verified-master',
            defaults={
                'name': 'Verified Solution Master 🏅',
                'description': 'Answer was verified as correct solution by student author',
                'icon': '🏅',
                'points_threshold': 200
            }
        )
        UserBadge.objects.get_or_create(user=answer.user, badge=verified_badge)

        # Send Notification to Helper Student
        if answer.user != request.user:
            Notification.objects.create(
                user=answer.user,
                title="🎉 Solution Verified & Accepted!",
                message=f"{request.user.username} verified your answer as correct on '{post.title[:40]}...'. You earned +50 XP Points!",
                link=f"/forum/{post.id}/"
            )

        messages.success(request, f"Answer verified as correct solution! {answer.user.username} rewarded +50 XP Points 🌟")
    
    return redirect('forum_detail', post_id=post.id)

@login_required
def upvote_post(request, post_id):
    post = get_object_or_404(ForumPost, id=post_id)
    if request.user in post.upvotes.all():
        post.upvotes.remove(request.user)
        upvoted = False
    else:
        post.upvotes.add(request.user)
        upvoted = True
    return JsonResponse({'upvoted': upvoted, 'count': post.upvotes.count()})
