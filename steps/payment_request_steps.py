"""
Step definitions for Payment Request API
POST /bff/v3/order/payment/request

This API creates a payment request from a beneficiary to request money from a payer.
Requires user token (accessToken) from PIN Verify API.
"""

import requests
from behave import given, when, then
import logging

logger = logging.getLogger(__name__)


@given('I have payment request details')
@when('I have payment request details')
@then('I have payment request details')
def step_have_payment_request_details(context):
    """
    Prepare payment request payload with all required fields.
    
    Expected table format:
    | field       | value                                  |
    | feeAmount   | 0.0                                    |
    | currency    | ZWG                                    |
    | payerAmount | 3                                      |
    | payeeAmount | 3                                      |
    | channel     | sasai-super-app                        |
    | customerId  | ef1ebf57-8e9b-4c6c-be89-de72dfd7376c   |
    | message     | Test Payment Request                    |
    """
    data = {}
    for row in context.table:
        data[row['field']] = row['value']
    
    # Convert numeric fields
    fee_amount = float(data.get('feeAmount', 0.0))
    payer_amount = float(data.get('payerAmount', 0))
    payee_amount = float(data.get('payeeAmount', 0))
    
    # Build the request payload
    context.payment_request_payload = {
        "feeAmount": fee_amount,
        "currency": data.get('currency', 'ZWG'),
        "payerAmount": payer_amount,
        "channel": data.get('channel', 'sasai-super-app'),
        "beneficiaryDetails": {
            "payeeAmount": payee_amount
        },
        "payerDetails": {
            "customerId": data.get('customerId')
        },
        "notes": {
            "message": data.get('message', '')
        }
    }
    
    logger.info(f"Payment Request Payload: {context.payment_request_payload}")


@given('I have payment request without feeAmount')
def step_have_payment_request_without_fee_amount(context):
    """Prepare payment request payload without feeAmount field."""
    data = {}
    for row in context.table:
        data[row['field']] = row['value']
    
    payer_amount = float(data.get('payerAmount', 0))
    payee_amount = float(data.get('payeeAmount', 0))
    
    context.payment_request_payload = {
        "currency": data.get('currency', 'ZWG'),
        "payerAmount": payer_amount,
        "channel": data.get('channel', 'sasai-super-app'),
        "beneficiaryDetails": {
            "payeeAmount": payee_amount
        },
        "payerDetails": {
            "customerId": data.get('customerId')
        },
        "notes": {
            "message": data.get('message', '')
        }
    }
    logger.info(f"Payment Request Payload (without feeAmount): {context.payment_request_payload}")


@given('I have payment request without currency')
def step_have_payment_request_without_currency(context):
    """Prepare payment request payload without currency field."""
    data = {}
    for row in context.table:
        data[row['field']] = row['value']
    
    fee_amount = float(data.get('feeAmount', 0.0))
    payer_amount = float(data.get('payerAmount', 0))
    payee_amount = float(data.get('payeeAmount', 0))
    
    context.payment_request_payload = {
        "feeAmount": fee_amount,
        "payerAmount": payer_amount,
        "channel": data.get('channel', 'sasai-super-app'),
        "beneficiaryDetails": {
            "payeeAmount": payee_amount
        },
        "payerDetails": {
            "customerId": data.get('customerId')
        },
        "notes": {
            "message": data.get('message', '')
        }
    }
    logger.info(f"Payment Request Payload (without currency): {context.payment_request_payload}")


@given('I have payment request without payerAmount')
def step_have_payment_request_without_payer_amount(context):
    """Prepare payment request payload without payerAmount field."""
    data = {}
    for row in context.table:
        data[row['field']] = row['value']
    
    fee_amount = float(data.get('feeAmount', 0.0))
    payee_amount = float(data.get('payeeAmount', 0))
    
    context.payment_request_payload = {
        "feeAmount": fee_amount,
        "currency": data.get('currency', 'ZWG'),
        "channel": data.get('channel', 'sasai-super-app'),
        "beneficiaryDetails": {
            "payeeAmount": payee_amount
        },
        "payerDetails": {
            "customerId": data.get('customerId')
        },
        "notes": {
            "message": data.get('message', '')
        }
    }
    logger.info(f"Payment Request Payload (without payerAmount): {context.payment_request_payload}")


