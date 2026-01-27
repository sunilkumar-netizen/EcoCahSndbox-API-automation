"""
Assertions Module
Provides comprehensive assertion methods for API response validation.
Includes status code, headers, body, JSON schema, and custom validations.
"""

import json
import jsonschema
from jsonschema import validate, ValidationError
from typing import Dict, Any, List, Union, Optional
import requests
from core.logger import Logger


class APIAssertions:
    """
    Assertion utilities for API response validation.
    Provides fluent interface for chaining assertions.
    """
    
    def __init__(self, response: requests.Response):
        """
        Initialize assertions with response object.
        
        Args:
            response: requests.Response object to validate
        """
        self.response = response
        self.logger = Logger.get_logger(__name__)
        self._response_json = None
    
    @property
    def response_json(self) -> Dict:
        """
        Lazy load and cache response JSON.
        
        Returns:
            Response body as dictionary
        """
        if self._response_json is None:
            try:
                self._response_json = self.response.json()
            except json.JSONDecodeError:
                self.logger.error("Response body is not valid JSON")
                raise AssertionError("Response body is not valid JSON")
        return self._response_json
    
    def assert_status_code(self, expected_status: int) -> 'APIAssertions':
        """
        Assert response status code.
        
        Args:
            expected_status: Expected HTTP status code
            
        Returns:
            Self for method chaining
        """
        actual_status = self.response.status_code
        assert actual_status == expected_status, \
            f"Expected status code {expected_status}, but got {actual_status}. " \
            f"Response: {self.response.text[:200]}"
        
        self.logger.info(f"✅ Status code assertion passed: {actual_status}")
        return self
    
    def assert_status_code_in(self, expected_statuses: List[int]) -> 'APIAssertions':
        """
        Assert response status code is in expected list.
        
        Args:
            expected_statuses: List of acceptable status codes
            
        Returns:
            Self for method chaining
        """
        actual_status = self.response.status_code
        assert actual_status in expected_statuses, \
            f"Expected status code to be in {expected_statuses}, but got {actual_status}"
        
        self.logger.info(f"✅ Status code in range assertion passed: {actual_status}")
        return self
    
    def assert_ok(self) -> 'APIAssertions':
        """
        Assert response is successful (2xx status code).
        
        Returns:
            Self for method chaining
        """
        assert self.response.ok, \
            f"Expected successful response (2xx), but got {self.response.status_code}. " \
            f"Response: {self.response.text[:200]}"
        
        self.logger.info(f"✅ Response OK assertion passed")
        return self
    
    def assert_header_exists(self, header_name: str) -> 'APIAssertions':
        """
        Assert response header exists.
        
        Args:
            header_name: Name of the header
            
        Returns:
            Self for method chaining
        """
        assert header_name in self.response.headers, \
            f"Header '{header_name}' not found in response headers. " \
            f"Available headers: {list(self.response.headers.keys())}"
        
        self.logger.info(f"✅ Header exists assertion passed: {header_name}")
        return self
    
    def assert_header_value(self, header_name: str, expected_value: str) -> 'APIAssertions':
        """
        Assert response header value.
        
        Args:
            header_name: Name of the header
            expected_value: Expected header value
            
        Returns:
            Self for method chaining
        """
        self.assert_header_exists(header_name)
        actual_value = self.response.headers[header_name]
        
        assert actual_value == expected_value, \
            f"Header '{header_name}' expected value '{expected_value}', " \
            f"but got '{actual_value}'"
        
        self.logger.info(f"✅ Header value assertion passed: {header_name}={actual_value}")
        return self
    
    def assert_content_type(self, expected_type: str = 'application/json') -> 'APIAssertions':
        """
        Assert response content type.
        
        Args:
            expected_type: Expected content type
            
        Returns:
            Self for method chaining
        """
        content_type = self.response.headers.get('Content-Type', '')
        assert expected_type in content_type, \
            f"Expected content type '{expected_type}', but got '{content_type}'"
        
        self.logger.info(f"✅ Content type assertion passed: {content_type}")
        return self
    
    def assert_json_contains_key(self, key: str) -> 'APIAssertions':
        """
        Assert JSON response contains key.
        
        Args:
            key: Key name to check
            
        Returns:
            Self for method chaining
        """
        assert key in self.response_json, \
            f"Key '{key}' not found in response. Available keys: {list(self.response_json.keys())}"
        
        self.logger.info(f"✅ JSON contains key assertion passed: {key}")
        return self
    
    def assert_json_value(self, key: str, expected_value: Any) -> 'APIAssertions':
        """
        Assert JSON response key value.
        
        Args:
            key: Key name
            expected_value: Expected value
            
        Returns:
            Self for method chaining
        """
        self.assert_json_contains_key(key)
        actual_value = self.response_json[key]
        
        assert actual_value == expected_value, \
            f"Key '{key}' expected value '{expected_value}', but got '{actual_value}'"
        
        self.logger.info(f"✅ JSON value assertion passed: {key}={actual_value}")
        return self
    
    def assert_json_value_not_none(self, key: str) -> 'APIAssertions':
        """
        Assert JSON response key value is not None.
        
        Args:
            key: Key name
            
        Returns:
            Self for method chaining
        """
        self.assert_json_contains_key(key)
        actual_value = self.response_json[key]
        
        assert actual_value is not None, f"Key '{key}' is None"
        
        self.logger.info(f"✅ JSON value not None assertion passed: {key}")
        return self
    
    def assert_json_value_type(self, key: str, expected_type: type) -> 'APIAssertions':
        """
        Assert JSON response key value type.
        
        Args:
            key: Key name
            expected_type: Expected Python type
            
        Returns:
            Self for method chaining
        """
        self.assert_json_contains_key(key)
        actual_value = self.response_json[key]
        
        assert isinstance(actual_value, expected_type), \
            f"Key '{key}' expected type {expected_type.__name__}, " \
            f"but got {type(actual_value).__name__}"
        
        self.logger.info(f"✅ JSON value type assertion passed: {key} is {expected_type.__name__}")
        return self
    
    def assert_json_nested_value(self, key_path: str, expected_value: Any, 
                                 separator: str = '.') -> 'APIAssertions':
        """
        Assert nested JSON value using dot notation.
        
        Args:
            key_path: Dot-separated key path (e.g., 'data.user.id')
            expected_value: Expected value
            separator: Path separator (default: '.')
            
        Returns:
            Self for method chaining
        """
        keys = key_path.split(separator)
        current = self.response_json
        
        for key in keys:
            assert isinstance(current, dict) and key in current, \
                f"Key path '{key_path}' not found in response"
            current = current[key]
        
        assert current == expected_value, \
            f"Key path '{key_path}' expected value '{expected_value}', but got '{current}'"
        
        self.logger.info(f"✅ Nested JSON value assertion passed: {key_path}={current}")
        return self
    
    def assert_json_list_length(self, key: str, expected_length: int) -> 'APIAssertions':
        """
        Assert JSON list length.
        
        Args:
            key: Key name containing list
            expected_length: Expected list length
            
        Returns:
            Self for method chaining
        """
        self.assert_json_contains_key(key)
        actual_list = self.response_json[key]
        
        assert isinstance(actual_list, list), \
            f"Key '{key}' is not a list, got {type(actual_list).__name__}"
        
        actual_length = len(actual_list)
        assert actual_length == expected_length, \
            f"List '{key}' expected length {expected_length}, but got {actual_length}"
        
        self.logger.info(f"✅ JSON list length assertion passed: {key} has {actual_length} items")
        return self
    
    def assert_json_list_not_empty(self, key: str) -> 'APIAssertions':
        """
        Assert JSON list is not empty.
        
        Args:
            key: Key name containing list
            
        Returns:
            Self for method chaining
        """
        self.assert_json_contains_key(key)
        actual_list = self.response_json[key]
        
        assert isinstance(actual_list, list), \
            f"Key '{key}' is not a list"
        assert len(actual_list) > 0, \
            f"List '{key}' is empty"
        
        self.logger.info(f"✅ JSON list not empty assertion passed: {key}")
        return self
    
    def assert_json_schema(self, schema: Dict) -> 'APIAssertions':
        """
        Validate response against JSON schema.
        
        Args:
            schema: JSON schema dictionary
            
        Returns:
            Self for method chaining
        """
        try:
            validate(instance=self.response_json, schema=schema)
            self.logger.info("✅ JSON schema validation passed")
        except ValidationError as e:
            self.logger.error(f"JSON schema validation failed: {e.message}")
            raise AssertionError(f"JSON schema validation failed: {e.message}")
        
        return self
    
    def assert_response_time_less_than(self, max_time_ms: int) -> 'APIAssertions':
        """
        Assert response time is less than specified milliseconds.
        
        Args:
            max_time_ms: Maximum response time in milliseconds
            
        Returns:
            Self for method chaining
        """
        actual_time_ms = self.response.elapsed.total_seconds() * 1000
        
        assert actual_time_ms < max_time_ms, \
            f"Response time {actual_time_ms:.2f}ms exceeds maximum {max_time_ms}ms"
        
        self.logger.info(f"✅ Response time assertion passed: {actual_time_ms:.2f}ms")
        return self
    
    def assert_json_contains_keys(self, keys: List[str]) -> 'APIAssertions':
        """
        Assert JSON response contains all specified keys.
        
        Args:
            keys: List of key names to check
            
        Returns:
            Self for method chaining
        """
        for key in keys:
            self.assert_json_contains_key(key)
        
        return self
    
    def get_json_value(self, key: str, default: Any = None) -> Any:
        """
        Get value from JSON response.
        
        Args:
            key: Key name
            default: Default value if key not found
            
        Returns:
            Value from response
        """
        return self.response_json.get(key, default)
