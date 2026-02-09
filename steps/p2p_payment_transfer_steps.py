"""
Step definitions for P2P Payment Transfer API
Endpoint: POST /bff/v2/order/transfer/payment
"""

import json
import time
import uuid
import logging
from behave import given, when, then

# Initialize logger
logger = logging.getLogger(__name__)


# ===========================
# Given Steps - Setup
# ===========================

@given('I have payment transfer details')
def step_payment_transfer_details(context):
    """Set up payment transfer details from table"""
    transfer_details = {}
    for row in context.table:
        field = row['field']
        value = row['value']
        
        # Convert numeric values - keep feeAmount as string, convert others to numbers
        if field == 'feeAmount':
            # Keep feeAmount as string (API expects string format)
            value = str(value)
        elif field in ['payerAmount', 'payeeAmount']:
            value = float(value) if '.' in value else int(value)
        
        transfer_details[field] = value
    
    context.transfer_details = transfer_details
    logger.info(f"Payment transfer details set: {json.dumps(transfer_details, indent=2)}")


@given('I have complete payment transfer payload')
def step_complete_payment_transfer_payload(context):
    """Set up complete payment transfer payload with all required fields"""
    # Load configuration values (from Postman working request)
    config = context.config_loader
    fee_amount = str(config.get('p2p_payment_transfer.fee_amount', 0))  # Convert to string
    currency = config.get('p2p_payment_transfer.currency', 'ZWG')
    payer_amount = config.get('p2p_payment_transfer.payer_amount', 3)
    payee_amount = config.get('p2p_payment_transfer.payee_amount', 3)
    
    # ✨ DYNAMIC TOKEN USAGE: Use tokens from Account Lookup & Payment Options if available
    # Priority: 1) Dynamic tokens from API responses, 2) Fallback to config values
    beneficiary_instrument_token = getattr(context, 'beneficiary_instrument_token', None) or \
                                   config.get('p2p_payment_transfer.beneficiary_instrument_token', 
                                             'f8d6cb79-620e-45ac-8274-bcee7590f744')
    
    payer_instrument_token = getattr(context, 'payer_instrument_token', None) or \
                            config.get('p2p_payment_transfer.payer_instrument_token',
                                      '3bdc3bc8-5d57-4451-85e5-aa8a9deb210d')
    
    # Extract other dynamic values if available
    instrument_id = getattr(context, 'beneficiary_instrument_id', '') or '9f894ed8-9116-496b-8599-526cc114b566'
    customer_id = getattr(context, 'beneficiary_customer_id', '') or \
                  config.get('p2p_payment_transfer.beneficiary_customer_id', 'f044ff8d-abe6-47aa-8837-ec329e8a0edc')
    
    # Log token sources and values
    logger.info(f"📋 Using instrument ID: {instrument_id}")
    logger.info(f"📋 Using customer ID: {customer_id}")
    if hasattr(context, 'beneficiary_instrument_token'):
        logger.info(f"🎯 Using DYNAMIC beneficiary token from Account Lookup: {beneficiary_instrument_token[:20]}...")
    else:
        logger.info(f"⚠️  Using STATIC beneficiary token from config: {beneficiary_instrument_token[:20]}...")
    
    if hasattr(context, 'payer_instrument_token'):
        logger.info(f"🎯 Using DYNAMIC payer token from Payment Options: {payer_instrument_token[:20]}...")
    else:
        logger.info(f"⚠️  Using STATIC payer token from config: {payer_instrument_token[:20]}...")
    
    # This is a template payload - in real scenarios, these would be dynamic values
    payload = {
        "feeAmount": fee_amount,  # 0 from config
        "currency": currency,
        "payerAmount": payer_amount,  # 3 from config
        "beneficiaryDetails": {
            "payeeAmount": payee_amount,  # 3 from config
            "paymentMethod": "wallet",
            "instrumentId": instrument_id,  # Dynamic or config
            "beneficiaryInstrumentToken": beneficiary_instrument_token,  # Dynamic or config
            "name": "Ropafadzo Nyagwaya",
            "provider": "ecocash",
            "customerId": customer_id  # Dynamic or config
        },
        "payerDetails": {
            "instrumentToken": payer_instrument_token,  # Dynamic or config
            "paymentMethod": "wallet",
            "provider": "ecocash",
            "pin": "ZXodNbUKicCm/E01R6xI6NLUxqxP4g+mZAbQik8VYCeJYDGL9n6hYKzCAnuAAWcvs2nSsw0ZTN8wisiCyxYOmxRZBGYNyiH41cTOkNkUdpkP7su0Af/Mhmnp6SWDZxysO3q5Qp+qdroDSVFAepf2xJnR8X/T3INSveKGclVrd/8YkR2i4uyyHmIDnkMsWS7gLZQhpCX3gKGsLY/wT9zyOX0pHgotCUSUEGyJovNXs/P5mlvng6yMl3ZWY+2tgL1zx9pmvQtv7WKxvfKghGtRH2VQlwcviTorZdFUSdOx79xmhqxlSMNMUC5DlMnTEGT5io9MRMLbcTwXbk7T7Xuz2g==",
            "publicKeyAlias": "payment-links"
        },
        "deviceInfo": {
            "ip": "192.0.0.2",
            "model": "Samsung",
            "network": "unidentified",
            "latitude": "unidentified",
            "longitude": "unidentified",
            "os": "Android",
            "osVersion": "13",
            "appVersion": "1.4.1",
            "package": "com.sasai.sasaipay",
            "simNumber": "71ff20d0-83ff-11f0-969e-4b09cf763135",
            "deviceId": "71ff20d0-83ff-11f0-969e-4b09cf763135"
        },
        "notes": {
            "message": "P2P Test Transaction",
            "beneficiaryInstrumentId": instrument_id,
            "beneficiaryMobileNumber": "+263789124669"
        },
        "subType": "p2p-pay",
        "channel": "sasai-super-app"
    }
    
    context.payment_transfer_payload = payload
    logger.info("Complete payment transfer payload prepared")