@given('I have payment request without channel')
def step_have_payment_request_without_channel(context):
    """Prepare payment request payload without channel field."""
    data = {}
    for row in context.table:
        data[row['field']] = row['value']
    
    fee_amount = float(data.get('feeAmount', 0.0))
    payer_amount = float(data.get('payerAmount', 0))
    payee_amount = float(data.get('payeeAmount', 0))
    
    context.payment_request_payload = {
        "feeAmount": fee_amount,
        "currency": data.get('currency', 'ZWG'),
        "payerAmount": payer_amount,
        "beneficiaryDetails": {
            "payeeAmount": payee_amount
        },
        "payerDetails": {
            "customerId": data.get('customerId')
        },
        "notes": {
            "message": data.get('message', '')
        }
    }
    logger.info(f"Payment Request Payload (without channel): {context.payment_request_payload}")


@given('I have payment request without customerId')
def step_have_payment_request_without_customer_id(context):
    """Prepare payment request payload without customerId field."""
    data = {}
    for row in context.table:
        data[row['field']] = row['value']
    
    fee_amount = float(data.get('feeAmount', 0.0))
    payer_amount = float(data.get('payerAmount', 0))
    payee_amount = float(data.get('payeeAmount', 0))
    
    context.payment_request_payload = {
        "feeAmount": fee_amount,
        "currency": data.get('currency', 'ZWG'),
        "payerAmount": payer_amount,
        "channel": data.get('channel', 'sasai-super-app'),
        "beneficiaryDetails": {
            "payeeAmount": payee_amount
        },
        "payerDetails": {},
        "notes": {
            "message": data.get('message', '')
        }
    }
    logger.info(f"Payment Request Payload (without customerId): {context.payment_request_payload}")


@given('I have payment request details with extracted customer')
@when('I have payment request details with extracted customer')
@then('I have payment request details with extracted customer')
def step_have_payment_request_details_with_extracted_customer(context):
    """
    Prepare payment request payload using extracted customerId from previous response.
    This allows dynamic customer ID instead of hardcoded values.
    
    Expected table format:
    | field       | value                                  |
    | feeAmount   | 0.0                                    |
    | currency    | ZWG                                    |
    | payerAmount | 3                                      |
    | payeeAmount | 3                                      |
    | channel     | sasai-super-app                        |
    | message     | Test Payment Request                    |
    """
    data = {}
    for row in context.table:
        data[row['field']] = row['value']
    
    # Get customerId from context (extracted from previous response)
    customer_id = getattr(context, 'customerId', None)
    
    if not customer_id:
        # Fall back to hardcoded value if not extracted
        customer_id = "ef1ebf57-8e9b-4c6c-be89-de72dfd7376c"
        logger.warning(f"⚠️ customerId not found in context, using default: {customer_id}")
    else:
        logger.info(f"✓ Using extracted customerId: {customer_id}")
    
    # Convert numeric fields
    fee_amount = float(data.get('feeAmount', 0.0))
    payer_amount = float(data.get('payerAmount', 0))
    payee_amount = float(data.get('payeeAmount', 0))
    
    # Build the request payload with dynamic customerId
    context.payment_request_payload = {
        "feeAmount": fee_amount,
        "currency": data.get('currency', 'ZWG'),
        "payerAmount": payer_amount,
        "channel": data.get('channel', 'sasai-super-app'),
        "beneficiaryDetails": {
            "payeeAmount": payee_amount
        },
        "payerDetails": {
            "customerId": customer_id  # Dynamic customer ID from context
        },
        "notes": {
            "message": data.get('message', '')
        }
    }
    
    logger.info(f"Payment Request Payload (with dynamic customerId): {context.payment_request_payload}")


