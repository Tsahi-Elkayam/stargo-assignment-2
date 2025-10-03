# Cloud Deployment

Deploy Bitcoin Monitor to the cloud in 3 minutes - **100% FREE**.

## Quick Start

```bash
cd cloud-deploy
DEPLOY.bat
```

That's it!

## What's in this folder

```
cloud-deploy/
├── DEPLOY.bat              ⭐ Run this to deploy
├── deploy.py               (Deployment script)
├── DEPLOYMENT.md           (Detailed instructions)
├── render.yaml             (Cloud configuration)
├── Dockerfile.simple       (Bitcoin Exporter)
├── Dockerfile.prometheus   (Metrics storage)
└── Dockerfile.grafana      (Dashboard)
```

## After Deployment

Your Grafana dashboard: `https://grafana-XXXX.onrender.com`

See **DEPLOYMENT.md** for detailed instructions.
