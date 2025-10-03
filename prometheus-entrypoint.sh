#!/bin/sh
# Generate Prometheus config with actual Render URLs

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

# Start Prometheus
exec /bin/prometheus \
  --config.file=/etc/prometheus/prometheus.yml \
  --storage.tsdb.path=/prometheus \
  --web.listen-address=:${PORT:-9090}