@when('I send payment request to "{endpoint}"')
def step_send_payment_request(context, endpoint):
    """
    Send payment request to the specified endpoint using user token authentication.
    
    Args:
        endpoint: API endpoint path (e.g., /bff/v3/order/payment/request)
    """
    # Get user token from context (set by PIN verification or authentication steps)
    user_token = getattr(context, 'user_token', None)
    
    # Build full URL
    base_url = context.config_loader.get('api.base_url')
    url = f"{base_url}{endpoint}"
    
    # Prepare headers
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    # Add authentication if user token is available
    if user_token:
        headers['Authorization'] = f"Bearer {user_token}"
        logger.info(f"Using user token authentication")
    else:
        logger.warning("No authentication token provided")
    
    # Get the payload
    payload = context.payment_request_payload
    
    logger.info(f"\n{'='*80}")
    logger.info(f"Creating Payment Request:")
    logger.info(f"URL: {url}")
    logger.info(f"Headers: {headers}")
    logger.info(f"Payload: {payload}")
    logger.info(f"{'='*80}\n")
    
    # Send POST request
    try:
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=30
        )
        
        logger.info(f"Response Status: {response.status_code}")
        logger.info(f"Response Headers: {dict(response.headers)}")
        logger.info(f"Response Body: {response.text[:500]}...")  # Print first 500 chars
        
        # Store response in context
        context.response = response
        context.response_json = response.json() if response.text else {}
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed with error: {str(e)}")
        context.response = None
        context.response_json = {}
        raise


@when('I update payment request message to "{message}"')
def step_update_payment_request_message(context, message):
    """
    Update the message in the payment request payload.
    Used for consecutive request scenarios.
    
    Args:
        message: New message text
    """
    if hasattr(context, 'payment_request_payload'):
        context.payment_request_payload['notes']['message'] = message
        logger.info(f"Updated payment request message to: {message}")
    else:
        raise ValueError("Payment request payload not found in context")


@then('response should contain payment request details')
def step_response_should_contain_payment_request_details(context):
    """
    Verify that response contains expected payment request details.
    
    Expected response structure (actual from API):
    {
        "orderId": "177096-5127-640377",
        "status": "created",
        "requestPayId": "e0bfeb55-76fa-4ef5-b639-f71f12595122",
        "message": "Request Sent Successfully!",
        ...
    }
    """
    response_json = context.response_json
    
    logger.info(f"\nValidating Payment Request Response:")
    logger.info(f"Full Response: {response_json}")
    
    # Check for actual fields returned by API
    expected_fields = ['orderId', 'status', 'requestPayId', 'message']
    
    for field in expected_fields:
        assert field in response_json, \
            f"Expected field '{field}' not found in response. Response: {response_json}"
        logger.info(f"✓ Found field: {field} = {response_json[field]}")
    
    logger.info("✓ Payment request response validation passed")


@then('response should contain "{field}"')
def step_response_should_contain_field(context, field):
    """
    Verify that response contains a specific field.
    
    Args:
        field: Field name to check for in response
    """
    response_json = context.response_json
    
    assert field in response_json, \
        f"Expected field '{field}' not found in response. Response: {response_json}"
    
    logger.info(f"✓ Response contains field: {field} = {response_json[field]}")


@given('I have invalid user authentication')
def step_have_invalid_user_authentication(context):
    """Set invalid user token for authentication tests."""
    context.user_token = "invalid_user_token_12345"
    logger.info("Set invalid user authentication token")


@given('I have expired user authentication')
def step_have_expired_user_authentication(context):
    """Set expired user token for authentication tests."""
    # Use a JWT token that's obviously expired
    context.user_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1MDAwMDAwMDB9.expired"
    logger.info("Set expired user authentication token")


# ============================================================================
# Payment Request Details API Steps
# GET /bff/v2/order/details/{orderId}
# ============================================================================

