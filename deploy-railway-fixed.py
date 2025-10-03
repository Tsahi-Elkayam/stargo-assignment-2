#!/usr/bin/env python3
"""
Deploy to Railway - Fixed version
"""
import subprocess
import sys

print("🚂 Deploying to Railway with fixes...")
print("=" * 50)

# Remove PORT variable (Railway sets its own)
print("📝 Removing custom PORT variable (Railway sets its own)...")
subprocess.run("railway variables --remove PORT", shell=True)

print("\n✅ Fixed issues:")
print("1. Updated main.py to use Railway's PORT environment variable")
print("2. Created Dockerfile.railway for simpler deployment")
print("3. Updated railway.json to use new Dockerfile")
print("4. Removed custom PORT variable")

print("\n🚀 Now deploying...")
subprocess.run("railway up", shell=True)

print("\n📊 Getting deployment URL...")
subprocess.run("railway domain", shell=True)

print("\n✅ Deployment should work now!")
print("Check logs with: railway logs")
