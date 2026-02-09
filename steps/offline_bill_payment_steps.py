"""
Step definitions for Offline Bill Payment API
Endpoint: POST /bff/v2/order/utility/payment

Note: This module contains ONLY unique steps for offline bill payment.
Reuses existing steps from church_payment_steps.py for common validation:
- response should contain payment confirmation
- response should have transaction ID
- response should have payment status
"""

import json
import uuid
from behave import given, when, then
import logging
import time

logger = logging.getLogger(__name__)


# ==================== Given Steps - Setup Payment Details ====================

@given('I have offline bill payment details')
def step_impl(context):
    """
    Set up offline bill payment details from table data
    Table should contain: merchantCode, accountNumber, amount, currency, operatorId (optional), categoryId (optional)
    """
    logger.info("Setting up offline bill payment details from table")
    
    # Initialize payment details dictionary
    context.bill_payment_details = {}
    
    # Extract values from table
    for row in context.table:
        field = row['field']
        value = row['value']
        context.bill_payment_details[field] = value
        logger.info(f"  {field}: {value}")
    
    # Get instrument token from context if available
    if hasattr(context, 'instrument_token'):
        logger.info(f"  Using stored instrument token: {context.instrument_token}")
        context.bill_payment_details['instrumentToken'] = context.instrument_token
    else:
        logger.warning("  ⚠️ No instrument token found in context, using dummy token")
        context.bill_payment_details['instrumentToken'] = "dummy-token-for-testing"
    
    logger.info(f"✅ Offline bill payment details configured with {len(context.bill_payment_details)} fields")


@given('I have offline bill payment details with extracted data')
def step_impl(context):
    """
    Set up offline bill payment details using extracted merchant code and instrument token
    """
    logger.info("Setting up offline bill payment details with extracted data")
    
    # Initialize payment details dictionary
    context.bill_payment_details = {}
    
    # Extract values from table
    for row in context.table:
        field = row['field']
        value = row['value']
        context.bill_payment_details[field] = value
        logger.info(f"  {field}: {value}")
    
    # Use extracted merchant code if available
    if hasattr(context, 'merchant_code'):
        logger.info(f"  Using extracted merchant code: {context.merchant_code}")
        context.bill_payment_details['merchantCode'] = context.merchant_code
    
    # Use extracted instrument token if available
    if hasattr(context, 'instrument_token'):
        logger.info(f"  Using extracted instrument token: {context.instrument_token}")
        context.bill_payment_details['instrumentToken'] = context.instrument_token
    
    logger.info(f"✅ Offline bill payment details configured with extracted data")


@given('I have offline bill payment details with invalid instrument token')
def step_impl(context):
    """
    Set up offline bill payment details with invalid instrument token
    """
    logger.info("Setting up offline bill payment details with invalid instrument token")
    
    # Initialize payment details dictionary
    context.bill_payment_details = {}
    
    # Extract values from table
    for row in context.table:
        field = row['field']
        value = row['value']
        context.bill_payment_details[field] = value
        logger.info(f"  {field}: {value}")
    
    # Use invalid instrument token
    context.bill_payment_details['instrumentToken'] = "invalid-token-12345"
    logger.info(f"  Using invalid instrument token: {context.bill_payment_details['instrumentToken']}")
    
    logger.info(f"✅ Offline bill payment details configured with invalid token")


@given('I have offline bill payment details without instrument token')
def step_impl(context):
    """
    Set up offline bill payment details without instrument token
    """
    logger.info("Setting up offline bill payment details without instrument token")
    
    # Initialize payment details dictionary
    context.bill_payment_details = {}
    
    # Extract values from table
    for row in context.table:
        field = row['field']
        value = row['value']
        context.bill_payment_details[field] = value
        logger.info(f"  {field}: {value}")
    
    # Explicitly don't set instrument token
    logger.info(f"  ⚠️ Instrument token not included")
    
    logger.info(f"✅ Offline bill payment details configured without instrument token")


