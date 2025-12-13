# 🚀 Deployment Guide
## Portfolio Management System

Panduan lengkap untuk deploy aplikasi portfolio ke berbagai platform cloud hosting.

---

## 📋 Table of Contents
1. [Persiapan Deployment](#persiapan-deployment)
2. [Railway Deployment (Recommended)](#railway-deployment)
3. [Render Deployment](#render-deployment)
4. [DigitalOcean Deployment](#digitalocean-deployment)
5. [VPS Manual Deployment](#vps-manual-deployment)
6. [Environment Variables](#environment-variables)
7. [Post-Deployment](#post-deployment)
8. [Troubleshooting](#troubleshooting)

---

## 🎯 Persiapan Deployment

### 1. Push Code ke GitHub

```bash
# Initialize git repository (jika belum)
cd "d:\Semester 8\Taskmaster"
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Portfolio project"

# Create repository di GitHub, lalu:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

### 2. Siapkan Environment Variables

Copy file `.env.example` dan sesuaikan:
```bash
cp .env.example .env
nano .env
```

Update dengan values yang secure:
```env
POSTGRES_PASSWORD=random_secure_password_min_16_chars
JWT_SECRET_KEY=random_jwt_secret_minimum_32_characters
```

**Generate Secure Keys:**
```bash
# Generate random password (Python)
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Atau di PowerShell
-join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | % {[char]$_})
```

---

## 🚂 Railway Deployment (Recommended - Paling Mudah)

Railway menyediakan $5 kredit gratis per bulan dan sangat mudah digunakan.

### Step-by-Step:

#### 1. Sign Up Railway
- Kunjungi: https://railway.app
- Sign up dengan GitHub account
- Verify email

#### 2. Create New Project

```bash
# Install Railway CLI (optional)
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init
```

**Atau via Dashboard:**
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Connect GitHub account
4. Pilih repository Taskmaster

#### 3. Setup PostgreSQL Database

Di Railway Dashboard:
1. Click "New" → "Database" → "Add PostgreSQL"
2. Database akan auto-deploy
3. Copy `DATABASE_URL` dari Variables tab

#### 4. Deploy Backend Service

1. Click "New" → "GitHub Repo" → Pilih repo
2. Settings:
   - **Root Directory**: `Backend`
   - **Start Command**: `python app.py`
3. Add Environment Variables:
   ```
   DATABASE_URL=postgresql://user:pass@host:port/db
   JWT_SECRET_KEY=your_secret_key
   FLASK_ENV=production
   PORT=5000
   ```
4. Deploy!

#### 5. Deploy Frontend (Nginx)

1. Click "New" → "GitHub Repo" → Pilih repo lagi
2. Settings:
   - **Root Directory**: `/`
   - **Dockerfile Path**: `Dockerfile.nginx`
3. Add Environment Variables:
   ```
   BACKEND_URL=https://your-backend-url.railway.app
   ```
4. Deploy!

#### 6. Configure Domain

1. Pada Frontend service → Settings → Networking
2. Generate Domain atau add custom domain
3. Copy public URL: `https://your-app.railway.app`

#### 7. Update CORS di Backend

Edit `Backend/app.py`:
```python
CORS(app, origins=[
    "http://localhost",
    "https://your-app.railway.app"  # Add your Railway domain
])
```

Commit dan push perubahan.

### Railway Pricing
- **Free**: $5 credit/month (~500 hours)
- **Hobby**: $5/month
- **Pro**: $20/month

---

## 🎨 Render Deployment (Good Free Tier)

Render menyediakan free tier yang cukup untuk portfolio sederhana.

### Step-by-Step:

#### 1. Sign Up Render
- Kunjungi: https://render.com
- Sign up dengan GitHub

#### 2. Create PostgreSQL Database

1. Dashboard → "New +" → "PostgreSQL"
2. Settings:
   - **Name**: `portfolio-db`
   - **Database**: `portfolio_db`
   - **User**: `fitrah`
   - **Region**: Singapore (terdekat)
   - **Plan**: Free
3. Create Database
4. Copy "Internal Database URL"

#### 3. Deploy Backend

1. Dashboard → "New +" → "Web Service"
2. Connect GitHub repository
3. Settings:
   - **Name**: `portfolio-backend`
   - **Region**: Singapore
   - **Branch**: main
   - **Root Directory**: `Backend`
   - **Runtime**: Docker
   - **Dockerfile Path**: `Backend/Dockerfile`
   - **Plan**: Free
4. Environment Variables:
   ```
   DATABASE_URL=postgresql://user:pass@host/db
   JWT_SECRET_KEY=your_secret_key
   FLASK_ENV=production
   PORT=5000
   ```
5. Create Web Service

#### 4. Deploy Frontend/Nginx

1. Dashboard → "New +" → "Static Site"
2. Settings:
   - **Name**: `portfolio-web`
   - **Branch**: main
   - **Build Command**: `echo "Using pre-built files"`
   - **Publish Directory**: `Frontend`
3. Create Static Site

#### 5. Configure API Endpoint

Update `Frontend/script.js`:
```javascript
const API_URL = 'https://portfolio-backend.onrender.com/api';
```

Commit dan push.

#### 6. Custom Domain (Optional)

1. Settings → Custom Domains
2. Add domain dan configure DNS:
   ```
   Type: CNAME
   Name: @
   Value: your-app.onrender.com
   ```

### Render Limitations (Free Tier)
- ⚠️ Service sleeps after 15 mins inactivity
- ⚠️ Cold start ~30 seconds
- ✅ 750 hours/month
- ✅ Unlimited bandwidth

---

## 🌊 DigitalOcean Deployment (Most Reliable)

DigitalOcean App Platform atau Droplets - More control, paid service.

### Option A: App Platform (Easier)

#### 1. Sign Up & Create App
- https://cloud.digitalocean.com
- Create Account (get $200 credit for 60 days)
- Apps → "Create App"

#### 2. Connect GitHub
- Authorize DigitalOcean
- Select repository

#### 3. Configure Resources

**Database:**
- Component: Managed Database
- Engine: PostgreSQL 15
- Plan: Basic ($15/month)

**Backend:**
- Component: Web Service
- Dockerfile: `Backend/Dockerfile`
- HTTP Port: 5000
- Environment Variables: Add all required

**Frontend:**
- Component: Static Site
- Build: None
- Output: `Frontend`

#### 4. Deploy
- Review & Create
- Wait ~5-10 minutes
- App URL: `https://your-app.ondigitalocean.app`

### Option B: Droplet (VPS - More Control)

Lihat section [VPS Manual Deployment](#vps-manual-deployment)

---

## 🖥️ VPS Manual Deployment (Any VPS Provider)

Panduan untuk deploy di VPS seperti DigitalOcean Droplet, AWS EC2, Linode, dll.

### 1. Create VPS

**Recommended Specs:**
- OS: Ubuntu 22.04 LTS
- RAM: 2GB minimum
- Storage: 25GB SSD
- CPU: 1 vCPU

**Providers:**
- DigitalOcean Droplet: $12/month
- AWS EC2 t3.small: ~$15/month
- Linode: $12/month
- Vultr: $10/month

### 2. Initial Server Setup

```bash
# SSH ke server
ssh root@your_server_ip

# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
apt install docker-compose -y

# Create user (optional)
adduser fitrah
usermod -aG docker fitrah
usermod -aG sudo fitrah
```

### 3. Clone Project

```bash
# Login as user
su - fitrah

# Clone repository
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
```

### 4. Configure Environment

```bash
# Create .env file
cp .env.example .env
nano .env
```

Update:
```env
POSTGRES_PASSWORD=secure_random_password
JWT_SECRET_KEY=random_jwt_secret_key
FLASK_ENV=production
PORT=80
```

### 5. Deploy with Docker Compose

```bash
# Build and start services
docker-compose -f docker-compose.prod.yml up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### 6. Initialize Database

```bash
# Run seed data (optional)
docker-compose exec backend python seed_data.py

# Or manual:
docker-compose exec backend python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

### 7. Configure Firewall

```bash
# Enable UFW
ufw allow OpenSSH
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable

# Check status
ufw status
```

### 8. Setup SSL with Let's Encrypt (HTTPS)

```bash
# Install Certbot
apt install certbot python3-certbot-nginx -y

# Stop nginx container temporarily
docker-compose stop nginx

# Get certificate
certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# Update nginx config
nano nginx/default.conf
```

Add SSL configuration:
```nginx
server {
    listen 80;
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # Redirect HTTP to HTTPS
    if ($scheme != "https") {
        return 301 https://$host$request_uri;
    }

    # ... rest of config
}
```

Update docker-compose to mount SSL certs:
```yaml
nginx:
  volumes:
    - /etc/letsencrypt:/etc/letsencrypt:ro
```

```bash
# Restart nginx
docker-compose up -d nginx
```

### 9. Setup Auto-Renewal

```bash
# Test renewal
certbot renew --dry-run

# Add cron job
crontab -e

# Add line:
0 3 * * * certbot renew --quiet && docker-compose restart nginx
```

### 10. Configure Domain DNS

Di domain registrar (Namecheap, Cloudflare, dll):

```
Type: A
Name: @
Value: YOUR_SERVER_IP

Type: A
Name: www
Value: YOUR_SERVER_IP
```

Wait 5-15 minutes for DNS propagation.

---

## 🔐 Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `POSTGRES_USER` | Database username | `fitrah` |
| `POSTGRES_PASSWORD` | Database password | `secure_random_pass` |
| `POSTGRES_DB` | Database name | `portfolio_db` |
| `DATABASE_URL` | Full database URL | `postgresql://user:pass@host:5432/db` |
| `JWT_SECRET_KEY` | JWT signing key | `random_32_char_string` |
| `FLASK_ENV` | Flask environment | `production` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_DEBUG` | Debug mode | `0` (off) |
| `PORT` | Server port | `80` |
| `UPLOAD_FOLDER` | Upload directory | `/app/uploads` |
| `MAX_CONTENT_LENGTH` | Max upload size | `16777216` (16MB) |

### Generate Secure Values

**PostgreSQL Password:**
```bash
openssl rand -base64 32
```

**JWT Secret Key:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## ✅ Post-Deployment

### 1. Verify Deployment

```bash
# Check website
curl https://yourdomain.com

# Check API
curl https://yourdomain.com/api/stats

# Expected response:
{
  "status": "ok",
  "total_projects": 6,
  "total_skills": 12,
  ...
}
```

### 2. Initialize Database

```bash
# SSH to server atau use platform console
docker-compose exec backend python seed_data.py
```

### 3. Test Admin Login

- Visit: `https://yourdomain.com/admin.html`
- Login: `admin` / `admin123`
- **Change password immediately!**

### 4. Update Admin Password

```bash
docker-compose exec backend python
>>> from app import app, db, User
>>> with app.app_context():
...     admin = User.query.filter_by(username='admin').first()
...     admin.set_password('new_secure_password')
...     db.session.commit()
>>> exit()
```

### 5. Setup Monitoring

**Uptime Monitoring:**
- UptimeRobot: https://uptimerobot.com (Free)
- Pingdom (Paid)
- StatusCake (Free tier)

**Error Tracking:**
- Sentry: https://sentry.io (Free tier)
- Rollbar
- Bugsnag

### 6. Setup Backups

**Database Backup Script:**
```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"
mkdir -p $BACKUP_DIR

docker-compose exec -T postgres-db pg_dump -U fitrah portfolio_db > $BACKUP_DIR/backup_$DATE.sql

# Keep only last 7 days
find $BACKUP_DIR -name "backup_*.sql" -mtime +7 -delete
```

**Cron job:**
```bash
crontab -e
# Add:
0 2 * * * /path/to/backup.sh
```

### 7. Configure CORS for Production

Edit `Backend/app.py`:
```python
CORS(app, origins=[
    "https://yourdomain.com",
    "https://www.yourdomain.com"
])
```

### 8. Enable Gzip Compression

Update `nginx/default.conf`:
```nginx
gzip on;
gzip_vary on;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml text/javascript;
gzip_min_length 1000;
```

### 9. Setup CDN (Optional)

- Cloudflare (Free): https://cloudflare.com
- BunnyCDN (Paid)
- AWS CloudFront (Paid)

Benefits:
- Faster load times
- DDoS protection
- SSL certificate
- Caching

---

## 🔧 Troubleshooting

### Issue: Database Connection Failed

**Symptoms:** Backend can't connect to PostgreSQL

**Solutions:**
```bash
# Check database is running
docker-compose ps postgres-db

# Check logs
docker-compose logs postgres-db

# Verify environment variables
docker-compose exec backend env | grep DATABASE_URL

# Test connection
docker-compose exec backend python -c "from app import db; db.create_all(); print('Connected!')"
```

### Issue: 502 Bad Gateway

**Symptoms:** Nginx shows 502 error

**Solutions:**
```bash
# Check backend is running
docker-compose ps backend

# Check backend logs
docker-compose logs backend

# Verify backend health
docker-compose exec backend curl http://localhost:5000/api/stats

# Restart services
docker-compose restart backend nginx
```

### Issue: CORS Errors

**Symptoms:** Browser console shows CORS error

**Solutions:**
1. Update `Backend/app.py`:
```python
CORS(app, origins=["https://yourdomain.com"], supports_credentials=True)
```

2. Commit and redeploy:
```bash
git add Backend/app.py
git commit -m "Fix CORS"
git push
```

### Issue: File Upload Fails

**Symptoms:** Can't upload images in admin

**Solutions:**
```bash
# Check uploads directory exists
docker-compose exec backend ls -la /app/uploads

# Create if missing
docker-compose exec backend mkdir -p /app/uploads

# Check permissions
docker-compose exec backend chmod 777 /app/uploads

# Verify volume mount
docker-compose ps -a
docker inspect container_name | grep Mounts
```

### Issue: JWT Token Expired

**Symptoms:** Admin logged out frequently

**Solutions:**
Update `Backend/app.py`:
```python
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)
```

### Issue: Slow Performance

**Solutions:**
1. Enable database connection pooling
2. Add Redis caching
3. Optimize queries with indexes
4. Use CDN for static files
5. Enable gzip compression
6. Upgrade server specs

### Issue: Out of Memory

**Symptoms:** Services crash, restart loops

**Solutions:**
```bash
# Check memory usage
docker stats

# Limit container memory
# Edit docker-compose.prod.yml:
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 512M
```

---

## 📊 Performance Optimization

### 1. Database Indexes
Already implemented in models.py

### 2. Enable Caching
```bash
# Add Redis service
docker-compose.prod.yml:
  redis:
    image: redis:alpine
    restart: unless-stopped
```

### 3. Optimize Images
```bash
# Install image optimization
pip install pillow

# Use in upload endpoint
from PIL import Image
image = Image.open(file)
image.thumbnail((1200, 1200))
image.save(filepath, optimize=True, quality=85)
```

### 4. CDN Setup
- Upload static assets to CDN
- Update URLs in frontend

---

## 🔒 Security Checklist

- [x] Change default admin password
- [x] Use environment variables for secrets
- [x] Enable HTTPS/SSL
- [x] Configure firewall
- [x] Regular backups
- [x] Update dependencies regularly
- [x] Enable rate limiting
- [x] Configure CORS properly
- [x] Use strong JWT secret
- [x] Implement password policies

---

## 📞 Support

Jika mengalami masalah:
1. Check logs: `docker-compose logs -f`
2. Verify environment variables
3. Test database connection
4. Check firewall rules
5. Review nginx configuration

---

**Happy Deploying! 🚀**

Pilih platform yang sesuai kebutuhan:
- **Railway**: Tercepat, paling mudah
- **Render**: Free tier bagus
- **DigitalOcean**: Paling reliable
- **VPS**: Maximum control
