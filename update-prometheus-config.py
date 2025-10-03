#!/usr/bin/env python3
"""
Get Bitcoin Exporter URL and update Prometheus config
"""
import subprocess
import re

print("📊 Getting Bitcoin Exporter URL...")

# Get the exporter URL
result = subprocess.run("railway domain", shell=True, capture_output=True, text=True)
url = result.stdout.strip()

if url and "railway.app" in url:
    print(f"✅ Found exporter URL: {url}")
    
    # Update prometheus config
    with open("prometheus-railway.yml", "r") as f:
        content = f.read()
    
    # Replace the targets line
    content = re.sub(
        r"- targets: \['[^']+'\]",
        f"- targets: ['{url}']",
        content
    )
    
    with open("prometheus-railway.yml", "w") as f:
        f.write(content)
    
    print("✅ Updated prometheus-railway.yml with correct URL")
    print("\nNow you can deploy Prometheus and it will scrape your exporter!")
else:
    print("❌ Could not get exporter URL. Make sure you're linked to the exporter service.")
    print("Run: railway link (select stargo-assignment-2)")
