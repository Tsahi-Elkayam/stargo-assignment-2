#!/usr/bin/env python3
"""
Health check script for Bitcoin Price Monitor.
Returns 0 if all services are healthy, 1 otherwise.
"""
import requests
import sys
import json
from datetime import datetime


def check_service(name, url, expected_content=None):
    """Check if a service is healthy."""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            if expected_content and expected_content not in response.text:
                return False, f"Missing expected content: {expected_content}"
            return True, "OK"
        else:
            return False, f"HTTP {response.status_code}"
    except requests.exceptions.ConnectionError:
        return False, "Connection failed"
    except requests.exceptions.Timeout:
        return False, "Timeout"
    except Exception as e:
        return False, str(e)


def main():
    """Run health checks on all services."""
    print(f"🏥 Bitcoin Price Monitor Health Check - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    checks = [
        ("Bitcoin Exporter Metrics", "http://localhost:8000/metrics", "bitcoin_price"),
        ("Bitcoin Exporter Health", "http://localhost:8000/health", "healthy"),
        ("Prometheus", "http://localhost:9090/-/healthy", None),
        ("Grafana", "http://localhost:3000/api/health", None),
    ]
    
    all_healthy = True
    results = []
    
    for service_name, url, expected_content in checks:
        healthy, message = check_service(service_name, url, expected_content)
        results.append({
            "service": service_name,
            "healthy": healthy,
            "message": message,
            "url": url
        })
        
        status_icon = "✅" if healthy else "❌"
        print(f"{status_icon} {service_name:30} {message}")
        
        if not healthy:
            all_healthy = False
    
    print("=" * 60)
    
    # Check Bitcoin price value
    try:
        response = requests.get("http://localhost:8000/metrics", timeout=5)
        if response.status_code == 200:
            for line in response.text.split('\n'):
                if line.startswith('bitcoin_price{') and not line.startswith('#'):
                    try:
                        value = float(line.split()[-1])
                        print(f"💰 Current Bitcoin Price: ${value:,.2f}")
                    except:
                        pass
    except:
        pass
    
    # Summary
    healthy_count = sum(1 for r in results if r["healthy"])
    total_count = len(results)
    
    if all_healthy:
        print(f"\n✅ All {total_count} services are healthy!")
        return 0
    else:
        print(f"\n⚠️  {healthy_count}/{total_count} services are healthy")
        print("\nFailed services:")
        for result in results:
            if not result["healthy"]:
                print(f"  - {result['service']}: {result['message']}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
