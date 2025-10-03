#!/bin/sh
set -e

echo "=== Prometheus Startup Debug ==="
echo "BITCOIN_EXPORTER_URL: ${BITCOIN_EXPORTER_URL}"
echo "PORT: ${PORT}"

# If BITCOIN_EXPORTER_URL is not set, use a fallback
if [ -z "$BITCOIN_EXPORTER_URL" ]; then
    echo "WARNING: BITCOIN_EXPORTER_URL not set!"
    BITCOIN_EXPORTER_URL="bitcoin-exporter-production.up.railway.app"
fi

echo "Using target: ${BITCOIN_EXPORTER_URL}"
echo "================================"

# Generate Prometheus config
cat > /etc/prometheus/prometheus.yml <<EOF
global:
  scrape_interval: 60s
  evaluation_interval: 60s
  scrape_timeout: 30s

scrape_configs:
  - job_name: 'bitcoin-exporter'
    scheme: https
    metrics_path: /metrics
    static_configs:
      - targets: ['${BITCOIN_EXPORTER_URL}']
    scrape_interval: 60s
    scrape_timeout: 30s
EOF

echo "Generated config:"
cat /etc/prometheus/prometheus.yml
echo "================================"

# Test config validity
/bin/prometheus --config.file=/etc/prometheus/prometheus.yml --help > /dev/null 2>&1
echo "Config validation: OK"

# Start Prometheus
echo "Starting Prometheus on 0.0.0.0:${PORT:-9090}..."
exec /bin/prometheus \
  --config.file=/etc/prometheus/prometheus.yml \
  --storage.tsdb.path=/prometheus \
  --storage.tsdb.retention.time=2h \
  --web.listen-address=0.0.0.0:${PORT:-9090} \
  --web.enable-lifecycle \
  --log.level=debug
