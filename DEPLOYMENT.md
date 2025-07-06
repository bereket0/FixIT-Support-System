# FixIT Deployment Guide

This guide will help you deploy your FixIT application to various hosting platforms.

## 🚀 Quick Deploy to Render (Recommended)

### Step 1: Prepare Your Repository
1. Make sure all changes are committed and pushed to GitHub
2. Your repository should be at: `https://github.com/bereket0/FixIT-Support-System`

### Step 2: Deploy to Render
1. Go to [render.com](https://render.com) and sign up/login
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account and select your repository
4. Configure the service:

**Basic Settings:**
- **Name:** `fixit-support-system`
- **Environment:** `Python 3`
- **Region:** Choose closest to your users
- **Branch:** `main`

**Build & Deploy:**
- **Build Command:** `./build.sh`
- **Start Command:** `gunicorn fixit.wsgi:application`
- **Plan:** `Free` (or choose paid for better performance)

**Environment Variables:**
```
DEBUG=False
SECRET_KEY=gcg@*+a9oiby!2e(^0^jazsx(q3q1)f6cgay$%&j-p3v2h1!lz
DATABASE_URL=sqlite:///db.sqlite3
```

### Step 3: Access Your Application
- Your app will be available at: `https://your-app-name.onrender.com`
- The deployment process takes 5-10 minutes

## 🔧 Alternative Deployment Options

### Railway
1. Go to [railway.app](https://railway.app)
2. Connect your GitHub repository
3. Use the same build and start commands as Render
4. Add the same environment variables

### PythonAnywhere
1. Sign up at [pythonanywhere.com](https://pythonanywhere.com)
2. Upload your code or clone from GitHub
3. Set up a virtual environment
4. Install requirements: `pip install -r requirements.txt`
5. Configure WSGI file
6. Set environment variables

### Heroku
1. Install Heroku CLI
2. Create a new Heroku app
3. Add PostgreSQL addon
4. Deploy using Git: `git push heroku main`
5. Set environment variables in Heroku dashboard

## 🔐 Security Configuration

### Generate a New Secret Key
```bash
python manage.py generate_secret_key
```

### Environment Variables for Production
```bash
DEBUG=False
SECRET_KEY=your_generated_secret_key_here
DATABASE_URL=your_database_url_here
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
```

## 📊 Database Setup

### SQLite (Development/Simple)
- No additional setup required
- Data stored in `db.sqlite3` file

### PostgreSQL (Production Recommended)
1. Set up PostgreSQL database
2. Update `DATABASE_URL` environment variable
3. Run migrations: `python manage.py migrate`

## 🛠️ Troubleshooting

### Common Issues

**Build Fails:**
- Check that all dependencies are in `requirements.txt`
- Ensure `build.sh` has execute permissions
- Verify Python version compatibility

**Static Files Not Loading:**
- Run `python manage.py collectstatic`
- Check `STATIC_ROOT` and `STATIC_URL` settings
- Verify WhiteNoise middleware is configured

**Database Connection Issues:**
- Check `DATABASE_URL` format
- Ensure database is accessible from your hosting provider
- Verify database credentials

**500 Server Errors:**
- Check application logs
- Verify all environment variables are set
- Ensure `DEBUG=False` in production

### Logs and Debugging
- Check your hosting provider's log viewer
- Use Django's logging configuration
- Monitor application performance

## 📈 Performance Optimization

### For Production
1. Use a production database (PostgreSQL)
2. Enable caching (Redis/Memcached)
3. Use CDN for static files
4. Optimize database queries
5. Enable compression

### Monitoring
- Set up error tracking (Sentry)
- Monitor application performance
- Set up uptime monitoring
- Configure backup strategies

## 🔄 Continuous Deployment

### Automatic Deployments
- Connect your GitHub repository
- Enable automatic deployments on push
- Set up staging environment
- Configure deployment notifications

### Manual Deployments
```bash
# Update code
git add .
git commit -m "Update for deployment"
git push origin main

# Deploy (if using Heroku)
git push heroku main
```

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review your hosting provider's documentation
3. Check Django deployment documentation
4. Contact your hosting provider's support

## 🎉 Success!

Once deployed, your FixIT application will be accessible online and ready to help your organization manage IT support tickets, share tech tips, and conduct quizzes! 