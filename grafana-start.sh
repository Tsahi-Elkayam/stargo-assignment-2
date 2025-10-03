#!/bin/sh
set -e

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

echo "Grafana datasource config generated:"
cat /etc/grafana/provisioning/datasources/datasources.yaml

# Start Grafana
exec /run.sh
