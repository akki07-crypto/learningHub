import os
import requests
from django.conf import settings
from .models import Course, Category

MOCK_COURSES = [
    {
        'youtube_id': 'rfscVS0vtbw',
        'title': 'Python Full Course for Beginners [2026 Tutorial]',
        'description': 'Master Python programming from scratch. Learn syntax, OOP, data structures, and build real-world Python projects.',
        'channel_title': 'Programming with Mosh',
        'thumbnail_url': 'https://img.youtube.com/vi/rfscVS0vtbw/maxresdefault.jpg',
        'views': 4500000,
        'difficulty': 'Beginner',
        'category': 'Python'
    },
    {
        'youtube_id': 'F5mRW0jo-U4',
        'title': 'Django 5.0 Full Course - Build Full Stack Web Apps',
        'description': 'Comprehensive Django 5.0 framework tutorial. Build scalable web applications with ORM, authentication, admin panel, and REST APIs.',
        'channel_title': 'Programming with Mosh',
        'thumbnail_url': 'https://img.youtube.com/vi/F5mRW0jo-U4/maxresdefault.jpg',
        'views': 2100000,
        'difficulty': 'Intermediate',
        'category': 'Django'
    },
    {
        'youtube_id': 'W6NZfCO5SIk',
        'title': 'JavaScript Masterclass - Modern ES6+ & DOM Manipulation',
        'description': 'Learn modern JavaScript from scratch. Master variables, functions, async/await, promises, DOM manipulation, and ES6 features.',
        'channel_title': 'Programming with Mosh',
        'thumbnail_url': 'https://img.youtube.com/vi/W6NZfCO5SIk/maxresdefault.jpg',
        'views': 3800000,
        'difficulty': 'Beginner',
        'category': 'Web Development'
    },
    {
        'youtube_id': 'bMknfKXIFA8',
        'title': 'React JS Full Course 2026 - Build 4 Modern Apps',
        'description': 'Build responsive modern user interfaces with React 18, Hooks, Context API, state management, and Component Architecture.',
        'channel_title': 'freeCodeCamp.org',
        'thumbnail_url': 'https://img.youtube.com/vi/bMknfKXIFA8/maxresdefault.jpg',
        'views': 3100000,
        'difficulty': 'Intermediate',
        'category': 'Web Development'
    },
    {
        'youtube_id': 'HXV3zeQKqGY',
        'title': 'MySQL Database Design & SQL Query Optimization',
        'description': 'Learn SQL from basics to advanced index optimizations, joins, subqueries, and database schema architecture.',
        'channel_title': 'freeCodeCamp.org',
        'thumbnail_url': 'https://img.youtube.com/vi/HXV3zeQKqGY/maxresdefault.jpg',
        'views': 2800000,
        'difficulty': 'Beginner',
        'category': 'Database'
    },
    {
        'youtube_id': 'mU6anWqZJcc',
        'title': 'HTML & CSS Full Course - Build Responsive Websites',
        'description': 'Learn HTML5 & CSS3 layout design, Flexbox, Grid, animations, and responsive web design for beginners.',
        'channel_title': 'SuperSimpleDev',
        'thumbnail_url': 'https://img.youtube.com/vi/mU6anWqZJcc/maxresdefault.jpg',
        'views': 6400000,
        'difficulty': 'Beginner',
        'category': 'Web Development'
    },
    {
        'youtube_id': '8hly31xKLI0',
        'title': 'Data Structures & Algorithms (DSA) Course',
        'description': 'Master Big-O notation, Arrays, Linked Lists, Trees, Graphs, Sorting Algorithms, and Dynamic Programming for technical interviews.',
        'channel_title': 'freeCodeCamp.org',
        'thumbnail_url': 'https://img.youtube.com/vi/8hly31xKLI0/maxresdefault.jpg',
        'views': 2900000,
        'difficulty': 'Advanced',
        'category': 'Computer Science'
    },
    {
        'youtube_id': 'RGOj5yH7evk',
        'title': 'Git & GitHub Tutorial for Beginners',
        'description': 'Master Git version control, branching, merging, pull requests, merge conflict resolution, and GitHub collaboration workflow.',
        'channel_title': 'Programming with Mosh',
        'thumbnail_url': 'https://img.youtube.com/vi/RGOj5yH7evk/maxresdefault.jpg',
        'views': 4100000,
        'difficulty': 'Beginner',
        'category': 'DevOps'
    },
    {
        'youtube_id': 'fqMOX6JJhGo',
        'title': 'Docker & Kubernetes DevOps Crash Course',
        'description': 'Learn containerization with Docker, Docker Compose, Images, Containers, and Kubernetes deployment architecture.',
        'channel_title': 'TechWorld with Nana',
        'thumbnail_url': 'https://img.youtube.com/vi/fqMOX6JJhGo/maxresdefault.jpg',
        'views': 3600000,
        'difficulty': 'Intermediate',
        'category': 'DevOps'
    },
    {
        'youtube_id': 'i_LwzRVP7bg',
        'title': 'Machine Learning & AI Course with Python & Scikit-Learn',
        'description': 'Introduction to Machine Learning, Regression, Classification, Model Training, Neural Networks, and Data Analysis.',
        'channel_title': 'freeCodeCamp.org',
        'thumbnail_url': 'https://img.youtube.com/vi/i_LwzRVP7bg/maxresdefault.jpg',
        'views': 2700000,
        'difficulty': 'Advanced',
        'category': 'Artificial Intelligence'
    }
]

def fetch_and_sync_youtube_courses(query="Python Programming"):
    api_key = os.getenv('YOUTUBE_API_KEY', '')

    if api_key and api_key != 'your_youtube_api_key_here':
        try:
            url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&videoEmbeddable=true&maxResults=10&key={api_key}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                for item in data.get('items', []):
                    yt_id = item['id']['videoId']
                    snippet = item['snippet']
                    cat_name = query.split()[0].title()
                    category, _ = Category.objects.get_or_create(name=cat_name, defaults={'slug': cat_name.lower()})

                    Course.objects.get_or_create(
                        youtube_id=yt_id,
                        defaults={
                            'title': snippet['title'],
                            'description': snippet['description'],
                            'channel_title': snippet['channelTitle'],
                            'thumbnail_url': snippet['thumbnails']['high']['url'] if 'high' in snippet['thumbnails'] else snippet['thumbnails']['default']['url'],
                            'category': category,
                            'difficulty': 'Intermediate'
                        }
                    )
        except Exception as e:
            print(f"YouTube API Exception (fallback active): {e}")

    # Ensure Mock Data is populated in DB if DB is empty
    seed_mock_courses()

def seed_mock_courses():
    for item in MOCK_COURSES:
        category, _ = Category.objects.get_or_create(
            name=item['category'],
            defaults={'slug': item['category'].lower().replace(' ', '-')}
        )
        Course.objects.get_or_create(
            youtube_id=item['youtube_id'],
            defaults={
                'title': item['title'],
                'description': item['description'],
                'channel_title': item['channel_title'],
                'thumbnail_url': item['thumbnail_url'],
                'views': item['views'],
                'difficulty': item['difficulty'],
                'category': category
            }
        )
