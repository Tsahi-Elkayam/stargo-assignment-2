#!/usr/bin/env python3
"""
Simple setup script for Docker or Kubernetes
Usage: python setup.py --docker
       python setup.py --minikube
       python setup.py --clean
"""

import subprocess
import sys
import time
import os
import json
from time import sleep

try:
    import requests
except ImportError:
    print("Installing required packages...")
    subprocess.run([sys.executable, "-m", "pip", "install", "requests"], check=True)
    import requests

def run_with_retry(command, max_retries=3, delay=5, description="operation"):
    """Run command with retry mechanism"""
    for attempt in range(max_retries):
        print(f"Attempt {attempt + 1}/{max_retries}: {description}")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            return True
        
        error_msg = result.stderr.lower()
        if 'tls' in error_msg or 'bad record' in error_msg or 'connection' in error_msg:
            print(f"Network/TLS error detected. Retrying in {delay} seconds...")
            if attempt < max_retries - 1:
                sleep(delay)
                continue
        else:
            print(f"Command failed: {result.stderr}")
            break
    
    return False

def wait_for_service(url, service_name, max_wait=60):
    """Wait for service to be ready"""
    print(f"Waiting for {service_name} to be ready...")
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        try:
            response = requests.get(url, timeout=2)
            if response.status_code in [200, 302, 401]:  # Service is responding
                print(f"{service_name} is ready!")
                return True
        except:
            pass
        sleep(2)
    
    print(f"Warning: {service_name} not responding after {max_wait}s")
    return False

def setup_grafana_dashboard():
    """Setup Grafana dashboard with retry"""
    max_retries = 5
    
    for attempt in range(max_retries):
        try:
            print(f"Loading dashboard (attempt {attempt + 1}/{max_retries})...")
            
            # First ensure Grafana is ready
            grafana_ready = wait_for_service("http://localhost:3000", "Grafana", 30)
            
            if grafana_ready:
                # Add datasource
                datasource_payload = {
                    "name": "Prometheus",
                    "type": "prometheus",
                    "url": "http://prometheus:9090",
                    "access": "proxy",
                    "isDefault": True
                }
                
                response = requests.post(
                    "http://localhost:3000/api/datasources",
                    json=datasource_payload,
                    headers={"Content-Type": "application/json"},
                    auth=("admin", "admin")
                )
                
                if response.status_code in [200, 409]:  # 409 means already exists
                    print("Dashboard loaded successfully!")
                    return True
                    
        except Exception as e:
            print(f"Dashboard loading error: {e}")
        
        if attempt < max_retries - 1:
            print(f"Retrying in 5 seconds...")
            sleep(5)
    
    print("Warning: Could not load dashboard, but services are running")
    return False

def setup_docker():
    """Setup with Docker Compose"""
    print("Starting Docker Compose setup...")
    
    # Pull images with retry
    if not run_with_retry(
        "cd docker && docker-compose pull",
        max_retries=3,
        description="Pulling Docker images"
    ):
        print("Warning: Image pull had issues, trying to continue...")
    
    # Start services with retry
    if not run_with_retry(
        "cd docker && docker-compose up -d --build",
        max_retries=3,
        description="Starting Docker Compose"
    ):
        print("Error: Failed to start Docker Compose")
        sys.exit(1)
    
    # Wait for services to be ready
    print("\nWaiting for services to start...")
    sleep(5)
    
    services_ready = [
        wait_for_service("http://localhost:8000/metrics", "Bitcoin Exporter"),
        wait_for_service("http://localhost:9090", "Prometheus"),
        wait_for_service("http://localhost:3000", "Grafana")
    ]
    
    if all(services_ready):
        # Try to setup dashboard
        setup_grafana_dashboard()
        
        print("\nSetup complete! Access at:")
        print("  Bitcoin Exporter: http://localhost:8000/metrics")
        print("  Prometheus: http://localhost:9090")
        print("  Grafana: http://localhost:3000 (admin/admin)")
    else:
        print("\nWarning: Some services may not be ready. Check logs with:")
        print("  docker-compose -f docker/docker-compose.yml logs")

