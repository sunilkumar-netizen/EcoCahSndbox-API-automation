"""
Step definitions for Church Payment API (Pay to Church Flow)
POST /bff/v2/order/utility/payment

This API requires user token (accessToken) from PIN Verify API
Request Body: Contains payment details, biller details, payer details, device info
subType: "pay-to-church"
"""

import json
from behave import given, when, then


# ============================
# GIVEN Steps - Setup
# ============================

@given('I have church payment details')
def step_have_church_payment_details(context):
    """Set default church payment details"""
    # Get instrument token from context or use default
    instrument_token = getattr(context, 'instrument_token', '92c60cfb-4955-49a6-9f5a-0863f3f6fccb')
    
    context.payment_details = {
        "feeAmount": 0,
        "currency": "USD",
        "billerDetails": {
            "operatorId": "SZWOCH0001",
            "categoryId": "SZWC10018",
            "amount": 1.0,
            "currency": "USD",
            "Q1": "156611",  # Church code
            "Q2": "Offering"  # Transfer purpose
        },
        "payerAmount": 1.0,
        "payerDetails": {
            "instrumentToken": instrument_token,
            "paymentMethod": "wallet",
            "provider": "ecocash",
            "pin": "mvIkFBJqHn4YxGxx4/l1k2p+OyfrQgXJ11jQQi7C8N3+B5qZPDXggJrDAPFUFmezSo7CyUek15H+kSH4pWRT1MtuyKm9+M+2l9mpQnbSS2p7UDyHI17thhlc4ArhR1xRsEBfADLeCQSLL3mqk+de95FHJT/UlhjljhIbmm75Efhz67vcA+8E1YLMoWP6nA/VM/NMlWSD8HEofBQ8mDdDgKYlTjyZ86gpMroRb7Z9rC2SZfpVcl31aQE2nkx2m2OsZGo+Vqf2YqkIJBQ4Ae2llRf7PCPSB7tKY6OLiBWOYX+gISCQEthqr4sB5HgKHGwrP1+P9oxyQE2nrsdnMDTYng==",
            "publicKeyAlias": "payment-links"
        },
        "subType": "pay-to-church",
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
            "operatorName": "FAITH MINISTRIES MABVUKU",
            "code": "156611",
            "transferPurpose": "Offering"
        }
    }
    context.base_test.logger.info("⛪ Set default church payment details")


@given('I have church payment details with purpose "{purpose}"')
def step_have_church_payment_with_purpose(context, purpose):
    """Set church payment details with specific purpose"""
    step_have_church_payment_details(context)
    context.payment_details['billerDetails']['Q2'] = purpose
    context.payment_details['notes']['transferPurpose'] = purpose
    context.base_test.logger.info(f"⛪ Set church payment purpose: {purpose}")


@given('I have church payment details with amount {amount:f}')
def step_church_payment_with_amount_float(context, amount):
    """Setup church payment details with specific float amount"""
    step_have_church_payment_details(context)
    context.payment_details['payerAmount'] = amount
    context.payment_details['billerDetails']['amount'] = amount
    context.base_test.logger.info(f"Church payment amount set to: {amount}")


@given('I have church payment details with amount {amount:d}')
def step_church_payment_with_amount_int(context, amount):
    """Setup church payment details with specific integer amount"""
    step_have_church_payment_details(context)
    context.payment_details['payerAmount'] = float(amount)
    context.payment_details['billerDetails']['amount'] = float(amount)
    context.base_test.logger.info(f"Church payment amount set to: {amount}")


@given('I have church payment details with currency "{currency}"')
def step_have_church_payment_with_currency(context, currency):
    """Set church payment with specific currency"""
    step_have_church_payment_details(context)
    context.payment_details['currency'] = currency
    context.payment_details['billerDetails']['currency'] = currency
    context.base_test.logger.info(f"💱 Set church payment currency: {currency}")


@given('I have no payment details')
def step_have_no_payment_details(context):
    """Clear payment details"""
    if hasattr(context, 'payment_details'):
        delattr(context, 'payment_details')
    context.base_test.logger.info("🚫 Cleared payment details")


@given('I have church payment details without instrument token')
def step_have_church_payment_without_instrument_token(context):
    """Set church payment without instrument token"""
    step_have_church_payment_details(context)
    del context.payment_details['payerDetails']['instrumentToken']
    context.base_test.logger.info("🚫 Removed instrument token from payment details")


