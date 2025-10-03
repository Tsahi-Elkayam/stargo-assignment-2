"""Base class for data providers."""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseProvider(ABC):
    """Abstract base class for data providers."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize provider with configuration."""
        self.config = config
        self.endpoint = config.get('endpoint')
        self.timeout = config.get('timeout', 30)
        self.retry_config = config.get('retry', {})
    
    @abstractmethod
    def fetch_data(self) -> Optional[Dict[str, Any]]:
        """Fetch data from provider."""
        pass
    
    @abstractmethod
    def parse_response(self, response: Any) -> Dict[str, float]:
        """Parse provider response into metrics."""
        pass
    
    @abstractmethod
    def validate_config(self) -> bool:
        """Validate provider configuration."""
        pass
