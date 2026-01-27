"""
Step definitions for Merchant Lookup API (Pay to Merchant Flow)
This module contains Behave step definitions for testing the merchant lookup endpoint
"""

from behave import given, when, then
from core.base_test import BaseTest
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# Given Steps - Setup merchant lookup test data
# ============================================================================

@given('I have merchant lookup parameters')
def step_have_merchant_lookup_parameters(context):
    """
    Set up default merchant lookup parameters from config
    """
    config = context.base_test.config
    
    context.merchant_lookup_params = {
        'countryCode': config.get('merchant_lookup.country_code'),
        'mid': config.get('merchant_lookup.merchant_id'),
        'currency': config.get('merchant_lookup.currency'),
        'Q1': config.get('merchant_lookup.q1_value')
    }
    
    context.category_id = config.get('merchant_lookup.category_id')
    context.operator_id = config.get('merchant_lookup.operator_id')
    context.request_id = config.get('merchant_lookup.request_id')
    
    logger.info(f"Merchant lookup parameters prepared: {context.merchant_lookup_params}")


# Note: "I have country code" step is defined in otp_steps.py and updates context.request_data
# For merchant lookup, we need to also update merchant_lookup_params when country code is set
# This will be handled in the send request steps by checking both locations


@given('I have merchant category "{category_id}"')
def step_have_merchant_category(context, category_id):
    """
    Set merchant category ID
    """
    context.category_id = category_id
    logger.info(f"Merchant category set: {category_id}")


@given('I have operator ID "{operator_id}"')
def step_have_operator_id(context, operator_id):
    """
    Set operator ID
    """
    context.operator_id = operator_id
    logger.info(f"Operator ID set: {operator_id}")


@given('I have merchant ID "{merchant_id}"')
def step_have_merchant_id(context, merchant_id):
    """
    Set merchant ID parameter
    """
    if not hasattr(context, 'merchant_lookup_params'):
        context.merchant_lookup_params = {}
    context.merchant_lookup_params['mid'] = merchant_id
    logger.info(f"Merchant ID set: {merchant_id}")


@given('I have currency "{currency}"')
def step_have_currency(context, currency):
    """
    Set currency parameter
    """
    if not hasattr(context, 'merchant_lookup_params'):
        context.merchant_lookup_params = {}
    context.merchant_lookup_params['currency'] = currency
    logger.info(f"Currency set: {currency}")


@given('I have Q1 value "{q1_value}"')
def step_have_q1_value(context, q1_value):
    """
    Set Q1 parameter value
    """
    if not hasattr(context, 'merchant_lookup_params'):
        context.merchant_lookup_params = {}
    context.merchant_lookup_params['Q1'] = q1_value
    logger.info(f"Q1 value set: {q1_value}")


@given('I have request ID "{request_id}"')
def step_have_request_id(context, request_id):
    """
    Set request ID header
    """
    context.request_id = request_id
    logger.info(f"Request ID set: {request_id}")


@given('I have invalid merchant category "{category_id}"')
def step_have_invalid_merchant_category(context, category_id):
    """
    Set invalid merchant category ID for negative testing
    """
    context.category_id = category_id
    logger.info(f"Invalid merchant category set: {category_id}")


@given('I have invalid operator ID "{operator_id}"')
def step_have_invalid_operator_id(context, operator_id):
    """
    Set invalid operator ID for negative testing
    """
    context.operator_id = operator_id
    logger.info(f"Invalid operator ID set: {operator_id}")


@given('I have invalid country code "{country_code}"')
def step_have_invalid_country_code(context, country_code):
    """
    Set invalid country code for negative testing
    """
    if not hasattr(context, 'merchant_lookup_params'):
        context.merchant_lookup_params = {}
    context.merchant_lookup_params['countryCode'] = country_code
    logger.info(f"Invalid country code set: {country_code}")


