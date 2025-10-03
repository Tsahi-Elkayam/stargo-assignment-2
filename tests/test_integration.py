"""Integration tests for the complete Bitcoin Price Monitor stack."""
import pytest
import requests
import time
import subprocess
from pathlib import Path


class TestIntegration:
    """Integration test suite."""
    
    @classmethod
    def setup_class(cls):
        """Setup test environment."""
        cls.base_url = "http://localhost:8000"
        cls.prometheus_url = "http://localhost:9090"
        cls.grafana_url = "http://localhost:3000"
    
    @pytest.mark.integration
    def test_metrics_endpoint_available(self):
        """Test that metrics endpoint is available."""
        try:
            response = requests.get(f"{self.base_url}/metrics", timeout=5)
            assert response.status_code == 200
            assert "bitcoin_price" in response.text
        except requests.exceptions.ConnectionError:
            pytest.skip("Services not running, skipping integration test")
    
    @pytest.mark.integration
    def test_health_endpoint(self):
        """Test health check endpoint."""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            assert response.status_code == 200
            assert "healthy" in response.text.lower()
        except requests.exceptions.ConnectionError:
            pytest.skip("Services not running, skipping integration test")
    
    @pytest.mark.integration
    def test_bitcoin_price_metric_format(self):
        """Test that Bitcoin price metric has correct format."""
        try:
            response = requests.get(f"{self.base_url}/metrics", timeout=5)
            assert response.status_code == 200
            
            lines = response.text.split('\n')
            bitcoin_price_found = False
            
            for line in lines:
                if line.startswith('bitcoin_price{'):
                    bitcoin_price_found = True
                    # Check format: bitcoin_price{currency="BTC",source="coindesk"} 12345.67
                    assert 'currency="BTC"' in line
                    assert 'source="coindesk"' in line
                    # Extract value
                    parts = line.split()
                    if len(parts) > 1:
                        value = float(parts[-1])
                        assert value > 0, "Bitcoin price should be positive"
            
            assert bitcoin_price_found, "bitcoin_price metric not found"
        except requests.exceptions.ConnectionError:
            pytest.skip("Services not running, skipping integration test")
    
    @pytest.mark.integration
    def test_error_metrics_exist(self):
        """Test that error tracking metrics exist."""
        try:
            response = requests.get(f"{self.base_url}/metrics", timeout=5)
            assert response.status_code == 200
            
            # Check for error counter
            assert "bitcoin_price_errors_total" in response.text
            
            # Check for success gauge
            assert "bitcoin_price_fetch_success" in response.text
        except requests.exceptions.ConnectionError:
            pytest.skip("Services not running, skipping integration test")
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_prometheus_scraping(self):
        """Test that Prometheus is successfully scraping the exporter."""
        try:
            # Query Prometheus for our metric
            query_url = f"{self.prometheus_url}/api/v1/query"
            params = {"query": "bitcoin_price"}
            
            response = requests.get(query_url, params=params, timeout=5)
            assert response.status_code == 200
            
            data = response.json()
            assert data["status"] == "success"
            
            # Check if we have results
            if data["data"]["result"]:
                result = data["data"]["result"][0]
                assert "metric" in result
                assert "value" in result
                
                # Verify the value is recent
                timestamp = result["value"][0]
                current_time = time.time()
                age = current_time - timestamp
                assert age < 120, "Metric is too old (>2 minutes)"
        except requests.exceptions.ConnectionError:
            pytest.skip("Prometheus not running, skipping integration test")
    
    @pytest.mark.integration
    def test_grafana_datasource(self):
        """Test that Grafana has Prometheus configured as datasource."""
        try:
            # Check Grafana API for datasources
            response = requests.get(
                f"{self.grafana_url}/api/datasources",
                auth=("admin", "admin"),
                timeout=5
            )
            
            if response.status_code == 200:
                datasources = response.json()
                prometheus_found = False
                
                for ds in datasources:
                    if ds["type"] == "prometheus":
                        prometheus_found = True
                        assert ds["url"] == "http://prometheus:9090"
                        break
                
                assert prometheus_found, "Prometheus datasource not found in Grafana"
        except requests.exceptions.ConnectionError:
            pytest.skip("Grafana not running, skipping integration test")
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_metric_collection_over_time(self):
        """Test that metrics are being collected over time."""
        try:
            # Collect two samples 10 seconds apart
            response1 = requests.get(f"{self.base_url}/metrics", timeout=5)
            assert response1.status_code == 200
            
            # Extract first timestamp
            timestamp1 = None
            for line in response1.text.split('\n'):
                if line.startswith('bitcoin_price_last_updated'):
                    parts = line.split()
                    if len(parts) > 1:
                        timestamp1 = float(parts[-1])
                        break
            
            # Wait and collect second sample
            time.sleep(10)
            
            response2 = requests.get(f"{self.base_url}/metrics", timeout=5)
            assert response2.status_code == 200
            
            # Extract second timestamp
            timestamp2 = None
            for line in response2.text.split('\n'):
                if line.startswith('bitcoin_price_last_updated'):
                    parts = line.split()
                    if len(parts) > 1:
                        timestamp2 = float(parts[-1])
                        break
            
            # Timestamps should be different if collection is working
            if timestamp1 and timestamp2:
                assert timestamp2 >= timestamp1, "Timestamp should increase over time"
        except requests.exceptions.ConnectionError:
            pytest.skip("Services not running, skipping integration test")
    
    @pytest.mark.integration
    def test_docker_compose_config(self):
        """Test that docker-compose configuration is valid."""
        docker_compose_path = Path(__file__).parent.parent / "docker" / "docker-compose.yml"
        assert docker_compose_path.exists(), "docker-compose.yml not found"
        
        # Try to validate the compose file
        result = subprocess.run(
            f"docker-compose -f {docker_compose_path} config",
            shell=True,
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0, f"Invalid docker-compose config: {result.stderr}"
