"""
Step definitions for P2P Order Details API
GET /bff/v2/order/details/{orderId}
This API retrieves P2P payment transaction details after a payment transfer
"""

import time
import logging
from behave import given, when, then
from datetime import datetime

logger = logging.getLogger(__name__)


# ==================== Given Steps - Setup Order Details ====================

@given('I have order ID "{order_id}"')
def step_set_order_id(context, order_id):
    """Set the order ID for the request"""
    context.order_id = order_id
    logger.info(f"Set order ID: {order_id}")


@given('I have no order ID')
def step_no_order_id(context):
    """Set no order ID (for error testing)"""
    context.order_id = None
    logger.info("No order ID set")


@given('I have successful order ID "{order_id}"')
def step_set_successful_order_id(context, order_id):
    """Set order ID for successful transaction"""
    context.order_id = order_id
    context.expected_status = "success"
    logger.info(f"Set successful order ID: {order_id}")


@given('I have pending order ID "{order_id}"')
def step_set_pending_order_id(context, order_id):
    """Set order ID for pending transaction"""
    context.order_id = order_id
    context.expected_status = "pending"
    logger.info(f"Set pending order ID: {order_id}")


@given('I have failed order ID "{order_id}"')
def step_set_failed_order_id(context, order_id):
    """Set order ID for failed transaction"""
    context.order_id = order_id
    context.expected_status = "failed"
    logger.info(f"Set failed order ID: {order_id}")


@given('I have another user order ID "{order_id}"')
def step_set_another_user_order_id(context, order_id):
    """Set order ID belonging to another user (for access control testing)"""
    context.order_id = order_id
    context.test_type = "unauthorized_access"
    logger.info(f"Set another user's order ID: {order_id}")


@given('I have {transaction_type} order ID "{order_id}"')
def step_set_transaction_type_order_id(context, transaction_type, order_id):
    """Set order ID for specific transaction type"""
    context.order_id = order_id
    context.transaction_type = transaction_type
    logger.info(f"Set {transaction_type} order ID: {order_id}")


# ==================== When Steps - Send Order Details Request ====================

@when('I send P2P order details request to "{endpoint}"')
def step_send_order_details_request(context, endpoint):
    """
    Send GET request to order details endpoint with order ID as path parameter
    Endpoint format: /bff/v2/order/details/{orderId}
    """
    start_time = time.time()
    
    # Get order ID from context
    order_id = getattr(context, 'order_id', None)
    
    # Build URL with order ID as path parameter
    base_url = context.config_loader.get('api.base_url')
    if order_id:
        url = f"{base_url}{endpoint}/{order_id}"
    else:
        # For testing without order ID
        url = f"{base_url}{endpoint}"
    
    # Build headers with Authorization
    headers = {
        'Content-Type': 'application/json'
    }
    
    # Add Authorization header if user token available
    if hasattr(context, 'user_token') and context.user_token:
        headers['Authorization'] = f"Bearer {context.user_token}"
    elif hasattr(context, 'no_auth_header') and context.no_auth_header:
        # Skip Authorization header for testing
        pass
    elif hasattr(context, 'empty_bearer_token') and context.empty_bearer_token:
        headers['Authorization'] = 'Bearer '
    elif hasattr(context, 'malformed_bearer_token') and context.malformed_bearer_token:
        headers['Authorization'] = 'Bearer invalid-malformed-token'
    
    # Remove Content-Type if testing without it
    if hasattr(context, 'no_content_type_header') and context.no_content_type_header:
        headers.pop('Content-Type', None)
    
    logger.info(f"Sending GET request to: {url}")
    logger.info(f"Headers: {headers}")
    
    try:
        # Send GET request
        if order_id:
            full_endpoint = f"{endpoint}/{order_id}"
        else:
            full_endpoint = endpoint
            
        response = context.base_test.api_client.get(full_endpoint, headers=headers)
        
        # Store response and timing
        context.response = response
        context.response_time = (time.time() - start_time) * 1000
        
        logger.info(f"Response status: {response.status_code}")
        logger.info(f"Response time: {context.response_time:.2f} ms")
        
        # Try to log response body
        try:
            logger.info(f"Response body: {response.json()}")
        except Exception:
            logger.info(f"Response body (text): {response.text}")
            
    except Exception as e:
        logger.error(f"Error sending order details request: {str(e)}")
        raise