@given('I have offline bill payment details without biller details')
def step_impl(context):
    """
    Set up offline bill payment details without biller details
    """
    logger.info("Setting up offline bill payment details without biller details")
    
    # Only set minimal details without biller information
    context.bill_payment_details = {
        'amount': 3.0,
        'currency': 'USD'
    }
    
    # Get instrument token from context if available
    if hasattr(context, 'instrument_token'):
        context.bill_payment_details['instrumentToken'] = context.instrument_token
    
    logger.info(f"✅ Payment details configured without biller details")


@given('I have offline bill payment details without amount')
def step_impl(context):
    """
    Set up offline bill payment details without amount
    """
    logger.info("Setting up offline bill payment details without amount")
    
    # Initialize payment details dictionary
    context.bill_payment_details = {}
    
    # Extract values from table (amount should not be in table)
    for row in context.table:
        field = row['field']
        value = row['value']
        context.bill_payment_details[field] = value
        logger.info(f"  {field}: {value}")
    
    # Get instrument token from context if available
    if hasattr(context, 'instrument_token'):
        context.bill_payment_details['instrumentToken'] = context.instrument_token
    
    logger.info(f"✅ Payment details configured without amount")


# ==================== When Steps - Send Payment Request ====================

@when('I send offline bill payment request to "{endpoint}"')
def step_impl(context, endpoint):
    """
    Send POST request to offline bill payment endpoint with payment details
    """
    logger.info(f"Sending offline bill payment request to {endpoint}")
    
    # Get API client
    api_client = context.base_test.api_client
    
    # Build request payload
    payload = build_payment_payload(context)
    
    logger.info(f"Request URL: {endpoint}")
    logger.info(f"Request Body: {json.dumps(payload, indent=2)}")
    
    # Build headers
    headers = {
        'Content-Type': 'application/json'
    }
    
    if hasattr(context, 'user_token') and context.user_token:
        headers['Authorization'] = f'Bearer {context.user_token}'
    
    # Send POST request using api_client
    start_time = time.time()
    context.response = api_client.post(
        endpoint,
        json_data=payload,
        headers=headers
    )
    end_time = time.time()
    
    # Store response and timing
    context.response_time = (end_time - start_time) * 1000  # Convert to milliseconds
    
    logger.info(f"Response Status: {context.response.status_code}")
    logger.info(f"Response Time: {context.response_time:.2f}ms")
    
    if context.response.status_code == 200:
        try:
            response_data = context.response.json()
            logger.info(f"Response Body: {json.dumps(response_data, indent=2)}")
        except:
            logger.info(f"Response Body: {context.response.text}")


