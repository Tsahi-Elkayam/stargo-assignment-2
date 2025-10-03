# Docker Configuration

This folder contains all Docker-related configuration files.

## Files

### docker-compose.yml
Main orchestration file that defines:
- **bitcoin-exporter**: Custom Python service that fetches Bitcoin prices
- **prometheus**: Time-series database that scrapes metrics
- **grafana**: Visualization dashboard

## Service Architecture

```
bitcoin-exporter (port 8000)
    ↓ (scraped every 60s)
prometheus (port 9090)
    ↓ (data source)
grafana (port 3000)
```

## Volume Mounts

The compose file mounts these directories from parent:
- `../config` → Bitcoin exporter configuration
- `../helm/values` → Prometheus and Grafana configs
- `../dashboards` → Grafana dashboard templates
- `../exporter` → Build context for Bitcoin exporter

## Commands

```bash
# Start all services
docker-compose -f docker-compose.yml up -d --build

# Stop all services
docker-compose -f docker-compose.yml down

# View logs
docker-compose -f docker-compose.yml logs -f

# Check status
docker-compose -f docker-compose.yml ps
```

## Ports

- **8000**: Bitcoin price metrics endpoint
- **9090**: Prometheus web UI
- **3000**: Grafana dashboards (no login required)

## Data Persistence

Named volumes ensure data persists between restarts:
- `prometheus-data`: Time-series metrics storage
- `grafana-data`: Dashboard configurations and settings
