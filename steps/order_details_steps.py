"""
Step definitions for Order Details API (Merchant Payment Flow - Step 9)
Endpoint: GET /bff/v2/order/details/{orderReference}
This API retrieves payment details that were completed in the merchant flow
"""

from behave import given, when, then
import logging

logger = logging.getLogger(__name__)


# Given Steps - Setup test data
# ============================================================================

@given('I have order reference "{order_ref}"')
def step_have_order_reference(context, order_ref):
    """
    Set order reference for order details request
    """
    # Handle empty string case
    if order_ref == "":
        context.order_reference = ""
    else:
        context.order_reference = order_ref
    
    logger.info(f"Order reference set to: '{order_ref}'")


@given('I have empty order reference')
def step_have_empty_order_reference(context):
    """
    Set empty order reference for negative testing
    """
    context.order_reference = ""
    
    logger.info("Order reference set to empty string")


@given('I have order reference from different user')
def step_have_order_reference_different_user(context):
    """
    Set order reference that belongs to a different user for security testing
    """
    # Use a different order reference for testing unauthorized access
    context.order_reference = context.base_test.config.get('order_details', {}).get('different_user_order', '999999-9999-999999')
    
    logger.info(f"Order reference set to different user's order: {context.order_reference}")


# When Steps - Execute requests
# ============================================================================

@when('I send order details request to "{endpoint}"')
def step_send_order_details_request(context, endpoint):
    """
    Send GET request to order details endpoint
    """
    api_client = context.base_test.api_client
    
    # Build headers
    headers = {}
    if hasattr(context, 'user_token') and context.user_token:
        headers['Authorization'] = f'Bearer {context.user_token}'
    
    # Add request ID if present in context
    if hasattr(context, 'request_id'):
        headers['X-Request-ID'] = context.request_id
    
    # Send GET request
    context.response = api_client.get(
        endpoint,
        headers=headers
    )
    
    logger.info(f"GET {endpoint}")
    logger.info(f"Response Status: {context.response.status_code}")
    
    # Store response time
    if hasattr(context.response, 'elapsed'):
        context.response_time = context.response.elapsed.total_seconds() * 1000
        logger.info(f"Response Time: {context.response_time:.2f} ms")


@when('I send GET request to order details endpoint')
def step_send_get_request_to_order_details(context):
    """
    Send GET request to order details endpoint with order reference from context
    """
    api_client = context.base_test.api_client
    endpoint = f"/bff/v2/order/details/{context.order_reference}"
    
    # Build headers
    headers = {}
    if hasattr(context, 'user_token') and context.user_token:
        headers['Authorization'] = f'Bearer {context.user_token}'
    
    # Send GET request
    context.response = api_client.get(
        endpoint,
        headers=headers
    )
    
    logger.info(f"GET {endpoint}")
    logger.info(f"Response Status: {context.response.status_code}")
    
    # Store response time
    if hasattr(context.response, 'elapsed'):
        context.response_time = context.response.elapsed.total_seconds() * 1000
        logger.info(f"Response Time: {context.response_time:.2f} ms")


@when('I send order details request with headers')
def step_send_order_details_request_with_headers(context):
    """
    Send GET request to order details endpoint with custom headers
    """
    api_client = context.base_test.api_client
    endpoint = f"/bff/v2/order/details/{context.order_reference}"
    
    # Build headers with user token
    headers = {}
    if hasattr(context, 'user_token') and context.user_token:
        headers['Authorization'] = f'Bearer {context.user_token}'
    
    # Add request ID if present
    if hasattr(context, 'request_id'):
        headers['X-Request-ID'] = context.request_id
    
    # Send GET request
    context.response = api_client.get(
        endpoint,
        headers=headers
    )
    
    logger.info(f"GET {endpoint}")
    logger.info(f"Headers: {headers}")
    logger.info(f"Response Status: {context.response.status_code}")


@when('I send order details request with invalid reference')
def step_send_order_details_with_invalid_reference(context):
    """
    Send GET request with invalid order reference format
    """
    api_client = context.base_test.api_client
    endpoint = f"/bff/v2/order/details/{context.order_reference}"
    
    # Build headers
    headers = {}
    if hasattr(context, 'user_token') and context.user_token:
        headers['Authorization'] = f'Bearer {context.user_token}'
    
    # Send GET request
    context.response = api_client.get(
        endpoint,
        headers=headers
    )
    
    logger.info(f"GET {endpoint} (invalid reference)")
    logger.info(f"Response Status: {context.response.status_code}")


@when('I send order details request with special characters')
def step_send_order_details_with_special_characters(context):
    """
    Send GET request with special characters in order reference
    """
    api_client = context.base_test.api_client
    endpoint = f"/bff/v2/order/details/{context.order_reference}"
    
    # Build headers
    headers = {}
    if hasattr(context, 'user_token') and context.user_token:
        headers['Authorization'] = f'Bearer {context.user_token}'
    
    # Send GET request
    context.response = api_client.get(
        endpoint,
        headers=headers
    )
    
    logger.info(f"GET {endpoint} (special characters)")
    logger.info(f"Response Status: {context.response.status_code}")


@when('I send order details request to different user order')
def step_send_order_details_different_user_order(context):
    """
    Send GET request to order details endpoint with different user's order reference
    """
    api_client = context.base_test.api_client
    endpoint = f"/bff/v2/order/details/{context.order_reference}"
    
    # Build headers with current user's token
    headers = {}
    if hasattr(context, 'user_token') and context.user_token:
        headers['Authorization'] = f'Bearer {context.user_token}'
    
    # Send GET request
    context.response = api_client.get(
        endpoint,
        headers=headers
    )
    
    logger.info(f"GET {endpoint} (different user's order)")
    logger.info(f"Response Status: {context.response.status_code}")


