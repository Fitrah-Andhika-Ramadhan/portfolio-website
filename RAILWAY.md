# Railway Deployment Guide

## Quick Deploy to Railway

### 1. Prerequisites
- GitHub account with repository: `Fitrah-Andhika-Ramadhan/portfolio-website`
- Railway account (sign up at https://railway.app)

### 2. Deploy Steps

#### A. Create Railway Project
1. Go to https://railway.app/dashboard
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose: `Fitrah-Andhika-Ramadhan/portfolio-website`
5. Railway will auto-detect Docker and start building

#### B. Add PostgreSQL Database
1. In project dashboard, click "+ New"
2. Select "Database" → "PostgreSQL"
3. Wait for database to be ready (~30 seconds)
4. Click on PostgreSQL service → "Connect" tab
5. Copy the "Postgres Connection URL"

#### C. Configure Environment Variables
Click on your backend service → "Variables" tab, add:

```env
DATABASE_URL = <paste PostgreSQL URL from step B.5>
JWT_SECRET_KEY = JltycyknBH6wP5oQAiWBjEBoCyOD1Npo4qDHnYjf5tE
FLASK_ENV = production
FLASK_DEBUG = 0
PORT = 5000
ALLOWED_ORIGINS = https://your-app.railway.app,http://localhost
```

#### D. Generate Public Domain
1. Backend service → "Settings" → "Networking"
2. Click "Generate Domain"
3. Copy your public URL: `https://[your-app].railway.app`
4. Update `ALLOWED_ORIGINS` variable with this URL

#### E. Deploy Frontend (Optional - Static)
If you want separate frontend service:
1. "+ New" → "Empty Service"
2. Connect same GitHub repo
3. Settings → Root Directory: `Frontend`
4. Deploy Command: `echo "Static files"`

### 3. Initialize Database

After successful deployment:

1. Backend service → "..." menu → "Shell"
2. Run:
```bash
python seed_data.py
```

Or create admin manually:
```python
from app import app, db, User
with app.app_context():
    admin = User(username='admin', email='admin@portfolio.com', is_admin=True)
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()
```

### 4. Test Your Application

- Website: `https://[your-app].railway.app`
- Admin: `https://[your-app].railway.app/admin.html`
- API: `https://[your-app].railway.app/api/stats`

Login credentials:
- Username: `admin`
- Password: `admin123`

### 5. Monitor & Manage

- **Logs**: Deployments tab → View logs
- **Metrics**: Service → Metrics (CPU, RAM, Network)
- **Restart**: Service → "..." → Restart
- **Redeploy**: Deployments tab → Redeploy

### 6. Custom Domain (Optional)

1. Service → Settings → Networking
2. Click "Custom Domain"
3. Add your domain
4. Update DNS records:
   ```
   Type: CNAME
   Name: @
   Value: [your-app].railway.app
   ```

### 7. Troubleshooting

**Build Fails:**
- Check Dockerfile syntax
- Verify all dependencies in requirements.txt
- Check build logs for specific errors

**Database Connection Error:**
- Verify DATABASE_URL is correct
- Check if PostgreSQL service is running
- Ensure network connectivity between services

**502 Bad Gateway:**
- Check if backend is running
- Verify PORT environment variable
- Check application logs

**CORS Errors:**
- Update ALLOWED_ORIGINS with your Railway domain
- Redeploy after changing environment variables

### 8. Cost & Limits

**Free Tier:**
- $5 credit/month (~500 execution hours)
- 1GB RAM per service
- 1 vCPU
- 100GB bandwidth

**Hobby Plan ($5/month):**
- $5 execution credit
- Additional resources

**Pro Plan ($20/month):**
- $20 execution credit
- Priority support
- Custom domains

### 9. Best Practices

- ✅ Use environment variables for secrets
- ✅ Enable health checks
- ✅ Monitor usage to avoid overages
- ✅ Set up custom domain for production
- ✅ Regular backups of database
- ✅ Update dependencies regularly

### 10. Automatic Deployment

Railway auto-deploys on push to `main` branch:
1. Make changes locally
2. Commit: `git commit -m "Update"`
3. Push: `git push origin main`
4. Railway automatically builds and deploys

---

## Architecture on Railway

```
GitHub Repo
    ↓ (auto-deploy on push)
Railway Project
    ├─ Backend Service (Docker)
    │  ├─ Flask API (Port 5000)
    │  ├─ Static Files (Nginx)
    │  └─ Public Domain
    └─ PostgreSQL Database
       └─ Persistent Volume
```

---

## Support

- Railway Docs: https://docs.railway.app
- Discord: https://discord.gg/railway
- Status: https://status.railway.app

---

**Your Railway URL:** https://portfolio-website-production.up.railway.app

Generated on: December 13, 2025