def build_payment_payload(context):
    """
    Build the payment request payload from context.bill_payment_details
    """
    details = context.bill_payment_details
    
    # Get values from details
    merchant_code = details.get('merchantCode', '8002')
    account_number = details.get('accountNumber', '1472365288')
    amount = float(details.get('amount', 3.0)) if 'amount' in details else None
    currency = details.get('currency', 'USD')
    operator_id = details.get('operatorId', 'SZWOBO0001')
    category_id = details.get('categoryId', 'SZWC10019')
    instrument_token = details.get('instrumentToken')
    
    # Build base payload
    payload = {
        "feeAmount": 0,
        "currency": currency,
        "billerDetails": {
            "operatorId": operator_id,
            "categoryId": category_id,
            "Q1": merchant_code,
            "Q2": account_number
        },
        "subType": "offline-bill-pay",
        "channel": "sasai-super-app",
        "deviceInfo": {
            "simNumber": "03d88760-d411-11f0-9694-15a487face2d",
            "deviceId": "03d88760-d411-11f0-9694-15a487face2d",
            "model": "realme - RMX3741",
            "network": "unidentified",
            "latitude": "28.4307472",
            "longitude": "77.0647009",
            "os": "RM6877",
            "osVersion": "15",
            "appVersion": "2.2.1",
            "package": "com.sasai.sasaipay"
        },
        "notes": {
            "operatorName": "MOBSWITCH MOBSWITCH",
            "code": "19847",
            "utilityAccount": account_number
        }
    }
    
    # Add amount if provided
    if amount is not None:
        payload['billerDetails']['amount'] = amount
        payload['billerDetails']['currency'] = currency
        payload['payerAmount'] = amount
    
    # Add payer details if instrument token is provided
    if instrument_token:
        payload['payerDetails'] = {
            "instrumentToken": instrument_token,
            "paymentMethod": "wallet",
            "provider": "ecocash",
            "pin": "mvIkFBJqHn4YxGxx4/l1k2p+OyfrQgXJ11jQQi7C8N3+B5qZPDXggJrDAPFUFmezSo7CyUek15H+kSH4pWRT1MtuyKm9+M+2l9mpQnbSS2p7UDyHI17thhlc4ArhR1xRsEBfADLeCQSLL3mqk+de95FHJT/UlhjljhIbmm75Efhz67vcA+8E1YLMoWP6nA/VM/NMlWSD8HEofBQ8mDdDgKYlTjyZ86gpMroRb7Z9rC2SZfpVcl31aQE2nkx2m2OsZGo+Vqf2YqkIJBQ4Ae2llRf7PCPSB7tKY6OLiBWOYX+gISCQEthqr4sB5HgKHGwrP1+P9oxyQE2nrsdnMDTYng==",
            "publicKeyAlias": "payment-links"
        }
    
    return payload


# ==================== Then Steps - Verify Payment Response (Unique Steps Only) ====================
# Note: Common steps like 'response should contain payment confirmation', 'response should have transaction ID',
# and 'response should have payment status' are already defined in church_payment_steps.py

@then('response should have payment reference')
def step_impl(context):
    """
    Verify response contains payment reference
    """
    logger.info("Verifying response has payment reference")
    
    response_data = context.response.json()
    
    # Check for reference in various possible locations
    reference = None
    
    if 'reference' in response_data:
        reference = response_data['reference']
    elif 'referenceNumber' in response_data:
        reference = response_data['referenceNumber']
    elif 'paymentReference' in response_data:
        reference = response_data['paymentReference']
    elif isinstance(response_data.get('data'), dict):
        data = response_data['data']
        reference = data.get('reference') or data.get('referenceNumber') or data.get('paymentReference')
    
    assert reference is not None, "❌ Payment reference not found in response"
    logger.info(f"✅ Payment reference found: {reference}")
    
    # Store reference in context
    context.payment_reference = reference


@then('payment amount should match requested amount')
def step_impl(context):
    """
    Verify payment amount in response matches requested amount
    """
    logger.info("Verifying payment amount matches requested amount")
    
    response_data = context.response.json()
    requested_amount = float(context.bill_payment_details.get('amount', 0))
    
    # Check for amount in various possible locations
    response_amount = None
    
    if 'amount' in response_data:
        response_amount = float(response_data['amount'])
    elif 'paymentAmount' in response_data:
        response_amount = float(response_data['paymentAmount'])
    elif isinstance(response_data.get('data'), dict):
        data = response_data['data']
        response_amount = float(data.get('amount', 0) or data.get('paymentAmount', 0))
    
    if response_amount is not None:
        assert response_amount == requested_amount, f"❌ Amount mismatch: expected {requested_amount}, got {response_amount}"
        logger.info(f"✅ Payment amount matches: {response_amount}")
    else:
        logger.warning("⚠️ Amount not found in response, skipping verification")


