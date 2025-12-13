# Taskmaster Portfolio - Complete Portfolio Management System

[![Docker](https://img.shields.io/badge/Docker-Enabled-blue)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.9-green)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-lightgrey)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)](https://www.postgresql.org/)

Modern, professional portfolio management system built with microservices architecture using Docker, Python Flask, and PostgreSQL.

## 🎯 Features

### Public Features
- ✨ **Modern & Responsive Design** - Works perfectly on all devices
- 🎨 **Skills Showcase** - Display skills with proficiency levels
- 💼 **Work Experience Timeline** - Professional career journey display
- 📁 **Project Portfolio** - Showcase your best works with filters and search
- 📝 **Blog/Articles** - Share your knowledge and expertise
- 💬 **Contact Form** - Easy communication with visitors
- ❤️ **Interactive Elements** - Like projects, view counts, comments
- 🔍 **Advanced Search & Filters** - Find projects by category, tags, or keywords

### Admin Features
- 🔐 **Secure Authentication** - JWT-based login system
- 📊 **Analytics Dashboard** - Track views, likes, and engagement
- ➕ **Content Management** - Easy CRUD operations for all content
- 🖼️ **Image Upload** - Direct image upload functionality
- 📧 **Message Management** - View and manage contact messages
- 🎯 **Featured Projects** - Highlight your best work
- 📈 **Real-time Statistics** - Live data updates

## 🏗️ Architecture

```
┌─────────────┐
│   Nginx     │ ← Port 80 (Web Server & Reverse Proxy)
└──────┬──────┘
       │
┌──────┴──────┐
│   Frontend  │ ← Static HTML/CSS/JS with TailwindCSS
└─────────────┘
       │
┌──────┴──────┐
│ Flask API   │ ← Port 5000 (Python Backend)
└──────┬──────┘
       │
┌──────┴──────┐
│ PostgreSQL  │ ← Port 5432 (Database)
└─────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose installed
- Git installed
- 2GB RAM minimum
- 10GB storage space

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd taskmaster
```

2. **Start the application**
```bash
docker-compose up -d
```

3. **Wait for services to initialize** (about 10-15 seconds)

4. **Populate with sample data** (optional)
```bash
cd Backend
python seed_data.py
```

5. **Access the application**
- **Website**: http://localhost
- **Admin Panel**: http://localhost/admin.html
- **Login Credentials**: 
  - Username: `admin`
  - Password: `admin123`

## 📁 Project Structure

```
Taskmaster/
├── Backend/
│   ├── app.py              # Main Flask application
│   ├── models.py           # Database models (SQLAlchemy)
│   ├── seed_data.py        # Sample data seeder
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Backend container config
├── Frontend/
│   ├── index.html          # Main public page
│   ├── admin.html          # Admin dashboard
│   └── script.js           # Frontend JavaScript
├── nginx/
│   └── default.conf        # Nginx configuration
├── docs/
│   ├── BSD.md              # Business System Design
│   └── TSD.md              # Technical System Design
├── docker-compose.yml      # Docker orchestration
└── README.md              # This file
```

## 🛠️ Technology Stack

### Frontend
- HTML5, CSS3, JavaScript (Vanilla)
- TailwindCSS 3.x (Utility-first CSS)
- Font Awesome 6.x (Icons)

### Backend
- Python 3.9
- Flask 3.0 (Web Framework)
- SQLAlchemy (ORM)
- Flask-JWT-Extended (Authentication)
- Flask-CORS (Cross-Origin Resource Sharing)
- Werkzeug (Security & Utilities)

### Database
- PostgreSQL 15 Alpine
- Persistent volume storage

### DevOps
- Docker & Docker Compose
- Nginx Alpine (Reverse Proxy)

## 📖 API Documentation

Base URL: `http://localhost/api`

### Authentication
```http
POST /api/auth/login
POST /api/auth/register
GET  /api/auth/me
```

### Projects
```http
GET    /api/projects                # List all projects
GET    /api/projects/:id            # Get project details
POST   /api/projects                # Create project (admin)
PUT    /api/projects/:id            # Update project (admin)
DELETE /api/projects/:id            # Delete project (admin)
POST   /api/projects/:id/like       # Like project
```

### Skills, Experience, Articles, etc.
```http
GET    /api/skills
GET    /api/experiences
GET    /api/articles
POST   /api/contact
GET    /api/stats
GET    /api/dashboard               # Admin only
```

See [TSD.md](docs/TSD.md) for complete API documentation.

## 🔧 Configuration

### Environment Variables
Create `.env` file in root directory:

```env
# Database
DATABASE_URL=postgresql://fitrah:rahasia123@postgres-db:5432/portfolio_db

# JWT Secret
JWT_SECRET_KEY=your-secret-key-here

# Flask
FLASK_ENV=production
FLASK_DEBUG=0

# Upload Settings
UPLOAD_FOLDER=/app/uploads
MAX_CONTENT_LENGTH=16777216
```

### Docker Compose Configuration
Edit `docker-compose.yml` to customize:
- Database credentials
- Port mappings
- Volume locations
- Service dependencies

## 🎨 Customization

### Update Personal Information
1. Edit `Frontend/index.html`:
   - Hero section (name, tagline)
   - About section (bio, social links)
   - Contact information

2. Edit `Backend/seed_data.py`:
   - Skills
   - Work experience
   - Sample projects
   - Articles

### Styling
- Modify TailwindCSS classes in HTML files
- Add custom CSS in `<style>` tags
- Update color scheme in `tailwind.config`

### Branding
- Replace logo text in navigation
- Update favicon
- Customize gradient backgrounds

## 📊 Database Schema

### Main Tables
- **users** - Admin authentication
- **projects** - Portfolio projects
- **categories** - Project categories
- **skills** - Technical skills
- **experiences** - Work history
- **articles** - Blog posts
- **comments** - Project comments
- **contacts** - Contact messages

See [TSD.md](docs/TSD.md) for complete database schema.

## 🔒 Security

### Implemented Security Measures
- ✅ JWT authentication for admin routes
- ✅ Password hashing (Werkzeug pbkdf2:sha256)
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ XSS protection (input sanitization)
- ✅ File upload validation
- ✅ CORS configuration
- ✅ Secure headers

### Production Recommendations
- [ ] Enable HTTPS (SSL/TLS certificate)
- [ ] Implement rate limiting
- [ ] Add CSRF protection
- [ ] Restrict CORS origins
- [ ] Use environment variables for secrets
- [ ] Regular security updates
- [ ] Database backups

## 📈 Performance

### Optimization Features
- Database indexing for fast queries
- Pagination for large datasets
- Lazy loading for images
- Response caching
- Connection pooling
- Optimized Docker images (Alpine)

### Monitoring
- Application logs
- Database query logs
- Nginx access logs
- Docker stats: `docker stats`

## 🧪 Testing

### Run Tests
```bash
# Unit tests
python -m pytest tests/

# API tests
python -m pytest tests/test_api.py

# Database tests
python -m pytest tests/test_models.py
```

### Manual Testing Checklist
- [ ] Homepage loads correctly
- [ ] All sections visible and functional
- [ ] Projects filter and search work
- [ ] Contact form submits successfully
- [ ] Admin login functional
- [ ] CRUD operations work
- [ ] Responsive on mobile devices

## 🚢 Deployment

### Development
```bash
docker-compose up
```

### Production
```bash
# Build optimized images
docker-compose -f docker-compose.prod.yml build

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Monitor logs
docker-compose logs -f
```

### Cloud Deployment Options
- **AWS**: EC2 + RDS
- **Google Cloud**: Cloud Run + Cloud SQL
- **DigitalOcean**: Droplets + Managed Database
- **Heroku**: Container deployment
- **Railway**: One-click deployment

## 🔄 Backup & Restore

### Backup Database
```bash
docker-compose exec postgres-db pg_dump -U fitrah portfolio_db > backup.sql
```

### Restore Database
```bash
docker-compose exec -T postgres-db psql -U fitrah portfolio_db < backup.sql
```

### Backup Uploads
```bash
tar -czf uploads_backup.tar.gz Backend/uploads/
```

## 🐛 Troubleshooting

### Common Issues

**Problem**: Container fails to start
```bash
# Check logs
docker-compose logs backend
docker-compose logs postgres-db

# Restart containers
docker-compose restart
```

**Problem**: Database connection error
```bash
# Verify database is running
docker-compose ps

# Check database logs
docker-compose logs postgres-db

# Recreate database
docker-compose down -v
docker-compose up -d
```

**Problem**: Port already in use
```bash
# Stop existing services
docker-compose down

# Change port in docker-compose.yml
ports:
  - "8080:80"  # Instead of "80:80"
```

## 📚 Documentation

- [Business System Design (BSD)](docs/BSD.md) - Business requirements, use cases, user stories
- [Technical System Design (TSD)](docs/TSD.md) - Architecture, database schema, API docs
- [API Documentation](docs/TSD.md#4-api-design) - Complete API reference

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Fitrah**
- Position: Functional Intern @ PT Sisis
- Role: Software Developer & AI Enthusiast
- Skills: PHP Laravel, Python, Figma, UI/UX Design
- Email: admin@portfolio.com

## 🙏 Acknowledgments

- Flask Framework Team
- PostgreSQL Community
- Docker Community
- TailwindCSS Team
- Font Awesome
- All open-source contributors

## 📞 Support

For support, email admin@portfolio.com or open an issue in the repository.

## 🗺️ Roadmap

### Version 1.1 (Q1 2026)
- [ ] Multi-language support (EN/ID)
- [ ] Advanced analytics with charts
- [ ] Comment system for blog posts
- [ ] Newsletter subscription

### Version 2.0 (Q2 2026)
- [ ] Social media integration
- [ ] Resume/CV download
- [ ] Testimonials section
- [ ] Real-time chat support
- [ ] Mobile app (React Native)

---

**Built with ❤️ using Docker & Microservices**

⭐ Star this repo if you find it useful!
