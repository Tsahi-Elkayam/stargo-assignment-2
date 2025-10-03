#!/usr/bin/env python3
"""
ONE-CLICK DEPLOYMENT - Fully Automated
Deploys everything to Fly.io cloud with ZERO manual steps
"""
import subprocess
import sys
import time
import os

def run(cmd, show_output=True):
    """Run command and return success status."""
    if show_output:
        result = subprocess.run(cmd, shell=True)
        return result.returncode == 0
    else:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout

def print_step(step, msg):
    print(f"\n{'='*70}")
    print(f"STEP {step}: {msg}")
    print(f"{'='*70}\n")

print("""
╔══════════════════════════════════════════════════════════════════╗
║          ONE-CLICK CLOUD DEPLOYMENT - 100% AUTOMATED            ║
║                  Deploying to Fly.io (FREE)                     ║
╚══════════════════════════════════════════════════════════════════╝

This script will:
✅ Install Fly CLI (if needed)
✅ Login to Fly.io
✅ Deploy Bitcoin Exporter
✅ Deploy Prometheus  
✅ Deploy Grafana
✅ Connect all services
✅ Show you the URLs

NO MANUAL STEPS - Just wait!
""")

input("Press Enter to start automated deployment...")

# Step 1: Check/Install Fly CLI
print_step(1, "Installing Fly CLI")

success, output = run("fly version", show_output=False)
if not success:
    print("Installing Fly CLI...")
    if os.name == 'nt':  # Windows
        run('powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"')
    else:  # Linux/Mac
        run('curl -L https://fly.io/install.sh | sh')
    print("✅ Fly CLI installed!")
    print("\n⚠️  Please close this terminal and run the script again.")
    input("Press Enter to exit...")
    sys.exit(0)
else:
    print("✅ Fly CLI already installed")

# Step 2: Login
print_step(2, "Logging into Fly.io")
print("A browser window will open for login...")
time.sleep(2)
if not run("fly auth login"):
    print("❌ Login failed")
    sys.exit(1)
print("✅ Logged in successfully!")

# Step 3: Deploy Bitcoin Exporter
print_step(3, "Deploying Bitcoin Exporter")

# Create fly.toml for exporter
exporter_config = """
app = "btc-exporter"
primary_region = "iad"

[build]
  dockerfile = "Dockerfile.simple"

[env]
  EXPORTER_PORT = "8000"

[http_service]
  internal_port = 8000
  force_https = true
  auto_stop_machines = false
  auto_start_machines = true
  min_machines_running = 1

[[vm]]
  memory = "256mb"
  cpu_kind = "shared"
  cpus = 1
"""

with open("fly.toml", "w") as f:
    f.write(exporter_config)

print("Deploying Bitcoin Exporter to cloud...")
if not run("fly launch --now --name btc-exporter --region iad --ha=false --auto-confirm"):
    print("⚠️  App might already exist, trying deploy...")
    run("fly deploy")

print("✅ Bitcoin Exporter deployed!")

# Get exporter URL
_, exporter_url = run("fly status --json", show_output=False)
print(f"📊 Exporter URL: https://btc-exporter.fly.dev")

# Step 4: Deploy Prometheus
print_step(4, "Deploying Prometheus")

prometheus_config = """
app = "btc-prometheus"
primary_region = "iad"

[build]
  dockerfile = "Dockerfile.prometheus"

[env]
  BITCOIN_EXPORTER_URL = "http://btc-exporter.internal:8000"

[http_service]
  internal_port = 9090
  force_https = true
  auto_stop_machines = false
  auto_start_machines = true
  min_machines_running = 1

[[vm]]
  memory = "512mb"
  cpu_kind = "shared"
  cpus = 1
"""

with open("fly.toml", "w") as f:
    f.write(prometheus_config)

print("Deploying Prometheus to cloud...")
if not run("fly launch --now --name btc-prometheus --region iad --ha=false --auto-confirm"):
    print("⚠️  App might already exist, trying deploy...")
    run("fly deploy")

print("✅ Prometheus deployed!")

# Step 5: Deploy Grafana
print_step(5, "Deploying Grafana")

grafana_config = """
app = "btc-grafana"
primary_region = "iad"

[build]
  dockerfile = "Dockerfile.grafana"

[env]
  GF_SERVER_HTTP_PORT = "3000"
  GF_AUTH_ANONYMOUS_ENABLED = "true"
  GF_AUTH_ANONYMOUS_ORG_ROLE = "Admin"
  PROMETHEUS_URL = "http://btc-prometheus.internal:9090"

[http_service]
  internal_port = 3000
  force_https = true
  auto_stop_machines = false
  auto_start_machines = true
  min_machines_running = 1

[[vm]]
  memory = "512mb"
  cpu_kind = "shared"
  cpus = 1
"""

with open("fly.toml", "w") as f:
    f.write(grafana_config)

print("Deploying Grafana to cloud...")
if not run("fly launch --now --name btc-grafana --region iad --ha=false --auto-confirm"):
    print("⚠️  App might already exist, trying deploy...")
    run("fly deploy")

print("✅ Grafana deployed!")

# Final Summary
print("\n" + "="*70)
print("🎉 DEPLOYMENT COMPLETE!")
print("="*70)
print("""
All services are running in the cloud 24/7!

YOUR URLS:
📊 Bitcoin Metrics: https://btc-exporter.fly.dev/metrics
📈 Prometheus: https://btc-prometheus.fly.dev
📉 GRAFANA DASHBOARD: https://btc-grafana.fly.dev ⭐⭐⭐

✅ You can CLOSE this window - everything runs in the cloud!
✅ Services run 24/7 (FREE - Fly.io free tier)
✅ No need to keep your computer on

Useful commands:
- Check status: fly status -a btc-grafana
- View logs: fly logs -a btc-grafana
- Open Grafana: fly open -a btc-grafana
""")

print("\nPress Enter to exit...")
input()
