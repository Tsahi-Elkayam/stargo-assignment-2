#!/usr/bin/env python3
"""
Simple One-Click Deployment to Render.com
Free forever - No credit card required
"""
import subprocess
import webbrowser
import sys
import os

# Change to project root directory
os.chdir('..')

print("""
╔══════════════════════════════════════════════════════════════════╗
║              DEPLOY TO CLOUD - 100% FREE                         ║
╚══════════════════════════════════════════════════════════════════╝

Deploying Bitcoin Monitor to Render.com:
✅ Bitcoin Price Exporter
✅ Prometheus Metrics
✅ Grafana Dashboard

Cost: $0 forever
Time: 3 minutes
""")

def run(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode == 0

# Check Git setup
print("\n[1/3] Checking repository...")
if not run("git rev-parse --git-dir"):
    print("Initializing Git...")
    run("git init")
    run("git add .")
    run('git commit -m "Initial commit"')

# Check GitHub remote
has_remote = run("git remote get-url origin")

if not has_remote:
    print("\n⚠️  GitHub Setup Required (One-time)")
    print("\n1. Go to: https://github.com/new")
    print("2. Create repository: bitcoin-monitor")
    print("3. Run these commands:\n")
    print("   git remote add origin https://github.com/YOUR_USERNAME/bitcoin-monitor.git")
    print("   git branch -M main")
    print("   git push -u origin main\n")
    print("4. Then run cloud-deploy/DEPLOY.bat again")
    
    webbrowser.open("https://github.com/new")
    input("\nPress Enter after pushing to GitHub...")
    sys.exit(0)

# Push to GitHub
print("\n[2/3] Pushing to GitHub...")
run("git add .")
run('git commit -m "Deploy to Render" --allow-empty')
run("git push origin main")
print("✅ Code synced to GitHub")

# Deploy to Render
print("\n[3/3] Deploying to Render.com...")
print("""
Your browser will open. Follow these 3 steps:

1. Sign in with GitHub
2. Click "New" → "Blueprint"  
3. Select your repository and click "Apply"

Render will automatically deploy all 3 services!

After 2-3 minutes, your Grafana dashboard will be at:
📊 https://grafana-XXXX.onrender.com
""")

input("\nPress Enter to open Render...")
webbrowser.open("https://dashboard.render.com/select-repo?type=blueprint")

print("\n✅ Deployment started in cloud!")
print("✅ You can close this window")
print("\nView your services at: https://dashboard.render.com")
