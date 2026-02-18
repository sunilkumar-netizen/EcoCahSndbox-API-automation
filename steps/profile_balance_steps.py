"""
Step definitions for Wallet Profile Balance API (Check Balance)
Endpoint: GET /bff/v1/wallet/profile/balance
"""

from behave import given, when, then
from core.api_client import APIClient
import logging
import uuid

logger = logging.getLogger(__name__)


@given('I have profile balance query parameters')
def step_have_profile_balance_query_params(context):
    """
    Parse profile balance query parameters from data table.
    Expected fields: currency, providerCode
    """
    # Initialize query parameters dictionary
    context.profile_balance_params = {}
    
    # Parse data table
    for row in context.table:
        field = row['parameter']
        value = row['value']
        context.profile_balance_params[field] = value
    
    currency = context.profile_balance_params.get('currency', 'N/A')
    provider = context.profile_balance_params.get('providerCode', 'N/A')
    
    print(f"\n✓ Profile balance query parameters prepared:")
    print(f"  Currency: {currency}")
    print(f"  Provider Code: {provider}")
    
    logger.info(f"Profile balance query params prepared - Currency: {currency}, Provider: {provider}")


@when('I send profile balance request to "{endpoint}"')
def step_send_profile_balance_request(context, endpoint):
    """
    Send GET request to profile balance endpoint with query parameters.
    Uses user token for authentication.
    """
    # Generate request ID
    request_id = str(uuid.uuid4())
    
    # Build headers
    headers = {
        'Authorization': f'Bearer {context.user_token}',
        'Content-Type': 'application/json',
        'requestId': request_id,
        'appChannel': 'sasai-super-app'
    }
    
    # Get query parameters
    params = context.profile_balance_params if hasattr(context, 'profile_balance_params') else {}
    
    currency = params.get('currency', 'N/A')
    provider = params.get('providerCode', 'N/A')
    
    print(f"\nSending GET request to {endpoint}")
    print(f"Query parameters:")
    print(f"  currency: {currency}")
    print(f"  providerCode: {provider}")
    print(f"Headers: {list(headers.keys())}")
    
    logger.info(f"Sending profile balance request - Currency: {currency}, Provider: {provider}")
    
    # Send GET request with error handling
    api_client = APIClient(context.base_test.config)
    
    try:
        context.response = api_client.get(
            endpoint,
            params=params,
            headers=headers
        )
        context.base_test.response = context.response
        
        print(f"✅ Response status: {context.response.status_code}")
        
        if context.response.status_code != 200:
            print(f"⚠️ Non-200 Response body: {context.response.text[:500]}")
        
        logger.info(f"Profile balance request sent - Status: {context.response.status_code}")
        
    except Exception as e:
        # Capture detailed error information for reporting
        error_details = {
            'error_type': type(e).__name__,
            'error_message': str(e),
            'endpoint': endpoint,
            'currency': params.get('currency', 'Unknown'),
            'provider': params.get('providerCode', 'Unknown'),
            'request_id': request_id
        }
        
        print(f"\n{'='*80}")
        print(f"❌ BACKEND ERROR DETAILS:")
        print(f"{'='*80}")
        print(f"Error Type: {error_details['error_type']}")
        print(f"Error Message: {error_details['error_message']}")
        print(f"Endpoint: {error_details['endpoint']}")
        print(f"Currency: {error_details['currency']}")
        print(f"Provider: {error_details['provider']}")
        print(f"Request ID: {error_details['request_id']}")
        print(f"{'='*80}\n")
        
        # Check if it's a 500 error
        if '500' in str(e).lower() or 'internal server error' in str(e).lower():
            print("🔴 This is a BACKEND API SERVER ERROR (HTTP 500)")
            print("   The request is correct, but the API backend cannot process it")
            print("   This issue needs to be fixed by the backend team\n")
        
        logger.error(f"Profile balance request failed: {error_details}")
        
        # Store error details in context
        context.error_details = error_details
        
        # Re-raise the exception
        raise


