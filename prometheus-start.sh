#!/bin/sh
set -e

echo "=== Prometheus Startup ==="
echo "BITCOIN_EXPORTER_URL: ${BITCOIN_EXPORTER_URL}"
echo "PORT: ${PORT}"
echo "=========================="

# Generate Prometheus config with actual Render URL
cat > /etc/prometheus/prometheus.yml <<EOF
global:
  scrape_interval: 60s
  evaluation_interval: 60s

scrape_configs:
  - job_name: 'bitcoin-exporter'
    scheme: https
    static_configs:
      - targets: ['${BITCOIN_EXPORTER_URL}']
    scrape_interval: 60s
    scrape_timeout: 10s
EOF

echo "Generated Prometheus config:"
cat /etc/prometheus/prometheus.yml
echo "=========================="

# Start Prometheus - bind to all interfaces
exec /bin/prometheus \
  --config.file=/etc/prometheus/prometheus.yml \
  --storage.tsdb.path=/prometheus \
  --web.listen-address=0.0.0.0:${PORT:-9090} \
  --log.level=info
