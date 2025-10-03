"""Base class for metric collectors."""
from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseCollector(ABC):
    """Abstract base class for metric collectors."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize collector with configuration."""
        self.config = config
        self.metrics = {}
    
    @abstractmethod
    def collect(self) -> Dict[str, float]:
        """Collect metrics from source."""
        pass
    
    @abstractmethod
    def validate(self) -> bool:
        """Validate collector configuration."""
        pass
    
    def get_labels(self) -> Dict[str, str]:
        """Get metric labels."""
        return self.config.get('labels', {})
