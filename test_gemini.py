import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY', '')

models_to_test = [
    "gemini-2.0-flash",
    "gemini-1.5-flash-latest",
    "gemini-pro",
]

for model in models_to_test:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    payload = {
        "contents": [{
            "parts": [{
                "text": "Hello Gemini! Confirm connection."
            }]
        }]
    }

    try:
        res = requests.post(url, json=payload, timeout=8)
        print(f"Model {model} Status Code: {res.status_code}")
        if res.status_code == 200:
            resp_json = res.json()
            reply = resp_json['candidates'][0]['content']['parts'][0]['text']
            print(f"[SUCCESS] {model} Reply: {reply[:100]}")
            break
        else:
            print(f"Error {model}: {res.text[:150]}")
    except Exception as e:
        print(f"Error {model}: {e}")
