"""
Helper functions for common operations.
"""

import json
from typing import Any, Dict, List
from pathlib import Path


def load_json_file(file_path: str) -> Dict:
    """
    Load JSON file and return as dictionary.
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        Dictionary from JSON file
    """
    with open(file_path, 'r') as f:
        return json.load(f)


def save_json_file(data: Dict, file_path: str) -> None:
    """
    Save dictionary to JSON file.
    
    Args:
        data: Dictionary to save
        file_path: Path to save file
    """
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)


def replace_placeholders(template: str, values: Dict[str, Any]) -> str:
    """
    Replace {{placeholder}} in template with actual values.
    
    Args:
        template: String with {{placeholders}}
        values: Dictionary of placeholder values
        
    Returns:
        String with replaced values
    """
    result = template
    for key, value in values.items():
        placeholder = f"{{{{{key}}}}}"
        result = result.replace(placeholder, str(value))
    return result


def load_payload(payload_name: str, **replacements) -> Dict:
    """
    Load payload from payloads directory and replace placeholders.
    
    Args:
        payload_name: Name of payload file (without .json)
        **replacements: Values to replace in payload
        
    Returns:
        Payload dictionary with replaced values
    """
    payload_dir = Path(__file__).resolve().parent.parent / 'payloads'
    payload_file = payload_dir / f'{payload_name}.json'
    
    if not payload_file.exists():
        raise FileNotFoundError(f"Payload file not found: {payload_file}")
    
    with open(payload_file, 'r') as f:
        template = f.read()
    
    # Replace placeholders if any
    if replacements:
        template = replace_placeholders(template, replacements)
    
    return json.loads(template)


def flatten_dict(d: Dict, parent_key: str = '', sep: str = '.') -> Dict:
    """
    Flatten nested dictionary.
    
    Args:
        d: Dictionary to flatten
        parent_key: Parent key prefix
        sep: Separator for keys
        
    Returns:
        Flattened dictionary
        
    Example:
        {'a': {'b': 1}} -> {'a.b': 1}
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def get_nested_value(data: Dict, key_path: str, default=None, sep: str = '.'):
    """
    Get value from nested dictionary using dot notation.
    
    Args:
        data: Dictionary to search
        key_path: Dot-separated key path
        default: Default value if not found
        sep: Key separator
        
    Returns:
        Value at key path
        
    Example:
        get_nested_value({'a': {'b': 1}}, 'a.b') -> 1
    """
    keys = key_path.split(sep)
    current = data
    
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    
    return current


def set_nested_value(data: Dict, key_path: str, value: Any, sep: str = '.') -> None:
    """
    Set value in nested dictionary using dot notation.
    
    Args:
        data: Dictionary to modify
        key_path: Dot-separated key path
        value: Value to set
        sep: Key separator
        
    Example:
        set_nested_value({}, 'a.b.c', 1) -> {'a': {'b': {'c': 1}}}
    """
    keys = key_path.split(sep)
    current = data
    
    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]
    
    current[keys[-1]] = value


def filter_dict_keys(data: Dict, keys: List[str]) -> Dict:
    """
    Filter dictionary to include only specified keys.
    
    Args:
        data: Source dictionary
        keys: Keys to include
        
    Returns:
        Filtered dictionary
    """
    return {k: v for k, v in data.items() if k in keys}


def merge_dicts(*dicts: Dict) -> Dict:
    """
    Merge multiple dictionaries (later dicts override earlier ones).
    
    Args:
        *dicts: Dictionaries to merge
        
    Returns:
        Merged dictionary
    """
    result = {}
    for d in dicts:
        result.update(d)
    return result


def is_valid_json(text: str) -> bool:
    """
    Check if string is valid JSON.
    
    Args:
        text: String to check
        
    Returns:
        True if valid JSON
    """
    try:
        json.loads(text)
        return True
    except (ValueError, TypeError):
        return False


def pretty_print_json(data: Dict) -> None:
    """
    Pretty print JSON data.
    
    Args:
        data: Dictionary to print
    """
    print(json.dumps(data, indent=2, sort_keys=True))