@then('I extract "{field}" from payment request response')
def step_extract_field_from_payment_request_response(context, field):
    """
    Extract a field from payment request response and store it in context.
    
    Args:
        field: Field name to extract (e.g., 'orderId', 'requestPayId')
    """
    response_json = context.response_json
    
    assert field in response_json, \
        f"Field '{field}' not found in payment request response. Response: {response_json}"
    
    extracted_value = response_json[field]
    
    # Store in context for later use
    if field == 'orderId':
        context.order_id = extracted_value
        logger.info(f"✓ Extracted orderId: {extracted_value}")
    elif field == 'requestPayId':
        context.request_pay_id = extracted_value
        logger.info(f"✓ Extracted requestPayId: {extracted_value}")
    else:
        setattr(context, field, extracted_value)
        logger.info(f"✓ Extracted {field}: {extracted_value}")


@given('I set order ID "{order_id}"')
def step_set_order_id(context, order_id):
    """
    Set a specific order ID for testing.
    
    Args:
        order_id: Order ID to use for the request
    """
    context.order_id = order_id
    logger.info(f"Set order ID: {order_id}")


@given('I set invalid order ID "{order_id}"')
def step_set_invalid_order_id(context, order_id):
    """
    Set an invalid order ID for negative testing.
    
    Args:
        order_id: Invalid order ID to use for the request
    """
    context.order_id = order_id
    logger.info(f"Set invalid order ID: {order_id}")


@when('I send GET request to payment request details endpoint')
def step_send_get_request_to_payment_request_details(context):
    """
    Send GET request to retrieve payment request details by order ID.
    
    Endpoint: GET /bff/v2/order/details/{orderId}
    Authentication: User token (Bearer token)
    """
    # Get order ID from context
    order_id = getattr(context, 'order_id', None)
    
    assert order_id is not None, \
        "Order ID not found. Please extract orderId from payment request response first."
    
    # Build endpoint URL
    endpoint = f"/bff/v2/order/details/{order_id}"
    base_url = context.config_loader.get('api.base_url')
    full_url = f"{base_url}{endpoint}"
    
    # Get user token
    user_token = getattr(context, 'user_token', None)
    
    # Prepare headers
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    # Add authorization if user token exists
    if user_token:
        headers['Authorization'] = f'Bearer {user_token}'
        logger.info("Using user token authentication")
    else:
        logger.info("No authentication token provided")
    
    logger.info("\n" + "="*80)
    logger.info("Getting Payment Request Details:")
    logger.info(f"URL: {full_url}")
    logger.info(f"Order ID: {order_id}")
    logger.info(f"Headers: {headers}")
    logger.info("="*80 + "\n")
    
    try:
        # Send GET request
        response = requests.get(
            full_url,
            headers=headers,
            timeout=30
        )
        
        # Store response
        context.response = response
        context.response_json = response.json() if response.text else {}
        
        logger.info(f"Response Status: {response.status_code}")
        logger.info(f"Response Headers: {dict(response.headers)}")
        logger.info(f"Response Body: {response.text[:500]}...")  # First 500 chars
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {str(e)}")
        context.response = None
        context.response_json = {}
        raise


@then('response should contain payment request order details')
def step_response_should_contain_payment_request_order_details(context):
    """
    Verify that response contains expected order details fields.
    
    Expected response structure:
    {
        "id": "string",
        "orderId": "177089-5320-994120",
        "status": "created",
        "requestPayId": "uuid",
        "amount": number,
        "currency": "ZWG",
        "customerId": "uuid",
        "payerInfo": {...},
        ...
    }
    """
    response_json = context.response_json
    
    logger.info(f"\nValidating Payment Request Details Response:")
    logger.info(f"Full Response: {response_json}")
    
    # Check for essential fields (using payerAmount instead of amount based on actual API response)
    essential_fields = ['orderId', 'status', 'payerAmount', 'currency']
    
    for field in essential_fields:
        assert field in response_json, \
            f"Expected field '{field}' not found in response. Response: {response_json}"
        logger.info(f"✓ Found field: {field} = {response_json[field]}")
    
    logger.info("✓ Payment request details response validation passed")

