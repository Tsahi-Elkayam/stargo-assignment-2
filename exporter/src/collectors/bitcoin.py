"""Bitcoin metric collector implementation."""
import logging
from typing import Dict, Any
from prometheus_client import Gauge, Counter
from collectors.base import BaseCollector
from providers.coindesk import CoindeskProvider


logger = logging.getLogger(__name__)


class BitcoinCollector(BaseCollector):
    """Collector for Bitcoin price metrics."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize Bitcoin collector."""
        super().__init__(config)
        self.provider = self._init_provider()
        self._setup_metrics()
    
    def _init_provider(self):
        """Initialize data provider based on config."""
        provider_name = self.config.get('api', {}).get('provider', 'coindesk')

        if provider_name == 'coindesk':
            return CoindeskProvider(self.config.get('api', {}))
        else:
            raise ValueError(f"Unknown provider: {provider_name}")
    
    def _setup_metrics(self):
        """Setup Prometheus metrics."""
        metrics_config = self.config.get('metrics', {})
        namespace = metrics_config.get('namespace', 'bitcoin')
        subsystem = metrics_config.get('subsystem', 'price')
        
        # Create Prometheus gauges
        self.price_gauge = Gauge(
            'bitcoin_price',
            'Bitcoin price in USD',
            labelnames=['currency', 'source']
        )
        
        self.last_updated_gauge = Gauge(
            'bitcoin_price_last_updated',
            'Timestamp of last price update'
        )
        
        # Error tracking metrics
        self.error_counter = Counter(
            'bitcoin_price_errors_total',
            'Total number of errors fetching Bitcoin price',
            labelnames=['error_type']
        )
        
        self.fetch_success_gauge = Gauge(
            'bitcoin_price_fetch_success',
            'Whether the last fetch was successful (1=success, 0=failure)'
        )
    
    def collect(self) -> Dict[str, float]:
        """Collect Bitcoin metrics."""
        try:
            # Fetch data from provider
            raw_data = self.provider.fetch_data()
            if not raw_data:
                logger.warning("No data received from provider")
                self.error_counter.labels(error_type='no_data').inc()
                self.fetch_success_gauge.set(0)
                return {}
            
            # Parse response
            metrics = self.provider.parse_response(raw_data)
            
            # Check if we got valid price data
            if 'bitcoin_price' not in metrics:
                logger.error("No bitcoin_price in parsed metrics")
                self.error_counter.labels(error_type='parse_error').inc()
                self.fetch_success_gauge.set(0)
                return {}
            
            # Update Prometheus metrics
            provider_name = self.config.get('api', {}).get('provider', 'coindesk')
            self.price_gauge.labels(
                currency='BTC',
                source=provider_name
            ).set(metrics['bitcoin_price'])
                
            if 'last_updated' in metrics:
                self.last_updated_gauge.set(metrics['last_updated'])
            
            # Mark success
            self.fetch_success_gauge.set(1)
            
            logger.info(f"Collected metrics: {metrics}")
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to collect metrics: {e}")
            self.error_counter.labels(error_type='exception').inc()
            self.fetch_success_gauge.set(0)
            return {}
    
    def validate(self) -> bool:
        """Validate collector configuration."""
        if not self.provider:
            logger.error("No provider configured")
            return False
        return self.provider.validate_config()
