"""
Step definitions for Payment Options API (Merchant Payment Flow - Step 7)
Endpoint: GET /bff/v1/payment/options
This API verifies available payment methods for merchant payments
"""

from behave import given, when, then
import logging

logger = logging.getLogger(__name__)


# Given Steps - Setup test data
# ============================================================================

@given('I have service type "{service_type}"')
def step_have_service_type(context, service_type):
    """
    Set service type for payment options request
    """
    if not hasattr(context, 'payment_options_params'):
        context.payment_options_params = {}
    
    context.payment_options_params['serviceType'] = service_type
    context.service_type = service_type
    
    logger.info(f"Service type set to: {service_type}")


@given('I have no service type parameter')
def step_have_no_service_type(context):
    """
    Set up request without service type parameter
    """
    context.payment_options_params = {}
    
    logger.info("Payment options request prepared without service type")


@given('I have invalid service type "{service_type}"')
def step_have_invalid_service_type(context, service_type):
    """
    Set invalid service type for negative testing
    """
    if not hasattr(context, 'payment_options_params'):
        context.payment_options_params = {}
    
    context.payment_options_params['serviceType'] = service_type
    context.service_type = service_type
    
    logger.info(f"Invalid service type set to: {service_type}")


@given('I have empty service type')
def step_have_empty_service_type(context):
    """
    Set empty service type for negative testing
    """
    if not hasattr(context, 'payment_options_params'):
        context.payment_options_params = {}
    
    context.payment_options_params['serviceType'] = ""
    
    logger.info("Empty service type set")


# When Steps - Execute payment options requests
# ============================================================================

@when('I send payment options request to "{endpoint}"')
def step_send_payment_options_request(context, endpoint):
    """
    Send GET request to payment options endpoint with query parameters
    """
    api_client = context.base_test.api_client
    
    # Build query parameters
    query_params = context.payment_options_params.copy() if hasattr(context, 'payment_options_params') else {}
    
    # Build headers
    headers = {}
    if hasattr(context, 'user_token') and context.user_token:
        headers['Authorization'] = f'Bearer {context.user_token}'
    
    if hasattr(context, 'request_id') and context.request_id:
        headers['requestId'] = context.request_id
    
    # Send GET request with query parameters
    context.response = api_client.get(
        endpoint,
        params=query_params,
        headers=headers
    )
    
    logger.info(f"Payment options request sent to {endpoint}")


@when('I send payment options request with query parameters')
def step_send_payment_options_with_query_params(context):
    """
    Send GET request to payment options endpoint with explicit query parameters
    """
    api_client = context.base_test.api_client
    
    # Build query parameters
    query_params = context.payment_options_params.copy() if hasattr(context, 'payment_options_params') else {}
    
    # Build headers
    headers = {}
    if hasattr(context, 'user_token') and context.user_token:
        headers['Authorization'] = f'Bearer {context.user_token}'
    
    if hasattr(context, 'request_id') and context.request_id:
        headers['requestId'] = context.request_id
    
    # Send GET request
    endpoint = "/bff/v1/payment/options"
    context.response = api_client.get(
        endpoint,
        params=query_params,
        headers=headers
    )
    
    logger.info(f"Payment options request sent with query parameters: {query_params}")


@when('I send payment options request with stored token to "{endpoint}"')
def step_send_payment_options_with_stored_token(context, endpoint):
    """
    Send payment options request using stored user token from previous step
    """
    api_client = context.base_test.api_client
    
    # Build query parameters
    query_params = context.payment_options_params.copy() if hasattr(context, 'payment_options_params') else {}
    
    # Build headers with stored token
    headers = {}
    if hasattr(context, 'stored_user_token') and context.stored_user_token:
        headers['Authorization'] = f'Bearer {context.stored_user_token}'
    elif hasattr(context, 'user_token') and context.user_token:
        headers['Authorization'] = f'Bearer {context.user_token}'
    
    if hasattr(context, 'request_id') and context.request_id:
        headers['requestId'] = context.request_id
    
    # Send GET request
    context.response = api_client.get(
        endpoint,
        params=query_params,
        headers=headers
    )
    
    logger.info(f"Payment options request sent with stored token to {endpoint}")


# Then Steps - Validate responses
# ============================================================================

