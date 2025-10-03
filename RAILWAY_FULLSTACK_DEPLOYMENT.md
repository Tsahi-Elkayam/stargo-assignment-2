# 🚀 RAILWAY FULL STACK DEPLOYMENT GUIDE

## Deploy Bitcoin Monitor + Prometheus + Grafana to Railway

### ⚠️ IMPORTANT: Railway Pricing
- Each service costs ~$5/month
- 3 services = ~$15/month
- First $5 is free

---

## 📋 Quick Deployment Steps

### Step 1: Open Railway Dashboard
Go to: https://railway.app/project/788de3a1-37c8-4ab0-abeb-7afb1120be07

---

### Step 2: Deploy Prometheus

#### A. Create Service:
1. Click **"+ New"** → **"Empty Service"**
2. Name it: **prometheus**

#### B. Add Variables:
Click on prometheus service → Variables → Add:
```
RAILWAY_DOCKERFILE_PATH=Dockerfile.prometheus
```

#### C. Connect GitHub:
1. Go to Settings → Source
2. Connect your GitHub repo
3. Railway will auto-deploy

---

### Step 3: Deploy Grafana

#### A. Create Service:
1. Click **"+ New"** → **"Empty Service"** 
2. Name it: **grafana**

#### B. Add Variables:
Click on grafana service → Variables → Add:
```
RAILWAY_DOCKERFILE_PATH=Dockerfile.grafana
GF_SERVER_HTTP_PORT=${PORT}
GF_AUTH_ANONYMOUS_ENABLED=true
GF_AUTH_ANONYMOUS_ORG_ROLE=Admin
GF_AUTH_DISABLE_LOGIN_FORM=true
```

#### C. Connect GitHub:
1. Go to Settings → Source
2. Connect your GitHub repo
3. Railway will auto-deploy

---

### Step 4: Update Prometheus Config

Update `prometheus-railway.yml`:
```yaml
global:
  scrape_interval: 60s

scrape_configs:
  - job_name: 'bitcoin-exporter'
    static_configs:
      # Use your exporter's public URL
      - targets: ['stargo-assignment-2-production.up.railway.app']
```

Push to GitHub to trigger redeploy.

---

### Step 5: Generate Domains

For each service, generate public URLs:

```bash
# For Prometheus
railway link
# Select: prometheus
railway domain

# For Grafana  
railway link
# Select: grafana
railway domain
```

---

## 🎉 Access Your Services

After deployment:
- **Grafana**: https://[grafana-url].railway.app
- **Prometheus**: https://[prometheus-url].railway.app
- **Exporter**: https://[exporter-url].railway.app/metrics

---

## 🔧 Troubleshooting

If services can't communicate:
1. Use public URLs instead of internal domains
2. Update datasource configs
3. Check Railway logs for each service

---

## 💡 Alternative: Use Railway Templates

Search Railway templates for:
- "Prometheus + Grafana Stack"
- Deploy with one click
- Auto-configured
