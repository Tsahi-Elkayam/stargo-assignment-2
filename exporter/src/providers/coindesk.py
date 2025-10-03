"""Coindesk API provider implementation."""
import requests
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from providers.base import BaseProvider


logger = logging.getLogger(__name__)


class CoindeskProvider(BaseProvider):
    """Provider for Coindesk Bitcoin price API."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize Coindesk provider."""
        super().__init__(config)
        # Use Coinbase API (better rate limits, no auth required)
        if not self.endpoint:
            self.endpoint = "https://api.coinbase.com/v2/prices/BTC-USD/spot"
    
    def fetch_data(self) -> Optional[Dict[str, Any]]:
        """Fetch Bitcoin price from API."""
        try:
            max_attempts = self.retry_config.get('max_attempts', 3)
            backoff = self.retry_config.get('backoff', 2)
            
            for attempt in range(max_attempts):
                try:
                    response = requests.get(
                        self.endpoint,
                        timeout=self.timeout
                    )
                    response.raise_for_status()
                    return response.json()
                except requests.exceptions.RequestException as e:
                    if attempt < max_attempts - 1:
                        logger.warning(f"Attempt {attempt + 1} failed: {e}")
                        import time
                        time.sleep(backoff ** attempt)
                    else:
                        raise
                        
        except Exception as e:
            logger.error(f"Failed to fetch data: {e}")
            return None
    
    def parse_response(self, response: Dict[str, Any]) -> Dict[str, float]:
        """Parse API response (supports Coinbase, CoinGecko, and Coindesk formats)."""
        if not response:
            return {}
        
        try:
            metrics = {}
            
            # Try Coinbase format (new default)
            if 'data' in response and 'amount' in response['data']:
                metrics['bitcoin_price'] = float(response['data']['amount'])
                logger.info(f"Parsed Coinbase response: ${metrics['bitcoin_price']}")
            # Try CoinGecko format
            elif 'bitcoin' in response and 'usd' in response['bitcoin']:
                metrics['bitcoin_price'] = float(response['bitcoin']['usd'])
                logger.info(f"Parsed CoinGecko response: ${metrics['bitcoin_price']}")
            # Try Coindesk format
            elif 'bpi' in response:
                bpi = response.get('bpi', {})
                usd = bpi.get('USD', {})
                
                if 'rate_float' in usd:
                    try:
                        metrics['bitcoin_price'] = float(usd['rate_float'])
                        logger.info(f"Parsed Coindesk response: ${metrics['bitcoin_price']}")
                    except (ValueError, TypeError):
                        logger.error(f"Invalid USD price format: {usd.get('rate_float')}")
                else:
                    logger.warning("No USD rate_float found in response")
            else:
                logger.warning(f"Unknown response format: {list(response.keys())}")
            
            # Add current timestamp
            metrics['last_updated'] = datetime.now().timestamp()
            
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to parse response: {e}")
            return {}
    
    def validate_config(self) -> bool:
        """Validate provider configuration."""
        if not self.endpoint:
            logger.error("No endpoint configured")
            return False
        return True