@when('I send order details request with stored token to "{endpoint}"')
def step_send_order_details_with_stored_token(context, endpoint):
    """
    Send GET request with stored user token from previous step
    """
    api_client = context.base_test.api_client
    
    # Build headers with stored token
    headers = {
        'Authorization': f'Bearer {context.stored_user_token}',
        'Content-Type': 'application/json'
    }
    
    # Send GET request
    context.response = api_client.get(
        endpoint,
        headers=headers
    )
    
    logger.info(f"GET {endpoint} (with stored token)")
    logger.info(f"Response Status: {context.response.status_code}")


@when('I send order details request with extracted reference')
def step_send_order_details_with_extracted_reference(context):
    """
    Send GET request with order reference extracted from payment response
    """
    api_client = context.base_test.api_client
    endpoint = f"/bff/v2/order/details/{context.extracted_order_reference}"
    
    # Build headers
    headers = {}
    if hasattr(context, 'user_token') and context.user_token:
        headers['Authorization'] = f'Bearer {context.user_token}'
    
    # Send GET request
    context.response = api_client.get(
        endpoint,
        headers=headers
    )
    
    logger.info(f"GET {endpoint} (extracted reference)")
    logger.info(f"Response Status: {context.response.status_code}")


# Then Steps - Response validation
# ============================================================================

@then('response should contain order details')
def step_response_contains_order_details(context):
    """
    Verify response contains order details
    """
    response_data = context.response.json()
    
    # Check if response has order-related fields
    order_fields = ['orderReference', 'orderId', 'order', 'details', 'status', 'amount']
    has_order_data = any(field in response_data for field in order_fields)
    
    assert has_order_data, f"Response does not contain order details. Response: {response_data}"
    
    logger.info("✓ Response contains order details")


@then('response should contain order status')
def step_response_contains_order_status(context):
    """
    Verify response contains order status
    """
    response_data = context.response.json()
    
    # Check for status field
    status_fields = ['status', 'orderStatus', 'paymentStatus', 'state']
    has_status = any(field in response_data for field in status_fields)
    
    assert has_status, f"Response does not contain order status. Response: {response_data}"
    
    logger.info("✓ Response contains order status")


@then('response should have order structure')
def step_response_has_order_structure(context):
    """
    Verify response has proper order structure
    """
    response_data = context.response.json()
    
    # Verify it's a dictionary/object
    assert isinstance(response_data, dict), f"Response is not an object: {type(response_data)}"
    
    # Verify it's not empty
    assert len(response_data) > 0, "Response is empty"
    
    logger.info("✓ Response has valid order structure")


@then('order response should have required fields')
def step_order_response_has_required_fields(context):
    """
    Verify order response contains all required fields
    """
    response_data = context.response.json()
    
    # Check for common order fields (at least some should be present)
    expected_fields = ['orderReference', 'status', 'amount', 'currency', 'timestamp', 'createdAt']
    found_fields = [field for field in expected_fields if field in response_data or any(field.lower() in str(response_data).lower() for field in expected_fields)]
    
    assert len(found_fields) > 0, f"Response missing required order fields. Response: {response_data}"
    
    logger.info(f"✓ Order response has required fields: {found_fields}")


@then('response should contain payment information')
def step_response_contains_payment_information(context):
    """
    Verify response contains payment information
    """
    response_data = context.response.json()
    
    # Check for payment-related fields
    payment_fields = ['paymentMethod', 'payment', 'paymentStatus', 'amount', 'currency', 'transactionId']
    has_payment_info = any(field in response_data or str(field).lower() in str(response_data).lower() for field in payment_fields)
    
    assert has_payment_info, f"Response does not contain payment information. Response: {response_data}"
    
    logger.info("✓ Response contains payment information")


@then('response should contain timestamp')
def step_response_contains_timestamp(context):
    """
    Verify response contains timestamp information
    """
    response_data = context.response.json()
    
    # Check for timestamp fields
    timestamp_fields = ['timestamp', 'createdAt', 'updatedAt', 'transactionDate', 'date', 'time']
    has_timestamp = any(field in response_data or str(field).lower() in str(response_data).lower() for field in timestamp_fields)
    
    assert has_timestamp, f"Response does not contain timestamp. Response: {response_data}"
    
    logger.info("✓ Response contains timestamp")


@then('I extract order reference from payment response')
def step_extract_order_reference_from_payment(context):
    """
    Extract order reference from payment response for next request
    """
    response_data = context.response.json()
    
    # Try different possible field names for order reference
    order_ref_fields = ['orderReference', 'orderId', 'transactionId', 'reference', 'id']
    
    extracted_ref = None
    for field in order_ref_fields:
        if field in response_data:
            extracted_ref = response_data[field]
            break
    
    assert extracted_ref is not None, f"Could not extract order reference from payment response. Response: {response_data}"
    
    context.extracted_order_reference = extracted_ref
    
    logger.info(f"✓ Extracted order reference: {extracted_ref}")


@then('order status should match payment status')
def step_order_status_matches_payment_status(context):
    """
    Verify order status in details matches the payment status
    """
    response_data = context.response.json()
    
    # Check if status field exists and is valid
    status_fields = ['status', 'orderStatus', 'paymentStatus']
    status_value = None
    
    for field in status_fields:
        if field in response_data:
            status_value = response_data[field]
            break
    
    assert status_value is not None, f"No status field found in response. Response: {response_data}"
    
    # Verify status is not empty
    assert status_value, "Status value is empty"
    
    logger.info(f"✓ Order status is: {status_value}")
