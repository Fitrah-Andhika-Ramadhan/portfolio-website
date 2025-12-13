# Technical System Design (TSD)
## Portfolio Management System

**Project Name:** Taskmaster Portfolio  
**Version:** 1.0  
**Date:** December 13, 2025  
**Author:** Fitrah

---

## 1. System Overview

### 1.1 Architecture Summary
Portfolio Management System menggunakan arsitektur **microservices containerized** dengan Docker, terdiri dari 3 main components:
- **Frontend**: Static HTML/CSS/JavaScript
- **Backend API**: Python Flask REST API
- **Database**: PostgreSQL
- **Web Server**: Nginx (Reverse Proxy)

### 1.2 Technology Stack

#### Frontend
- HTML5, CSS3, JavaScript (Vanilla)
- TailwindCSS for styling
- Font Awesome for icons

#### Backend
- **Framework**: Python Flask 3.x
- **ORM**: SQLAlchemy
- **Authentication**: Flask-JWT-Extended
- **CORS**: Flask-CORS
- **Utilities**: Werkzeug, python-slugify

#### Database
- PostgreSQL 15 (Alpine)

#### DevOps
- Docker & Docker Compose
- Nginx Alpine

---

## 2. System Architecture

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Internet                          │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
         ┌─────────────────┐
         │   Port 80 (HTTP) │
         └────────┬─────────┘
                  │
         ┌────────▼─────────┐
         │   Nginx (Alpine)  │
         │  Reverse Proxy    │
         │  Static File Srv  │
         └────────┬─────────┘
                  │
      ┌───────────┴───────────┐
      │                       │
      ▼                       ▼
┌──────────┐          ┌────────────┐
│ Frontend │          │  Backend   │
│  Static  │          │ Flask API  │
│   Files  │          │  Port 5000 │
└──────────┘          └──────┬─────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   PostgreSQL    │
                    │   Database      │
                    │   Port 5432     │
                    └─────────────────┘
```

### 2.2 Docker Architecture

```yaml
Services:
  ├─ postgres-db (Database Layer)
  ├─ backend (Application Layer)
  └─ nginx (Presentation Layer)

Volumes:
  └─ db-data (Persistent Storage)

Networks:
  └─ taskmaster_default (Bridge Network)
```

### 2.3 Component Interaction

```
Client Browser
    ↓ HTTP Request