@given('I have church payment details with invalid instrument token')
def step_have_church_payment_with_invalid_instrument_token(context):
    """Set church payment with invalid instrument token"""
    step_have_church_payment_details(context)
    context.payment_details['payerDetails']['instrumentToken'] = 'invalid-token-12345'
    context.base_test.logger.info("⚠️ Set invalid instrument token")


@given('I have church payment details without PIN')
def step_have_church_payment_without_pin(context):
    """Set church payment without PIN"""
    step_have_church_payment_details(context)
    del context.payment_details['payerDetails']['pin']
    context.base_test.logger.info("🚫 Removed PIN from payment details")


@given('I have church payment details with incorrect PIN')
def step_have_church_payment_with_incorrect_pin(context):
    """Set church payment with incorrect PIN"""
    step_have_church_payment_details(context)
    context.payment_details['payerDetails']['pin'] = 'incorrect-pin-value'
    context.base_test.logger.info("⚠️ Set incorrect PIN")


@given('I have church payment details without operator ID')
def step_have_church_payment_without_operator_id(context):
    """Set church payment without operator ID"""
    step_have_church_payment_details(context)
    del context.payment_details['billerDetails']['operatorId']
    context.base_test.logger.info("🚫 Removed operator ID from payment details")


@given('I have church payment details with operator ID "{operator_id}"')
def step_have_church_payment_with_operator_id(context, operator_id):
    """Set church payment with specific operator ID"""
    step_have_church_payment_details(context)
    context.payment_details['billerDetails']['operatorId'] = operator_id
    context.base_test.logger.info(f"🏢 Set operator ID: {operator_id}")


@given('I have church payment details without category ID')
def step_have_church_payment_without_category_id(context):
    """Set church payment without category ID"""
    step_have_church_payment_details(context)
    del context.payment_details['billerDetails']['categoryId']
    context.base_test.logger.info("🚫 Removed category ID from payment details")


@given('I have church payment details with category ID "{category_id}"')
def step_have_church_payment_with_category_id(context, category_id):
    """Set church payment with specific category ID"""
    step_have_church_payment_details(context)
    context.payment_details['billerDetails']['categoryId'] = category_id
    context.base_test.logger.info(f"📂 Set category ID: {category_id}")


@given('I have church payment details without church code')
def step_have_church_payment_without_church_code(context):
    """Set church payment without church code"""
    step_have_church_payment_details(context)
    del context.payment_details['billerDetails']['Q1']
    del context.payment_details['notes']['code']
    context.base_test.logger.info("🚫 Removed church code from payment details")


@given('I have church payment details without payment method')
def step_have_church_payment_without_payment_method(context):
    """Set church payment without payment method"""
    step_have_church_payment_details(context)
    del context.payment_details['payerDetails']['paymentMethod']
    context.base_test.logger.info("🚫 Removed payment method from payment details")


@given('I have church payment details with extracted instrument token')
def step_have_church_payment_with_extracted_token(context):
    """Set church payment with extracted instrument token from previous response"""
    assert hasattr(context, 'instrument_token'), "No instrument token extracted"
    step_have_church_payment_details(context)
    context.base_test.logger.info(f"🔑 Using extracted instrument token: {context.instrument_token[:20]}...")


@given('I have church payment details with extracted merchant info')
def step_have_church_payment_with_extracted_merchant_info(context):
    """Set church payment with extracted merchant information"""
    step_have_church_payment_details(context)
    
    if hasattr(context, 'extracted_merchant_code'):
        context.payment_details['billerDetails']['Q1'] = context.extracted_merchant_code
        context.payment_details['notes']['code'] = context.extracted_merchant_code
        context.base_test.logger.info(f"🏢 Using extracted merchant code: {context.extracted_merchant_code}")
    
    if hasattr(context, 'extracted_merchant_name'):
        context.payment_details['notes']['operatorName'] = context.extracted_merchant_name
        context.base_test.logger.info(f"🏢 Using extracted merchant name: {context.extracted_merchant_name}")


@given('I have church payment details with extracted info')
def step_have_church_payment_with_extracted_info(context):
    """Set church payment with all extracted information"""
    step_have_church_payment_details(context)
    
    # Use extracted merchant info
    if hasattr(context, 'extracted_merchant_code'):
        context.payment_details['billerDetails']['Q1'] = context.extracted_merchant_code
        context.payment_details['notes']['code'] = context.extracted_merchant_code
    
    if hasattr(context, 'extracted_merchant_name'):
        context.payment_details['notes']['operatorName'] = context.extracted_merchant_name
    
    # Use extracted instrument token
    if hasattr(context, 'instrument_token'):
        context.payment_details['payerDetails']['instrumentToken'] = context.instrument_token
        context.base_test.logger.info(f"🔑 Using extracted instrument token")
    
    context.base_test.logger.info("✅ Set church payment with all extracted information")


