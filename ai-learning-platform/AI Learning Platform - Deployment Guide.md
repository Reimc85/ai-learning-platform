# AI Learning Platform - Deployment Guide

## 🚀 Production Deployment Options

This guide covers multiple deployment strategies for your AI Learning Platform, from simple managed hosting to advanced cloud deployments.

## 📋 Prerequisites

- OpenAI API Key (get from [OpenAI Platform](https://platform.openai.com/))
- Git repository (GitHub, GitLab, or Bitbucket)
- Domain name (optional but recommended)

## 🎯 Quick Deployment (Recommended)

### Option 1: Railway (Backend + Database)

Railway provides the simplest deployment for full-stack applications.

1. **Prepare Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Deploy to Railway**
   - Go to [Railway.app](https://railway.app/)
   - Connect your GitHub repository
   - Railway will automatically detect the Python app
   - Set environment variables:
     - `OPENAI_API_KEY`: Your OpenAI API key
     - `SECRET_KEY`: A secure random string
   - Railway will provide a PostgreSQL database automatically

3. **Domain Setup**
   - Railway provides a free subdomain
   - Optional: Add your custom domain in Railway settings

### Option 2: Render (Backend) + Vercel (Frontend)

Split deployment for better performance and scaling.

#### Backend on Render:

1. **Deploy Backend**
   - Go to [Render.com](https://render.com/)
   - Create new Web Service from your repository
   - Use these settings:
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn app:app`
     - Environment Variables:
       - `OPENAI_API_KEY`: Your OpenAI API key
       - `SECRET_KEY`: A secure random string
   - Render provides free PostgreSQL database

#### Frontend on Vercel:

1. **Update Frontend Configuration**
   ```javascript
   // frontend/src/config/api.js
   const API_CONFIG = {
     production: 'https://your-backend-url.onrender.com/api',
     // ... rest of config
   };
   ```

2. **Deploy Frontend**
   - Go to [Vercel.com](https://vercel.com/)
   - Import your repository
   - Set build settings:
     - Framework: Vite
     - Root Directory: `frontend`
     - Build Command: `npm run build`
     - Output Directory: `dist`

### Option 3: Heroku (All-in-One)

1. **Install Heroku CLI**
2. **Deploy**
   ```bash
   heroku create your-app-name
   heroku config:set OPENAI_API_KEY=your_key_here
   heroku config:set SECRET_KEY=your_secret_key_here
   heroku addons:create heroku-postgresql:hobby-dev
   git push heroku main
   ```

## 🔧 Environment Variables

Set these environment variables in your hosting platform:

```env
# Required
OPENAI_API_KEY=sk-proj-your-openai-api-key
SECRET_KEY=your-secure-secret-key-minimum-32-characters

# Optional
DATABASE_URL=postgresql://user:pass@host:port/db
PORT=5000
FLASK_ENV=production
```

## 📁 File Structure for Deployment

```
ai_learning_platform/
├── app.py                 # Production Flask app
├── requirements.txt       # Python dependencies
├── Procfile              # Process configuration
├── .env.production       # Environment template
├── src/                  # Source code
│   ├── models/          # Database models
│   ├── routes/          # API routes
│   └── services/        # Business logic
└── frontend/
    ├── dist/            # Built frontend (auto-generated)
    ├── src/             # Frontend source
    └── package.json     # Frontend dependencies
```

## 🗄️ Database Setup

### Development (SQLite)
- Automatically created in `src/database/app.db`
- No additional setup required

### Production (PostgreSQL)
- Automatically provided by hosting platforms
- Database tables created automatically on first run
- Existing data can be migrated using standard SQL tools

## 🔐 Security Considerations

1. **Environment Variables**
   - Never commit API keys to version control
   - Use platform-specific environment variable systems
   - Generate strong secret keys (32+ characters)

2. **HTTPS**
   - All recommended platforms provide HTTPS by default
   - Ensure API calls use HTTPS in production

3. **CORS**
   - Currently set to allow all origins for development
   - In production, update CORS settings to specific domains

## 📊 Monitoring & Analytics

### Built-in Health Check
- Endpoint: `/api/health`
- Returns platform status and environment info

### Logging
- Application logs available through hosting platform dashboards
- Monitor API usage and errors

### Performance
- Built-in analytics endpoints provide learning metrics
- Monitor OpenAI API usage to manage costs

## 💰 Cost Estimation

### Free Tier Options:
- **Railway**: Free tier with 500 hours/month
- **Render**: Free tier with limitations
- **Vercel**: Generous free tier for frontend
- **Heroku**: Limited free tier (requires credit card)

### Paid Tier Costs (Monthly):
- **Hosting**: $5-20/month for basic production use
- **Database**: $5-15/month for managed PostgreSQL
- **OpenAI API**: Pay-per-use (typically $10-50/month depending on usage)

## 🚀 Deployment Checklist

- [ ] Repository pushed to Git provider
- [ ] OpenAI API key obtained
- [ ] Environment variables configured
- [ ] Frontend built successfully (`npm run build`)
- [ ] Backend tested locally
- [ ] Database connection verified
- [ ] Health check endpoint responding
- [ ] Custom domain configured (optional)
- [ ] HTTPS certificate active
- [ ] Analytics endpoints tested

## 🔄 Updates & Maintenance

### Automatic Deployments
- Most platforms support automatic deployment from Git
- Push to main branch triggers new deployment
- Zero-downtime deployments supported

### Manual Updates
```bash
git add .
git commit -m "Update description"
git push origin main
# Platform automatically deploys
```

### Database Migrations
- New tables/columns added automatically
- Backup database before major updates
- Test migrations in staging environment

## 🆘 Troubleshooting

### Common Issues:

1. **Database Connection Errors**
   - Verify DATABASE_URL environment variable
   - Check database service status
   - Ensure database exists and is accessible

2. **OpenAI API Errors**
   - Verify API key is correct and active
   - Check API quota and billing status
   - Monitor rate limits

3. **Frontend Not Loading**
   - Ensure frontend is built (`npm run build`)
   - Check API URL configuration
   - Verify CORS settings

4. **500 Internal Server Errors**
   - Check application logs
   - Verify all environment variables are set
   - Test endpoints individually

### Support Resources:
- Platform documentation (Railway, Render, Vercel)
- OpenAI API documentation
- Flask deployment guides
- React/Vite deployment guides

## 🎉 Success Metrics

After successful deployment, you should have:
- ✅ Public URL for your learning platform
- ✅ Working user registration and onboarding
- ✅ AI-powered content generation
- ✅ Learning analytics and progress tracking
- ✅ Responsive design on all devices
- ✅ Secure HTTPS connection
- ✅ Automated deployments from Git

Your AI Learning Platform is now ready to serve users worldwide! 🌍