def wait_for_pods(namespace, timeout=300):
    """Wait for all pods in namespace to be ready"""
    print(f"Waiting for pods in namespace '{namespace}' to be ready...")
    start_time = time.time()

    while time.time() - start_time < timeout:
        result = subprocess.run(
            f"kubectl get pods -n {namespace} -o json",
            shell=True,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            try:
                pods = json.loads(result.stdout)
                if not pods.get('items'):
                    print("  No pods found yet, waiting...")
                    sleep(5)
                    continue

                all_ready = True
                for pod in pods['items']:
                    pod_name = pod['metadata']['name']
                    status = pod.get('status', {})
                    phase = status.get('phase', 'Unknown')

                    if phase != 'Running':
                        all_ready = False
                        print(f"  {pod_name}: {phase}")
                        break

                    conditions = status.get('conditions', [])
                    ready = False
                    for condition in conditions:
                        if condition.get('type') == 'Ready':
                            ready = condition.get('status') == 'True'
                            break

                    if not ready:
                        all_ready = False
                        print(f"  {pod_name}: Running but not ready")
                        break

                if all_ready:
                    print(f"[OK] All pods are ready!")
                    return True

            except json.JSONDecodeError:
                pass

        sleep(5)

    print(f"[WARNING] Timeout waiting for pods")
    return False

def setup_minikube():
    """Setup with Kubernetes/Minikube - STAGE 1: Port-forwarding"""
    print("\n" + "="*60)
    print("  Bitcoin Price Monitor - Kubernetes Installation")
    print("="*60 + "\n")

    # Check kubectl
    print("Checking kubectl availability...")
    result = subprocess.run("kubectl version --client", shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print("Error: kubectl not found or not configured")
        sys.exit(1)
    print("[OK] kubectl is available\n")

    # Check cluster connectivity
    print("Checking cluster connectivity...")
    result = subprocess.run("kubectl cluster-info", shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print("Error: Cannot connect to Kubernetes cluster")
        sys.exit(1)
    print("[OK] Connected to cluster\n")

    # Build bitcoin-exporter image
    script_dir = os.path.dirname(os.path.abspath(__file__))
    exporter_dir = os.path.join(script_dir, "exporter")

    print("Building bitcoin-exporter Docker image...")
    result = subprocess.run(
        f'docker build -t bitcoin-exporter:latest "{exporter_dir}"',
        shell=True,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"Error building image: {result.stderr}")
        sys.exit(1)
    print("[OK] Image built successfully\n")

    # Apply Kubernetes manifests
    helm_templates = os.path.join(script_dir, "helm", "charts", "bitcoin-exporter", "templates")

    manifests = [
        "namespace.yaml",
        "configmap.yaml",
        "dashboard-configmap.yaml",
        "bitcoin-exporter-deployment.yaml",
        "prometheus-deployment.yaml",
        "grafana-deployment.yaml"
    ]

    print("Applying Kubernetes manifests...")
    for manifest in manifests:
        manifest_path = os.path.join(helm_templates, manifest)
        if os.path.exists(manifest_path):
            result = subprocess.run(
                f'kubectl apply -f "{manifest_path}"',
                shell=True,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f"  [OK] {manifest}")
            else:
                print(f"  [ERROR] {manifest}: {result.stderr}")
                sys.exit(1)
        else:
            print(f"  [WARNING] {manifest} not found, skipping")

    print()

    # Wait for pods to be ready
    if not wait_for_pods("bitcoin-monitoring", timeout=300):
        print("\n[WARNING] Not all pods are ready. Check logs:")
        print("  kubectl logs -n bitcoin-monitoring -l app=bitcoin-exporter")
        print("  kubectl logs -n bitcoin-monitoring -l app=prometheus")
        print("  kubectl logs -n bitcoin-monitoring -l app=grafana")

    # Display access information
    print("\n" + "="*60)
    print("Installation Completed!")
    print("="*60)

    # Get services
    result = subprocess.run(
        "kubectl get svc -n bitcoin-monitoring",
        shell=True,
        capture_output=True,
        text=True
    )
    print("\nServices:")
    print(result.stdout)

    print("="*60)
    print("STAGE 1: Access via Port-Forwarding")
    print("="*60)
    print("\nTo access the services, run these commands in separate terminals:\n")
    print("  # Prometheus")
    print("  kubectl port-forward -n bitcoin-monitoring svc/prometheus 9090:9090")
    print("\n  # Grafana")
    print("  kubectl port-forward -n bitcoin-monitoring svc/grafana 3000:3000")
    print("\nThen access:")
    print("  Prometheus: http://localhost:9090")
    print("  Grafana:    http://localhost:3000")

    print("\n" + "="*60)
    print("Useful Commands")
    print("="*60)
    print("  # Check pod status")
    print("  kubectl get pods -n bitcoin-monitoring")
    print("\n  # View logs")
    print("  kubectl logs -n bitcoin-monitoring -l app=bitcoin-exporter")
    print("  kubectl logs -n bitcoin-monitoring -l app=prometheus")
    print("  kubectl logs -n bitcoin-monitoring -l app=grafana")
    print("\n  # Uninstall")
    print("  python setup.py --clean")
    print("\n" + "="*60)

def clean():
    """Remove all Docker and Kubernetes resources"""
    print("\n" + "="*60)
    print("  Cleaning up resources...")
    print("="*60 + "\n")

    # Stop Docker Compose services
    print("Stopping Docker Compose services...")
    result = subprocess.run("cd docker && docker-compose down -v", shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print("[OK] Docker Compose services stopped\n")
    else:
        print("[INFO] No Docker Compose services running\n")

    # Delete Kubernetes namespace
    print("Deleting Kubernetes resources...")
    result = subprocess.run("kubectl delete namespace bitcoin-monitoring", shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print("[OK] Kubernetes namespace deleted")

        # Wait for namespace deletion
        print("Waiting for namespace deletion...")
        for _ in range(30):
            result = subprocess.run(
                "kubectl get namespace bitcoin-monitoring",
                shell=True,
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                print("[OK] Namespace fully deleted\n")
                break
            sleep(2)
    else:
        print("[INFO] No Kubernetes resources found\n")

    print("="*60)
    print("Cleanup complete!")
    print("="*60)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python setup.py --docker")
        print("       python setup.py --minikube")
        print("       python setup.py --clean")
        sys.exit(1)

    if sys.argv[1] == "--docker":
        setup_docker()
    elif sys.argv[1] == "--minikube":
        setup_minikube()
    elif sys.argv[1] == "--clean":
        clean()
    else:
        print("Invalid option. Use --docker, --minikube, or --clean")