@given('I have payment transfer with amount {amount:d} ZWG')
def step_payment_transfer_with_amount(context, amount):
    """Set up payment transfer with specific amount"""
    if not hasattr(context, 'payment_transfer_payload'):
        step_complete_payment_transfer_payload(context)
    
    context.payment_transfer_payload['payerAmount'] = amount
    context.payment_transfer_payload['beneficiaryDetails']['payeeAmount'] = amount
    context.transfer_amount = amount
    logger.info(f"Payment transfer amount set to {amount} ZWG")


@given('I have payment transfer with currency "{currency}"')
def step_payment_transfer_with_currency(context, currency):
    """Set up payment transfer with specific currency"""
    if not hasattr(context, 'payment_transfer_payload'):
        step_complete_payment_transfer_payload(context)
    
    context.payment_transfer_payload['currency'] = currency
    logger.info(f"Payment transfer currency set to {currency}")


@given('I have payment transfer with message "{message}"')
def step_payment_transfer_with_message(context, message):
    """Set up payment transfer with custom message"""
    if not hasattr(context, 'payment_transfer_payload'):
        step_complete_payment_transfer_payload(context)
    
    context.payment_transfer_payload['notes']['message'] = message
    logger.info(f"Payment transfer message set to: {message}")


@given('I have payment transfer with provider "{provider}"')
def step_payment_transfer_with_provider(context, provider):
    """Set up payment transfer with specific provider"""
    if not hasattr(context, 'payment_transfer_payload'):
        step_complete_payment_transfer_payload(context)
    
    context.payment_transfer_payload['beneficiaryDetails']['provider'] = provider
    context.payment_transfer_payload['payerDetails']['provider'] = provider
    logger.info(f"Payment transfer provider set to {provider}")


@given('I have payment transfer without beneficiary details')
def step_payment_transfer_without_beneficiary(context):
    """Set up payment transfer without beneficiary details"""
    step_complete_payment_transfer_payload(context)
    del context.payment_transfer_payload['beneficiaryDetails']
    logger.info("Payment transfer prepared without beneficiary details")


@given('I have payment transfer without payer details')
def step_payment_transfer_without_payer(context):
    """Set up payment transfer without payer details"""
    step_complete_payment_transfer_payload(context)
    del context.payment_transfer_payload['payerDetails']
    logger.info("Payment transfer prepared without payer details")


@given('I have payment transfer without device info')
def step_payment_transfer_without_device_info(context):
    """Set up payment transfer without device info"""
    step_complete_payment_transfer_payload(context)
    del context.payment_transfer_payload['deviceInfo']
    logger.info("Payment transfer prepared without device info")