Nginx (Port 80)
    ↓ Static Files → Direct Response
    ↓ /api/* → Proxy to Backend
Backend Flask (Port 5000)
    ↓ Query
PostgreSQL Database (Port 5432)
    ↓ Result
Backend Flask
    ↓ JSON Response
Client Browser
```

---

## 3. Database Design

### 3.1 Entity Relationship Diagram (ERD)

```
┌─────────────┐       ┌──────────────┐
│   users     │       │  categories  │
├─────────────┤       ├──────────────┤
│ id (PK)     │       │ id (PK)      │
│ username    │       │ name         │
│ email       │       │ icon         │
│ password_   │       └──────┬───────┘
│   hash      │              │
│ is_admin    │              │ 1
│ created_at  │              │
└─────────────┘              │
                             │
                             │ N
┌─────────────┐       ┌──────▼───────┐       ┌──────────────┐
│  comments   │   N   │   projects   │       │   skills     │
├─────────────┤──────▶├──────────────┤       ├──────────────┤
│ id (PK)     │       │ id (PK)      │       │ id (PK)      │
│ project_id  │       │ title        │       │ name         │
│   (FK)      │       │ description  │       │ level        │
│ name        │       │ long_desc    │       │ icon         │
│ email       │       │ image_url    │       │ category     │
│ message     │       │ demo_url     │       └──────────────┘
│ rating      │       │ github_url   │
│ approved    │       │ category_id  │       ┌──────────────┐
│ created_at  │       │   (FK)       │       │ experiences  │
└─────────────┘       │ tags         │       ├──────────────┤
                      │ views        │       │ id (PK)      │
┌─────────────┐       │ likes        │       │ title        │
│  articles   │       │ featured     │       │ company      │
├─────────────┤       │ created_at   │       │ location     │
│ id (PK)     │       │ updated_at   │       │ start_date   │
│ title       │       └──────────────┘       │ end_date     │
│ slug        │                              │ description  │
│ content     │       ┌──────────────┐       │ current      │
│ excerpt     │       │   contacts   │       └──────────────┘
│ cover_image │       ├──────────────┤
│ tags        │       │ id (PK)      │
│ views       │       │ name         │
│ published   │       │ email        │
│ created_at  │       │ subject      │
│ updated_at  │       │ message      │
└─────────────┘       │ read         │
                      │ created_at   │
                      └──────────────┘
```

### 3.2 Database Schema

#### Table: users
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Table: categories
```sql
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    icon VARCHAR(50)
);
```

#### Table: projects
```sql
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    long_description TEXT,
    image_url VARCHAR(255) NOT NULL,
    demo_url VARCHAR(255),
    github_url VARCHAR(255),
    category_id INTEGER REFERENCES categories(id),
    tags VARCHAR(255),
    views INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    featured BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Table: skills
```sql
CREATE TABLE skills (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    level INTEGER DEFAULT 50,
    icon VARCHAR(50),
    category VARCHAR(50)
);
```

#### Table: experiences
```sql
CREATE TABLE experiences (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    company VARCHAR(100) NOT NULL,
    location VARCHAR(100),
    start_date VARCHAR(20),
    end_date VARCHAR(20),
    description TEXT,
    current BOOLEAN DEFAULT FALSE
);
```

#### Table: articles
```sql
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    slug VARCHAR(200) UNIQUE NOT NULL,
    content TEXT NOT NULL,
    excerpt TEXT,
    cover_image VARCHAR(255),
    tags VARCHAR(255),
    views INTEGER DEFAULT 0,
    published BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Table: comments
```sql
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL,
    message TEXT NOT NULL,
    rating INTEGER DEFAULT 5,
    approved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Table: contacts
```sql
CREATE TABLE contacts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL,
    subject VARCHAR(200),
    message TEXT NOT NULL,
    read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 3.3 Database Indexes

```sql
-- Performance optimization indexes
CREATE INDEX idx_projects_category ON projects(category_id);
CREATE INDEX idx_projects_featured ON projects(featured);
CREATE INDEX idx_projects_created ON projects(created_at DESC);
CREATE INDEX idx_articles_published ON articles(published);
CREATE INDEX idx_articles_slug ON articles(slug);
CREATE INDEX idx_comments_project ON comments(project_id);
CREATE INDEX idx_comments_approved ON comments(approved);
CREATE INDEX idx_contacts_read ON contacts(read);
```

---

## 4. API Design

### 4.1 API Architecture
- **Style**: RESTful API
- **Format**: JSON
- **Base URL**: `http://localhost/api`
- **Authentication**: JWT Bearer Token

### 4.2 Authentication Endpoints

#### POST /api/auth/register
```json
Request:
{
    "username": "string",
    "email": "string",
    "password": "string",
    "is_admin": "boolean (optional)"
}

Response (201):
{
    "message": "User registered successfully"
}
```

#### POST /api/auth/login
```json
Request:
{
    "username": "string",
    "password": "string"
}

Response (200):
{
    "access_token": "string",
    "user": {
        "id": "integer",
        "username": "string",
        "email": "string",
        "is_admin": "boolean"
    }
}
```

#### GET /api/auth/me
```
Headers: Authorization: Bearer {token}

Response (200):
{
    "id": "integer",
    "username": "string",
    "email": "string",
    "is_admin": "boolean"
}
```

### 4.3 Project Endpoints

#### GET /api/projects
```
Query Parameters:
- page: integer (default: 1)
- per_page: integer (default: 10)
- category: integer (optional)
- search: string (optional)
- sort: string (created_at|views|likes|title)
- featured: boolean (optional)

Response (200):
{
    "projects": [
        {
            "id": "integer",
            "title": "string",
            "description": "string",
            "long_description": "string",
            "image": "string (url)",
            "demo_url": "string",
            "github_url": "string",
            "category": {
                "id": "integer",
                "name": "string",
                "icon": "string"
            },
            "tags": ["string"],
            "views": "integer",
            "likes": "integer",
            "featured": "boolean",
            "comments_count": "integer",
            "created_at": "string (ISO 8601)",
            "updated_at": "string (ISO 8601)"
        }
    ],
    "total": "integer",
    "pages": "integer",
    "current_page": "integer",
    "has_next": "boolean",
    "has_prev": "boolean"
}
```

#### GET /api/projects/:id
```
Response (200):
{
    "id": "integer",
    "title": "string",
    "description": "string",
    ...
}
```

#### POST /api/projects
```
Request:
{
    "title": "string",
    "description": "string",
    "long_description": "string (optional)",
    "image": "string (url)",
    "demo_url": "string (optional)",
    "github_url": "string (optional)",
    "category_id": "integer (optional)",
    "tags": "string (comma separated)",
    "featured": "boolean"
}

Response (201):
{
    "message": "Project created",
    "project": {...}
}
```

#### PUT /api/projects/:id
```
Request: Same as POST

Response (200):
{
    "message": "Project updated",
    "project": {...}
}
```

#### DELETE /api/projects/:id
```
Response (200):
{
    "message": "Project deleted"
}
```

#### POST /api/projects/:id/like
```
Response (200):
{
    "likes": "integer"
}
```

### 4.4 Other Endpoints

#### Categories
- `GET /api/categories` - List all categories
- `POST /api/categories` - Create category

#### Skills
- `GET /api/skills?category=string` - List skills
- `POST /api/skills` - Create skill
- `DELETE /api/skills/:id` - Delete skill

#### Experiences
- `GET /api/experiences` - List experiences
- `POST /api/experiences` - Create experience
- `DELETE /api/experiences/:id` - Delete experience

#### Articles
- `GET /api/articles?page=1&per_page=6&published=true` - List articles
- `GET /api/articles/:slug` - Get article by slug
- `POST /api/articles` - Create article

#### Comments
- `GET /api/projects/:id/comments` - List approved comments
- `POST /api/projects/:id/comments` - Submit comment
- `PUT /api/comments/:id/approve` - Approve comment (admin)

#### Contacts
- `POST /api/contact` - Submit contact message
- `GET /api/contacts` - List messages (admin)
- `PUT /api/contacts/:id/read` - Mark as read (admin)

#### Stats & Dashboard
- `GET /api/stats` - Get statistics
- `GET /api/dashboard` - Get dashboard data (admin)

#### File Upload
- `POST /api/upload` - Upload image file
- `GET /uploads/:filename` - Serve uploaded file

### 4.5 API Response Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 500 | Internal Server Error |

---

## 5. Security Design

### 5.1 Authentication & Authorization
- **Method**: JWT (JSON Web Token)
- **Token Expiry**: 24 hours
- **Password Storage**: Werkzeug pbkdf2:sha256
- **Protected Routes**: Admin endpoints require valid JWT

### 5.2 Security Measures

#### Input Validation
- All user inputs sanitized
- SQL injection prevention via ORM (SQLAlchemy)
- XSS protection via input escaping
- File upload validation (type, size)

#### CORS Configuration
- Enabled for all origins (development)
- Should be restricted in production

#### Rate Limiting
- Recommended: Implement rate limiting for API endpoints
- Use Flask-Limiter or Nginx rate limiting

#### HTTPS
- Required for production
- SSL/TLS certificate (Let's Encrypt)

### 5.3 Data Protection
- Sensitive data encrypted
- Database connection secured
- Environment variables for secrets
- No hardcoded credentials

---

## 6. Infrastructure Design

### 6.1 Docker Configuration

#### docker-compose.yml
```yaml
version: '3.8'

services:
  postgres-db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=fitrah
      - POSTGRES_PASSWORD=rahasia123
      - POSTGRES_DB=portfolio_db
    volumes:
      - db-data:/var/lib/postgresql/data

  backend:
    build: ./backend
    volumes:
      - ./backend:/app
    environment:
      - DATABASE_URL=postgresql://fitrah:rahasia123@postgres-db:5432/portfolio_db
    depends_on:
      - postgres-db

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf:ro
      - ./frontend:/usr/share/nginx/html:ro
    depends_on:
      - backend

volumes:
  db-data:
```

#### Backend Dockerfile
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

### 6.2 Nginx Configuration

```nginx
server {
    listen 80;
    server_name localhost;

    # Frontend static files
    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
    }

    # Backend API proxy
    location /api/ {
        proxy_pass http://backend:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # Uploaded files
    location /uploads/ {
        proxy_pass http://backend:5000;
    }
}
```

### 6.3 Environment Variables

```env
# Database
DATABASE_URL=postgresql://user:password@host:port/dbname

# JWT
JWT_SECRET_KEY=your-secret-key-change-in-production

# Upload
UPLOAD_FOLDER=/app/uploads
MAX_CONTENT_LENGTH=16777216

# Flask
FLASK_ENV=production
FLASK_DEBUG=0
```

---

## 7. Deployment Design

### 7.1 Deployment Architecture

```
Development → Testing → Staging → Production

Local Machine
  ↓
Docker Build
  ↓
Container Registry (Docker Hub / Private)
  ↓
Production Server
  ↓
Docker Compose Up
  ↓
Live Application
```

### 7.2 Deployment Steps

#### Initial Setup
```bash
# 1. Clone repository
git clone <repository-url>
cd taskmaster

# 2. Configure environment
cp .env.example .env
nano .env

# 3. Build and start containers
docker-compose build
docker-compose up -d

# 4. Initialize database
docker-compose exec backend python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()

# 5. Verify deployment
curl http://localhost/api/stats
```

#### Update Deployment
```bash
# 1. Pull latest changes
git pull origin main

# 2. Rebuild containers
docker-compose build

# 3. Restart services
docker-compose down
docker-compose up -d

# 4. Verify
docker-compose logs backend
```

### 7.3 Backup Strategy

#### Database Backup
```bash
# Manual backup
docker-compose exec postgres-db pg_dump -U fitrah portfolio_db > backup.sql

# Automated backup (cron)
0 2 * * * docker-compose exec postgres-db pg_dump -U fitrah portfolio_db > /backups/portfolio_$(date +\%Y\%m\%d).sql
```

#### File Backup
```bash
# Backup uploads folder
tar -czf uploads_backup.tar.gz backend/uploads/

# Sync to cloud storage
aws s3 sync backend/uploads/ s3://bucket-name/uploads/
```

---

## 8. Performance Optimization

### 8.1 Database Optimization
- Connection pooling
- Query optimization with indexes
- Pagination for large datasets
- Lazy loading relationships

### 8.2 Application Optimization
- Response caching
- Gzip compression
- Static file caching
- CDN for static assets

### 8.3 Frontend Optimization
- Minification (CSS/JS)
- Image optimization
- Lazy loading images
- Browser caching

### 8.4 Monitoring
- Application logs
- Error tracking (Sentry)
- Performance monitoring (New Relic)
- Uptime monitoring (UptimeRobot)

---

## 9. Testing Strategy

### 9.1 Unit Testing
```python
# Example: test_models.py
def test_user_creation():
    user = User(username='test', email='test@example.com')
    user.set_password('password123')
    assert user.check_password('password123')

def test_project_to_json():
    project = Project(title='Test', description='Desc')
    json_data = project.to_json()
    assert json_data['title'] == 'Test'
```

### 9.2 Integration Testing
```python
# Example: test_api.py
def test_get_projects(client):
    response = client.get('/api/projects')
    assert response.status_code == 200
    assert 'projects' in response.json

def test_create_project_unauthorized(client):
    data = {'title': 'Test', 'description': 'Test'}
    response = client.post('/api/projects', json=data)
    assert response.status_code == 401
```

### 9.3 End-to-End Testing
- Selenium for browser automation
- Test user workflows
- Cross-browser testing

---

## 10. Maintenance & Support

### 10.1 Logging
```python
# Configure logging
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### 10.2 Error Handling
```python
# Global error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({"error": "Internal server error"}), 500
```

### 10.3 Health Check
```python
@app.route('/health')
def health_check():
    try:
        db.session.execute('SELECT 1')
        return jsonify({"status": "healthy", "database": "ok"}), 200
    except:
        return jsonify({"status": "unhealthy", "database": "error"}), 503
```

---

## 11. Technical Specifications

### 11.1 System Requirements

#### Server Requirements
- **OS**: Linux (Ubuntu 20.04+ recommended)
- **RAM**: Minimum 2GB
- **Storage**: Minimum 10GB SSD
- **CPU**: 2 cores minimum
- **Network**: Stable internet connection

#### Client Requirements
- **Browser**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Screen Resolution**: 320px - 4K
- **Internet**: Minimum 1 Mbps

### 11.2 Dependencies

#### Python Packages
```txt
flask==3.0.0
flask-cors==4.0.0
flask-sqlalchemy==3.1.1
flask-jwt-extended==4.6.0
psycopg2-binary==2.9.9
werkzeug==3.0.1
pillow==10.1.0
python-slugify==8.0.1
```

#### System Packages
- Docker Engine 20.10+
- Docker Compose 2.0+
- Git

---

## 12. Appendices

### Appendix A: Glossary
- **JWT**: JSON Web Token - Authentication token format
- **ORM**: Object-Relational Mapping - Database abstraction layer
- **REST**: Representational State Transfer - API architectural style
- **CRUD**: Create, Read, Update, Delete operations
- **CDN**: Content Delivery Network
- **SSL/TLS**: Secure Sockets Layer / Transport Layer Security

### Appendix B: References
- Flask Documentation: https://flask.palletsprojects.com/
- SQLAlchemy Documentation: https://docs.sqlalchemy.org/
- Docker Documentation: https://docs.docker.com/
- PostgreSQL Documentation: https://www.postgresql.org/docs/

### Appendix C: Contact Information
- **Developer**: Fitrah
- **Email**: admin@portfolio.com
- **Repository**: [GitHub Repository URL]

---

**Document Status:** Approved  
**Next Review Date:** January 13, 2026  
**Version History:**
- v1.0 (2025-12-13): Initial TSD document