@given('I have church payment details with payment method "{payment_method}"')
def step_have_church_payment_with_payment_method(context, payment_method):
    """Set church payment with specific payment method"""
    step_have_church_payment_details(context)
    context.payment_details['payerDetails']['paymentMethod'] = payment_method
    context.base_test.logger.info(f"💳 Set payment method: {payment_method}")


@given('I have church payment details with provider "{provider}"')
def step_have_church_payment_with_provider(context, provider):
    """Set church payment with specific provider"""
    step_have_church_payment_details(context)
    context.payment_details['payerDetails']['provider'] = provider
    context.base_test.logger.info(f"🏦 Set payment provider: {provider}")


@given('I have church payment details with subtype "{subtype}"')
def step_have_church_payment_with_subtype(context, subtype):
    """Set church payment with specific subtype"""
    step_have_church_payment_details(context)
    context.payment_details['subType'] = subtype
    context.base_test.logger.info(f"📋 Set payment subtype: {subtype}")


@given('I have church payment details with channel "{channel}"')
def step_have_church_payment_with_channel(context, channel):
    """Set church payment with specific channel"""
    step_have_church_payment_details(context)
    context.payment_details['channel'] = channel
    context.base_test.logger.info(f"📡 Set payment channel: {channel}")


@given('I have complete device information in payload')
def step_have_complete_device_info_in_payload(context):
    """Ensure complete device information is in payment payload"""
    if not hasattr(context, 'payment_details'):
        step_have_church_payment_details(context)
    
    # Device info is already included in default payment details
    context.base_test.logger.info("✅ Payment details include complete device information")


# ============================
# WHEN Steps - Actions
# ============================

@when('I send church payment request to "{endpoint}"')
def step_send_church_payment_request(context, endpoint):
    """Send POST request to church payment endpoint"""
    api_client = context.base_test.api_client
    
    # Get payment details
    if not hasattr(context, 'payment_details'):
        step_have_church_payment_details(context)
    
    payload = context.payment_details
    
    context.base_test.logger.info(f"💳 Church Payment Payload: {json.dumps(payload, indent=2)[:500]}...")
    
    # Build headers
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    # Add custom headers if set (device info)
    if hasattr(context, 'custom_headers'):
        headers.update(context.custom_headers)
        context.base_test.logger.info(f"📋 Custom headers added: {list(context.custom_headers.keys())}")
    
    # Add Authorization header if token exists
    if hasattr(context, 'no_auth') and context.no_auth:
        context.base_test.logger.info("🚫 Skipping Authorization header (testing no auth)")
    elif hasattr(context, 'no_auth_header') and context.no_auth_header:
        context.base_test.logger.info("🚫 Skipping Authorization header (testing missing header)")
    elif hasattr(context, 'user_token') and context.user_token:
        headers['Authorization'] = f'Bearer {context.user_token}'
        context.base_test.logger.info(f"🔑 Using user token: {context.user_token[:20]}...")
    elif hasattr(context, 'app_token_only') and context.app_token_only:
        if hasattr(context, 'app_token'):
            headers['Authorization'] = f'Bearer {context.app_token}'
            context.base_test.logger.info(f"🔑 Using app token (should fail): {context.app_token[:20]}...")
    else:
        context.base_test.logger.warning("⚠️ No user token available for Authorization header")
    
    # Make the POST request
    context.base_test.logger.info(f"🚀 Sending POST request to: {endpoint}")
    
    context.response = api_client.post(
        endpoint=endpoint,
        json=payload,
        headers=headers
    )
    
    # Log response details
    context.base_test.logger.info(f"📥 Response Status: {context.response.status_code}")
    context.base_test.logger.info(f"⏱️ Response Time: {context.response.elapsed.total_seconds() * 1000:.2f} ms")
    
    try:
        response_json = context.response.json()
        context.base_test.logger.info(f"📦 Response Body: {json.dumps(response_json, indent=2)[:1000]}...")
    except Exception as e:
        context.base_test.logger.warning(f"⚠️ Could not parse response as JSON: {str(e)}")
        context.base_test.logger.info(f"📦 Raw Response: {context.response.text[:500]}")