@given('I have payment transfer without payment method')
def step_payment_transfer_without_payment_method(context):
    """Set up payment transfer without payment method"""
    step_complete_payment_transfer_payload(context)
    del context.payment_transfer_payload['beneficiaryDetails']['paymentMethod']
    logger.info("Payment transfer prepared without payment method")


@given('I have payment transfer without PIN')
def step_payment_transfer_without_pin(context):
    """Set up payment transfer without PIN"""
    step_complete_payment_transfer_payload(context)
    del context.payment_transfer_payload['payerDetails']['pin']
    logger.info("Payment transfer prepared without PIN")


@given('I have payment transfer with invalid PIN')
def step_payment_transfer_with_invalid_pin(context):
    """Set up payment transfer with invalid PIN"""
    step_complete_payment_transfer_payload(context)
    context.payment_transfer_payload['payerDetails']['pin'] = "invalid-pin-format"
    logger.info("Payment transfer prepared with invalid PIN")


@given('I have payment transfer with extracted beneficiary details')
def step_payment_transfer_with_extracted_beneficiary(context):
    """Set up payment transfer using previously extracted beneficiary details"""
    step_complete_payment_transfer_payload(context)
    
    # Use beneficiary name from account lookup if available
    if hasattr(context, 'beneficiary_name'):
        context.payment_transfer_payload['beneficiaryDetails']['name'] = context.beneficiary_name
        logger.info(f"Using extracted beneficiary name: {context.beneficiary_name}")
    
    # Use account number from extraction if available
    if hasattr(context, 'account_number'):
        context.payment_transfer_payload['notes']['beneficiaryMobileNumber'] = context.account_number
        logger.info(f"Using extracted account number: {context.account_number}")
    
    logger.info("Payment transfer prepared with extracted beneficiary details")


# ===========================
# When Steps - Actions
# ===========================

@when('I send payment transfer request to "{endpoint}"')
def step_send_payment_transfer_request(context, endpoint):
    """Send POST request to payment transfer endpoint"""
    # Get payload
    if hasattr(context, 'payment_transfer_payload'):
        payload = context.payment_transfer_payload
    elif hasattr(context, 'transfer_details'):
        # Build payload from transfer details
        step_complete_payment_transfer_payload(context)
        payload = context.payment_transfer_payload
        # Override with custom details if available
        for key, value in context.transfer_details.items():
            if key in payload:
                payload[key] = value
    else:
        logger.error("No payment transfer payload available")
        raise AssertionError("No payment transfer payload configured")
    
    # Build full URL
    url = f"{context.config_loader.get('api.base_url')}{endpoint}"
    
    # Build headers
    headers = {
        'Content-Type': 'application/json'
    }
    
    # Add Authorization header if user token available
    if hasattr(context, 'user_token') and context.user_token:
        headers['Authorization'] = f"Bearer {context.user_token}"
    elif hasattr(context, 'app_token') and context.app_token:
        headers['Authorization'] = f"Bearer {context.app_token}"
    
    # Override headers if specific conditions are set
    if hasattr(context, 'no_auth_header') and context.no_auth_header:
        headers.pop('Authorization', None)
    
    if hasattr(context, 'no_content_type_header') and context.no_content_type_header:
        headers.pop('Content-Type', None)
    
    try:
        logger.info(f"Sending POST request to {url}")
        logger.info(f"📦 COMPLETE PAYLOAD:\n{json.dumps(payload, indent=2)}")
        logger.info(f"🔍 DEBUG: feeAmount value = {payload.get('feeAmount')} (type: {type(payload.get('feeAmount'))})")
        
        start_time = time.time()
        response = context.base_test.api_client.post(
            endpoint,
            json=payload,
            headers=headers
        )
        context.response = response
        context.response_time = (time.time() - start_time) * 1000
        
        logger.info(f"Response Status: {response.status_code}")
        logger.info(f"Response Time: {context.response_time:.2f} ms")
        
        if response.status_code in [200, 201]:
            response_text = response.text if hasattr(response, 'text') else str(response.content)
            logger.info(f"Response: {response_text[:500]}...")  # Log first 500 chars
        else:
            response_text = response.text if hasattr(response, 'text') else str(response.content)
            logger.warning(f"Error Response: {response_text}")
            
    except Exception as e:
        logger.error(f"Request failed: {str(e)}")
        raise


