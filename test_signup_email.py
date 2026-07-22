import os
import requests
import datetime
from dotenv import load_dotenv

load_dotenv()

admin_email = os.getenv('ADMIN_EMAIL', 'akakash94655@gmail.com')
endpoint_id = os.getenv('FORMSPREE_ENDPOINT_ID', 'mbdnkpdv')

print(f"Sending test signup notification to Formspree endpoint '{endpoint_id}'...")

url = f"https://formspree.io/f/{endpoint_id}"
payload = {
    'subject': "🎉 New User Signup Alert: test_student_99",
    'name': "test_student_99",
    'email': admin_email,
    'message': f"A new student registered on LearnHub!\nUsername: test_student_99\nDate: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nMySQL Database: elearn_db"
}

try:
    res = requests.post(url, json=payload, timeout=5)
    print(f"Formspree Status Code: {res.status_code}")
    print(f"Formspree Response Text: {res.text[:200]}")
except Exception as e:
    print(f"Error: {e}")
