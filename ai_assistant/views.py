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
                    "and Direct 1-on-1 Chat. Provide helpful, structured, and friendly answers."
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
        
        # Skill Swap Questions (Hindi & English)
        if any(w in lower_msg for w in ['skill swap', 'swap', 'exchange', 'kaise kare', 'kaise karein', 'collaborate']):
            reply = (
                "🤝 **Skill Swap & Peer Matchmaking Guide / गाइड**:\n\n"
                "• **English**: Go to **Skill Swap** page, post a skill you offer (e.g. Python) in exchange for what you want (e.g. React). Click 'Send Swap Request' on matching offers!\n"
                "• **Hinglish**: **Skill Swap** पेज पर जाएं, अपनी पसंदीदा स्किल (जैसे Python) ऑफर करें और जो सीखना चाहते हैं (जैसे UI/UX) उसे लिखें। ऑफर पोस्ट करने पर **+15 XP** मिलेंगे!"
            )
        # Mentorship & Video Call Questions
        elif any(w in lower_msg for w in ['mentor', 'booking', 'jitsi', 'video call', 'appointment', 'schedule']):
            reply = (
                "📅 **Mentorship & Jitsi Video Call / मेंटॉरशिप गाइड**:\n\n"
                "• **English**: Visit **Mentorship** page, choose your topic, preferred date & time slot. Booking generates an instant **Jitsi Meet** video call link (+25 XP)!\n"
                "• **Hinglish**: **Mentorship** पेज पर जाकर डेट और टाइम स्लॉट सेलेक्ट करें। बुक बटन दबाते ही आपको **Live Jitsi Video Call Room** लिंक मिल जाएगी!"
            )
        # XP Points, Badges & Streaks
        elif any(w in lower_msg for w in ['point', 'xp', 'badge', 'streak', 'rank', 'leaderboard', 'level']):
            reply = (
                "🏆 **XP Points, Badges & Login Streaks / गेमिंग सिस्टम**:\n\n"
                "• **Earn XP**: +100 XP (Signup), +15 XP (Skill Offer/Review), +25 XP (Mentorship), +30 XP (Skill Swap Accepted), +50 XP (Course Complete/Referral).\n"
                "• **Daily Streak**: Daily login rewards you with 🔥 streak days! Check your rank on the **Ranks Leaderboard**."
            )
        # Certificates
        elif any(w in lower_msg for w in ['certificate', 'pdf', 'proof', 'download']):
            reply = (
                "📜 **Printable PDF Certificate / सर्टिफिकेट कैसे मिलेगा**:\n\n"
                "• Complete any video course or complete a peer skill exchange session to generate your official signed **LearnHub Certificate** in your Dashboard!"
            )
        # Python & Django
        elif 'python' in lower_msg or 'django' in lower_msg or 'coding' in lower_msg:
            reply = (
                "🐍 **Python & Django Learning / पाइथन और डैंगो**:\n\n"
                "• LearnHub has full YouTube course tutorials on Python 3, Django ORM, and MySQL database setup. Search our **Courses** directory to start watching now!"
            )
        # General Hello / Greetings
        elif any(w in lower_msg for w in ['hello', 'hi', 'hey', 'namaste', 'kaise ho']):
            reply = (
                "👋 **Namaste & Welcome to LearnHub!**\n\n"
                "I am your **Gemini AI Tutor**. Ask me anything about Skill Swaps, YouTube Courses, Mentorship Calls, or Coding!"
            )
        else:
            reply = (
                f"🤖 **LearnBot AI**: Thanks for asking: *'{user_message}'*!\n\n"
                "You can ask me about: **Skill Swaps**, **Mentorship Video Calls**, **Course Certificates**, or **XP Leaderboards** in both English & Hindi!"
            )

        return JsonResponse({'reply': reply})

    except Exception as e:
        return JsonResponse({'reply': f'Sorry, an error occurred: {str(e)}'}, status=500)
