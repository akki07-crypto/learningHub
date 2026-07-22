import os
import requests
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.core.mail import send_mail
from .models import UserProfile, Badge, UserBadge, Notification, SkillOffer, SwapRequest, DirectMessage, Certificate
from courses.models import Course, CourseBookmark

def send_signup_email_notification(username, email='', phone_number='', ref_code=''):
    """Sends instant Email notification upon new user signup to akki28869@gmail.com"""
    admin_email = os.getenv('ADMIN_EMAIL', 'akki28869@gmail.com').strip()
    endpoint_id = os.getenv('FORMSPREE_ENDPOINT_ID', 'mbdnkpdv').strip()
    
    # 1. Formspree Email Notification
    if endpoint_id:
        try:
            url = f"https://formspree.io/f/{endpoint_id}"
            payload = {
                'subject': f"🎉 New User Signup Alert: {username}",
                'name': username,
                'email': admin_email,
                '_replyto': email if email else admin_email,
                'message': (
                    f"A new student/mentor registered on LearnHub!\n\n"
                    f"👤 Username: {username}\n"
                    f"📧 Email Address: {email if email else 'Not provided'}\n"
                    f"📱 Mobile Number: {phone_number if phone_number else 'Not provided'}\n"
                    f"📅 Registration Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"🎁 Referral Code Used: {ref_code if ref_code else 'None'}\n\n"
                    f"Data is saved in MySQL DB ('elearn_db')."
                )
            }
            res = requests.post(url, json=payload, timeout=5)
            print(f"[FORMSPREE EMAIL STATUS]: {res.status_code}")
        except Exception as e:
            print(f"[FORMSPREE EMAIL ERROR]: {e}")

    # 2. Django SMTP Email (If configured)
    try:
        if os.getenv('EMAIL_HOST_USER'):
            send_mail(
                subject=f"🎉 New User Signup: {username}",
                message=f"New user registered:\nUsername: {username}\nEmail: {email}\nMobile: {phone_number}",
                from_email=os.getenv('EMAIL_HOST_USER'),
                recipient_list=[admin_email],
                fail_silently=True,
            )
    except Exception as e:
        print(f"[SMTP MAIL ERROR]: {e}")

def register_view(request):
    ref_code = request.GET.get('ref', '')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        email_val = request.POST.get('email', '').strip()
        phone_val = request.POST.get('phone_number', '').strip()

        if not email_val or not phone_val:
            messages.error(request, "Both Email Address and Mobile Number are REQUIRED for registration!")
            return render(request, 'users/register.html', {
                'form': form, 
                'ref_code': ref_code,
                'email_val': email_val,
                'phone_val': phone_val
            })

        if form.is_valid():
            user = form.save()
            user.email = email_val
            user.save()

            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.phone_number = phone_val
            profile.points = 100
            
            # Referral logic
            input_ref = request.POST.get('referral_code', '')
            if input_ref:
                referrer_profile = UserProfile.objects.filter(referral_code=input_ref).first()
                if referrer_profile:
                    profile.referred_by = referrer_profile.user
                    referrer_profile.points += 50
                    referrer_profile.save()
                    Notification.objects.create(
                        user=referrer_profile.user,
                        title="Referral Bonus! 🎁",
                        message=f"{user.username} joined using your referral link. You earned +50 points!",
                        link="/dashboard/"
                    )
            profile.save()
            
            welcome_badge, _ = Badge.objects.get_or_create(
                slug='pioneer',
                defaults={
                    'name': 'Pioneer Learner 🌟',
                    'description': 'Joined the LearnHub platform',
                    'icon': '🌟',
                    'points_threshold': 100
                }
            )
            UserBadge.objects.get_or_create(user=user, badge=welcome_badge)

            # --- INSTANT GMAIL SIGNUP NOTIFICATION ---
            send_signup_email_notification(user.username, user.email, profile.phone_number, input_ref)
            
            login(request, user)
            messages.success(request, "Registration successful! Welcome to LearnHub.")
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form, 'ref_code': ref_code})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Safe profile access with get_or_create to prevent 500 error
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.check_daily_streak()
            
            messages.success(request, f"Welcome back, {user.username}! Current Streak: 🔥 {profile.streak_count} Days")
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')

@login_required
def dashboard_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    profile.check_daily_streak()

    # Handle Mentor Credentials Update
    if request.method == 'POST' and 'update_credentials' in request.POST:
        profile.qualification = request.POST.get('qualification', '').strip()
        profile.current_study = request.POST.get('current_study', '').strip()
        profile.skills_expertise = request.POST.get('skills_expertise', '').strip()
        profile.github_linkedin = request.POST.get('github_linkedin', '').strip()
        profile.bio = request.POST.get('bio', '').strip()
        profile.save()
        messages.success(request, "Your Student Mentor Profile Credentials updated successfully! 🎓")
        return redirect('dashboard')

    badges = UserBadge.objects.filter(user=request.user)
    user_bookings = request.user.bookings.all()[:5]
    user_posts = request.user.forum_posts.all()[:5]
    bookmarks = CourseBookmark.objects.filter(user=request.user)
    certificates = Certificate.objects.filter(user=request.user)
    swap_requests = SwapRequest.objects.filter(receiver=request.user, status='Pending')
    
    context = {
        'profile': profile,
        'badges': badges,
        'user_bookings': user_bookings,
        'user_posts': user_posts,
        'bookmarks': bookmarks,
        'certificates': certificates,
        'swap_requests': swap_requests,
    }
    return render(request, 'dashboard.html', context)