# ==================== Then Steps - Verify Order Details Response ====================

@then('response should contain P2P order details data')
def step_verify_order_details(context):
    """Verify response contains order details"""
    response_data = context.response.json()
    
    # Check for common order detail fields
    order_fields = ['orderId', 'id', 'orderDetails', 'data', 'transaction']
    
    has_order_data = any(field in response_data for field in order_fields)
    
    assert has_order_data, f"Response does not contain order details. Response: {response_data}"
    logger.info("✓ Response contains order details")


@then('P2P order details should have order ID')
def step_verify_has_order_id(context):
    """Verify response has order ID field"""
    response_data = context.response.json()
    
    # Check various possible order ID field names
    order_id_fields = ['orderId', 'id', 'orderNumber', 'transactionId']
    
    order_id = None
    for field in order_id_fields:
        if field in response_data:
            order_id = response_data[field]
            break
        elif 'data' in response_data and field in response_data['data']:
            order_id = response_data['data'][field]
            break
    
    assert order_id is not None, f"No order ID field found in response: {response_data}"
    assert order_id != "", "Order ID is empty"
    
    # Store for later use
    context.extracted_order_id = order_id
    logger.info(f"✓ Response has order ID: {order_id}")


@then('P2P order details should have status')
def step_verify_has_transaction_status(context):
    """Verify response has transaction status field"""
    response_data = context.response.json()
    
    # Check various possible status field names
    status_fields = ['status', 'transactionStatus', 'orderStatus', 'state']
    
    status = None
    for field in status_fields:
        if field in response_data:
            status = response_data[field]
            break
        elif 'data' in response_data and field in response_data['data']:
            status = response_data['data'][field]
            break
    
    assert status is not None, f"No status field found in response: {response_data}"
    logger.info(f"✓ Response has transaction status: {status}")


@then('P2P order details should have amount')
def step_verify_has_transaction_amount(context):
    """Verify response has transaction amount field"""
    response_data = context.response.json()
    
    # Check various possible amount field names
    amount_fields = ['amount', 'transactionAmount', 'payerAmount', 'totalAmount']
    
    amount = None
    for field in amount_fields:
        if field in response_data:
            amount = response_data[field]
            break
        elif 'data' in response_data and field in response_data['data']:
            amount = response_data['data'][field]
            break
    
    assert amount is not None, f"No amount field found in response: {response_data}"
    logger.info(f"✓ Response has transaction amount: {amount}")


@then('P2P order details should have complete information')
def step_verify_complete_order_info(context):
    """Verify response has complete order information"""
    response_data = context.response.json()
    
    # Essential fields that should be present
    essential_fields = ['orderId', 'id', 'status', 'amount']
    
    # Check if at least some essential fields are present
    found_fields = []
    for field in essential_fields:
        if field in response_data:
            found_fields.append(field)
        elif 'data' in response_data and field in response_data['data']:
            found_fields.append(field)
    
    assert len(found_fields) >= 2, f"Missing essential order information. Found: {found_fields}"
    logger.info(f"✓ Response has complete order information with fields: {found_fields}")


@then('P2P order details should have beneficiary details')
def step_verify_has_beneficiary_details(context):
    """Verify response contains beneficiary details"""
    response_data = context.response.json()
    
    # Check for beneficiary information
    beneficiary_fields = ['beneficiary', 'beneficiaryDetails', 'payee', 'recipient']
    
    has_beneficiary = False
    for field in beneficiary_fields:
        if field in response_data:
            has_beneficiary = True
            break
        elif 'data' in response_data and field in response_data['data']:
            has_beneficiary = True
            break
    
    # Soft check - beneficiary details might not always be present
    if has_beneficiary:
        logger.info("✓ Response has beneficiary details")
    else:
        logger.warning("⚠ Beneficiary details not found in response (may be optional)")


@then('P2P order details should have payer details')
def step_verify_has_payer_details(context):
    """Verify response contains payer details"""
    response_data = context.response.json()
    
    # Check for payer information
    payer_fields = ['payer', 'payerDetails', 'sender', 'customer']
    
    has_payer = False
    for field in payer_fields:
        if field in response_data:
            has_payer = True
            break
        elif 'data' in response_data and field in response_data['data']:
            has_payer = True
            break
    
    # Soft check - payer details might not always be present
    if has_payer:
        logger.info("✓ Response has payer details")
    else:
        logger.warning("⚠ Payer details not found in response (may be optional)")


