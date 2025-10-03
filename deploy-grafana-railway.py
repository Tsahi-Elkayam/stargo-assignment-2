#!/usr/bin/env python3
"""
Deploy Grafana to Railway as a separate service
"""
import subprocess
import json

print("🎨 Deploying Grafana to Railway...")
print("=" * 50)

# First, we need to create a new service for Grafana
print("\n1️⃣ Creating Grafana service in Railway...")
print("Go to your Railway dashboard:")
print("https://railway.app/project/788de3a1-37c8-4ab0-abeb-7afb1120be07")
print("\n📝 Steps:")
print("1. Click '+ New' button")
print("2. Select 'Deploy Template'")
print("3. Search for 'Grafana'")
print("4. Or select 'Docker Image'")
print("5. Enter: grafana/grafana:latest")

print("\n2️⃣ Set Grafana Environment Variables:")
print("Add these in the Railway dashboard:")

grafana_vars = {
    "GF_AUTH_ANONYMOUS_ENABLED": "true",
    "GF_AUTH_ANONYMOUS_ORG_ROLE": "Admin", 
    "GF_AUTH_DISABLE_LOGIN_FORM": "true",
    "GF_SERVER_HTTP_PORT": "${PORT}",
    "GF_SERVER_ROOT_URL": "https://${RAILWAY_STATIC_URL}"
}

print("\n```")
for key, value in grafana_vars.items():
    print(f"{key}={value}")
print("```")

print("\n3️⃣ After Grafana deploys, configure it:")
print("1. Get Grafana's public URL from Railway")
print("2. Access Grafana (no login required)")
print("3. Add Prometheus datasource:")
print("   - URL: Your Bitcoin exporter URL/metrics")
print("   - Or deploy Prometheus separately first")

print("\n" + "=" * 50)
print("📊 EASIER OPTION: Use Local Docker Instead!")
print("=" * 50)
print("\nRun locally with Docker for full stack:")
print("cd docker")
print("docker-compose up -d")
print("\nThen access:")
print("- Grafana: http://localhost:3000")
print("- Prometheus: http://localhost:9090")
print("- Exporter: http://localhost:8000/metrics")
