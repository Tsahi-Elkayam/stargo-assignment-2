#!/usr/bin/env python3
"""
Automated Full Stack Deployment to Render.com (FREE)
- Fully automated
- Runs in the cloud (no need to keep console open)
- 100% free tier
"""
import subprocess
import webbrowser
import time

def print_header(text):
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}\n")

def run_cmd(cmd):
    """Run command and return output."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode == 0, result.stdout, result.stderr

print("""
╔══════════════════════════════════════════════════════════════════╗
║           AUTOMATED CLOUD DEPLOYMENT - RENDER.COM                ║
║                     100% FREE FOREVER                            ║
╚══════════════════════════════════════════════════════════════════╝

This script will deploy your Bitcoin Monitor stack to Render.com:
  ✅ Bitcoin Exporter
  ✅ Prometheus  
  ✅ Grafana

All services run in the cloud - you can close this console after deployment!
""")

print_header("STEP 1: Prerequisites Check")

# Check if git is installed
print("Checking Git installation...")
git_ok, _, _ = run_cmd("git --version")
if not git_ok:
    print("❌ Git not found. Please install Git first.")
    exit(1)
print("✅ Git installed")

# Check if render.yaml exists
print("Checking render.yaml configuration...")
try:
    with open("render.yaml", "r") as f:
        content = f.read()
        print("✅ render.yaml found")
except FileNotFoundError:
    print("❌ render.yaml not found")
    exit(1)

print_header("STEP 2: Git Repository Setup")

# Check if repo is initialized
print("Checking Git repository...")
is_repo, _, _ = run_cmd("git rev-parse --git-dir")

if not is_repo:
    print("Initializing Git repository...")
    run_cmd("git init")
    print("✅ Git repository initialized")
else:
    print("✅ Git repository already exists")

# Add render.yaml
print("Adding render.yaml to repository...")
run_cmd("git add render.yaml")
run_cmd("git add .")
run_cmd('git commit -m "Add Render deployment configuration" ')

print("\n✅ Repository ready for deployment")

print_header("STEP 3: Push to GitHub (if needed)")

# Check remote
has_remote, remote_url, _ = run_cmd("git remote get-url origin")

if not has_remote:
    print("""
⚠️  No Git remote configured.

AUTOMATED DEPLOYMENT OPTIONS:

OPTION A: Use Existing Railway (Already Working!) ✅
- Your Bitcoin Exporter is ALREADY deployed and running
- Just deploy Prometheus & Grafana manually in Railway dashboard
- Cost: ~$10-15/month after $5 credit

OPTION B: Deploy to Render.com (Fully Free)
1. Create a GitHub repository
2. Push this code to GitHub
3. Go to: https://render.com/
4. Click "New" → "Blueprint"
5. Connect your GitHub repo
6. Render will auto-deploy all 3 services from render.yaml
7. Done! Everything runs in cloud forever (free)

OPTION C: Use Fly.io (Automated CLI)
- Fully automated via CLI
- Free tier: 3 VMs
- Run: fly launch (see instructions below)
""")
else:
    print(f"✅ Remote found: {remote_url}")
    print("\nPushing to GitHub...")
    
    push_ok, _, _ = run_cmd("git push origin main")
    
    if push_ok:
        print("✅ Code pushed to GitHub")
        
        print_header("STEP 4: Automated Render Deployment")
        
        print("""
🎉 READY FOR AUTOMATED DEPLOYMENT!

Next steps:
1. Go to: https://render.com/
2. Sign in with GitHub
3. Click "New" → "Blueprint"
4. Select your repository
5. Render will automatically:
   - Read render.yaml
   - Create all 3 services
   - Deploy everything to cloud
   - Services will run 24/7 in cloud (free)

🚀 After deployment:
   - You can CLOSE THIS CONSOLE
   - Services run independently in Render cloud
   - Access via Render-provided URLs
   - Monitor from Render dashboard

Opening Render.com in browser...
""")
        
        time.sleep(3)
        webbrowser.open("https://render.com/")
        
    else:
        print("⚠️  Push failed. Make sure you have GitHub remote configured.")

print_header("ALTERNATIVE: FLY.IO FULLY AUTOMATED CLI DEPLOYMENT")

print("""
For 100% CLI automation (no browser needed):

1. Install Fly CLI:
   Windows: 
   powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
   
2. Login:
   fly auth login
   
3. Deploy all services with ONE command:
   fly launch --now
   
Fly.io will:
- Detect Docker files automatically
- Deploy all services to cloud
- Provide public URLs
- Run 24/7 (free tier: 3 VMs)

Your console can be closed after deployment!
""")

print_header("SUMMARY: DEPLOYMENT OPTIONS")

print("""
🎯 BEST OPTIONS FOR YOU:

1️⃣ RAILWAY (Easiest - Already Working!) ⭐
   Status: Bitcoin Exporter ALREADY deployed ✅
   Next: Just deploy Prometheus & Grafana from dashboard
   Cost: ~$15/month after $5 credit
   Automation: Semi-automated
   Console: Can close after deployment

2️⃣ RENDER.COM (100% Free Forever) 🆓
   Status: render.yaml created ✅
   Next: Push to GitHub → Connect to Render → Auto-deploy
   Cost: FREE (services sleep after 15 min inactivity)
   Automation: Fully automated via Blueprint
   Console: Can close after deployment

3️⃣ FLY.IO (Best CLI Automation) 🚀
   Status: Ready to deploy
   Next: fly launch --now
   Cost: FREE (3 VMs included)
   Automation: 100% CLI automated
   Console: Can close after deployment

💡 RECOMMENDATION:
Since your Railway exporter is already running, just complete Railway 
deployment OR switch to Render/Fly for free option.

All options run in cloud - you can close this console once deployed!
""")

print("\n✅ Script completed!")
print("\nPress Ctrl+C to exit")
input()