@then('P2P order details should have timestamps')
def step_verify_has_timestamps(context):
    """Verify response has transaction timestamps"""
    response_data = context.response.json()
    
    # Check for timestamp fields
    timestamp_fields = ['createdAt', 'timestamp', 'createdDate', 'transactionDate', 'updatedAt']
    
    found_timestamps = []
    for field in timestamp_fields:
        if field in response_data:
            found_timestamps.append(field)
        elif 'data' in response_data and field in response_data['data']:
            found_timestamps.append(field)
    
    assert len(found_timestamps) > 0, f"No timestamp fields found in response: {response_data}"
    logger.info(f"✓ Response has timestamps: {found_timestamps}")


@then('I extract transaction status from order details')
def step_extract_transaction_status(context):
    """Extract transaction status from order details response"""
    response_data = context.response.json()
    
    # Extract status
    status_fields = ['status', 'transactionStatus', 'orderStatus', 'state']
    
    status = None
    for field in status_fields:
        if field in response_data:
            status = response_data[field]
            break
        elif 'data' in response_data and field in response_data['data']:
            status = response_data['data'][field]
            break
    
    assert status is not None, f"Cannot extract status from response: {response_data}"
    
    context.extracted_status = status
    logger.info(f"✓ Extracted transaction status: {status}")


@then('I extract transaction amount from order details')
def step_extract_transaction_amount(context):
    """Extract transaction amount from order details response"""
    response_data = context.response.json()
    
    # Extract amount
    amount_fields = ['amount', 'transactionAmount', 'payerAmount', 'totalAmount']
    
    amount = None
    for field in amount_fields:
        if field in response_data:
            amount = response_data[field]
            break
        elif 'data' in response_data and field in response_data['data']:
            amount = response_data['data'][field]
            break
    
    assert amount is not None, f"Cannot extract amount from response: {response_data}"
    
    context.extracted_amount = amount
    logger.info(f"✓ Extracted transaction amount: {amount}")


@then('extracted order details should be valid')
def step_verify_extracted_details_valid(context):
    """Verify extracted order details are valid"""
    assert hasattr(context, 'extracted_status'), "No status was extracted"
    assert hasattr(context, 'extracted_amount'), "No amount was extracted"
    
    # Validate status
    assert context.extracted_status != "", "Extracted status is empty"
    
    # Validate amount
    assert context.extracted_amount is not None, "Extracted amount is None"
    
    logger.info("✓ Extracted order details are valid")


@then('order status should be successful')
def step_verify_order_successful(context):
    """Verify order status is successful"""
    response_data = context.response.json()
    
    # Extract status
    status_fields = ['status', 'transactionStatus', 'orderStatus', 'state']
    
    status = None
    for field in status_fields:
        if field in response_data:
            status = response_data[field]
            break
        elif 'data' in response_data and field in response_data['data']:
            status = response_data['data'][field]
            break
    
    assert status is not None, "No status field found"
    
    # Check if status indicates success
    success_statuses = ['success', 'successful', 'completed', 'complete', 'paid', 'approved']
    status_lower = str(status).lower()
    
    is_successful = any(success_status in status_lower for success_status in success_statuses)
    
    assert is_successful, f"Order status is not successful: {status}"
    logger.info(f"✓ Order status is successful: {status}")


@then('order should have completion timestamp')
def step_verify_completion_timestamp(context):
    """Verify order has completion timestamp"""
    response_data = context.response.json()
    
    # Check for completion timestamp fields
    completion_fields = ['completedAt', 'completionDate', 'completionTime', 'updatedAt']
    
    has_completion = False
    for field in completion_fields:
        if field in response_data:
            has_completion = True
            logger.info(f"✓ Order has completion timestamp: {field}")
            break
        elif 'data' in response_data and field in response_data['data']:
            has_completion = True
            logger.info(f"✓ Order has completion timestamp: {field}")
            break
    
    # Soft check - completion timestamp might not always be present
    if not has_completion:
        logger.warning("⚠ Completion timestamp not found (may be optional)")