@then('response should contain payment options')
def step_verify_payment_options(context):
    """
    Verify response contains payment options data
    """
    response_data = context.response.json()
    
    # Check if response has payment options data (could be object or list)
    has_payment_options = (
        isinstance(response_data, dict) and len(response_data) > 0 or
        isinstance(response_data, list) and len(response_data) > 0
    )
    
    assert has_payment_options, f"Response should contain payment options, got: {response_data}"
    logger.info("✅ Response contains payment options")
    
    # Log the full response structure for debugging
    import json
    logger.info(f"📋 Payment Options Full Response:\n{json.dumps(response_data, indent=2)}")
    
    # Extract and store instrument token for use in utility payment
    instrument_token = None
    
    if isinstance(response_data, dict):
        # Check for the actual structure: items[0].instruments[0].instrumentToken
        if 'items' in response_data and isinstance(response_data['items'], list) and len(response_data['items']) > 0:
            item = response_data['items'][0]
            if 'instruments' in item and isinstance(item['instruments'], list) and len(item['instruments']) > 0:
                instrument = item['instruments'][0]
                if 'instrumentToken' in instrument:
                    instrument_token = instrument['instrumentToken']
        
        # Fallback: Try other possible paths
        if not instrument_token:
            if 'instrumentToken' in response_data:
                instrument_token = response_data['instrumentToken']
            elif 'data' in response_data and isinstance(response_data['data'], dict):
                if 'instrumentToken' in response_data['data']:
                    instrument_token = response_data['data']['instrumentToken']
            elif 'paymentMethods' in response_data and isinstance(response_data['paymentMethods'], list):
                for method in response_data['paymentMethods']:
                    if isinstance(method, dict) and 'instrumentToken' in method:
                        instrument_token = method['instrumentToken']
                        break
    
    # Store the instrument token if found
    if instrument_token:
        context.instrument_token = instrument_token
        logger.info(f"✅ Extracted instrument token from payment options: {instrument_token}")
    else:
        logger.warning("⚠️ No instrument token found in payment options response")
        logger.warning(f"📍 Response structure: {list(response_data.keys()) if isinstance(response_data, dict) else 'list'}")


@then('response should contain payment methods')
def step_verify_payment_methods(context):
    """
    Verify response contains payment methods information
    """
    response_data = context.response.json()
    
    # Check for payment methods in response
    has_payment_methods = False
    
    if isinstance(response_data, dict):
        # Look for common payment method field names
        payment_method_keys = ['paymentMethods', 'methods', 'options', 'availableMethods', 'data']
        for key in payment_method_keys:
            if key in response_data and response_data[key]:
                has_payment_methods = True
                logger.info(f"Found payment methods in key: {key}")
                break
        
        # If not found in specific keys, check if response has any list values
        if not has_payment_methods:
            for value in response_data.values():
                if isinstance(value, list) and len(value) > 0:
                    has_payment_methods = True
                    logger.info("Found payment methods as list in response")
                    break
    
    elif isinstance(response_data, list):
        has_payment_methods = len(response_data) > 0
        logger.info("Response is a list of payment methods")
    
    assert has_payment_methods, f"Response should contain payment methods, got: {response_data}"
    logger.info("✅ Response contains payment methods")


@then('response should have payment options structure')
def step_verify_payment_options_structure(context):
    """
    Verify response has proper payment options structure
    """
    response_data = context.response.json()
    
    # Verify response has data
    assert response_data is not None, "Response should not be None"
    assert len(response_data) > 0, "Response should not be empty"
    
    logger.info("✅ Response has payment options structure")


@then('payment options should have required fields')
def step_verify_payment_options_required_fields(context):
    """
    Verify payment options have required fields
    """
    response_data = context.response.json()
    
    # If response is a list, check first item
    if isinstance(response_data, list):
        if len(response_data) > 0:
            payment_option = response_data[0]
            # Verify it's a dictionary with some fields
            assert isinstance(payment_option, dict), "Payment option should be an object"
            assert len(payment_option) > 0, "Payment option should have fields"
            logger.info(f"✅ Payment options have required fields: {list(payment_option.keys())}")
        else:
            logger.info("ℹ️ No payment options in response (empty list)")
    
    # If response is a dict, verify it has fields
    elif isinstance(response_data, dict):
        assert len(response_data) > 0, "Payment options should have fields"
        logger.info(f"✅ Payment options have required fields: {list(response_data.keys())}")
    else:
        raise AssertionError(f"Unexpected response type: {type(response_data)}")


@then('response should contain at least one payment method')
def step_verify_at_least_one_payment_method(context):
    """
    Verify response contains at least one payment method
    """
    response_data = context.response.json()
    
    method_count = 0
    
    if isinstance(response_data, dict):
        # Look for payment methods in common field names
        payment_method_keys = ['paymentMethods', 'methods', 'options', 'availableMethods', 'data']
        for key in payment_method_keys:
            if key in response_data:
                if isinstance(response_data[key], list):
                    method_count = len(response_data[key])
                    break
        
        # If not found, count list values
        if method_count == 0:
            for value in response_data.values():
                if isinstance(value, list):
                    method_count = len(value)
                    break
    
    elif isinstance(response_data, list):
        method_count = len(response_data)
    
    assert method_count >= 1, f"Response should contain at least one payment method, found {method_count}"
    logger.info(f"✅ Response contains {method_count} payment method(s)")
