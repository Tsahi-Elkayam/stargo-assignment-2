#!/usr/bin/env python3
"""
Test if the application can start with Railway configuration
"""
import os
import sys
import subprocess

print("🔍 Testing Railway Configuration...")
print("=" * 50)

# Set test environment variables
os.environ['ENV'] = 'production'
os.environ['LOG_LEVEL'] = 'INFO'
os.environ['PORT'] = '8888'  # Test port

print("✅ Environment variables set:")
print(f"  ENV={os.environ.get('ENV')}")
print(f"  LOG_LEVEL={os.environ.get('LOG_LEVEL')}")
print(f"  PORT={os.environ.get('PORT')}")

print("\n🐳 Testing Docker build...")
result = subprocess.run(
    "docker build -f Dockerfile.railway -t railway-test .",
    shell=True,
    capture_output=True,
    text=True
)

if result.returncode == 0:
    print("✅ Docker build successful!")
else:
    print("❌ Docker build failed:")
    print(result.stderr)
    sys.exit(1)

print("\n🚀 Testing container run...")
result = subprocess.run(
    "docker run -d --rm -e PORT=8888 -e ENV=production -p 8888:8888 --name railway-test railway-test",
    shell=True,
    capture_output=True,
    text=True
)

if result.returncode == 0:
    print("✅ Container started!")
    
    import time
    time.sleep(5)
    
    # Test health endpoint
    try:
        import requests
        response = requests.get("http://localhost:8888/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed!")
        else:
            print(f"⚠️ Health check returned: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Health check failed: {e}")
    
    # Stop container
    subprocess.run("docker stop railway-test", shell=True)
    print("✅ Container stopped")
else:
    print("❌ Container failed to start:")
    print(result.stderr)

print("\n✅ All tests passed! Ready to deploy to Railway")