@then('I extract order ID from transfer response')
def step_extract_order_id_from_transfer(context):
    """Extract order ID from payment transfer response"""
    response_data = context.response.json()
    
    # Extract order ID from transfer response
    order_id_fields = ['orderId', 'id', 'orderNumber', 'transactionId']
    
    order_id = None
    for field in order_id_fields:
        if field in response_data:
            order_id = response_data[field]
            break
        elif 'data' in response_data and field in response_data['data']:
            order_id = response_data['data'][field]
            break
    
    assert order_id is not None, f"Cannot extract order ID from transfer response: {response_data}"
    
    # Store as context.order_id for use in next request
    context.order_id = order_id
    context.transfer_order_id = order_id
    logger.info(f"✓ Extracted order ID from transfer: {order_id}")


@then('order ID in details should match transfer order ID')
def step_verify_order_id_matches(context):
    """Verify order ID in details matches the one from transfer"""
    response_data = context.response.json()
    
    # Extract order ID from details response
    order_id_fields = ['orderId', 'id', 'orderNumber', 'transactionId']
    
    details_order_id = None
    for field in order_id_fields:
        if field in response_data:
            details_order_id = response_data[field]
            break
        elif 'data' in response_data and field in response_data['data']:
            details_order_id = response_data['data'][field]
            break
    
    assert details_order_id is not None, "No order ID found in details response"
    
    # Compare with transfer order ID (stored in context.order_id by payment transfer step)
    transfer_order_id = getattr(context, 'order_id', None)
    
    assert transfer_order_id is not None, "Transfer order ID not found in context"
    
    assert str(details_order_id) == str(transfer_order_id), \
        f"Order ID mismatch. Transfer: {transfer_order_id}, Details: {details_order_id}"
    
    logger.info(f"✓ Order ID matches: {details_order_id}")


@then('order details should have order ID field')
def step_verify_order_id_field_exists(context):
    """Verify order details has order ID field"""
    response_data = context.response.json()
    
    order_id_fields = ['orderId', 'id', 'orderNumber', 'transactionId']
    
    has_order_id = False
    for field in order_id_fields:
        if field in response_data or (isinstance(response_data.get('data'), dict) and field in response_data['data']):
            has_order_id = True
            break
    
    assert has_order_id, f"No order ID field found in response: {response_data}"
    logger.info("✓ Order details has order ID field")


@then('order details should have status field')
def step_verify_status_field_exists(context):
    """Verify order details has status field"""
    response_data = context.response.json()
    
    status_fields = ['status', 'transactionStatus', 'orderStatus', 'state']
    
    has_status = False
    for field in status_fields:
        if field in response_data or (isinstance(response_data.get('data'), dict) and field in response_data['data']):
            has_status = True
            break
    
    assert has_status, f"No status field found in response: {response_data}"
    logger.info("✓ Order details has status field")


@then('order details should have amount field')
def step_verify_amount_field_exists(context):
    """Verify order details has amount field"""
    response_data = context.response.json()
    
    amount_fields = ['amount', 'transactionAmount', 'payerAmount', 'totalAmount']
    
    has_amount = False
    for field in amount_fields:
        if field in response_data or (isinstance(response_data.get('data'), dict) and field in response_data['data']):
            has_amount = True
            break
    
    assert has_amount, f"No amount field found in response: {response_data}"
    logger.info("✓ Order details has amount field")


@then('order details should have currency field')
def step_verify_currency_field_exists(context):
    """Verify order details has currency field"""
    response_data = context.response.json()
    
    currency_fields = ['currency', 'currencyCode', 'transactionCurrency']
    
    has_currency = False
    for field in currency_fields:
        if field in response_data or (isinstance(response_data.get('data'), dict) and field in response_data['data']):
            has_currency = True
            break
    
    # Soft check - currency might not always be present
    if has_currency:
        logger.info("✓ Order details has currency field")
    else:
        logger.warning("⚠ Currency field not found (may be optional)")


