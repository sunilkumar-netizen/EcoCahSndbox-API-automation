"""
Step definitions for Utility Payment API (Merchant Payment Flow - Step 8)
Endpoint: POST /bff/v2/order/utility/payment
This API processes utility payments for merchant transactions
"""

from behave import given, when, then
import logging
import json

logger = logging.getLogger(__name__)


# Given Steps - Setup test data
# ============================================================================

@given('I have utility payment request body')
def step_have_utility_payment_body(context):
    """
    Set up complete utility payment request body with all required fields
    """
    config = context.base_test.config
    
    # Use instrument token from payment options if available, otherwise use config
    instrument_token = getattr(context, 'instrument_token', None) or config.get('utility_payment.instrument_token', 'b92b7a27-99cb-4c72-9731-3df21d791334')
    
    if hasattr(context, 'instrument_token'):
        logger.info(f"🔑 Using dynamic instrument token from Payment Options API: {instrument_token}")
    else:
        logger.info(f"🔑 Using instrument token from config: {instrument_token}")
    
    context.utility_payment_body = {
        "feeAmount": config.get('utility_payment.fee_amount', 0),
        "currency": config.get('utility_payment.currency', 'USD'),
        "billerDetails": {
            "operatorId": config.get('utility_payment.operator_id', 'SZWOM00001'),
            "categoryId": config.get('utility_payment.category_id', 'SZWC10002'),
            "amount": config.get('utility_payment.payer_amount', 7),
            "currency": config.get('utility_payment.currency', 'USD'),
            "integratorTxnId": config.get('utility_payment.integrator_txn_id', 'c26af4c4-a62b-47f2-84e3-0167e4ece571'),
            "Q1": config.get('utility_payment.q1_value', '001535')
        },
        "payerAmount": config.get('utility_payment.payer_amount', 7),
        "payerDetails": {
            "instrumentToken": instrument_token,  # Use dynamic token here
            "paymentMethod": config.get('utility_payment.payment_method', 'wallet'),
            "provider": config.get('utility_payment.provider', 'ecocash'),
            "pin": config.get('utility_payment.encrypted_pin'),
            "publicKeyAlias": config.get('utility_payment.public_key_alias', 'payment-links')
        },
        "subType": config.get('utility_payment.subtype', 'merchant-pay'),
        "channel": config.get('utility_payment.channel', 'sasai-super-app'),
        "deviceInfo": {
            "ip": config.get('utility_payment.device_ip', '192.0.0.2'),
            "model": config.get('utility_payment.device_model', 'Samsung'),
            "network": "unidentified",
            "latitude": "unidentified",
            "longitude": "unidentified",
            "os": config.get('utility_payment.device_os', 'Android'),
            "osVersion": config.get('utility_payment.device_os_version', '13'),
            "appVersion": config.get('utility_payment.app_version', '1.4.1'),
            "package": config.get('utility_payment.app_package', 'com.sasai.sasaipay'),
            "simNumber": config.get('utility_payment.sim_number', 'SIM_777222015'),
            "deviceId": config.get('utility_payment.device_id', 'deviceID_777222015')
        },
        "notes": {}
    }
    
    logger.info(f"Utility payment request body prepared: {json.dumps(context.utility_payment_body, indent=2)}")


@given('I have fee amount {fee_amount:d}')
def step_have_fee_amount(context, fee_amount):
    """
    Set fee amount for utility payment
    """
    if not hasattr(context, 'utility_payment_body'):
        context.utility_payment_body = {}
    
    context.utility_payment_body['feeAmount'] = fee_amount
    logger.info(f"Fee amount set to: {fee_amount}")


@given('I have biller details for utility payment')
def step_have_biller_details(context):
    """
    Set up biller details for utility payment
    """
    config = context.base_test.config
    
    if not hasattr(context, 'utility_payment_body'):
        context.utility_payment_body = {}
    
    context.utility_payment_body['billerDetails'] = {
        "operatorId": config.get('utility_payment.operator_id', 'SZWOM00001'),
        "categoryId": config.get('utility_payment.category_id', 'SZWC10002'),
        "amount": 7,
        "currency": "USD",
        "integratorTxnId": config.get('utility_payment.integrator_txn_id'),
        "Q1": config.get('utility_payment.q1_value', '001535')
    }
    
    logger.info("Biller details configured")


