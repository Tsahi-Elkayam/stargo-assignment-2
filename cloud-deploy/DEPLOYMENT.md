# 🚀 Cloud Deployment Guide

Deploy Bitcoin Monitor to the cloud in 3 minutes - **100% FREE forever**.

## Quick Start

### Option 1: One-Click Deployment (Recommended)

1. Run: **`DEPLOY.bat`**
2. Follow the 3 simple steps
3. Done!

### Option 2: Local Development

```bash
docker-compose -f docker/docker-compose.yml up
```

Access at:
- Grafana: http://localhost:3000
- Prometheus: http://localhost:9090
- Metrics: http://localhost:8000/metrics

---

## Cloud Deployment (Render.com)

### Prerequisites
- GitHub account (free)
- 5 minutes of time

### Steps

1. **Run the deployment script:**
   ```bash
   DEPLOY.bat
   ```

2. **First-time GitHub setup** (if needed):
   - Script opens GitHub
   - Create repository: `bitcoin-monitor`
   - Push code (commands provided by script)
   - Run `DEPLOY.bat` again

3. **Deploy to Render:**
   - Browser opens automatically
   - Sign in with GitHub
   - Click "New" → "Blueprint"
   - Select your repository
   - Click "Apply"

4. **Wait 2-3 minutes** for deployment

5. **Access your dashboard:**
   - Grafana: `https://grafana-XXXX.onrender.com`
   - View URL in Render dashboard

---

## What Gets Deployed

✅ **Bitcoin Exporter** - Fetches BTC price every 60 seconds  
✅ **Prometheus** - Stores metrics data  
✅ **Grafana** - Beautiful dashboard with charts

All services run 24/7 in the cloud - **FREE forever**!

---

## After Deployment

### Services will:
- Run 24/7 in Render cloud
- Auto-restart if they crash
- Sleep after 15 min inactivity (free tier)
- Wake up automatically on first request

### Your URLs:
Check your Render dashboard for the exact URLs.

---

## Troubleshooting

**"No GitHub remote found"**
- Push your code to GitHub first
- Script will guide you through setup

**"Services not showing in Render"**
- Make sure `render.yaml` exists in root directory
- Check Render dashboard for error logs

**Need help?**
- Check Render logs in dashboard
- Ensure all Dockerfiles are present

---

## Cost

**$0 forever** on Render.com free tier
- Unlimited services
- 750 hours/month per service
- Services sleep when inactive

---

## Clean Up

To remove all services:
1. Go to Render dashboard
2. Delete each service individually

---

That's it! Simple, clean, and free. 🎉
