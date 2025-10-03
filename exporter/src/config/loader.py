"""Configuration loader and manager."""
import os
import yaml
import logging
from typing import Dict, Any, Optional
from pathlib import Path


logger = logging.getLogger(__name__)


class ConfigLoader:
    """Load and manage application configuration."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration loader."""
        self.config_path = config_path or self._get_default_path()
        self.config = {}
        self.environment = os.getenv('ENV', 'local')
    
    def _get_default_path(self) -> str:
        """Get default configuration path."""
        # Go up from src/config/loader.py to project root
        # loader.py is at exporter/src/config/loader.py
        # config is at config/
        return str(Path(__file__).parent.parent.parent.parent / 'config')
    
    def load(self) -> Dict[str, Any]:
        """Load configuration from YAML files."""
        try:
            # Load base configuration
            self.config = self._load_file('app-config.yaml')
            
            # Load environment-specific config
            env_config = self._load_env_config()
            if env_config:
                self.config = self._merge_configs(self.config, env_config)
            
            # Load metrics configuration
            metrics_config = self._load_file('metrics.yaml')
            if metrics_config:
                self.config['metrics_definitions'] = metrics_config
            
            # Load labels configuration
            labels_config = self._load_file('labels.yaml')
            if labels_config:
                self.config['labels'] = labels_config
            
            # Apply environment variables
            self._apply_env_vars()
            
            return self.config
            
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            raise
    
    def _load_file(self, filename: str) -> Dict[str, Any]:
        """Load YAML file."""
        filepath = Path(self.config_path) / filename
        
        if not filepath.exists():
            logger.warning(f"Configuration file not found: {filepath}")
            return {}
        
        try:
            with open(filepath, 'r') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            logger.error(f"Failed to load {filepath}: {e}")
            return {}
    
    def _load_env_config(self) -> Dict[str, Any]:
        """Load environment-specific configuration."""
        env_file = f"environments/{self.environment}.yaml"
        return self._load_file(env_file)
    
    def _merge_configs(self, base: Dict, override: Dict) -> Dict:
        """Recursively merge configuration dictionaries."""
        merged = base.copy()
        
        for key, value in override.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = self._merge_configs(merged[key], value)
            else:
                merged[key] = value
        
        return merged
    
    def _apply_env_vars(self):
        """Apply environment variable overrides."""
        # Override with environment variables
        if 'EXPORTER_PORT' in os.environ:
            self.config.setdefault('exporter', {})['port'] = int(os.environ['EXPORTER_PORT'])
        
        if 'LOG_LEVEL' in os.environ:
            self.config.setdefault('logging', {})['level'] = os.environ['LOG_LEVEL']
        
        if 'API_ENDPOINT' in os.environ:
            self.config.setdefault('api', {})['endpoint'] = os.environ['API_ENDPOINT']
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key."""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value