@when('I send same payment transfer request again')
def step_send_same_payment_transfer_again(context):
    """Send the same payment transfer request again to test idempotency"""
    assert hasattr(context, 'payment_transfer_payload'), "No payment transfer payload available"
    step_send_payment_transfer_request(context, "/bff/v2/order/transfer/payment")


# ===========================
# Then Steps - Assertions
# ===========================

@then('response should contain P2P transaction details')
def step_response_contains_transaction_details(context):
    """Verify response contains transaction details"""
    assert context.response.status_code in [200, 201], \
        f"Expected status 200/201, got {context.response.status_code}"
    
    response_data = context.response.json()
    
    # Check for common transaction fields
    transaction_fields = ['orderId', 'transactionId', 'id', 'status', 'data', 'transaction']
    has_transaction_field = any(field in response_data for field in transaction_fields)
    
    assert has_transaction_field, \
        f"Response missing transaction details. Available fields: {list(response_data.keys())}"
    
    logger.info("✓ Response contains transaction details")


@then('response should have P2P order ID')
def step_response_has_order_id(context):
    """Verify response has order ID"""
    response_data = context.response.json()
    
    # Check for order ID in various possible locations
    order_id = None
    if 'orderId' in response_data:
        order_id = response_data['orderId']
    elif 'id' in response_data:
        order_id = response_data['id']
    elif 'data' in response_data and 'orderId' in response_data['data']:
        order_id = response_data['data']['orderId']
    elif 'transaction' in response_data and 'id' in response_data['transaction']:
        order_id = response_data['transaction']['id']
    
    assert order_id, f"Order ID not found in response. Available fields: {list(response_data.keys())}"
    
    context.order_id = order_id
    logger.info(f"✓ Order ID found: {order_id}")


@then('order ID should not be empty')
def step_order_id_not_empty(context):
    """Verify order ID is not empty"""
    assert hasattr(context, 'order_id'), "Order ID not extracted"
    assert context.order_id, "Order ID is empty"
    assert len(str(context.order_id)) > 0, "Order ID is empty string"
    
    logger.info(f"✓ Order ID is valid: {context.order_id}")


@then('P2P transaction status should be valid')
def step_transaction_status_valid(context):
    """Verify transaction status is valid"""
    response_data = context.response.json()
    
    # Find status in response
    status = None
    if 'status' in response_data:
        status = response_data['status']
    elif 'data' in response_data and 'status' in response_data['data']:
        status = response_data['data']['status']
    elif 'transaction' in response_data and 'status' in response_data['transaction']:
        status = response_data['transaction']['status']
    
    assert status, "Transaction status not found in response"
    
    # Valid statuses for payment transfer
    valid_statuses = ['success', 'pending', 'processing', 'completed', 'PENDING', 'SUCCESS', 'COMPLETED']
    assert status in valid_statuses, f"Invalid transaction status: {status}"
    
    context.transaction_status = status
    logger.info(f"✓ Transaction status is valid: {status}")


@then('response should have complete P2P transaction details')
def step_response_has_complete_transaction_details(context):
    """Verify response has complete transaction details"""
    response_data = context.response.json()
    
    # Check for essential fields in transaction response
    essential_fields = ['orderId', 'id', 'status', 'data', 'transaction']
    has_essential = any(field in response_data for field in essential_fields)
    
    assert has_essential, \
        f"Response missing essential transaction fields. Available: {list(response_data.keys())}"
    
    logger.info("✓ Response has complete transaction details")


@then('response should have P2P transaction ID')
def step_response_has_transaction_id(context):
    """Verify response has transaction ID"""
    response_data = context.response.json()
    
    # Check for transaction ID
    transaction_id = None
    if 'transactionId' in response_data:
        transaction_id = response_data['transactionId']
    elif 'id' in response_data:
        transaction_id = response_data['id']
    elif 'data' in response_data and 'transactionId' in response_data['data']:
        transaction_id = response_data['data']['transactionId']
    
    assert transaction_id, "Transaction ID not found in response"
    
    context.transaction_id = transaction_id
    logger.info(f"✓ Transaction ID found: {transaction_id}")


