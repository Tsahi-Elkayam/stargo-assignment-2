# Makefile for Bitcoin Price Monitor

.PHONY: help build run stop clean test lint docker k8s

help:  ## Show this help message
	@echo "Bitcoin Price Monitor - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

# Development Commands
install:  ## Install Python dependencies
	pip install -r exporter/requirements.txt

test:  ## Run unit tests
	pytest tests/ -v --cov=exporter/src

test-watch:  ## Run tests in watch mode
	pytest-watch tests/ -v

lint:  ## Run code linting
	flake8 exporter/src tests/
	black --check exporter/src tests/
	mypy exporter/src

format:  ## Format code with black
	black exporter/src tests/

# Docker Commands
build:  ## Build Docker image
	docker build -t bitcoin-exporter:latest exporter/

docker:  ## Start with Docker Compose
	cd docker && docker-compose up -d --build

docker-logs:  ## Show Docker logs
	cd docker && docker-compose logs -f

docker-stop:  ## Stop Docker Compose
	cd docker && docker-compose down

docker-clean:  ## Clean Docker resources
	cd docker && docker-compose down -v
	docker rmi bitcoin-exporter:latest || true

# Kubernetes Commands
k8s-start:  ## Start Minikube
	minikube start
	minikube addons enable ingress

k8s-build:  ## Build and load image to Minikube
	docker build -t bitcoin-exporter:latest exporter/
	minikube image load bitcoin-exporter:latest

k8s-deploy:  ## Deploy to Kubernetes
	kubectl apply -f k8s/all-in-one.yaml

k8s-status:  ## Check Kubernetes status
	kubectl get all -n monitoring

k8s-delete:  ## Delete Kubernetes resources
	kubectl delete -f k8s/all-in-one.yaml

k8s-dashboard:  ## Open Kubernetes dashboard
	minikube dashboard

# Monitoring Commands
prometheus:  ## Open Prometheus UI
	@echo "Opening Prometheus at http://localhost:9090"
	@start http://localhost:9090 || open http://localhost:9090 || xdg-open http://localhost:9090

grafana:  ## Open Grafana UI
	@echo "Opening Grafana at http://localhost:3000"
	@start http://localhost:3000 || open http://localhost:3000 || xdg-open http://localhost:3000

metrics:  ## Show current metrics
	@curl -s http://localhost:8000/metrics | grep bitcoin_price

# Setup Commands
setup-docker:  ## Complete Docker setup
	python setup.py --docker

setup-k8s:  ## Complete Kubernetes setup
	python setup.py --k8s

clean:  ## Clean all resources
	python setup.py --clean
	rm -rf __pycache__ .pytest_cache htmlcov
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

# CI/CD Commands
ci-test:  ## Run CI tests
	@echo "Running CI test suite..."
	pytest tests/ -v --cov=exporter/src --cov-report=xml
	flake8 exporter/src tests/
	black --check exporter/src tests/

ci-build:  ## CI build process
	docker build -t bitcoin-exporter:latest exporter/
	docker run --rm bitcoin-exporter:latest python -c "import sys; print('Image OK')"

# Quick Commands
quick-start:  ## Quick start with Docker
	@make docker
	@sleep 10
	@make test-docker

test-docker:  ## Test Docker deployment
	python scripts/test-docker.py

rebuild:  ## Rebuild everything
	python setup.py --rebuild

# Documentation
docs:  ## Generate documentation
	@echo "Generating documentation..."
	@echo "See docs/requirements.md and docs/solution.md"
