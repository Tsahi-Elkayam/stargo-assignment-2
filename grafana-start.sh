#!/bin/sh
set -e

echo "=== Grafana Startup ==="
echo "PROMETHEUS_URL: ${PROMETHEUS_URL}"
echo "PORT: ${PORT}"
echo "=========================="

# Generate Grafana datasource config with actual Render URL
mkdir -p /etc/grafana/provisioning/datasources

cat > /etc/grafana/provisioning/datasources/datasources.yaml <<EOF
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: https://${PROMETHEUS_URL}
    isDefault: true
    editable: false
EOF

echo "Generated Grafana datasource config:"
cat /etc/grafana/provisioning/datasources/datasources.yaml
echo "=========================="

# Start Grafana
exec /run.sh
