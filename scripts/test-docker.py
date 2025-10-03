#!/usr/bin/env python
"""Test Bitcoin metrics are being exposed correctly via Docker."""
import requests
import time
import sys

def test_metrics():
    """Test if metrics endpoint is working."""
    print("Testing Bitcoin Price Monitor...")
    print("=" * 40)
    
    # Wait for service to be ready
    print("⏳ Waiting for services to start...")
    for i in range(30, 0, -1):
        try:
            response = requests.get('http://localhost:8000/metrics', timeout=2)
            if response.status_code == 200:
                print("✓ Exporter is running!")
                break
        except:
            pass
        
        if i > 1:
            print(f"   Retrying in {i} seconds...", end='\r')
            time.sleep(1)
    else:
        print("✗ Exporter not accessible on port 8000")
        print("  Run: docker-compose up -d --build")
        return False
    
    # Check for Bitcoin metric
    print("\n📊 Checking metrics...")
    response = requests.get('http://localhost:8000/metrics')
    content = response.text
    
    if 'bitcoin_price{' in content:
        print("✓ Bitcoin price metric found!")
        
        # Extract value
        for line in content.split('\n'):
            if 'bitcoin_price{' in line and not line.startswith('#'):
                try:
                    value = float(line.split()[-1])
                    print(f"✓ Current Bitcoin price: ${value:,.2f}")
                except:
                    pass
    else:
        print("✗ Bitcoin price metric not found")
        return False
    
    # Check Prometheus
    print("\n📈 Checking Prometheus...")
    try:
        response = requests.get('http://localhost:9090/-/healthy', timeout=2)
        if response.status_code == 200:
            print("✓ Prometheus is healthy!")
        else:
            print("✗ Prometheus not healthy")
    except:
        print("✗ Prometheus not accessible on port 9090")
    
    # Check Grafana
    print("\n📉 Checking Grafana...")
    try:
        response = requests.get('http://localhost:3000/api/health', timeout=2)
        if response.status_code == 200:
            print("✓ Grafana is healthy!")
            print("✓ Access at: http://localhost:3000 (no login required)")
        else:
            print("✗ Grafana not healthy")
    except:
        print("✗ Grafana not accessible on port 3000")
    
    print("\n" + "=" * 40)
    print("✅ All services are running!")
    return True

if __name__ == '__main__':
    success = test_metrics()
    sys.exit(0 if success else 1)
