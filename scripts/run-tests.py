#!/usr/bin/env python3
"""
Run all tests and checks for the Bitcoin Price Monitor project.
"""
import subprocess
import sys
import os
from pathlib import Path

# Colors for terminal output
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_header(message):
    """Print a formatted header."""
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}{message}{RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")

def run_command(command, description):
    """Run a command and report results."""
    print(f"🔍 {description}...")
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        print(f"{GREEN}✓ {description} passed{RESET}")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"{RED}✗ {description} failed{RESET}")
        if e.stdout:
            print(e.stdout)
        if e.stderr:
            print(e.stderr)
        return False

def main():
    """Run all tests and checks."""
    print_header("Bitcoin Price Monitor - Test Suite")
    
    # Track results
    results = []
    
    # Change to project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    # 1. Check Python version
    print("📋 Checking environment...")
    python_version = sys.version_info
    if python_version.major >= 3 and python_version.minor >= 8:
        print(f"{GREEN}✓ Python {python_version.major}.{python_version.minor} detected{RESET}")
    else:
        print(f"{RED}✗ Python 3.8+ required (found {python_version.major}.{python_version.minor}){RESET}")
        sys.exit(1)
    
    # 2. Install test dependencies
    print("\n📦 Installing dependencies...")
    results.append(run_command(
        "pip install -q pytest pytest-cov pytest-mock flake8 black mypy",
        "Installing test dependencies"
    ))
    
    # 3. Run unit tests
    print_header("Running Unit Tests")
    results.append(run_command(
        "pytest tests/ -v --cov=exporter/src --cov-report=term-missing",
        "Unit tests with coverage"
    ))
    
    # 4. Run linting
    print_header("Running Code Quality Checks")
    
    # Flake8
    results.append(run_command(
        "flake8 exporter/src --max-line-length=120 --exclude=__pycache__",
        "Flake8 linting"
    ))
    
    # Black formatting check
    results.append(run_command(
        "black --check exporter/src tests/",
        "Black formatting check"
    ))
    
    # 5. Type checking
    print_header("Running Type Checking")
    results.append(run_command(
        "mypy exporter/src --ignore-missing-imports",
        "MyPy type checking"
    ))
    
    # 6. Docker build test
    print_header("Testing Docker Build")
    results.append(run_command(
        "docker build -t bitcoin-exporter:test exporter/",
        "Docker image build"
    ))
    
    # 7. Docker run test
    print("🐳 Testing Docker container...")
    container_started = run_command(
        "docker run -d --rm --name test-exporter -p 8001:8000 bitcoin-exporter:test",
        "Starting test container"
    )
    
    if container_started:
        import time
        time.sleep(5)  # Wait for container to start
        
        # Test metrics endpoint
        results.append(run_command(
            "curl -f http://localhost:8001/metrics",
            "Testing metrics endpoint"
        ))
        
        # Stop container
        run_command("docker stop test-exporter", "Stopping test container")
    
    # 8. Configuration validation
    print_header("Validating Configuration")
    config_files = [
        "config/app-config.yaml",
        "docker/docker-compose.yml",
        "k8s/bitcoin-exporter.yaml"
    ]
    
    for config_file in config_files:
        if Path(config_file).exists():
            print(f"{GREEN}✓ {config_file} exists{RESET}")
        else:
            print(f"{RED}✗ {config_file} missing{RESET}")
            results.append(False)
    
    # Summary
    print_header("Test Summary")
    
    passed = sum(1 for r in results if r)
    failed = sum(1 for r in results if not r)
    total = len(results)
    
    if failed == 0:
        print(f"{GREEN}{BOLD}🎉 All {total} checks passed!{RESET}")
        print(f"\n{GREEN}The project is ready for deployment!{RESET}")
        return 0
    else:
        print(f"{YELLOW}⚠️  {passed}/{total} checks passed{RESET}")
        print(f"{RED}✗ {failed} checks failed{RESET}")
        print(f"\n{YELLOW}Please fix the failing checks before deployment.{RESET}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