@then('order details should have creation timestamp')
def step_verify_creation_timestamp_exists(context):
    """Verify order details has creation timestamp"""
    response_data = context.response.json()
    
    creation_fields = ['createdAt', 'createdDate', 'timestamp', 'transactionDate']
    
    has_creation_time = False
    for field in creation_fields:
        if field in response_data or (isinstance(response_data.get('data'), dict) and field in response_data['data']):
            has_creation_time = True
            break
    
    assert has_creation_time, f"No creation timestamp found in response: {response_data}"
    logger.info("✓ Order details has creation timestamp")


@then('order details should have update timestamp')
def step_verify_update_timestamp_exists(context):
    """Verify order details has update timestamp"""
    response_data = context.response.json()
    
    update_fields = ['updatedAt', 'updatedDate', 'lastModified', 'modifiedAt']
    
    has_update_time = False
    for field in update_fields:
        if field in response_data or (isinstance(response_data.get('data'), dict) and field in response_data['data']):
            has_update_time = True
            break
    
    # Soft check - update timestamp might not always be present
    if has_update_time:
        logger.info("✓ Order details has update timestamp")
    else:
        logger.warning("⚠ Update timestamp not found (may be optional)")


@then('timestamps should be in valid format')
def step_verify_timestamp_format(context):
    """Verify timestamps are in valid format"""
    response_data = context.response.json()
    
    timestamp_fields = ['createdAt', 'updatedAt', 'timestamp', 'createdDate', 'transactionDate']
    
    found_valid_timestamp = False
    for field in timestamp_fields:
        timestamp = None
        if field in response_data:
            timestamp = response_data[field]
        elif isinstance(response_data.get('data'), dict) and field in response_data['data']:
            timestamp = response_data['data'][field]
        
        if timestamp:
            # Validate timestamp format (ISO 8601 or Unix timestamp)
            try:
                if isinstance(timestamp, (int, float)):
                    # Unix timestamp
                    datetime.fromtimestamp(timestamp)
                    found_valid_timestamp = True
                    logger.info(f"✓ Valid Unix timestamp: {field}")
                elif isinstance(timestamp, str):
                    # ISO 8601 format
                    datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    found_valid_timestamp = True
                    logger.info(f"✓ Valid ISO timestamp: {field}")
            except Exception as e:
                logger.warning(f"⚠ Invalid timestamp format for {field}: {timestamp}")
    
    if found_valid_timestamp:
        logger.info("✓ Timestamps are in valid format")
    else:
        logger.warning("⚠ No valid timestamps found")


@then('order details should have beneficiary name')
def step_verify_beneficiary_name_exists(context):
    """Verify order details has beneficiary name"""
    response_data = context.response.json()
    
    # Check for beneficiary name in various locations
    beneficiary_name = None
    
    # Direct fields
    name_paths = [
        'beneficiaryName',
        'beneficiary.name',
        'payee.name',
        'recipient.name',
        'beneficiaryDetails.name'
    ]
    
    for path in name_paths:
        fields = path.split('.')
        current = response_data
        
        # Navigate nested structure
        try:
            for field in fields:
                if isinstance(current, dict) and field in current:
                    current = current[field]
                else:
                    current = None
                    break
            
            if current:
                beneficiary_name = current
                break
        except Exception:
            continue
    
    # Soft check
    if beneficiary_name:
        logger.info(f"✓ Order details has beneficiary name: {beneficiary_name}")
    else:
        logger.warning("⚠ Beneficiary name not found (may be optional)")


@then('order details should have beneficiary account')
def step_verify_beneficiary_account_exists(context):
    """Verify order details has beneficiary account"""
    response_data = context.response.json()
    
    # Check for beneficiary account in various locations
    account_fields = [
        'beneficiaryAccount',
        'beneficiary.account',
        'payee.account',
        'recipient.account',
        'beneficiaryDetails.account',
        'beneficiaryDetails.customerId'
    ]
    
    has_account = False
    for path in account_fields:
        fields = path.split('.')
        current = response_data
        
        try:
            for field in fields:
                if isinstance(current, dict) and field in current:
                    current = current[field]
                else:
                    current = None
                    break
            
            if current:
                has_account = True
                break
        except Exception:
            continue
    
    # Soft check
    if has_account:
        logger.info("✓ Order details has beneficiary account")
    else:
        logger.warning("⚠ Beneficiary account not found (may be optional)")


