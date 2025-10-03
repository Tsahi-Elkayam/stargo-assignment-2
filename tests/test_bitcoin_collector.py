"""Unit tests for Bitcoin collector."""
import pytest
from unittest.mock import Mock, MagicMock, patch
from exporter.src.collectors.bitcoin import BitcoinCollector


class TestBitcoinCollector:
    """Test suite for Bitcoin collector."""
    
    @pytest.fixture
    def config(self):
        """Create test configuration."""
        return {
            'api': {
                'provider': 'coindesk',
                'endpoint': 'https://api.coindesk.com/v1/bpi/currentprice.json',
                'timeout': 10,
                'retry': {'max_attempts': 3, 'backoff': 2}
            },
            'metrics': {
                'namespace': 'bitcoin',
                'subsystem': 'price'
            }
        }
    
    @pytest.fixture
    def collector(self, config):
        """Create a collector instance with mocked provider."""
        with patch('exporter.src.collectors.bitcoin.CoindeskProvider') as mock_provider_class:
            mock_provider = Mock()
            mock_provider.validate_config.return_value = True
            mock_provider_class.return_value = mock_provider
            
            collector = BitcoinCollector(config)
            collector.provider = mock_provider
            return collector
    
    def test_collector_initialization(self, config):
        """Test collector initialization."""
        with patch('exporter.src.collectors.bitcoin.CoindeskProvider'):
            collector = BitcoinCollector(config)
            assert collector.config == config
            assert collector.provider is not None
            assert hasattr(collector, 'price_gauge')
            assert hasattr(collector, 'last_updated_gauge')
            assert hasattr(collector, 'error_counter')
            assert hasattr(collector, 'fetch_success_gauge')
    
    def test_collect_success(self, collector):
        """Test successful metric collection."""
        # Mock provider responses
        collector.provider.fetch_data.return_value = {"test": "data"}
        collector.provider.parse_response.return_value = {
            'bitcoin_price': 45123.45,
            'last_updated': 1234567890.0
        }
        
        # Mock Prometheus metrics
        mock_gauge = Mock()
        mock_labels = Mock()
        mock_labels.set = Mock()
        mock_gauge.labels.return_value = mock_labels
        collector.price_gauge = mock_gauge
        collector.last_updated_gauge = Mock()
        collector.fetch_success_gauge = Mock()
        
        metrics = collector.collect()
        
        assert metrics == {'bitcoin_price': 45123.45, 'last_updated': 1234567890.0}
        collector.provider.fetch_data.assert_called_once()
        collector.provider.parse_response.assert_called_once_with({"test": "data"})
        collector.fetch_success_gauge.set.assert_called_with(1)
        mock_gauge.labels.assert_called_with(currency='BTC', source='coindesk')
        mock_labels.set.assert_called_with(45123.45)
    
    def test_collect_no_data(self, collector):
        """Test collection when no data is received."""
        collector.provider.fetch_data.return_value = None
        
        mock_error_counter = Mock()
        mock_labels = Mock()
        mock_labels.inc = Mock()
        mock_error_counter.labels.return_value = mock_labels
        collector.error_counter = mock_error_counter
        collector.fetch_success_gauge = Mock()
        
        metrics = collector.collect()
        
        assert metrics == {}
        collector.provider.fetch_data.assert_called_once()
        mock_error_counter.labels.assert_called_with(error_type='no_data')
        mock_labels.inc.assert_called_once()
        collector.fetch_success_gauge.set.assert_called_with(0)
    
    def test_collect_parse_error(self, collector):
        """Test collection when parsing fails."""
        collector.provider.fetch_data.return_value = {"test": "data"}
        collector.provider.parse_response.return_value = {}  # No bitcoin_price
        
        mock_error_counter = Mock()
        mock_labels = Mock()
        mock_labels.inc = Mock()
        mock_error_counter.labels.return_value = mock_labels
        collector.error_counter = mock_error_counter
        collector.fetch_success_gauge = Mock()
        
        metrics = collector.collect()
        
        assert metrics == {}
        mock_error_counter.labels.assert_called_with(error_type='parse_error')
        mock_labels.inc.assert_called_once()
        collector.fetch_success_gauge.set.assert_called_with(0)
    
    def test_collect_exception(self, collector):
        """Test collection when an exception occurs."""
        collector.provider.fetch_data.side_effect = Exception("API error")
        
        mock_error_counter = Mock()
        mock_labels = Mock()
        mock_labels.inc = Mock()
        mock_error_counter.labels.return_value = mock_labels
        collector.error_counter = mock_error_counter
        collector.fetch_success_gauge = Mock()
        
        metrics = collector.collect()
        
        assert metrics == {}
        mock_error_counter.labels.assert_called_with(error_type='exception')
        mock_labels.inc.assert_called_once()
        collector.fetch_success_gauge.set.assert_called_with(0)
    
    def test_validate_success(self, collector):
        """Test successful validation."""
        collector.provider.validate_config.return_value = True
        assert collector.validate() is True
    
    def test_validate_no_provider(self, config):
        """Test validation with no provider."""
        with patch('exporter.src.collectors.bitcoin.CoindeskProvider'):
            collector = BitcoinCollector(config)
            collector.provider = None
            assert collector.validate() is False
    
    def test_validate_provider_invalid(self, collector):
        """Test validation with invalid provider config."""
        collector.provider.validate_config.return_value = False
        assert collector.validate() is False