@given('I have payer amount {amount:d}')
def step_have_payer_amount(context, amount):
    """
    Set payer amount for utility payment
    """
    if not hasattr(context, 'utility_payment_body'):
        context.utility_payment_body = {}
    
    context.utility_payment_body['payerAmount'] = amount
    
    # Also update amount in billerDetails if it exists
    if 'billerDetails' in context.utility_payment_body:
        context.utility_payment_body['billerDetails']['amount'] = amount
    
    logger.info(f"Payer amount set to: {amount}")


@given('I have payer details with encrypted PIN')
def step_have_payer_details(context):
    """
    Set up payer details with encrypted PIN
    """
    config = context.base_test.config
    
    if not hasattr(context, 'utility_payment_body'):
        context.utility_payment_body = {}
    
    context.utility_payment_body['payerDetails'] = {
        "instrumentToken": config.get('utility_payment.instrument_token'),
        "paymentMethod": "wallet",
        "provider": "ecocash",
        "pin": config.get('utility_payment.encrypted_pin'),
        "publicKeyAlias": "payment-links"
    }
    
    logger.info("Payer details configured with encrypted PIN")


@given('I have payment subtype "{subtype}"')
def step_have_payment_subtype(context, subtype):
    """
    Set payment subtype
    """
    if not hasattr(context, 'utility_payment_body'):
        context.utility_payment_body = {}
    
    context.utility_payment_body['subType'] = subtype
    logger.info(f"Payment subtype set to: {subtype}")


@given('I have channel "{channel}"')
def step_have_channel(context, channel):
    """
    Set channel for payment
    """
    if not hasattr(context, 'utility_payment_body'):
        context.utility_payment_body = {}
    
    context.utility_payment_body['channel'] = channel
    logger.info(f"Channel set to: {channel}")


@given('I have device information')
def step_have_device_info(context):
    """
    Set up device information
    """
    if not hasattr(context, 'utility_payment_body'):
        context.utility_payment_body = {}
    
    context.utility_payment_body['deviceInfo'] = {
        "ip": "192.0.0.2",
        "model": "Samsung",
        "network": "unidentified",
        "latitude": "unidentified",
        "longitude": "unidentified",
        "os": "Android",
        "osVersion": "13",
        "appVersion": "1.4.1",
        "package": "com.sasai.sasaipay",
        "simNumber": "SIM_771222221",
        "deviceId": "deviceID_771222221"
    }
    
    logger.info("Device information configured")


@given('I have payment notes')
def step_have_payment_notes(context):
    """
    Add notes to payment request
    """
    if not hasattr(context, 'utility_payment_body'):
        context.utility_payment_body = {}
    
    context.utility_payment_body['notes'] = {
        "comment": "Test payment",
        "reference": "TEST_REF_001"
    }
    
    logger.info("Payment notes added")


@given('I have utility payment request without biller details')
def step_have_payment_without_biller(context):
    """
    Create payment request without biller details
    """
    step_have_utility_payment_body(context)
    del context.utility_payment_body['billerDetails']
    logger.info("Payment request prepared without biller details")


@given('I have utility payment request without payer details')
def step_have_payment_without_payer(context):
    """
    Create payment request without payer details
    """
    step_have_utility_payment_body(context)
    del context.utility_payment_body['payerDetails']
    logger.info("Payment request prepared without payer details")


@given('I have utility payment request without encrypted PIN')
def step_have_payment_without_pin(context):
    """
    Create payment request without encrypted PIN
    """
    step_have_utility_payment_body(context)
    if 'payerDetails' in context.utility_payment_body:
        del context.utility_payment_body['payerDetails']['pin']
    logger.info("Payment request prepared without encrypted PIN")


@given('I have invalid payment PIN "{pin}"')
def step_have_invalid_payment_pin(context, pin):
    """
    Set invalid encrypted PIN for utility payment
    """
    if not hasattr(context, 'utility_payment_body'):
        step_have_utility_payment_body(context)
    
    if 'payerDetails' in context.utility_payment_body:
        context.utility_payment_body['payerDetails']['pin'] = pin
    
    logger.info(f"Invalid payment PIN set: {pin}")


@given('I have utility payment request without payment method')
def step_have_payment_without_method(context):
    """
    Create payment request without payment method
    """
    step_have_utility_payment_body(context)
    if 'payerDetails' in context.utility_payment_body:
        del context.utility_payment_body['payerDetails']['paymentMethod']
    logger.info("Payment request prepared without payment method")


