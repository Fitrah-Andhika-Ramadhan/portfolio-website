# Sample data initialization script
import requests
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_URL = os.environ.get('BASE_URL', 'http://localhost')

def add_sample_data():
    print("🚀 Adding sample data to portfolio...")
    
    # 1. Add Skills
    skills = [
        {"name": "PHP Laravel", "level": 88, "icon": "🐘", "category": "Backend"},
        {"name": "Python", "level": 85, "icon": "🐍", "category": "Backend"},
        {"name": "Figma", "level": 90, "icon": "🎨", "category": "Design"},
        {"name": "UI/UX Design", "level": 87, "icon": "✨", "category": "Design"},
        {"name": "JavaScript", "level": 82, "icon": "⚡", "category": "Frontend"},
        {"name": "MySQL", "level": 85, "icon": "💾", "category": "Database"},
        {"name": "PostgreSQL", "level": 80, "icon": "🐘", "category": "Database"},
        {"name": "Docker", "level": 75, "icon": "🐳", "category": "DevOps"},
        {"name": "Git", "level": 88, "icon": "🔧", "category": "Tools"},
        {"name": "RESTful API", "level": 85, "icon": "🔌", "category": "Backend"},
        {"name": "HTML/CSS", "level": 90, "icon": "🌐", "category": "Frontend"},
        {"name": "Bootstrap", "level": 85, "icon": "🅱️", "category": "Frontend"},
    ]
    
    for skill in skills:
        try:
            r = requests.post(f"{BASE_URL}/api/skills", json=skill)
            print(f"✅ Added skill: {skill['name']}")
        except Exception as e:
            print(f"❌ Error adding skill {skill['name']}: {e}")
    
    # 2. Add Experiences
    experiences = [
        {
            "title": "Functional Intern",
            "company": "PT Sisis",
            "location": "Indonesia",
            "start_date": "Nov 2024",
            "end_date": "",
            "current": True,
            "description": "Gaining hands-on experience in software development, working with cross-functional teams, and contributing to various development projects using modern technologies."
        },
        {
            "title": "Software Developer & AI Enthusiast",
            "company": "Freelance",
            "location": "Remote",
            "start_date": "Jan 2024",
            "end_date": "Oct 2024",
            "current": False,
            "description": "Developed web applications using PHP Laravel and Python. Explored AI/ML technologies, built intelligent applications, and implemented machine learning models for various client projects."
        },
        {
            "title": "System Analyst",
            "company": "Tech Solutions",
            "location": "Indonesia",
            "start_date": "Jun 2023",
            "end_date": "Dec 2023",
            "current": False,
            "description": "Analyzed business requirements, designed system architectures, created technical documentation, and worked closely with development teams to ensure successful project delivery."
        }
    ]
    
    for exp in experiences:
        try:
            r = requests.post(f"{BASE_URL}/api/experiences", json=exp)
            print(f"✅ Added experience: {exp['title']}")
        except Exception as e:
            print(f"❌ Error adding experience: {e}")
    
    # 3. Get categories first
    try:
        r = requests.get(f"{BASE_URL}/api/categories")
        categories = r.json()
        cat_map = {c['name']: c['id'] for c in categories}
    except Exception as e:
        print(f"❌ Error getting categories: {e}")
        cat_map = {}
    
    # 4. Add Projects
    projects = [
        {
            "title": "E-Commerce Platform with Laravel",
            "description": "Full-featured online store built with Laravel and modern UI",
            "long_description": "Complete e-commerce solution with product management, shopping cart, payment gateway integration, and admin dashboard. Built with Laravel 10, MySQL, and Bootstrap for responsive design.",
            "image": "https://images.unsplash.com/photo-1557821552-17105176677c?w=800",
            "demo_url": "",
            "github_url": "",
            "category_id": cat_map.get("Web Development"),
            "tags": "PHP,Laravel,MySQL,Bootstrap,E-Commerce",
            "featured": True
        },
        {
            "title": "AI Sentiment Analysis Tool",
            "description": "Machine learning application for text sentiment analysis",
            "long_description": "AI-powered tool that analyzes text sentiment using Python and Natural Language Processing. Features include real-time analysis, data visualization, and API integration.",
            "image": "https://images.unsplash.com/photo-1531746790731-6c087fecd65a?w=800",
            "demo_url": "",
            "github_url": "",
            "category_id": cat_map.get("Machine Learning"),
            "tags": "Python,AI,NLP,Machine Learning,Flask",
            "featured": True
        },
        {
            "title": "Modern UI/UX Design System",
            "description": "Comprehensive design system created in Figma",
            "long_description": "Complete design system with reusable components, color palette, typography guidelines, and interactive prototypes. Includes both mobile and web design patterns.",
            "image": "https://images.unsplash.com/photo-1561070791-2526d30994b5?w=800",
            "demo_url": "",
            "github_url": "",
            "category_id": cat_map.get("Design"),
            "tags": "Figma,UI/UX,Design System,Prototyping",
            "featured": True
        },
        {
            "title": "Company Management System",
            "description": "Web-based system for managing company operations",
            "long_description": "Comprehensive management system built with Laravel featuring employee management, attendance tracking, payroll, and reporting modules. Designed with modern UI principles.",
            "image": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=800",
            "demo_url": "",
            "github_url": "",
            "category_id": cat_map.get("Web Development"),
            "tags": "Laravel,PHP,MySQL,Bootstrap,CRM",
            "featured": False
        },
        {
            "title": "Portfolio Website with Modern Design",
            "description": "Responsive portfolio showcasing creative work",
            "long_description": "Beautiful portfolio website designed in Figma and built with modern web technologies. Features smooth animations, interactive elements, and optimized performance.",
            "image": "https://images.unsplash.com/photo-1467232004584-a241de8bcf5d?w=800",
            "demo_url": "",
            "github_url": "",
            "category_id": cat_map.get("Web Development"),
            "tags": "HTML,CSS,JavaScript,Figma,Responsive",
            "featured": False
        },
        {
            "title": "RESTful API with Laravel",
            "description": "Scalable API backend for mobile and web applications",
            "long_description": "RESTful API built with Laravel featuring JWT authentication, rate limiting, API documentation, and comprehensive endpoint testing. Includes Docker setup for easy deployment.",
            "image": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=800",
            "demo_url": "",
            "github_url": "",
            "category_id": cat_map.get("Web Development"),
            "tags": "Laravel,API,REST,JWT,Docker",
            "featured": False
        }
    ]
    
    for project in projects:
        try:
            r = requests.post(f"{BASE_URL}/api/projects", json=project)
            print(f"✅ Added project: {project['title']}")
            time.sleep(0.5)
        except Exception as e:
            print(f"❌ Error adding project {project['title']}: {e}")
    
    # 5. Add some sample articles
    articles = [
        {
            "title": "Getting Started with Laravel Development",
            "content": "Laravel is one of the most popular PHP frameworks, offering elegant syntax and powerful features for modern web development...",
            "excerpt": "Learn the fundamentals of Laravel framework and build your first application",
            "cover_image": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800",
            "tags": "Laravel,PHP,Web Development",
            "published": True
        },
        {
            "title": "UI/UX Design Principles for Beginners",
            "content": "Great design is more than just aesthetics. Understanding user needs and creating intuitive interfaces is crucial...",
            "excerpt": "Essential UI/UX principles every designer should know",
            "cover_image": "https://images.unsplash.com/photo-1561070791-2526d30994b5?w=800",
            "tags": "UI/UX,Design,Figma",
            "published": True
        },
        {
            "title": "Introduction to AI and Machine Learning with Python",
            "content": "Artificial Intelligence and Machine Learning are transforming industries. Python makes it accessible for everyone...",
            "excerpt": "Start your journey in AI with Python and popular ML libraries",
            "cover_image": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800",
            "tags": "Python,AI,Machine Learning",
            "published": True
        }
    ]
    
    for article in articles:
        try:
            r = requests.post(f"{BASE_URL}/api/articles", json=article)
            print(f"✅ Added article: {article['title']}")
        except Exception as e:
            print(f"❌ Error adding article: {e}")
    
    print("\n✨ Sample data added successfully!")
    print(f"🌐 Visit: {BASE_URL}")
    print(f"👨‍💼 Admin: {BASE_URL}/admin.html")
    print("🔐 Login: admin (tanpa password)")

if __name__ == "__main__":
    print("⏳ Waiting for services to be ready...")
    time.sleep(5)
    add_sample_data()
