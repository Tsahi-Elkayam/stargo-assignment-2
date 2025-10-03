#!/usr/bin/env python3
"""
Deploy Full Stack (Exporter + Prometheus + Grafana) to Railway
This script will guide you through deploying all services.
"""
import subprocess
import time
import sys
import json

def run_cmd(cmd, capture=False):
    """Run command and return output."""
    if capture:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    else:
        return subprocess.run(cmd, shell=True)

def print_section(title):
    """Print formatted section header."""
    print(f"\n{'='*60}")
    print(f"🚂 {title}")
    print('='*60)

print("""
╔══════════════════════════════════════════════════════════╗
║     RAILWAY FULL STACK DEPLOYMENT                       ║
║     Bitcoin Exporter + Prometheus + Grafana             ║
╚══════════════════════════════════════════════════════════╝
""")

# Check if logged in
print("Checking Railway login...")
result = run_cmd("railway whoami", capture=True)
if "Logged in as" not in result:
    print("❌ Not logged in to Railway. Please run: railway login")
    sys.exit(1)
print(f"✅ {result}")

print_section("DEPLOYMENT PLAN")
print("""
We will deploy 3 services to Railway:
1. Bitcoin Exporter (already running) ✅
2. Prometheus (metrics storage)
3. Grafana (visualization)

Each service will be a separate Railway service in your project.
They will communicate via Railway's internal network.
""")

input("\nPress Enter to continue...")

# Step 1: Check existing services
print_section("Step 1: Current Project Status")
print("Your project: stargo-assignment-2")
print("Project ID: 788de3a1-37c8-4ab0-abeb-7afb1120be07")
print("\n✅ Bitcoin Exporter is already running")

exporter_url = run_cmd("railway domain", capture=True)
if exporter_url:
    print(f"📊 Exporter URL: {exporter_url}")

# Step 2: Deploy Prometheus
print_section("Step 2: Deploy Prometheus")
print("""
MANUAL STEPS REQUIRED:
1. Go to Railway Dashboard: https://railway.app/project/788de3a1-37c8-4ab0-abeb-7afb1120be07
2. Click the "+ New" button
3. Select "Empty Service"
4. Name it: prometheus
5. After creation, go to Settings → Source → Connect GitHub repo
6. Come back here and press Enter
""")

input("\nPress Enter after creating Prometheus service...")

print("\nPreparing Prometheus configuration...")

# Create railway.json for Prometheus
prometheus_config = {
    "build": {
        "builder": "DOCKERFILE",
        "dockerfilePath": "Dockerfile.prometheus"
    },
    "deploy": {
        "restartPolicyType": "ON_FAILURE"
    }
}

with open("railway-prometheus.json", "w") as f:
    json.dump(prometheus_config, f, indent=2)

print("✅ Created railway-prometheus.json")
print("\nNow deploying Prometheus...")

print("""
RUN THESE COMMANDS:
1. railway link
2. Select 'prometheus' service
3. railway up
""")

input("\nPress Enter after Prometheus is deployed...")

# Step 3: Deploy Grafana
print_section("Step 3: Deploy Grafana")
print("""
MANUAL STEPS REQUIRED:
1. Go back to Railway Dashboard
2. Click the "+ New" button again
3. Select "Empty Service"
4. Name it: grafana
5. After creation, go to Settings → Source → Connect GitHub repo
6. Come back here and press Enter
""")

input("\nPress Enter after creating Grafana service...")

print("\nPreparing Grafana configuration...")

# Create railway.json for Grafana
grafana_config = {
    "build": {
        "builder": "DOCKERFILE",
        "dockerfilePath": "Dockerfile.grafana"
    },
    "deploy": {
        "restartPolicyType": "ON_FAILURE"
    }
}

with open("railway-grafana.json", "w") as f:
    json.dump(grafana_config, f, indent=2)

print("✅ Created railway-grafana.json")
print("\nNow deploying Grafana...")

print("""
RUN THESE COMMANDS:
1. railway link
2. Select 'grafana' service
3. railway up
""")

input("\nPress Enter after Grafana is deployed...")

# Step 4: Configure and verify
print_section("Step 4: Configure Services")
print("""
FINAL CONFIGURATION:

1. Generate domains for each service:
   - railway link (select prometheus) → railway domain
   - railway link (select grafana) → railway domain

2. Your services will be available at:
   - Exporter: https://stargo-assignment-2-production.up.railway.app/metrics
   - Prometheus: https://prometheus-production.up.railway.app
   - Grafana: https://grafana-production.up.railway.app

3. Internal communication:
   - Services communicate via: servicename.railway.internal
""")

print_section("DEPLOYMENT COMPLETE!")
print("""
🎉 Your full monitoring stack should now be running on Railway!

📊 Access your services:
1. Grafana Dashboard (main UI): https://grafana-production.up.railway.app
2. Prometheus: https://prometheus-production.up.railway.app
3. Bitcoin Metrics: https://stargo-assignment-2-production.up.railway.app/metrics

⚠️ Note: Domain names might be slightly different. Use 'railway domain' to get exact URLs.

📝 Useful commands:
- railway logs (view logs for selected service)
- railway link (switch between services)
- railway domain (get public URL)
""")
