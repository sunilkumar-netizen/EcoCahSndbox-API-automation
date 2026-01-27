"""
Base Test Module
Provides base test class with common setup and utilities.
"""

from core.api_client import APIClient
from core.assertions import APIAssertions
from core.logger import Logger
from utils.config_loader import ConfigLoader
import requests


class BaseTest:
    """
    Base class for API tests.
    Provides common setup and utility methods.
    """
    
    def __init__(self, config: ConfigLoader):
        """
        Initialize base test with configuration.
        
        Args:
            config: ConfigLoader instance
        """
        self.config = config
        self.logger = Logger.get_logger(__name__)
        self.api_client = APIClient(config)
        self.context = {}  # Store data between steps
    
    def assert_response(self, response: requests.Response) -> APIAssertions:
        """
        Create assertion object for response validation.
        
        Args:
            response: Response object to validate
            
        Returns:
            APIAssertions instance
        """
        return APIAssertions(response)
    
    def get_endpoint(self, endpoint_key: str) -> str:
        """
        Get endpoint from configuration.
        
        Args:
            endpoint_key: Dot-separated endpoint key (e.g., 'payments.create')
            
        Returns:
            Endpoint path
        """
        return self.config.get(f'endpoints.{endpoint_key}')
    
    def store_value(self, key: str, value: any) -> None:
        """
        Store value in context for later use.
        
        Args:
            key: Storage key
            value: Value to store
        """
        self.context[key] = value
        self.logger.debug(f"Stored value: {key}={value}")
    
    def get_stored_value(self, key: str, default=None):
        """
        Get stored value from context.
        
        Args:
            key: Storage key
            default: Default value if key not found
            
        Returns:
            Stored value
        """
        return self.context.get(key, default)
    
    def cleanup(self) -> None:
        """Cleanup resources after test."""
        self.api_client.close()
        self.context.clear()