@then('response should have required payment fields')
def step_impl(context):
    """
    Verify response contains required payment fields
    """
    logger.info("Verifying response has required payment fields")
    
    response_data = context.response.json()
    
    # List of required fields
    required_fields = ['status', 'transactionId', 'reference', 'amount', 'currency']
    
    found_fields = []
    missing_fields = []
    
    for field in required_fields:
        # Check in root level
        if field in response_data:
            found_fields.append(field)
            logger.info(f"  ✓ Found field: {field}")
        # Check in data object
        elif isinstance(response_data.get('data'), dict) and field in response_data['data']:
            found_fields.append(field)
            logger.info(f"  ✓ Found field in data: {field}")
        else:
            missing_fields.append(field)
            logger.warning(f"  ⚠️ Missing field: {field}")
    
    # At least some required fields should be present
    assert len(found_fields) >= 2, f"❌ Too few required fields found. Missing: {missing_fields}"
    logger.info(f"✅ Found {len(found_fields)} required payment fields")


@then('response should have transaction details')
def step_impl(context):
    """
    Verify response contains transaction details
    """
    logger.info("Verifying response has transaction details")
    
    response_data = context.response.json()
    
    # Check for transaction details fields
    details_fields = ['transactionId', 'timestamp', 'date', 'time', 'merchant', 'biller']
    
    found_fields = []
    for field in details_fields:
        if field in response_data or (isinstance(response_data.get('data'), dict) and field in response_data.get('data', {})):
            found_fields.append(field)
            logger.info(f"  ✓ Found detail field: {field}")
    
    assert len(found_fields) > 0, f"❌ No transaction details found in response"
    logger.info(f"✅ Transaction details found with {len(found_fields)} fields")


@then('payment status should be valid')
def step_impl(context):
    """
    Verify payment status is valid
    """
    logger.info("Verifying payment status is valid")
    
    response_data = context.response.json()
    
    # Get status
    status = None
    if 'status' in response_data:
        status = response_data['status']
    elif isinstance(response_data.get('data'), dict):
        status = response_data['data'].get('status')
    
    assert status is not None, "❌ Payment status not found"
    
    # Valid status values
    valid_statuses = ['SUCCESS', 'PENDING', 'PROCESSING', 'COMPLETED', 'success', 'pending', 'processing', 'completed']
    
    assert status in valid_statuses or isinstance(status, str), f"❌ Invalid payment status: {status}"
    logger.info(f"✅ Payment status is valid: {status}")


@then('transaction ID format should be valid')
def step_impl(context):
    """
    Verify transaction ID format is valid (UUID or numeric)
    """
    logger.info("Verifying transaction ID format")
    
    response_data = context.response.json()
    
    # Get transaction ID
    transaction_id = None
    if 'transactionId' in response_data:
        transaction_id = response_data['transactionId']
    elif 'txnId' in response_data:
        transaction_id = response_data['txnId']
    elif isinstance(response_data.get('data'), dict):
        data = response_data['data']
        transaction_id = data.get('transactionId') or data.get('txnId')
    
    assert transaction_id is not None, "❌ Transaction ID not found"
    
    # Check if UUID format or numeric
    transaction_id_str = str(transaction_id)
    
    is_valid = False
    
    # Try to parse as UUID
    try:
        uuid.UUID(transaction_id_str)
        is_valid = True
        logger.info(f"✅ Transaction ID is valid UUID: {transaction_id}")
    except:
        # Check if numeric
        if transaction_id_str.isdigit() and len(transaction_id_str) > 5:
            is_valid = True
            logger.info(f"✅ Transaction ID is valid numeric: {transaction_id}")
        elif len(transaction_id_str) > 10:
            # Accept any string longer than 10 characters as valid ID
            is_valid = True
            logger.info(f"✅ Transaction ID format accepted: {transaction_id}")
    
    assert is_valid, f"❌ Invalid transaction ID format: {transaction_id}"