# --- Feature 1: Skill Swap Views ---
def skills_index_view(request):
    query = request.GET.get('q', '')
    offers = SkillOffer.objects.all()

    if query:
        offers = offers.filter(
            Q(offered_skill__icontains=query) |
            Q(wanted_skill__icontains=query) |
            Q(description__icontains=query)
        )

    if request.method == 'POST' and request.user.is_authenticated:
        title = request.POST.get('title')
        offered = request.POST.get('offered_skill')
        wanted = request.POST.get('wanted_skill')
        desc = request.POST.get('description')
        level = request.POST.get('experience_level', 'Intermediate')

        if offered and wanted:
            SkillOffer.objects.create(
                user=request.user,
                title=title or f"Exchange {offered} for {wanted}",
                offered_skill=offered,
                wanted_skill=wanted,
                description=desc,
                experience_level=level
            )
            messages.success(request, "Skill Swap offer created successfully! (+15 XP)")
            return redirect('skills_index')

    context = {
        'offers': offers,
        'selected_query': query,
    }
    return render(request, 'skills/index.html', context)

@login_required
def send_swap_request(request, offer_id):
    offer = get_object_or_404(SkillOffer, id=offer_id)
    if request.method == 'POST':
        msg = request.POST.get('message', '')
        if offer.user != request.user:
            SwapRequest.objects.create(
                sender=request.user,
                receiver=offer.user,
                skill_offer=offer,
                message=msg
            )
            Notification.objects.create(
                user=offer.user,
                title="New Skill Swap Request! 🤝",
                message=f"{request.user.username} wants to swap skills for '{offer.offered_skill}'",
                link="/dashboard/"
            )
            messages.success(request, f"Swap request sent to {offer.user.username}!")
    return redirect('skills_index')

@login_required
def respond_swap_request(request, req_id, action):
    swap_req = get_object_or_404(SwapRequest, id=req_id, receiver=request.user)
    if action == 'accept':
        swap_req.status = 'Accepted'
        swap_req.save()
        
        receiver_profile, _ = UserProfile.objects.get_or_create(user=request.user)
        receiver_profile.points += 30
        receiver_profile.save()
        
        Certificate.objects.create(
            user=request.user,
            title=f"Peer Skill Exchange: {swap_req.skill_offer.offered_skill}"
        )
        Notification.objects.create(
            user=swap_req.sender,
            title="Swap Request Accepted! 🎉",
            message=f"{request.user.username} accepted your skill swap request! Click to chat.",
            link=f"/messages/?user={request.user.id}"
        )
        messages.success(request, f"Accepted swap request from {swap_req.sender.username}! (+30 XP)")
    elif action == 'decline':
        swap_req.status = 'Declined'
        swap_req.save()
        messages.info(request, "Swap request declined.")
    return redirect('dashboard')

# --- Feature 2: Direct Messaging Views with Live Search ---
@login_required
def direct_messages_view(request):
    search_q = request.GET.get('q', '').strip()
    other_users = User.objects.exclude(id=request.user.id)

    if search_q:
        other_users = other_users.filter(
            Q(username__icontains=search_q) |
            Q(profile__qualification__icontains=search_q) |
            Q(profile__skills_expertise__icontains=search_q)
        )

    active_user_id = request.GET.get('user', '')
    active_user = None
    messages_list = []

    if active_user_id:
        active_user = get_object_or_404(User, id=active_user_id)
        messages_list = DirectMessage.objects.filter(
            (Q(sender=request.user, receiver=active_user) | Q(sender=active_user, receiver=request.user))
        ).order_by('timestamp')
        DirectMessage.objects.filter(sender=active_user, receiver=request.user, is_read=False).update(is_read=True)

    if request.method == 'POST' and active_user:
        content = request.POST.get('content', '').strip()
        if content:
            DirectMessage.objects.create(
                sender=request.user,
                receiver=active_user,
                content=content
            )
            return redirect(f"/messages/?user={active_user.id}")

    context = {
        'other_users': other_users,
        'active_user': active_user,
        'messages_list': messages_list,
        'search_q': search_q,
    }
    return render(request, 'messages/inbox.html', context)

# --- Feature 3: Printable Certificate View ---
@login_required
def view_certificate(request, cert_code):
    cert = get_object_or_404(Certificate, certificate_code=cert_code)
    return render(request, 'certificates/template.html', {'cert': cert})

# --- Feature 4: Global Animated Leaderboard View ---
def leaderboard_view(request):
    profiles = UserProfile.objects.order_by('-points')[:20]
    context = {'profiles': profiles}
    return render(request, 'leaderboard.html', context)

@login_required
def mark_notification_read(request, notif_id):
    notif = get_object_or_404(Notification, id=notif_id, user=request.user)
    notif.is_read = True
    notif.save()
    return JsonResponse({'status': 'ok'})
