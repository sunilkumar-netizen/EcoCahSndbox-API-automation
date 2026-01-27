"""
API Client Module
Provides a robust, reusable HTTP client with retry logic, logging, and error handling.
Enterprise-grade implementation following SOLID principles.
"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import Dict, Optional, Any, Union
import json
from core.logger import Logger
from utils.config_loader import ConfigLoader


class APIClient:
    """
    Generic HTTP client for REST API automation.
    Handles GET, POST, PUT, PATCH, DELETE with automatic retry and logging.
    """

    def __init__(self, config: ConfigLoader):
        """
        Initialize API Client with configuration.
        
        Args:
            config: ConfigLoader instance with environment configuration
        """
        self.config = config
        self.logger = Logger.get_logger(__name__)
        self.base_url = config.get('api.base_url')
        self.timeout = config.get('api.timeout', 30)
        self.session = self._create_session()
        self._setup_default_headers()
        
    def _create_session(self) -> requests.Session:
        """
        Create requests session with retry strategy.
        
        Returns:
            Configured requests.Session object
        """
        session = requests.Session()
        
        # Configure retry strategy
        retry_count = self.config.get('api.retry_count', 3)
        retry_delay = self.config.get('api.retry_delay', 2)
        
        retry_strategy = Retry(
            total=retry_count,
            backoff_factor=retry_delay,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "PATCH", "DELETE"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        self.logger.info(f"Session created with {retry_count} retries and {retry_delay}s backoff")
        return session
    
    def _setup_default_headers(self) -> None:
        """Setup default headers from configuration."""
        headers = self.config.get('headers', {})
        self.session.headers.update(headers)
        
        # Add authentication header
        auth_type = self.config.get('auth.type', 'bearer')
        
        if auth_type == 'bearer':
            token = self.config.get('auth.token')
            if token:
                self.session.headers['Authorization'] = f'Bearer {token}'
        elif auth_type == 'api_key':
            api_key_header = self.config.get('auth.api_key_header', 'X-API-Key')
            api_key_value = self.config.get('auth.api_key_value')
            if api_key_value:
                self.session.headers[api_key_header] = api_key_value
        
        self.logger.debug(f"Default headers configured: {self.session.headers}")
    
    def _build_url(self, endpoint: str, **path_params) -> str:
        """
        Build complete URL from endpoint and path parameters.
        
        Args:
            endpoint: API endpoint (can contain placeholders like {id})
            **path_params: Path parameters to replace in endpoint
            
        Returns:
            Complete URL
        """
        # Replace path parameters
        if path_params:
            endpoint = endpoint.format(**path_params)
        
        # Handle both absolute and relative endpoints
        if endpoint.startswith('http'):
            return endpoint
        
        # Remove leading slash if present in endpoint
        endpoint = endpoint.lstrip('/')
        
        return f"{self.base_url}/{endpoint}"
    
    def _log_request(self, method: str, url: str, **kwargs) -> None:
        """Log HTTP request details."""
        self.logger.info(f"🔵 {method} {url}")
        
        if kwargs.get('params'):
            self.logger.debug(f"Query Params: {json.dumps(kwargs['params'], indent=2)}")
        
        if kwargs.get('json'):
            self.logger.debug(f"Request Body: {json.dumps(kwargs['json'], indent=2)}")
        elif kwargs.get('data'):
            self.logger.debug(f"Request Data: {kwargs['data']}")
        
        if kwargs.get('headers'):
            # Mask sensitive headers
            safe_headers = self._mask_sensitive_data(kwargs['headers'])
            self.logger.debug(f"Headers: {json.dumps(safe_headers, indent=2)}")
    
    def _log_response(self, response: requests.Response) -> None:
        """Log HTTP response details."""
        status_emoji = "🟢" if response.ok else "🔴"
        self.logger.info(f"{status_emoji} Response Status: {response.status_code} {response.reason}")
        self.logger.debug(f"Response Headers: {json.dumps(dict(response.headers), indent=2)}")
        
        try:
            if response.text:
                response_json = response.json()
                self.logger.debug(f"Response Body: {json.dumps(response_json, indent=2)}")
        except json.JSONDecodeError:
            self.logger.debug(f"Response Body (text): {response.text[:500]}")
    
    def _mask_sensitive_data(self, data: Dict) -> Dict:
        """
        Mask sensitive information in logs.
        
        Args:
            data: Dictionary potentially containing sensitive data
            
        Returns:
            Dictionary with masked sensitive values
        """
        sensitive_keys = ['authorization', 'token', 'password', 'api_key', 'secret']
        masked_data = data.copy()
        
        for key in masked_data:
            if any(sensitive in key.lower() for sensitive in sensitive_keys):
                masked_data[key] = '***MASKED***'
        
        return masked_data
    
    def request(
        self,
        method: str,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        timeout: Optional[int] = None,
        **path_params
    ) -> requests.Response:
        """
        Generic HTTP request method.
        
        Args:
            method: HTTP method (GET, POST, PUT, PATCH, DELETE)
            endpoint: API endpoint
            headers: Additional headers
            params: Query parameters
            json_data: JSON request body
            data: Form data or raw body
            timeout: Request timeout (overrides default)
            **path_params: Path parameters for URL formatting
            
        Returns:
            requests.Response object
            
        Raises:
            requests.RequestException: On request failure
        """
        url = self._build_url(endpoint, **path_params)
        timeout = timeout or self.timeout
        
        request_kwargs = {
            'headers': headers,
            'params': params,
            'json': json_data,
            'data': data,
            'timeout': timeout
        }
        
        # Remove None values
        request_kwargs = {k: v for k, v in request_kwargs.items() if v is not None}
        
        self._log_request(method, url, **request_kwargs)
        
        try:
            response = self.session.request(method, url, **request_kwargs)
            self._log_response(response)
            return response
            
        except requests.exceptions.Timeout:
            self.logger.error(f"Request timeout after {timeout}s: {method} {url}")
            raise
        except requests.exceptions.ConnectionError as e:
            self.logger.error(f"Connection error: {str(e)}")
            raise
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed: {str(e)}")
            raise
    
    def get(self, endpoint: str, params: Optional[Dict] = None, 
            headers: Optional[Dict] = None, **path_params) -> requests.Response:
        """
        Send GET request.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            headers: Additional headers
            **path_params: Path parameters
            
        Returns:
            requests.Response object
        """
        return self.request('GET', endpoint, params=params, headers=headers, **path_params)
    
    def post(self, endpoint: str, json_data: Optional[Dict] = None,
             data: Optional[Any] = None, headers: Optional[Dict] = None,
             **path_params) -> requests.Response:
        """
        Send POST request.
        
        Args:
            endpoint: API endpoint
            json_data: JSON request body
            data: Form data or raw body
            headers: Additional headers
            **path_params: Path parameters
            
        Returns:
            requests.Response object
        """
        return self.request('POST', endpoint, json_data=json_data, 
                          data=data, headers=headers, **path_params)
    
    def put(self, endpoint: str, json_data: Optional[Dict] = None,
            data: Optional[Any] = None, headers: Optional[Dict] = None,
            **path_params) -> requests.Response:
        """
        Send PUT request.
        
        Args:
            endpoint: API endpoint
            json_data: JSON request body
            data: Form data or raw body
            headers: Additional headers
            **path_params: Path parameters
            
        Returns:
            requests.Response object
        """
        return self.request('PUT', endpoint, json_data=json_data,
                          data=data, headers=headers, **path_params)
    
    def patch(self, endpoint: str, json_data: Optional[Dict] = None,
              data: Optional[Any] = None, headers: Optional[Dict] = None,
              **path_params) -> requests.Response:
        """
        Send PATCH request.
        
        Args:
            endpoint: API endpoint
            json_data: JSON request body
            data: Form data or raw body
            headers: Additional headers
            **path_params: Path parameters
            
        Returns:
            requests.Response object
        """
        return self.request('PATCH', endpoint, json_data=json_data,
                          data=data, headers=headers, **path_params)
    
    def delete(self, endpoint: str, params: Optional[Dict] = None,
               headers: Optional[Dict] = None, **path_params) -> requests.Response:
        """
        Send DELETE request.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            headers: Additional headers
            **path_params: Path parameters
            
        Returns:
            requests.Response object
        """
        return self.request('DELETE', endpoint, params=params, 
                          headers=headers, **path_params)
    
    def update_token(self, token: str) -> None:
        """
        Update authentication token.
        
        Args:
            token: New authentication token
        """
        self.session.headers['Authorization'] = f'Bearer {token}'
        self.logger.info("Authentication token updated")
    
    def close(self) -> None:
        """Close the session and cleanup resources."""
        self.session.close()
        self.logger.info("API Client session closed")
