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
    
    logger.info(f"Sending GET request to {endpoint}")
    logger.info(f"Query params: {params}")
    logger.info(f"Headers: {list(headers.keys())}")
    
    # Send GET request
    api_client = APIClient(context.base_test.config)
    context.response = api_client.get(endpoint, params=params, headers=headers)
    context.base_test.response = context.response
    
    logger.info(f"Response status: {context.response.status_code}")


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