@given('I have invalid payment method "{method}"')
def step_have_invalid_payment_method(context, method):
    """
    Set invalid payment method
    """
    if not hasattr(context, 'utility_payment_body'):
        step_have_utility_payment_body(context)
    
    if 'payerDetails' in context.utility_payment_body:
        context.utility_payment_body['payerDetails']['paymentMethod'] = method
    
    logger.info(f"Invalid payment method set: {method}")


@given('I have utility payment request without amount')
def step_have_payment_without_amount(context):
    """
    Create payment request without amount
    """
    step_have_utility_payment_body(context)
    del context.utility_payment_body['payerAmount']
    if 'billerDetails' in context.utility_payment_body:
        del context.utility_payment_body['billerDetails']['amount']
    logger.info("Payment request prepared without amount")


@given('I have malformed JSON request body')
def step_have_malformed_json(context):
    """
    Set malformed JSON for negative testing
    """
    context.utility_payment_body = "{ malformed json"
    context.is_malformed_json = True
    logger.info("Malformed JSON body set")


# When Steps - Execute utility payment requests
# ============================================================================

@when('I send utility payment request to "{endpoint}"')
def step_send_utility_payment_request(context, endpoint):
    """
    Send POST request to utility payment endpoint
    """
    api_client = context.base_test.api_client
    
    # Build headers
    headers = {
        'Content-Type': 'application/json'
    }
    
    if hasattr(context, 'user_token') and context.user_token:
        headers['Authorization'] = f'Bearer {context.user_token}'
    
    # Get request body
    body = context.utility_payment_body if hasattr(context, 'utility_payment_body') else {}
    
    # Log the request body being sent
    logger.info(f"📤 Sending utility payment request to {endpoint}")
    logger.info(f"📦 Request Body: {json.dumps(body, indent=2)}")
    
    # Handle malformed JSON case
    if hasattr(context, 'is_malformed_json') and context.is_malformed_json:
        # Send raw malformed string
        context.response = api_client.session.post(
            f"{api_client.base_url}{endpoint}",
            data=body,
            headers=headers
        )
    else:
        # Send normal JSON request
        context.response = api_client.post(
            endpoint,
            json_data=body,
            headers=headers
        )
    
    logger.info(f"Utility payment request sent to {endpoint}")


@when('I send utility payment request with complete body')
def step_send_utility_payment_complete(context):
    """
    Send utility payment request with complete body
    """
    step_send_utility_payment_request(context, "/bff/v2/order/utility/payment")


@when('I send utility payment request with stored token to "{endpoint}"')
def step_send_utility_payment_with_stored_token(context, endpoint):
    """
    Send utility payment request using stored user token from previous step
    """
    api_client = context.base_test.api_client
    
    # Build headers
    headers = {
        'Content-Type': 'application/json'
    }
    
    if hasattr(context, 'stored_user_token') and context.stored_user_token:
        headers['Authorization'] = f'Bearer {context.stored_user_token}'
    elif hasattr(context, 'user_token') and context.user_token:
        headers['Authorization'] = f'Bearer {context.user_token}'
    
    # Get request body
    body = context.utility_payment_body if hasattr(context, 'utility_payment_body') else {}
    
    # Send POST request
    context.response = api_client.post(
        endpoint,
        json=body,
        headers=headers
    )
    
    logger.info(f"Utility payment request sent with stored token to {endpoint}")


# Then Steps - Validate responses
# ============================================================================

@then('response should contain transaction ID')
def step_verify_transaction_id(context):
    """
    Verify response contains transaction ID
    """
    response_data = context.response.json()
    
    # Check for transaction ID
    has_transaction_id = False
    transaction_id_keys = ['transactionId', 'txnId', 'orderId', 'paymentId', 'id', 'transactionID']
    
    if isinstance(response_data, dict):
        for key in transaction_id_keys:
            if key in response_data and response_data[key]:
                has_transaction_id = True
                logger.info(f"Found transaction ID in key '{key}': {response_data[key]}")
                break
        
        # Check nested data
        if not has_transaction_id and 'data' in response_data and isinstance(response_data['data'], dict):
            for key in transaction_id_keys:
                if key in response_data['data'] and response_data['data'][key]:
                    has_transaction_id = True
                    logger.info(f"Found transaction ID in data.{key}: {response_data['data'][key]}")
                    break
    
    assert has_transaction_id, f"Response should contain transaction ID, got: {response_data}"
    logger.info("✅ Response contains transaction ID")

