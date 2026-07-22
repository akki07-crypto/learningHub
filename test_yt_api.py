import os
import requests
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

api_key = os.getenv('YOUTUBE_API_KEY', '')
print(f"Testing YouTube API Key: {api_key}")

url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q=Python+Programming&type=video&videoEmbeddable=true&maxResults=5&key={api_key}"
res = requests.get(url)
print(f"Status Code: {res.status_code}")
print("Response JSON:")
print(res.text[:800])
