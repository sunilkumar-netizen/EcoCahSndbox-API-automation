"""
Configuration Loader Module
Loads environment-specific configuration from YAML files.
Supports multiple environments: dev, qa, uat, prod.
"""

import yaml
import os
from pathlib import Path
from typing import Any, Dict
from core.logger import Logger


class ConfigLoader:
    """
    Configuration loader for environment-specific settings.
    Implements singleton pattern to ensure single config instance.
    """
    
    _instance = None
    _config = None
    _environment = None
    
    def __new__(cls, environment: str = 'qa'):
        """
        Singleton implementation.
        
        Args:
            environment: Environment name (dev, qa, uat, prod)
        """
        if cls._instance is None:
            cls._instance = super(ConfigLoader, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, environment: str = 'qa'):
        """
        Initialize configuration loader.
        
        Args:
            environment: Environment name (dev, qa, uat, prod)
        """
        if self._config is None or self._environment != environment:
            self._environment = environment
            self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from YAML file."""
        # Determine config directory
        current_dir = Path(__file__).resolve().parent.parent
        config_dir = current_dir / 'config'
        config_file = config_dir / f'{self._environment}.yaml'
        
        if not config_file.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {config_file}. "
                f"Available environments: dev, qa, uat"
            )
        
        with open(config_file, 'r') as f:
            self._config = yaml.safe_load(f)
        
        logger = Logger.get_logger(__name__)
        logger.info(f"Configuration loaded for environment: {self._environment}")
        logger.debug(f"Config file: {config_file}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.
        
        Args:
            key: Configuration key (e.g., 'api.base_url')
            default: Default value if key not found
            
        Returns:
            Configuration value
            
        Example:
            config.get('api.base_url')
            config.get('endpoints.payments.create')
        """
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_all(self) -> Dict:
        """
        Get all configuration.
        
        Returns:
            Complete configuration dictionary
        """
        return self._config.copy()
    
    def get_environment(self) -> str:
        """
        Get current environment name.
        
        Returns:
            Environment name
        """
        return self._environment
    
    def reload(self) -> None:
        """Reload configuration from file."""
        self._load_config()
    
    @classmethod
    def get_instance(cls, environment: str = 'qa') -> 'ConfigLoader':
        """
        Get ConfigLoader instance.
        
        Args:
            environment: Environment name
            
        Returns:
            ConfigLoader instance
        """
        return cls(environment)
