import os
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def gemini_chat_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST request required'}, status=400)

    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        if not user_message:
            return JsonResponse({'reply': 'Please ask a valid question.'})

        api_key = os.getenv('GEMINI_API_KEY', '').strip()

        if api_key and api_key != 'your_gemini_api_key_here':
            try:
                # Call Google Gemini 2.0 Flash API with Multi-lingual Hinglish & English System Prompt
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
                system_instruction = (
                    "You are LearnBot, an enthusiastic, highly intelligent AI study tutor and navigator for the LearnHub platform. "
                    "You answer questions in BOTH English and Hinglish (Hindi written in Roman script) depending on the user's input language. "
                    "Features of LearnHub: Peer Skill Exchange (Python for React, etc.), YouTube Video Courses with reviews & ratings, "
                    "1-on-1 Mentorship booking with Jitsi video call, Gamification XP points & Badges, Daily Login Streaks, Printable PDF Certificates, "
                    "Live Student Doubt Broadcasts (+50 XP solution verification), and Direct 1-on-1 Chat with live user search bar. "
                    "Provide helpful, structured, and friendly answers with emojis."
                )
                payload = {
                    "contents": [{
                        "parts": [{
                            "text": f"{system_instruction}\n\nUser Question: {user_message}"
                        }]
                    }]
                }
                res = requests.post(url, json=payload, timeout=8)
                if res.status_code == 200:
                    resp_json = res.json()
                    candidates = resp_json.get('candidates', [])
                    if candidates:
                        bot_reply = candidates[0]['content']['parts'][0]['text']
                        return JsonResponse({'reply': bot_reply})
            except Exception as e:
                print(f"Gemini API exception: {e}")

        # Intelligent Multi-lingual Fallback AI Assistant Logic
        lower_msg = user_message.lower()
        
        # 1. Skill Swap Questions
        if any(w in lower_msg for w in ['skill swap', 'swap', 'exchange', 'kaise kare', 'kaise karein', 'collaborate']):
            reply = (
                "🤝 **Skill Swap & Peer Matchmaking Guide / गाइड**:\n\n"
                "• **English**: Go to **Skill Swap** page, post a skill you offer (e.g. Python) in exchange for what you want (e.g. React). Click 'Send Swap Request' on matching offers!\n"
                "• **Hinglish**: **Skill Swap** पेज पर जाएं, अपनी पसंदीदा स्किल (जैसे Python) ऑफर करें और जो सीखना चाहते हैं (जैसे UI/UX) उसे लिखें। ऑफर पोस्ट करने पर **+15 XP** मिलेंगे!"
            )
        # 2. Mentorship & Video Call Questions
        elif any(w in lower_msg for w in ['mentor', 'booking', 'jitsi', 'video call', 'appointment', 'schedule']):
            reply = (
                "📅 **1-on-1 Mentorship & Jitsi Call / मेंटॉरशिप गाइड**:\n\n"
                "• **English**: Visit **Mentorship** page, select a student mentor by qualification/degree, choose a mode (Career Roadmap, Mock Interview, Code Audit), and lock date & time (+25 XP)!\n"
                "• **Hinglish**: **Mentorship** पेज पर जाकर मेंटर चुनें, मोड (Roadmap/Interview/Code Audit) सेलेक्ट करें। बुक बटन दबाते ही **Live Jitsi Video Call Room** मिल जाएगा!"
            )
        # 3. Live Doubt Broadcast & Verification Questions
        elif any(w in lower_msg for w in ['doubt', 'error', 'bug', 'solve', 'broadcast', 'verify']):
            reply = (
                "🚨 **Live Student Doubt Broadcast / लाइव डाउट सिस्टम**:\n\n"
                "• **English**: Click '🚨 Raise Live Doubt' on **Forum** page. An instant notification is broadcasted to ALL registered students! Helper students can solve it via Video Call or Chat.\n"
                "• **Verification Bonus**: Marking an answer as verified awards **+50 XP** & unlocks the **Verified Solution Master 🏅** Badge!"
            )
        # 4. Direct Chat & User Search
        elif any(w in lower_msg for w in ['chat', 'message', 'inbox', 'search user', 'find student']):
            reply = (
                "💬 **Direct 1-on-1 Student Chat & Search / डायरेक्ट चैट**:\n\n"
                "• **English**: Go to **Messages** page. Use the live search bar (`🔍 Search username, skills, degree...`) to find any student and start chatting directly!\n"
                "• **Hinglish**: **Messages** पेज खोलें और सर्च बार में किसी भी छात्र का Username, Degree या Skill टाइप करके 1-on-1 चैट शुरू करें!"
            )
        # 5. XP Points, Badges & Leaderboard Ranks
        elif any(w in lower_msg for w in ['point', 'xp', 'badge', 'streak', 'rank', 'leaderboard', 'level']):
            reply = (
                "🏆 **XP Points, Badges & Login Streaks / गेमिंग रिवॉर्ड्स**:\n\n"
                "• **Earn XP**: +100 XP (Signup), +15 XP (Doubt/Offer), +25 XP (Mentorship), +30 XP (Swap Accept), +50 XP (Verified Solution/Referral).\n"
                "• **Daily Streak**: Daily login rewards you with 🔥 streak days! Check your rank on the **Ranks Leaderboard**."
            )
        # 6. Certificates & PDF Proof
        elif any(w in lower_msg for w in ['certificate', 'pdf', 'proof', 'download', 'print']):
            reply = (
                "📜 **Printable PDF Certificate / ऑफिशियल सर्टिफिकेट**:\n\n"
                "• Complete any video course or peer skill swap to generate your official signed **LearnHub PDF Certificate** in your Dashboard!"
            )
        # 7. Referral Link & Earn Points
        elif any(w in lower_msg for w in ['refer', 'referral', 'invite', 'friend', 'earn']):
            reply = (
                "🎁 **Referral Bonus (+50 XP) / दोस्तों को इनवाइट करें**:\n\n"
                "• **English**: Copy your unique referral link from your **Dashboard**. Share it with friends! Earn **+50 XP** for every friend who signs up.\n"
                "• **Hinglish**: डैशबोर्ड से अपना यूनिक रेफरल लिंक कॉपी करके दोस्तों को भेजें। नए दोस्त के जुड़ने पर **+50 XP Points** मिलेंगे!"
            )
        # 8. Admin Panel Credentials
        elif any(w in lower_msg for w in ['admin', 'panel', 'login admin', 'superuser', 'password']):
            reply = (
                "🔐 **Admin Panel Login Credentials / एडमिन पैनल**:\n\n"
                "• **Admin URL**: http://127.0.0.1:8000/admin/\n"
                "• **Username**: `admin` | **Password**: `AdminPassword123`\n"
                "• Manage all MySQL database records, users, courses, and bookings as Administrator!"
            )
        # 9. Python, Django, React, MySQL Courses
        elif any(w in lower_msg for w in ['python', 'django', 'react', 'mysql', 'course', 'video', 'tutorial']):
            reply = (
                "🐍 **YouTube Data API Video Courses / वीडियो कोर्सेज**:\n\n"
                "• We have 10+ verified courses on Python 3, Django 5, React JS, MySQL, DSA, Git, and Docker! Search our **Courses** page to watch free tutorials with `youtube-nocookie.com` player."
            )
        # 10. General Greetings
        elif any(w in lower_msg for w in ['hello', 'hi', 'hey', 'namaste', 'kaise ho', 'who are you']):
            reply = (
                "👋 **Namaste & Welcome to LearnHub!**\n\n"
                "I am your **Gemini AI Tutor**. Ask me anything about Skill Swaps, YouTube Courses, Mentorship Calls, Live Doubts, or Coding!"
            )
        else:
            reply = (
                f"🤖 **LearnBot AI**: Thanks for asking: *'{user_message}'*!\n\n"
                "You can ask me about: **Skill Swaps**, **Mentorship Video Calls**, **Live Doubts (+50 XP)**, **Direct Chat Search**, **Course Certificates**, or **Leaderboards** in English & Hindi!"
            )

        return JsonResponse({'reply': reply})

    except Exception as e:
        return JsonResponse({'reply': f'Sorry, an error occurred: {str(e)}'}, status=500)