@when('I send church payment request with stored token to "{endpoint}"')
def step_send_church_payment_with_stored_token(context, endpoint):
    """Send church payment request using token stored from previous step"""
    step_send_church_payment_request(context, endpoint)


# ============================
# THEN Steps - Assertions
# ============================

@then('response should contain payment confirmation')
def step_verify_payment_confirmation(context):
    """Verify response contains payment confirmation"""
    response_json = context.response.json()
    
    # Check for common payment confirmation fields
    has_confirmation = False
    
    if 'status' in response_json or 'transactionId' in response_json or 'orderId' in response_json:
        has_confirmation = True
    
    assert has_confirmation, "Response should contain payment confirmation"
    context.base_test.logger.info("✅ Response contains payment confirmation")


@then('response should have transaction ID')
def step_verify_transaction_id(context):
    """Verify response contains transaction ID"""
    response_json = context.response.json()
    
    has_transaction_id = False
    transaction_id = None
    
    # Check various possible field names
    for field in ['transactionId', 'transaction_id', 'txnId', 'orderId', 'order_id', 'id']:
        if field in response_json:
            transaction_id = response_json[field]
            has_transaction_id = True
            break
    
    assert has_transaction_id, "Response should contain transaction ID"
    context.base_test.logger.info(f"✅ Transaction ID found: {transaction_id}")
    
    # Store for later use
    context.transaction_id = transaction_id


@then('transaction ID should be valid format')
def step_verify_transaction_id_format(context):
    """Verify transaction ID has valid format"""
    assert hasattr(context, 'transaction_id'), "Transaction ID not found in response"
    assert context.transaction_id, "Transaction ID should not be empty"
    assert len(str(context.transaction_id)) > 5, "Transaction ID should have valid length"
    
    context.base_test.logger.info(f"✅ Transaction ID has valid format: {context.transaction_id}")


@then('response should have payment structure')
def step_verify_payment_structure(context):
    """Verify response has valid payment structure"""
    response_json = context.response.json()
    
    # Verify response is not empty
    assert response_json, "Response should not be empty"
    assert isinstance(response_json, dict), "Response should be a dictionary"
    
    context.base_test.logger.info("✅ Response has valid payment structure")


@then('payment response should have required fields')
def step_verify_payment_required_fields(context):
    """Verify payment response has required fields"""
    response_json = context.response.json()
    
    # Check for at least some key fields (different APIs may return different fields)
    required_field_found = False
    
    required_fields = ['status', 'transactionId', 'orderId', 'id', 'message']
    for field in required_fields:
        if field in response_json:
            required_field_found = True
            context.base_test.logger.info(f"✓ Found required field: {field}")
            break
    
    assert required_field_found, f"Response should contain at least one of: {required_fields}"
    context.base_test.logger.info("✅ Payment response has required fields")


@then('payment confirmation should have transaction details')
def step_verify_payment_transaction_details(context):
    """Verify payment confirmation has transaction details"""
    response_json = context.response.json()
    
    # Check for transaction-related details
    has_details = False
    
    detail_fields = ['transactionId', 'orderId', 'status', 'amount', 'currency']
    for field in detail_fields:
        if field in response_json:
            has_details = True
            context.base_test.logger.info(f"✓ Found transaction detail: {field}")
    
    assert has_details, "Payment confirmation should have transaction details"
    context.base_test.logger.info("✅ Payment confirmation has transaction details")


@then('payment confirmation should have amount')
def step_verify_payment_amount_in_confirmation(context):
    """Verify payment confirmation contains amount"""
    response_json = context.response.json()
    
    has_amount = False
    
    amount_fields = ['amount', 'totalAmount', 'payerAmount', 'billerAmount']
    for field in amount_fields:
        if field in response_json:
            has_amount = True
            context.base_test.logger.info(f"✓ Found amount field: {field} = {response_json[field]}")
            break
    
    assert has_amount, "Payment confirmation should contain amount"
    context.base_test.logger.info("✅ Payment confirmation has amount")


@then('response should contain church name')
def step_verify_church_name_in_response(context):
    """Verify response contains church name"""
    response_json = context.response.json()
    
    has_church_name = False
    
    # Check various possible locations for church name
    if 'operatorName' in response_json or 'merchantName' in response_json:
        has_church_name = True
    elif 'notes' in response_json and 'operatorName' in response_json['notes']:
        has_church_name = True
    
    assert has_church_name, "Response should contain church name"
    context.base_test.logger.info("✅ Response contains church name")


