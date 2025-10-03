# Solution

## Architecture
Python Exporter → Prometheus → Grafana

## Components

### Bitcoin Exporter
- Queries Coindesk API every 60 seconds
- Exposes metrics on port 8000
- Uses prometheus-client library

### Prometheus  
- Scrapes metrics from exporter
- Stores time-series data

### Grafana
- Visualizes Bitcoin price data
- No login required (anonymous access)
- Auto-provisioned dashboard

## Deployment Options

1. **Docker Compose**: Simple local testing
2. **Kubernetes**: Production-ready with Minikube or cloud

## SOLID Principles
- Abstract base classes for extensibility
- Configuration-driven design
- Dependency injection