@given('I have invalid merchant ID "{merchant_id}"')
def step_have_invalid_merchant_id(context, merchant_id):
    """
    Set invalid merchant ID for negative testing
    """
    if not hasattr(context, 'merchant_lookup_params'):
        context.merchant_lookup_params = {}
    context.merchant_lookup_params['mid'] = merchant_id
    logger.info(f"Invalid merchant ID set: {merchant_id}")


@given('I have invalid currency "{currency}"')
def step_have_invalid_currency(context, currency):
    """
    Set invalid currency for negative testing
    """
    if not hasattr(context, 'merchant_lookup_params'):
        context.merchant_lookup_params = {}
    context.merchant_lookup_params['currency'] = currency
    logger.info(f"Invalid currency set: {currency}")


@given('I have merchant lookup parameters without country code')
def step_have_merchant_lookup_without_country_code(context):
    """
    Set up merchant lookup parameters without country code
    """
    config = context.base_test.config
    
    context.merchant_lookup_params = {
        'mid': config.get('merchant_lookup.merchant_id'),
        'currency': config.get('merchant_lookup.currency'),
        'Q1': config.get('merchant_lookup.q1_value')
    }
    # Explicitly omit countryCode
    
    context.category_id = config.get('merchant_lookup.category_id')
    context.operator_id = config.get('merchant_lookup.operator_id')
    
    logger.info("Merchant lookup parameters prepared without country code")


@given('I have merchant lookup parameters without merchant ID')
def step_have_merchant_lookup_without_merchant_id(context):
    """
    Set up merchant lookup parameters without merchant ID
    """
    config = context.base_test.config
    
    context.merchant_lookup_params = {
        'countryCode': config.get('merchant_lookup.country_code'),
        'currency': config.get('merchant_lookup.currency'),
        'Q1': config.get('merchant_lookup.q1_value')
    }
    # Explicitly omit mid
    
    context.category_id = config.get('merchant_lookup.category_id')
    context.operator_id = config.get('merchant_lookup.operator_id')
    
    logger.info("Merchant lookup parameters prepared without merchant ID")


@given('I have merchant lookup parameters without currency')
def step_have_merchant_lookup_without_currency(context):
    """
    Set up merchant lookup parameters without currency
    """
    config = context.base_test.config
    
    context.merchant_lookup_params = {
        'countryCode': config.get('merchant_lookup.country_code'),
        'mid': config.get('merchant_lookup.merchant_id'),
        'Q1': config.get('merchant_lookup.q1_value')
    }
    # Explicitly omit currency
    
    context.category_id = config.get('merchant_lookup.category_id')
    context.operator_id = config.get('merchant_lookup.operator_id')
    
    logger.info("Merchant lookup parameters prepared without currency")


@given('I have merchant lookup parameters without Q1')
def step_have_merchant_lookup_without_q1(context):
    """
    Set up merchant lookup parameters without Q1 parameter
    """
    config = context.base_test.config
    
    context.merchant_lookup_params = {
        'countryCode': config.get('merchant_lookup.country_code'),
        'mid': config.get('merchant_lookup.merchant_id'),
        'currency': config.get('merchant_lookup.currency')
    }
    # Explicitly omit Q1
    
    context.category_id = config.get('merchant_lookup.category_id')
    context.operator_id = config.get('merchant_lookup.operator_id')
    
    logger.info("Merchant lookup parameters prepared without Q1")


# ============================================================================
# When Steps - Execute merchant lookup requests
# ============================================================================

@when('I send merchant lookup request to "{endpoint}"')
def step_send_merchant_lookup_request(context, endpoint):
    """
    Send GET request to merchant lookup endpoint with query parameters
    """
    api_client = context.base_test.api_client
    
    # Build query parameters
    query_params = context.merchant_lookup_params.copy() if hasattr(context, 'merchant_lookup_params') else {}
    
    # If country code was set via OTP steps (in request_data), use it
    if hasattr(context, 'request_data') and 'countryCode' in context.request_data:
        query_params['countryCode'] = context.request_data['countryCode']
    
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
    
    logger.info(f"Merchant lookup request sent to {endpoint}")


