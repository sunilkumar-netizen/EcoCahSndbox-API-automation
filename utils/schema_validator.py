"""
Schema Validator Utility
Loads and validates JSON schemas for contract testing.
"""

import json
from pathlib import Path
from typing import Dict
from jsonschema import validate, ValidationError
from core.logger import Logger


class SchemaValidator:
    """
    JSON Schema validator for API contract testing.
    """
    
    def __init__(self):
        """Initialize schema validator."""
        self.logger = Logger.get_logger(__name__)
        self.schemas = {}
        self._load_schemas()
    
    def _load_schemas(self) -> None:
        """Load all JSON schemas from schemas directory."""
        schema_dir = Path(__file__).resolve().parent.parent / 'schemas'
        
        if not schema_dir.exists():
            self.logger.warning(f"Schemas directory not found: {schema_dir}")
            return
        
        for schema_file in schema_dir.glob('*.json'):
            schema_name = schema_file.stem
            with open(schema_file, 'r') as f:
                self.schemas[schema_name] = json.load(f)
            self.logger.debug(f"Loaded schema: {schema_name}")
    
    def validate(self, data: Dict, schema_name: str) -> bool:
        """
        Validate data against named schema.
        
        Args:
            data: Data to validate
            schema_name: Name of schema (without .json extension)
            
        Returns:
            True if valid
            
        Raises:
            ValidationError: If validation fails
            KeyError: If schema not found
        """
        if schema_name not in self.schemas:
            available = ', '.join(self.schemas.keys())
            raise KeyError(
                f"Schema '{schema_name}' not found. "
                f"Available schemas: {available}"
            )
        
        schema = self.schemas[schema_name]
        
        try:
            validate(instance=data, schema=schema)
            self.logger.info(f"✅ Schema validation passed: {schema_name}")
            return True
        except ValidationError as e:
            self.logger.error(f"❌ Schema validation failed: {e.message}")
            raise
    
    def get_schema(self, schema_name: str) -> Dict:
        """
        Get schema by name.
        
        Args:
            schema_name: Name of schema
            
        Returns:
            Schema dictionary
        """
        return self.schemas.get(schema_name)
    
    def list_schemas(self) -> list:
        """
        List all available schemas.
        
        Returns:
            List of schema names
        """
        return list(self.schemas.keys())
