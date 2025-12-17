import json
import os
from datetime import datetime

# In-memory database using JSON
DATABASE_FILE = os.path.join(os.path.dirname(__file__), 'data.json')

# Initialize database with default data
DEFAULT_DATA = {
    "users": [
        {
            "id": 1,
            "username": "admin",
            "email": "admin@portfolio.com",
            "password_hash": "admin123",
            "is_admin": True
        }
    ],
    "projects": [
        {
            "id": 1,
            "title": "Portfolio Website",
            "description": "Personal portfolio website",
            "long_description": "A modern portfolio website built with Flask and React",
            "image_url": "/images/portfolio.jpg",
            "demo_url": "https://example.com",
            "github_url": "https://github.com/example/portfolio",
            "category_id": 1,
            "tags": "web,flask,react",
            "views": 150,
            "likes": 25,
            "featured": True,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
    ],
    "skills": [
        {"id": 1, "name": "Python", "level": 90, "category": "Backend"},
        {"id": 2, "name": "JavaScript", "level": 85, "category": "Frontend"},
        {"id": 3, "name": "React", "level": 80, "category": "Frontend"},
        {"id": 4, "name": "Flask", "level": 90, "category": "Backend"}
    ],
    "experiences": [
        {
            "id": 1,
            "title": "Senior Developer",
            "company": "Tech Company",
            "description": "Led development team",
            "start_date": "2020-01-01",
            "end_date": "2023-12-31",
            "is_current": False
        }
    ],
    "articles": [
        {
            "id": 1,
            "title": "Getting Started with Flask",
            "content": "Learn Flask basics",
            "published": True,
            "created_at": datetime.now().isoformat()
        }
    ]
}

def load_db():
    """Load database from JSON file"""
    if os.path.exists(DATABASE_FILE):
        try:
            with open(DATABASE_FILE, 'r') as f:
                return json.load(f)
        except:
            return DEFAULT_DATA
    return DEFAULT_DATA

def save_db(data):
    """Save database to JSON file"""
    os.makedirs(os.path.dirname(DATABASE_FILE) or '.', exist_ok=True)
    with open(DATABASE_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# Initialize database
if not os.path.exists(DATABASE_FILE):
    save_db(DEFAULT_DATA)

def query_one(sql, params=None):
    """Simulate database query - return one result"""
    db = load_db()
    
    # Parse simple SQL queries
    if 'FROM users WHERE' in sql and 'username' in sql:
        username = params[0] if params else None
        for user in db['users']:
            if user['username'] == username:
                return user
        return None
    
    elif 'FROM users WHERE id' in sql:
        user_id = params[0] if params else None
        for user in db['users']:
            if user['id'] == user_id:
                return user
        return None
    
    elif 'FROM projects' in sql:
        if db['projects']:
            return {'count': len(db['projects'])}
        return {'count': 0}
    
    elif 'FROM skills' in sql:
        if db['skills']:
            return {'count': len(db['skills'])}
        return {'count': 0}
    
    elif 'FROM experiences' in sql:
        if db['experiences']:
            return {'count': len(db['experiences'])}
        return {'count': 0}
    
    elif 'FROM articles' in sql and 'published' in sql:
        published_count = len([a for a in db['articles'] if a.get('published')])
        return {'count': published_count}
    
    return None

def query_all(sql, params=None):
    """Simulate database query - return all results"""
    db = load_db()
    
    if 'FROM projects' in sql:
        return db['projects']
    elif 'FROM skills' in sql:
        return db['skills']
    elif 'FROM experiences' in sql:
        return db['experiences']
    elif 'FROM articles' in sql:
        return [a for a in db['articles'] if a.get('published', True)]
    
    return []

def execute(sql, params=None, fetch=False):
    """Execute insert/update/delete"""
    db = load_db()
    
    # Placeholder - for JSON database, writes are simple
    # This would need custom logic for actual inserts/updates
    save_db(db)
    return None
