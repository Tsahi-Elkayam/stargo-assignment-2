"""Unit tests for Coindesk provider."""
import pytest
from unittest.mock import Mock, patch, MagicMock
from exporter.src.providers.coindesk import CoindeskProvider


class TestCoindeskProvider:
    """Test suite for Coindesk provider."""
    
    @pytest.fixture
    def provider(self):
        """Create a provider instance."""
        config = {
            'endpoint': 'https://api.coindesk.com/v1/bpi/currentprice.json',
            'timeout': 10,
            'retry': {'max_attempts': 3, 'backoff': 2}
        }
        return CoindeskProvider(config)
    
    def test_parse_valid_response(self, provider):
        """Test parsing a valid Coindesk response."""
        response = {
            "time": {
                "updated": "Oct 3, 2025 12:00:00 UTC",
                "updatedISO": "2025-10-03T12:00:00+00:00",
                "updateduk": "Oct 3, 2025 at 13:00 BST"
            },
            "bpi": {
                "USD": {
                    "code": "USD",
                    "symbol": "&#36;",
                    "rate": "45,123.4567",
                    "description": "United States Dollar",
                    "rate_float": 45123.4567
                },
                "GBP": {
                    "code": "GBP",
                    "rate": "36,098.7654",
                    "rate_float": 36098.7654
                }
            }
        }
        
        metrics = provider.parse_response(response)
        
        assert 'bitcoin_price' in metrics
        assert metrics['bitcoin_price'] == 45123.4567
        assert 'last_updated' in metrics
        assert isinstance(metrics['last_updated'], float)
    
    def test_parse_empty_response(self, provider):
        """Test parsing an empty response."""
        metrics = provider.parse_response({})
        assert metrics == {}
    
    def test_parse_invalid_response(self, provider):
        """Test parsing a response with missing fields."""
        response = {"bpi": {}}
        metrics = provider.parse_response(response)
        assert 'bitcoin_price' not in metrics
        assert 'last_updated' in metrics
    
    def test_parse_malformed_price(self, provider):
        """Test parsing with malformed price data."""
        response = {
            "bpi": {
                "USD": {
                    "rate_float": "not_a_number"
                }
            }
        }
        metrics = provider.parse_response(response)
        assert 'bitcoin_price' not in metrics
    
    @patch('requests.get')
    def test_fetch_data_success(self, mock_get, provider):
        """Test successful data fetching."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"test": "data"}
        mock_get.return_value = mock_response
        
        result = provider.fetch_data()
        assert result == {"test": "data"}
        mock_get.assert_called_once_with(
            provider.endpoint,
            timeout=provider.timeout
        )
    
    @patch('requests.get')
    def test_fetch_data_retry_on_failure(self, mock_get, provider):
        """Test retry mechanism on failure."""
        mock_get.side_effect = [
            Exception("Connection error"),
            Exception("Connection error"),
            Mock(status_code=200, json=lambda: {"test": "data"})
        ]
        
        result = provider.fetch_data()
        assert result == {"test": "data"}
        assert mock_get.call_count == 3
    
    @patch('requests.get')
    def test_fetch_data_max_retries_exceeded(self, mock_get, provider):
        """Test when max retries are exceeded."""
        mock_get.side_effect = Exception("Connection error")
        
        result = provider.fetch_data()
        assert result is None
        assert mock_get.call_count == 3
    
    def test_validate_config_valid(self, provider):
        """Test configuration validation with valid config."""
        assert provider.validate_config() is True
    
    def test_validate_config_no_endpoint(self):
        """Test configuration validation without endpoint."""
        provider = CoindeskProvider({})
        # Should use default endpoint
        assert provider.validate_config() is True