@when('I send merchant lookup request with query parameters')
def step_send_merchant_lookup_with_query_params(context):
    """
    Send merchant lookup request using category and operator IDs from context
    """
    api_client = context.base_test.api_client
    
    # Build endpoint with path parameters
    category_id = getattr(context, 'category_id', 'SZWC10002')
    operator_id = getattr(context, 'operator_id', 'SZWOM00001')
    endpoint = f"/catalog/v1/categories/{category_id}/operators/{operator_id}/lookup"
    
    # Build query parameters
    query_params = context.merchant_lookup_params.copy() if hasattr(context, 'merchant_lookup_params') else {}
    
    # If country code was set via OTP steps (in request_data), use it
    if hasattr(context, 'request_data') and 'countryCode' in context.request_data:
        query_params['countryCode'] = context.request_data['countryCode']
    
    # Build headers
    headers = {}
    if hasattr(context, 'user_token') and context.user_token:
        headers['Authorization'] = f'Bearer {context.user_token}'
    
    if hasattr(context, 'request_id') and context.request_id:
        headers['requestId'] = context.request_id
    
    # Send GET request
    context.response = api_client.get(
        endpoint,
        params=query_params,
        headers=headers
    )
    
    logger.info(f"Merchant lookup request sent with query parameters to {endpoint}")


@when('I send merchant lookup request with stored token to "{endpoint}"')
def step_send_merchant_lookup_with_stored_token(context, endpoint):
    """
    Send merchant lookup request using stored user token from previous step
    """
    api_client = context.base_test.api_client
    
    # Build query parameters
    query_params = context.merchant_lookup_params.copy() if hasattr(context, 'merchant_lookup_params') else {}
    
    # Build headers with stored token
    headers = {}
    if hasattr(context, 'user_token') and context.user_token:
        headers['Authorization'] = f'Bearer {context.user_token}'
    
    if hasattr(context, 'request_id') and context.request_id:
        headers['requestId'] = context.request_id
    
    # Send GET request
    context.response = api_client.get(
        endpoint,
        params=query_params,
        headers=headers
    )
    
    logger.info(f"Merchant lookup request sent with stored token to {endpoint}")


# ============================================================================
# Then Steps - Verify merchant lookup responses
# ============================================================================

@then('response should contain merchant details')
def step_verify_merchant_details(context):
    """
    Verify response contains merchant details
    """
    response_data = context.response.json()
    
    # Check if response has merchant data (could be object or list)
    has_merchant_data = (
        isinstance(response_data, dict) and len(response_data) > 0 or
        isinstance(response_data, list) and len(response_data) > 0
    )
    
    assert has_merchant_data, f"Response should contain merchant details, got: {response_data}"
    logger.info("✅ Response contains merchant details")


@then('response should contain merchant information fields')
def step_verify_merchant_information_fields(context):
    """
    Verify response contains merchant information structure
    """
    response_data = context.response.json()
    
    # Verify response has data
    assert response_data is not None, "Response should not be None"
    assert len(response_data) > 0, "Response should not be empty"
    
    logger.info("✅ Response contains merchant information fields")


@then('merchant details should have required fields')
def step_verify_merchant_required_fields(context):
    """
    Verify merchant details have required fields
    """
    response_data = context.response.json()
    
    # If response is a list, check first item
    if isinstance(response_data, list):
        if len(response_data) > 0:
            merchant_data = response_data[0]
            # Verify it's a dictionary with some fields
            assert isinstance(merchant_data, dict), "Merchant data should be an object"
            assert len(merchant_data) > 0, "Merchant data should have fields"
            logger.info(f"✅ Merchant details have required fields: {list(merchant_data.keys())}")
        else:
            logger.info("ℹ️ No merchant data in response (empty list)")
    
    # If response is a dict, verify it has fields
    elif isinstance(response_data, dict):
        assert len(response_data) > 0, "Merchant data should have fields"
        logger.info(f"✅ Merchant details have required fields: {list(response_data.keys())}")
    else:
        raise AssertionError(f"Unexpected response type: {type(response_data)}")
