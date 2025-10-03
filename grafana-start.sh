#!/bin/sh
set -e

echo "=== Grafana Startup Debug ==="
echo "PROMETHEUS_URL: ${PROMETHEUS_URL}"
echo "GF_SERVER_HTTP_PORT: ${GF_SERVER_HTTP_PORT}"
echo "PORT: ${PORT}"

# If PROMETHEUS_URL is not set, use a fallback
if [ -z "$PROMETHEUS_URL" ]; then
    echo "WARNING: PROMETHEUS_URL not set!"
    PROMETHEUS_URL="localhost:9090"
fi

echo "Using Prometheus URL: ${PROMETHEUS_URL}"
echo "==============================="

# Generate Grafana datasource config
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
    jsonData:
      timeInterval: 60s
      httpMethod: GET
EOF

echo "Generated datasource config:"
cat /etc/grafana/provisioning/datasources/datasources.yaml
echo "==============================="

# Start Grafana
echo "Starting Grafana..."
exec /run.sh
