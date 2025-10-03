"""Unit tests for configuration loader."""
import pytest
import os
import tempfile
import yaml
from pathlib import Path
from unittest.mock import patch, mock_open
from exporter.src.config.loader import ConfigLoader


class TestConfigLoader:
    """Test suite for configuration loader."""
    
    @pytest.fixture
    def temp_config_dir(self):
        """Create a temporary directory with config files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create app-config.yaml
            app_config = {
                'app': {
                    'name': 'test-app',
                    'version': '1.0.0'
                },
                'exporter': {
                    'port': 8000,
                    'interval': 60
                }
            }
            app_config_path = Path(tmpdir) / 'app-config.yaml'
            with open(app_config_path, 'w') as f:
                yaml.dump(app_config, f)
            
            # Create environments directory
            env_dir = Path(tmpdir) / 'environments'
            env_dir.mkdir()
            
            # Create local.yaml
            local_config = {
                'exporter': {
                    'port': 8001
                },
                'logging': {
                    'level': 'DEBUG'
                }
            }
            local_config_path = env_dir / 'local.yaml'
            with open(local_config_path, 'w') as f:
                yaml.dump(local_config, f)
            
            # Create metrics.yaml
            metrics_config = {
                'metrics': {
                    'bitcoin_price': {
                        'type': 'gauge',
                        'help': 'Bitcoin price in USD'
                    }
                }
            }
            metrics_config_path = Path(tmpdir) / 'metrics.yaml'
            with open(metrics_config_path, 'w') as f:
                yaml.dump(metrics_config, f)
            
            yield tmpdir
    
    def test_load_config_success(self, temp_config_dir):
        """Test successful configuration loading."""
        loader = ConfigLoader(temp_config_dir)
        config = loader.load()
        
        assert config['app']['name'] == 'test-app'
        assert config['app']['version'] == '1.0.0'
        # Environment-specific override should take precedence
        assert config['exporter']['port'] == 8001
        assert config['exporter']['interval'] == 60
        assert config['logging']['level'] == 'DEBUG'
        assert 'metrics_definitions' in config
    
    def test_merge_configs(self, temp_config_dir):
        """Test configuration merging."""
        loader = ConfigLoader(temp_config_dir)
        
        base = {
            'a': 1,
            'b': {'c': 2, 'd': 3},
            'e': [1, 2, 3]
        }
        override = {
            'a': 10,
            'b': {'c': 20, 'f': 4},
            'g': 5
        }
        
        merged = loader._merge_configs(base, override)
        
        assert merged['a'] == 10  # Override
        assert merged['b']['c'] == 20  # Deep override
        assert merged['b']['d'] == 3  # Preserved from base
        assert merged['b']['f'] == 4  # Added from override
        assert merged['e'] == [1, 2, 3]  # Preserved from base
        assert merged['g'] == 5  # Added from override
    
    @patch.dict(os.environ, {'ENV': 'production'})
    def test_environment_selection(self, temp_config_dir):
        """Test environment-specific configuration loading."""
        # Create production config
        prod_config = {
            'exporter': {
                'port': 8080
            },
            'logging': {
                'level': 'INFO'
            }
        }
        env_dir = Path(temp_config_dir) / 'environments'
        prod_config_path = env_dir / 'production.yaml'
        with open(prod_config_path, 'w') as f:
            yaml.dump(prod_config, f)
        
        loader = ConfigLoader(temp_config_dir)
        config = loader.load()
        
        assert loader.environment == 'production'
        assert config['exporter']['port'] == 8080
        assert config['logging']['level'] == 'INFO'
    
    @patch.dict(os.environ, {
        'EXPORTER_PORT': '9000',
        'LOG_LEVEL': 'ERROR',
        'API_ENDPOINT': 'https://custom.api.com'
    })
    def test_env_var_overrides(self, temp_config_dir):
        """Test environment variable overrides."""
        loader = ConfigLoader(temp_config_dir)
        config = loader.load()
        
        assert config['exporter']['port'] == 9000
        assert config['logging']['level'] == 'ERROR'
        assert config['api']['endpoint'] == 'https://custom.api.com'
    
    def test_missing_config_file(self, temp_config_dir):
        """Test handling of missing configuration files."""
        # Delete app-config.yaml
        os.remove(Path(temp_config_dir) / 'app-config.yaml')
        
        loader = ConfigLoader(temp_config_dir)
        config = loader.load()
        
        # Should still load environment config
        assert config['exporter']['port'] == 8001
        assert config['logging']['level'] == 'DEBUG'
    
    def test_get_nested_value(self, temp_config_dir):
        """Test getting nested configuration values."""
        loader = ConfigLoader(temp_config_dir)
        config = loader.load()
        loader.config = config
        
        assert loader.get('app.name') == 'test-app'
        assert loader.get('exporter.port') == 8001
        assert loader.get('non.existent.key', 'default') == 'default'
        assert loader.get('app') == config['app']
    
    def test_default_path(self):
        """Test default configuration path calculation."""
        loader = ConfigLoader()
        path = loader._get_default_path()
        
        # Should point to config directory at project root
        assert path.endswith('config')
