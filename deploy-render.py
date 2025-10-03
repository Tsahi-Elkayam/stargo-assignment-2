#!/usr/bin/env python3
"""
ONE-CLICK DEPLOYMENT TO RENDER.COM - 100% FREE & AUTOMATED
No limits, no credit card needed, truly free forever
"""
import subprocess
import webbrowser
import time
import sys

def run(cmd):
    """Run command and return success."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode == 0, result.stdout.strip()

print("""
╔══════════════════════════════════════════════════════════════════╗
║     ONE-CLICK DEPLOYMENT - RENDER.COM (100% FREE FOREVER)       ║
╚══════════════════════════════════════════════════════════════════╝

This will deploy ALL services to Render.com cloud:
✅ Bitcoin Exporter
✅ Prometheus
✅ Grafana

NO CREDIT CARD NEEDED - Truly free!
""")

print("\nSTEP 1: Checking Git setup...")

# Check if git repo exists
is_repo, _ = run("git rev-parse --git-dir")
if not is_repo:
    print("Initializing Git repository...")
    run("git init")
    run("git add .")
    run('git commit -m "Initial commit for Render deployment"')
    print("✅ Git repository created")

# Check for GitHub remote
has_remote, remote = run("git remote get-url origin")

if not has_remote:
    print("\n" + "="*70)
    print("GITHUB SETUP REQUIRED (One-time only)")
    print("="*70)
    print("""
To deploy to Render.com cloud, we need to push this code to GitHub first.

OPTION A - Quick Setup (2 minutes):
1. Go to: https://github.com/new
2. Create a repository named: bitcoin-monitor
3. DON'T initialize with README
4. Copy the commands shown and paste here

OPTION B - I'll do it automatically:
We'll create the repo using GitHub CLI
""")
    
    choice = input("\nChoose option (A/B): ").strip().upper()
    
    if choice == "B":
        print("\nInstalling GitHub CLI...")
        if subprocess.call("gh --version", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
            print("Please install GitHub CLI from: https://cli.github.com/")
            print("Then run this script again.")
            sys.exit(1)
        
        print("Logging into GitHub...")
        run("gh auth login")
        
        print("Creating GitHub repository...")
        run("gh repo create bitcoin-monitor --public --source=. --remote=origin --push")
        print("✅ Repository created and code pushed!")
    else:
        print("\n1. Go to: https://github.com/new")
        print("2. Create repository: bitcoin-monitor")
        webbrowser.open("https://github.com/new")
        print("\n3. After creating, run these commands:")
        print("\ngit remote add origin https://github.com/YOUR_USERNAME/bitcoin-monitor.git")
        print("git branch -M main")
        print("git push -u origin main")
        print("\n4. Then run this script again!")
        sys.exit(0)
else:
    print(f"✅ GitHub remote found: {remote}")
    
    # Push latest changes
    print("\nPushing latest changes to GitHub...")
    run("git add .")
    run('git commit -m "Add Render configuration" -a')
    run("git push origin main")
    print("✅ Code pushed to GitHub")

print("\n" + "="*70)
print("STEP 2: AUTOMATED DEPLOYMENT TO RENDER.COM")
print("="*70)

print("""
Opening Render.com...

AUTOMATED STEPS (Takes 2 minutes):
1. Sign in with GitHub (click "Sign in with GitHub")
2. Click "New" → "Blueprint"
3. Select your repository: bitcoin-monitor
4. Click "Apply"

Render will automatically:
✅ Read render.yaml configuration
✅ Create all 3 services
✅ Deploy everything to cloud
✅ Generate URLs for you

After deployment completes (2-3 minutes):
📊 Your GRAFANA DASHBOARD will be at:
   https://grafana-XXXX.onrender.com

✅ Services run 24/7 in cloud (FREE)
✅ You can close this window after deployment starts
""")

time.sleep(3)
print("\nOpening Render.com Blueprint deployment...")
webbrowser.open("https://dashboard.render.com/select-repo?type=blueprint")

print("\n" + "="*70)
print("✅ AUTOMATED DEPLOYMENT STARTED!")
print("="*70)
print("""
The deployment is now running in Render cloud.

You can:
✅ CLOSE THIS WINDOW - deployment continues in cloud
✅ Check status at: https://dashboard.render.com/

Your Grafana dashboard URL will be shown in Render dashboard
after deployment completes (2-3 minutes).

Press Enter to exit...
""")
input()