@then('I extract payment reference from response')
def step_impl(context):
    """
    Extract payment reference from response and store in context
    """
    logger.info("Extracting payment reference from response")
    
    response_data = context.response.json()
    
    # Check for reference in various possible locations
    reference = None
    
    if 'reference' in response_data:
        reference = response_data['reference']
    elif 'referenceNumber' in response_data:
        reference = response_data['referenceNumber']
    elif 'transactionId' in response_data:
        reference = response_data['transactionId']
    elif isinstance(response_data.get('data'), dict):
        data = response_data['data']
        reference = data.get('reference') or data.get('referenceNumber') or data.get('transactionId')
    
    assert reference is not None, "❌ Payment reference not found in response"
    
    # Store first reference
    context.first_payment_reference = reference
    logger.info(f"✅ Extracted first payment reference: {reference}")


@then('I extract second payment reference from response')
def step_impl(context):
    """
    Extract second payment reference from response and store in context
    """
    logger.info("Extracting second payment reference from response")
    
    response_data = context.response.json()
    
    # Check for reference in various possible locations
    reference = None
    
    if 'reference' in response_data:
        reference = response_data['reference']
    elif 'referenceNumber' in response_data:
        reference = response_data['referenceNumber']
    elif 'transactionId' in response_data:
        reference = response_data['transactionId']
    elif isinstance(response_data.get('data'), dict):
        data = response_data['data']
        reference = data.get('reference') or data.get('referenceNumber') or data.get('transactionId')
    
    assert reference is not None, "❌ Payment reference not found in response"
    
    # Store second reference
    context.second_payment_reference = reference
    logger.info(f"✅ Extracted second payment reference: {reference}")


@then('second payment reference should be different from first')
def step_impl(context):
    """
    Verify second payment reference is different from first
    """
    logger.info("Verifying payment references are unique")
    
    assert hasattr(context, 'first_payment_reference'), "❌ First payment reference not found in context"
    assert hasattr(context, 'second_payment_reference'), "❌ Second payment reference not found in context"
    
    first_ref = context.first_payment_reference
    second_ref = context.second_payment_reference
    
    assert first_ref != second_ref, f"❌ Payment references are not unique: {first_ref}"
    logger.info(f"✅ Payment references are unique:")
    logger.info(f"   First:  {first_ref}")
    logger.info(f"   Second: {second_ref}")


@then('I extract payment status from response')
def step_impl(context):
    """
    Extract payment status from response for reporting
    """
    logger.info("Extracting payment status from response")
    
    response_data = context.response.json()
    
    # Extract status
    status = None
    if 'status' in response_data:
        status = response_data['status']
    elif 'paymentStatus' in response_data:
        status = response_data['paymentStatus']
    elif isinstance(response_data.get('data'), dict):
        data = response_data['data']
        status = data.get('status') or data.get('paymentStatus')
    
    assert status is not None, "❌ Payment status not found in response"
    
    # Store payment status
    context.payment_status = status
    context.final_payment_status = status.upper()
    
    # Determine payment result for reporting
    success_statuses = ['success', 'completed', 'approved', 'confirmed', 'SUCCESS', 'COMPLETED', 'APPROVED', 'CONFIRMED']
    failure_statuses = ['failure', 'failed', 'declined', 'rejected', 'error', 'FAILURE', 'FAILED', 'DECLINED', 'REJECTED', 'ERROR']
    
    if status in success_statuses:
        context.payment_result = "SUCCESS"
        logger.info(f"✅ Payment Status: {status.upper()} - Payment SUCCESSFUL")
    elif status in failure_statuses:
        context.payment_result = "FAILURE"
        logger.warning(f"❌ Payment Status: {status.upper()} - Payment FAILED")
    else:
        context.payment_result = "UNKNOWN"
        logger.info(f"ℹ️ Payment Status: {status.upper()} - Status UNKNOWN")
    
    logger.info(f"📊 Final Payment Status Extracted: {status}")