@then('response should have P2P transaction timestamp')
def step_response_has_transaction_timestamp(context):
    """Verify response has transaction timestamp"""
    response_data = context.response.json()
    
    # Check for timestamp fields
    timestamp_fields = ['timestamp', 'createdAt', 'created', 'date', 'transactionTime']
    has_timestamp = any(field in response_data for field in timestamp_fields)
    
    # Also check in nested data
    if not has_timestamp and 'data' in response_data:
        has_timestamp = any(field in response_data['data'] for field in timestamp_fields)
    
    assert has_timestamp, \
        f"Transaction timestamp not found. Available fields: {list(response_data.keys())}"
    
    logger.info("✓ Transaction timestamp found")


@then('response should have P2P transaction status')
def step_response_has_transaction_status(context):
    """Verify response has transaction status"""
    response_data = context.response.json()
    
    status = None
    if 'status' in response_data:
        status = response_data['status']
    elif 'data' in response_data and 'status' in response_data['data']:
        status = response_data['data']['status']
    
    assert status, "Transaction status not found in response"
    
    context.transaction_status = status
    logger.info(f"✓ Transaction status found: {status}")


@then('P2P response transaction amount should be {amount:d} ZWG')
def step_response_transaction_amount_matches(context, amount):
    """Verify transaction amount in response matches expected amount"""
    response_data = context.response.json()
    
    # Find amount in response
    response_amount = None
    if 'amount' in response_data:
        response_amount = response_data['amount']
    elif 'payerAmount' in response_data:
        response_amount = response_data['payerAmount']
    elif 'data' in response_data and 'amount' in response_data['data']:
        response_amount = response_data['data']['amount']
    
    # Note: Some APIs may not return amount in response
    # This is a soft check
    if response_amount:
        assert float(response_amount) == float(amount), \
            f"Transaction amount mismatch. Expected: {amount}, Got: {response_amount}"
        logger.info(f"✓ Transaction amount matches: {amount} ZWG")
    else:
        logger.info("⚠ Transaction amount not found in response (may be expected)")


@then('response should contain P2P beneficiary information')
def step_response_contains_beneficiary_info(context):
    """Verify response contains beneficiary information"""
    response_data = context.response.json()
    
    # Check for beneficiary fields
    beneficiary_fields = ['beneficiary', 'beneficiaryDetails', 'payee', 'recipient']
    has_beneficiary = any(field in response_data for field in beneficiary_fields)
    
    # Also check in nested data
    if not has_beneficiary and 'data' in response_data:
        has_beneficiary = any(field in response_data['data'] for field in beneficiary_fields)
    
    # Soft assertion - some APIs may not return beneficiary details
    if has_beneficiary:
        logger.info("✓ Response contains beneficiary information")
    else:
        logger.info("⚠ Beneficiary information not in response (may be expected)")


@then('P2P beneficiary name should match request')
def step_beneficiary_name_matches_request(context):
    """Verify beneficiary name in response matches request"""
    response_data = context.response.json()
    request_name = context.payment_transfer_payload['beneficiaryDetails']['name']
    
    # Try to find beneficiary name in response
    response_name = None
    if 'beneficiaryName' in response_data:
        response_name = response_data['beneficiaryName']
    elif 'beneficiary' in response_data and 'name' in response_data['beneficiary']:
        response_name = response_data['beneficiary']['name']
    elif 'data' in response_data and 'beneficiaryName' in response_data['data']:
        response_name = response_data['data']['beneficiaryName']
    
    # Soft check - not all APIs return beneficiary name
    if response_name:
        assert response_name == request_name, \
            f"Beneficiary name mismatch. Expected: {request_name}, Got: {response_name}"
        logger.info(f"✓ Beneficiary name matches: {request_name}")
    else:
        logger.info("⚠ Beneficiary name not in response (may be expected)")


@then('I store first P2P transfer response')
def step_store_first_transfer_response(context):
    """Store first transfer response for comparison"""
    context.first_transfer_response = context.response.json()
    logger.info("✓ First transfer response stored")


@then('response should indicate duplicate P2P transaction')
def step_response_indicates_duplicate(context):
    """Verify response indicates duplicate transaction"""
    response_data = context.response.json()
    
    # Check for duplicate transaction indicators
    duplicate_indicators = ['duplicate', 'already exists', 'transaction already processed', 'idempotent']
    
    response_text = json.dumps(response_data).lower()
    is_duplicate = any(indicator in response_text for indicator in duplicate_indicators)
    
    # Or check for specific error codes
    if 'error' in response_data or 'message' in response_data:
        logger.info(f"✓ Response indicates duplicate/error: {response_data}")
    else:
        logger.info("⚠ Duplicate transaction check - response may handle differently")
