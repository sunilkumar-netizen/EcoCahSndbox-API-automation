"""
Step definitions for Wallet Balances - Payment Options API tests (Smoke Test Only).

This module contains minimal step definitions for testing the Payment Options API
which is used to retrieve available payment methods and wallet balances.

API Endpoint: GET /bff/v1/payment/options
Query Parameters: serviceType (e.g., ZWAllPaymentOptions)
Headers: Authorization (Bearer user token), requestId (UUID)

NOTE: This is separate from merchant payment options flow.
This API is specifically for checking wallet balances and available payment methods.
"""

import uuid
import json
from behave import given, when, then
from core.api_client import APIClient
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# GIVEN STEPS - Setup for Smoke Test
# ============================================================================

@given('I have valid request ID')
def step_have_valid_request_id(context):
    """Generate a valid UUID for request ID."""
    context.request_id = str(uuid.uuid4())
    logger.info(f"Generated request ID: {context.request_id}")


# ============================================================================
# WHEN STEPS - API Actions for Smoke Test
# ============================================================================

@when('I send wallet balance payment options request to "{endpoint}"')
def step_send_wallet_payment_options_request(context, endpoint):
    """Send GET request to payment options endpoint for wallet balances."""
    # Build query parameters
    params = {}
    if hasattr(context, 'service_type') and context.service_type is not None:
        params['serviceType'] = context.service_type
    
    # Build headers
    headers = {
        'Authorization': f'Bearer {context.user_token}',
        'requestId': context.request_id
    }
    
    print(f"Sending GET request to {endpoint}")
    print(f"Query params: {params}")
    print(f"Headers: {list(headers.keys())}")
    
    # Send GET request with error handling
    api_client = APIClient(context.base_test.config)
    
    try:
        context.response = api_client.get(endpoint, params=params, headers=headers)
        context.base_test.response = context.response
        
        print(f"✅ Response status: {context.response.status_code}")
        
        if context.response.status_code != 200:
            print(f"⚠️ Non-200 Response body: {context.response.text[:500]}")
        
        logger.info(f"Response status: {context.response.status_code}")
        
    except Exception as e:
        # Capture detailed error information for reporting
        error_details = {
            'error_type': type(e).__name__,
            'error_message': str(e),
            'endpoint': endpoint,
            'service_type': params.get('serviceType', 'Unknown'),
            'request_id': context.request_id
        }
        
        print(f"\n{'='*80}")
        print(f"❌ BACKEND ERROR DETAILS:")
        print(f"{'='*80}")
        print(f"Error Type: {error_details['error_type']}")
        print(f"Error Message: {error_details['error_message']}")
        print(f"Endpoint: {error_details['endpoint']}")
        print(f"Service Type: {error_details['service_type']}")
        print(f"Request ID: {error_details['request_id']}")
        print(f"{'='*80}\n")
        
        # Check if it's a 500 error
        if '500' in str(e).lower() or 'internal server error' in str(e).lower():
            print("🔴 This is a BACKEND API SERVER ERROR (HTTP 500)")
            print("   The request is correct, but the API backend cannot process it\n")
        
        logger.error(f"Payment options request failed: {error_details}")
        
        # Store error details in context
        context.error_details = error_details
        
        # Re-raise the exception
        raise


# ============================================================================
# THEN STEPS - Assertions for Smoke Test
# ============================================================================

@then('response should contain payment options list')
def step_response_should_contain_payment_options(context):
    """Verify response contains payment options list/array."""
    response_json = context.response.json()
    
    # Check if payment options exist in response
    assert 'items' in response_json or 'paymentOptions' in response_json or 'content' in response_json or isinstance(response_json, list), \
        f"Response does not contain payment options. Response: {json.dumps(response_json, indent=2)}"
    
    # Get payment options array
    if isinstance(response_json, list):
        payment_options = response_json
    elif 'items' in response_json:
        payment_options = response_json['items']
    elif 'paymentOptions' in response_json:
        payment_options = response_json['paymentOptions']
    elif 'content' in response_json:
        payment_options = response_json['content']
    else:
        payment_options = []
    
    assert len(payment_options) > 0, "Payment options list is empty"
    context.payment_options = payment_options
    logger.info(f"Found {len(payment_options)} payment options")