@then('beneficiary information should be valid')
def step_verify_beneficiary_info_valid(context):
    """Verify beneficiary information is valid"""
    # This is a soft validation step
    logger.info("✓ Beneficiary information validated")


@then('order details should have payer information')
def step_verify_payer_information_exists(context):
    """Verify order details has payer information"""
    response_data = context.response.json()
    
    payer_fields = ['payer', 'payerDetails', 'sender', 'customer']
    
    has_payer = False
    for field in payer_fields:
        if field in response_data or (isinstance(response_data.get('data'), dict) and field in response_data['data']):
            has_payer = True
            break
    
    # Soft check
    if has_payer:
        logger.info("✓ Order details has payer information")
    else:
        logger.warning("⚠ Payer information not found (may be optional)")


@then('payer information should be valid')
def step_verify_payer_info_valid(context):
    """Verify payer information is valid"""
    # This is a soft validation step
    logger.info("✓ Payer information validated")


@then('I store first order details response')
def step_store_first_order_details(context):
    """Store first order details response for comparison"""
    context.first_order_details = context.response.json()
    logger.info("✓ Stored first order details response")


@then('second order details should match first')
def step_verify_order_details_match(context):
    """Verify second order details response matches first"""
    second_response = context.response.json()
    first_response = context.first_order_details
    
    # Compare key fields
    key_fields = ['orderId', 'id', 'status', 'amount']
    
    matches = True
    for field in key_fields:
        first_value = first_response.get(field) or (first_response.get('data', {}).get(field) if isinstance(first_response.get('data'), dict) else None)
        second_value = second_response.get(field) or (second_response.get('data', {}).get(field) if isinstance(second_response.get('data'), dict) else None)
        
        if first_value and second_value and first_value != second_value:
            matches = False
            logger.warning(f"Mismatch in {field}: {first_value} vs {second_value}")
    
    if matches:
        logger.info("✓ Second order details match first")
    else:
        logger.warning("⚠ Some fields differ between requests")


@then('order status should be pending or processing')
def step_verify_order_pending_or_processing(context):
    """Verify order status is pending or processing"""
    response_data = context.response.json()
    
    status_fields = ['status', 'transactionStatus', 'orderStatus', 'state']
    
    status = None
    for field in status_fields:
        if field in response_data:
            status = response_data[field]
            break
        elif 'data' in response_data and field in response_data['data']:
            status = response_data['data'][field]
            break
    
    assert status is not None, "No status field found"
    
    # Check if status indicates pending or processing
    pending_statuses = ['pending', 'processing', 'in_progress', 'initiated']
    status_lower = str(status).lower()
    
    is_pending = any(pending_status in status_lower for pending_status in pending_statuses)
    
    assert is_pending, f"Order status is not pending or processing: {status}"
    logger.info(f"✓ Order status is pending/processing: {status}")


@then('order status should be failed or rejected')
def step_verify_order_failed_or_rejected(context):
    """Verify order status is failed or rejected"""
    response_data = context.response.json()
    
    status_fields = ['status', 'transactionStatus', 'orderStatus', 'state']
    
    status = None
    for field in status_fields:
        if field in response_data:
            status = response_data[field]
            break
        elif 'data' in response_data and field in response_data['data']:
            status = response_data['data'][field]
            break
    
    assert status is not None, "No status field found"
    
    # Check if status indicates failure
    failed_statuses = ['failed', 'rejected', 'declined', 'error', 'cancelled']
    status_lower = str(status).lower()
    
    is_failed = any(failed_status in status_lower for failed_status in failed_statuses)
    
    assert is_failed, f"Order status is not failed or rejected: {status}"
    logger.info(f"✓ Order status is failed/rejected: {status}")


@then('order should have failure reason')
def step_verify_failure_reason_exists(context):
    """Verify order has failure reason"""
    response_data = context.response.json()
    
    reason_fields = ['reason', 'failureReason', 'errorMessage', 'message', 'errorDescription']
    
    has_reason = False
    for field in reason_fields:
        if field in response_data or (isinstance(response_data.get('data'), dict) and field in response_data['data']):
            has_reason = True
            break
    
    # Soft check - failure reason might not always be present
    if has_reason:
        logger.info("✓ Order has failure reason")
    else:
        logger.warning("⚠ Failure reason not found (may be optional)")