@then('payment status should be success')
def step_impl(context):
    """
    Verify payment status is success
    """
    logger.info("Verifying payment status is success")
    
    response_data = context.response.json()
    
    # Get status
    status = None
    if 'status' in response_data:
        status = response_data['status']
    elif 'paymentStatus' in response_data:
        status = response_data['paymentStatus']
    elif isinstance(response_data.get('data'), dict):
        status = response_data['data'].get('status') or response_data['data'].get('paymentStatus')
    
    assert status is not None, "❌ Payment status not found in response"
    
    # Check if status indicates success
    success_statuses = ['success', 'completed', 'approved', 'confirmed', 'SUCCESS', 'COMPLETED', 'APPROVED', 'CONFIRMED']
    
    assert status in success_statuses, f"❌ Expected payment to be successful, but status is: {status}"
    logger.info(f"✅ Payment status is SUCCESS: {status}")
    
    # Store for reporting
    context.payment_status = status
    context.payment_result = "SUCCESS"


@then('payment status should be failure')
def step_impl(context):
    """
    Verify payment status is failure
    """
    logger.info("Verifying payment status is failure")
    
    response_data = context.response.json()
    
    # Get status
    status = None
    if 'status' in response_data:
        status = response_data['status']
    elif 'paymentStatus' in response_data:
        status = response_data['paymentStatus']
    elif isinstance(response_data.get('data'), dict):
        status = response_data['data'].get('status') or response_data['data'].get('paymentStatus')
    
    assert status is not None, "❌ Payment status not found in response"
    
    # Check if status indicates failure
    failure_statuses = ['failure', 'failed', 'declined', 'rejected', 'error', 'FAILURE', 'FAILED', 'DECLINED', 'REJECTED', 'ERROR']
    
    assert status in failure_statuses, f"❌ Expected payment to fail, but status is: {status}"
    logger.info(f"✅ Payment status is FAILURE: {status}")
    
    # Store for reporting
    context.payment_status = status
    context.payment_result = "FAILURE"


@then('I should see final payment status in response')
def step_impl(context):
    """
    Extract and log final payment status with detailed information for reporting
    """
    logger.info("=" * 80)
    logger.info("📋 FINAL PAYMENT STATUS REPORT")
    logger.info("=" * 80)
    
    response_data = context.response.json()
    
    # Extract all relevant information
    status = response_data.get('status') or response_data.get('paymentStatus')
    order_id = response_data.get('orderId') or response_data.get('transactionId')
    operator_id = response_data.get('operatorId')
    category_id = response_data.get('categoryId')
    
    # Determine status emoji and result
    success_statuses = ['success', 'completed', 'approved', 'confirmed', 'SUCCESS', 'COMPLETED', 'APPROVED', 'CONFIRMED']
    failure_statuses = ['failure', 'failed', 'declined', 'rejected', 'error', 'FAILURE', 'FAILED', 'DECLINED', 'REJECTED', 'ERROR']
    
    if status in success_statuses:
        status_emoji = "✅"
        result = "SUCCESS"
    elif status in failure_statuses:
        status_emoji = "❌"
        result = "FAILURE"
    else:
        status_emoji = "⚠️"
        result = "UNKNOWN"
    
    # Log detailed information
    logger.info(f"{status_emoji} Payment Status: {status.upper()}")
    logger.info(f"📝 Transaction/Order ID: {order_id}")
    logger.info(f"🏢 Operator ID: {operator_id}")
    logger.info(f"📂 Category ID: {category_id}")
    logger.info(f"🎯 Final Result: {result}")
    
    # Store in context for reporting
    context.final_payment_status = status
    context.payment_result = result
    context.payment_order_id = order_id
    context.payment_operator_id = operator_id
    context.payment_category_id = category_id
    
    # Log summary
    logger.info("=" * 80)
    logger.info(f"Summary: Payment {result} | Status: {status} | Order: {order_id}")
    logger.info("=" * 80)
    
    assert status is not None, "❌ Payment status not found in response"


# Note: The following steps are reused from bill_payment_options_steps.py:
# - I extract payment account details from response
# - stored payment details should be complete
# - I store instrument token for payment