@when('I send profile balance request without token to "{endpoint}"')
def step_send_profile_balance_request_without_token(context, endpoint):
    """Send profile balance request without authentication token."""
    # Generate request ID
    request_id = str(uuid.uuid4())
    
    # Build headers WITHOUT Authorization
    headers = {
        'Content-Type': 'application/json',
        'requestId': request_id,
        'appChannel': 'sasai-super-app'
    }
    
    # Get query parameters
    params = context.profile_balance_params if hasattr(context, 'profile_balance_params') else {}
    
    print(f"\nSending GET request to {endpoint} WITHOUT authentication")
    print(f"Query parameters: {params}")
    
    logger.info(f"Sending profile balance request without token")
    
    # Send GET request
    api_client = APIClient(context.base_test.config)
    context.response = api_client.get(
        endpoint,
        params=params,
        headers=headers
    )
    context.base_test.response = context.response
    
    print(f"Response status: {context.response.status_code}")
    logger.info(f"Profile balance request sent without token - Status: {context.response.status_code}")


@then('response should contain profile balance information')
def step_verify_profile_balance_response(context):
    """
    Verify that response contains profile balance information.
    Checks for balance-related fields.
    """
    response_json = context.response.json()
    
    # Check for balance fields (API might return different field names)
    balance_fields = ['balance', 'balanceAmount', 'amount', 'availableBalance']
    
    has_balance = any(field in response_json for field in balance_fields)
    
    if has_balance:
        # Find which field exists
        for field in balance_fields:
            if field in response_json:
                balance_value = response_json[field]
                print(f"\n✓ Response contains profile balance information")
                print(f"  Balance field: {field}")
                print(f"  Balance value: {balance_value}")
                logger.info(f"Profile balance found - {field}: {balance_value}")
                break
    else:
        print(f"\n✗ Response missing balance information")
        print(f"Response: {response_json}")
        raise AssertionError(f"Response does not contain profile balance information. Expected one of: {balance_fields}")


@then('profile balance amount should be numeric')
def step_verify_profile_balance_numeric(context):
    """Verify that profile balance amount is numeric (int or float)."""
    response_json = context.response.json()
    
    # Check for balance fields
    balance_fields = ['balance', 'balanceAmount', 'amount', 'availableBalance']
    
    balance_found = False
    for field in balance_fields:
        if field in response_json:
            balance_value = response_json[field]
            balance_found = True
            
            # Check if numeric (int, float, or numeric string)
            is_numeric = isinstance(balance_value, (int, float))
            
            if not is_numeric and isinstance(balance_value, str):
                try:
                    float(balance_value)
                    is_numeric = True
                except ValueError:
                    pass
            
            if is_numeric:
                print(f"\n✓ Profile balance amount is numeric")
                print(f"  Field: {field}")
                print(f"  Value: {balance_value}")
                print(f"  Type: {type(balance_value).__name__}")
                logger.info(f"Profile balance is numeric - {field}: {balance_value}")
            else:
                raise AssertionError(f"Profile balance amount '{balance_value}' is not numeric")
            
            break
    
    if not balance_found:
        raise AssertionError(f"No balance field found in response. Expected one of: {balance_fields}")


@then('response should contain field "{field}" or "{alternative_field}"')
def step_verify_response_contains_field_or_alternative(context, field, alternative_field):
    """Verify that response contains either the specified field or an alternative field."""
    response_json = context.response.json()
    
    has_field = field in response_json
    has_alternative = alternative_field in response_json
    
    if has_field:
        field_value = response_json[field]
        print(f"\n✓ Response contains field: {field} = {field_value}")
        logger.info(f"Field '{field}' found in response: {field_value}")
    elif has_alternative:
        field_value = response_json[alternative_field]
        print(f"\n✓ Response contains alternative field: {alternative_field} = {field_value}")
        logger.info(f"Alternative field '{alternative_field}' found in response: {field_value}")
    else:
        print(f"\n✗ Response missing both fields: {field} and {alternative_field}")
        print(f"Response keys: {list(response_json.keys())}")
        raise AssertionError(f"Response does not contain field '{field}' or '{alternative_field}'")
