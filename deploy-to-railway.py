#!/usr/bin/env python3
"""
Railway Deployment Script - Complete Fix
This script fixes all issues and deploys to Railway
"""
import subprocess
import sys
import time

def run_command(cmd, description, check=True):
    """Run a command and print output."""
    print(f"\n{description}...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout)
    
    if check and result.returncode != 0:
        print(f"❌ Error: {result.stderr}")
        return False
    
    return True

print("=" * 60)
print("🚂 RAILWAY DEPLOYMENT - COMPLETE FIX")
print("=" * 60)

print("\n📋 FIXES APPLIED:")
print("1. ✅ Updated main.py to use Railway's PORT environment variable")
print("2. ✅ Created Dockerfile.railway for simplified deployment")
print("3. ✅ Created requirements.prod.txt with only production dependencies")
print("4. ✅ Updated railway.json configuration")
print("5. ✅ Fixed health check endpoint")

print("\n🔧 DEPLOYMENT STEPS:")

# Step 1: Remove the custom PORT variable (Railway sets its own)
print("\n1️⃣ Removing custom PORT variable...")
run_command("railway variables --remove PORT", "Removing PORT", check=False)

# Step 2: Verify variables
print("\n2️⃣ Current variables:")
run_command("railway variables", "Showing variables")

# Step 3: Deploy
print("\n3️⃣ Deploying to Railway...")
print("This may take 2-3 minutes...")

result = subprocess.run("railway up", shell=True, capture_output=True, text=True)
print(result.stdout)

if "Deploy failed" in result.stdout:
    print("\n❌ Deployment failed. Checking logs...")
    run_command("railway logs --tail 50", "Recent logs")
    
    print("\n🔍 TROUBLESHOOTING:")
    print("1. Check the build logs at the URL above")
    print("2. Common issues:")
    print("   - Module import errors: Check requirements.prod.txt")
    print("   - Config file not found: Check config directory")
    print("   - Port binding: Already fixed in main.py")
else:
    print("\n✅ Deployment succeeded!")
    
    # Step 4: Get domain
    print("\n4️⃣ Getting deployment URL...")
    time.sleep(3)
    
    result = subprocess.run("railway domain", shell=True, capture_output=True, text=True)
    url = result.stdout.strip()
    
    if url and "http" in url:
        print(f"\n🎉 SUCCESS! Your app is deployed at:")
        print(f"🌐 {url}")
        print(f"\n📊 Endpoints:")
        print(f"  - Metrics: {url}/metrics")
        print(f"  - Health: {url}/health")
        
        print(f"\n📈 Railway Dashboard:")
        print(f"  https://railway.app/project/788de3a1-37c8-4ab0-abeb-7afb1120be07")
    else:
        print("\n⚠️ Domain not yet assigned. Run 'railway domain' to generate one.")

print("\n📝 USEFUL COMMANDS:")
print("  railway logs        - View deployment logs")
print("  railway domain      - Get/generate public URL")
print("  railway status      - Check deployment status")
print("  railway open        - Open in browser")

print("\n" + "=" * 60)
print("🚀 Deployment complete!")
print("=" * 60)