@then('response should contain church code')
def step_verify_church_code_in_response(context):
    """Verify response contains church code"""
    response_json = context.response.json()
    
    has_church_code = False
    
    # Check various possible locations for church code
    if 'code' in response_json or 'merchantCode' in response_json:
        has_church_code = True
    elif 'notes' in response_json and 'code' in response_json['notes']:
        has_church_code = True
    
    assert has_church_code, "Response should contain church code"
    context.base_test.logger.info("✅ Response contains church code")


@then('I extract transaction ID from payment response')
def step_extract_transaction_id(context):
    """Extract transaction ID from payment response"""
    response_json = context.response.json()
    
    # Try to find transaction ID in various fields
    for field in ['transactionId', 'transaction_id', 'txnId', 'orderId', 'order_id', 'id']:
        if field in response_json:
            context.transaction_id = response_json[field]
            context.base_test.logger.info(f"✅ Extracted transaction ID: {context.transaction_id}")
            return
    
    raise AssertionError("Could not find transaction ID in response")


@then('I extract payment status from payment response')
def step_extract_payment_status(context):
    """Extract payment status from payment response"""
    response_json = context.response.json()
    
    # Try to find status in various fields
    for field in ['status', 'paymentStatus', 'transactionStatus']:
        if field in response_json:
            context.payment_status = response_json[field]
            context.base_test.logger.info(f"✅ Extracted payment status: {context.payment_status}")
            return
    
    raise AssertionError("Could not find payment status in response")


@then('extracted payment details should not be empty')
def step_verify_extracted_payment_details_not_empty(context):
    """Verify extracted payment details are not empty"""
    assert hasattr(context, 'transaction_id') or hasattr(context, 'payment_status'), \
        "No payment details were extracted"
    
    if hasattr(context, 'transaction_id'):
        assert context.transaction_id, "Transaction ID should not be empty"
        context.base_test.logger.info(f"✓ Transaction ID: {context.transaction_id}")
    
    if hasattr(context, 'payment_status'):
        assert context.payment_status, "Payment status should not be empty"
        context.base_test.logger.info(f"✓ Payment status: {context.payment_status}")
    
    context.base_test.logger.info("✅ Extracted payment details are not empty")


# ============================
# NOTE: Reused Steps from Other Files
# ============================
# The following steps are already defined in other step files and work for church payment:
#
# From school_payment_options_steps.py:
# - @given('I have device information headers')
# - @given('I have all required device headers')
# - @given('I have request ID "{request_id}"')
#
# From login_devices_steps.py:
# - @given('I have no authentication token')
# - @given('I have invalid user token')
# - @given('I have expired user token')
# - @given('I have app token only')
# - @given('I have no Authorization header')
# - @given('I have empty Bearer token')
# - @given('I have malformed Bearer token')
# - @given('I have valid user token from PIN verification')
# - @given('I have valid user authentication')
#
# From pin_verify_steps.py:
# - @given('I have valid PIN verification details')
# - @when('I send PIN verification request to "{endpoint}"')
# - @then('I store the user token from response')
#
# From merchant_lookup_code_steps.py:
# - @given('I have merchant code "{merchant_code}"')
# - @when('I send merchant lookup by code request to "{endpoint}"')
# - @when('I send merchant lookup by code request with extracted code to "{endpoint}"')
# - @then('I extract merchant name from response')
# - @then('I extract merchant code from response')
#
# From church_search_steps.py:
# - @given('I have search type "{search_type}"')
# - @given('I have page number {page_number:d}')
# - @given('I have page size {page_size:d}')
# - @given('I have name query "{name}"')
# - @when('I send church search request to "{endpoint}"')
# - @then('I extract first merchant code from search results')
#
# From church_payment_options_steps.py:
# - @given('I have service type "{service_type}"')
# - @when('I send church payment options request to "{endpoint}"')
# - @then('I extract instrument token from response')
#
# From common_steps.py:
# - @given('API is available')
# - @given('I am authenticated with valid app token')
# - @when('I send GET request to "{endpoint}"')
# - @when('I send POST request to "{endpoint}"')
# - @when('I send PUT request to "{endpoint}"')
# - @when('I send DELETE request to "{endpoint}"')
# - @then('response status code should be {status_code:d}')
# - @then('response status code should be {code1:d} or {code2:d}')
# - @then('response body should be valid JSON')
# - @then('response header "{header_name}" should be present')
# - @then('response header "{header_name}" should contain "{expected_value}"')
# - @then('response time should be less than {max_time:d} ms')
