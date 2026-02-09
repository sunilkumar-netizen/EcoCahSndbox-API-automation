"""
Step definitions for School Payment Processing API
Endpoint: POST /bff/v2/order/utility/payment
This is part of the "Pay to School" flow
"""

from behave import given, when, then
import json
import requests

import time


# ===========================
# Given Steps - Setup
# ===========================

@given('I have instrument token from payment options')
def step_have_instrument_token(context):
    """Set instrument token from payment options response"""
    # Try to get from extracted token, otherwise use default
    if hasattr(context, 'extracted_instrument_token'):
        context.instrument_token = context.extracted_instrument_token
    else:
        context.instrument_token = '9f144ae3-4feb-4299-aa31-f071d29e9381'
    context.base_test.logger.info(f"Set instrument token: {context.instrument_token[:20]}...")


@given('I have school payment details')
def step_have_school_payment_details(context):
    """Set default school payment details"""
    config = context.config_loader
    context.payment_details = {
        "feeAmount": 0,
        "currency": "USD",
        "billerDetails": {
            "operatorId": "SZWOSL0001",
            "categoryId": "SZWC10017",
            "amount": 2.0,
            "currency": "USD",
            "Q1": "054329",
            "Q2": "85558"
        },
        "payerAmount": 2.0,
        "payerDetails": {
            "instrumentToken": context.instrument_token,
            "paymentMethod": "wallet",
            "provider": "ecocash",
            "pin": "mvIkFBJqHn4YxGxx4/l1k2p+OyfrQgXJ11jQQi7C8N3+B5qZPDXggJrDAPFUFmezSo7CyUek15H+kSH4pWRT1MtuyKm9+M+2l9mpQnbSS2p7UDyHI17thhlc4ArhR1xRsEBfADLeCQSLL3mqk+de95FHJT/UlhjljhIbmm75Efhz67vcA+8E1YLMoWP6nA/VM/NMlWSD8HEofBQ8mDdDgKYlTjyZ86gpMroRb7Z9rC2SZfpVcl31aQE2nkx2m2OsZGo+Vqf2YqkIJBQ4Ae2llRf7PCPSB7tKY6OLiBWOYX+gISCQEthqr4sB5HgKHGwrP1+P9oxyQE2nrsdnMDTYng==",
            "publicKeyAlias": "payment-links"
        },
        "subType": "pay-to-school",
        "channel": "sasai-super-app",
        "deviceInfo": {
            "simNumber": "03d88760-d411-11f0-9694-15a487face2d",
            "deviceId": config.get('device_id', '03d88760-d411-11f0-9694-15a487face2d'),
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
            "operatorName": "PRINCE EDWARD HIGH SCHOOL",
            "code": "63540",
            "studentReference": "Alok Kumar Gupta"
        }
    }
    context.base_test.logger.info("Set default school payment details")


@given('I have school payment details with device info')
def step_have_school_payment_with_device_info(context):
    """Set school payment details with complete device information"""
    step_have_school_payment_details(context)
    # Device info is already included in default payment details
    context.base_test.logger.info("School payment details include device information")


@given('I have biller details with school code "{school_code}"')
def step_have_biller_details_with_school_code(context, school_code):
    """Set biller details with specific school code"""
    if not hasattr(context, 'payment_details'):
        step_have_school_payment_details(context)
    
    context.payment_details['billerDetails']['Q1'] = school_code
    context.school_code = school_code
    context.base_test.logger.info(f"Set biller school code: {school_code}")


@given('I have payment amount {amount:f}')
def step_have_payment_amount(context, amount):
    """Set payment amount"""
    if not hasattr(context, 'payment_details'):
        step_have_school_payment_details(context)
    
    context.payment_details['billerDetails']['amount'] = amount
    context.payment_details['payerAmount'] = amount
    context.payment_amount = amount
    context.base_test.logger.info(f"Payment amount set to: {amount}")


@given('I have payment amount {amount:d}')
def step_have_payment_amount_int(context, amount):
    """Set payment amount (integer version)"""
    step_have_payment_amount(context, float(amount))
    context.base_test.logger.info(f"Payment amount set to: {amount}")


@given('I have student reference "{student_ref}"')
def step_have_student_reference(context, student_ref):
    """Set student reference in notes"""
    if not hasattr(context, 'payment_details'):
        step_have_school_payment_details(context)
    
    context.payment_details['notes']['studentReference'] = student_ref
    context.base_test.logger.info(f"Set student reference: {student_ref}")


@given('I have school name "{school_name}"')
def step_have_school_name(context, school_name):
    """Set school name in notes"""
    if not hasattr(context, 'payment_details'):
        step_have_school_payment_details(context)
    
    context.payment_details['notes']['operatorName'] = school_name
    context.school_name = school_name
    context.base_test.logger.info(f"Set school name: {school_name}")


@given('I have invalid instrument token')
def step_have_invalid_instrument_token(context):
    """Set invalid instrument token"""
    context.instrument_token = "invalid-token-12345"
    if hasattr(context, 'payment_details'):
        context.payment_details['payerDetails']['instrumentToken'] = context.instrument_token
    context.base_test.logger.info("Set invalid instrument token")


@given('I have school payment details without instrument token')
def step_have_payment_without_instrument_token(context):
    """Set school payment details without instrument token"""
    step_have_school_payment_details(context)
    del context.payment_details['payerDetails']['instrumentToken']
    context.base_test.logger.info("Removed instrument token from payment details")


@given('I have school payment details without amount')
def step_have_payment_without_amount(context):
    """Set school payment details without amount"""
    step_have_school_payment_details(context)
    del context.payment_details['billerDetails']['amount']
    del context.payment_details['payerAmount']
    context.base_test.logger.info("Removed amount from payment details")


@given('I have school payment details without biller')
def step_have_payment_without_biller(context):
    """Set school payment details without biller details"""
    step_have_school_payment_details(context)
    del context.payment_details['billerDetails']
    context.base_test.logger.info("Removed biller details from payment")


@given('I have school payment details without currency')
def step_have_payment_without_currency(context):
    """Set school payment details without currency"""
    step_have_school_payment_details(context)
    del context.payment_details['currency']
    del context.payment_details['billerDetails']['currency']
    context.base_test.logger.info("Removed currency from payment details")


@given('I have school payment details with currency "{currency}"')
def step_have_payment_with_currency(context, currency):
    """Set school payment details with specific currency"""
    step_have_school_payment_details(context)
    context.payment_details['currency'] = currency
    context.payment_details['billerDetails']['currency'] = currency
    context.base_test.logger.info(f"Set currency: {currency}")


# NOTE: The following step is already defined in merchant_lookup_steps.py:
# @given('I have operator ID "{operator_id}"')
# This step is reused for school payment testing


@given('I have category ID "{category_id}"')
def step_have_category_id(context, category_id):
    """Set category ID in biller details"""
    if not hasattr(context, 'payment_details'):
        step_have_school_payment_details(context)
    
    context.payment_details['billerDetails']['categoryId'] = category_id
    context.base_test.logger.info(f"Set category ID: {category_id}")


@given('I have complete device information')
def step_have_complete_device_info(context):
    """Ensure complete device information is present"""
    if not hasattr(context, 'payment_details'):
        step_have_school_payment_details(context)
    
    # Device info is already complete in default payment details
    context.base_test.logger.info("Complete device information is present")


@given('I have payment notes with student info')
def step_have_notes_with_student_info(context):
    """Set payment notes with student information"""
    if not hasattr(context, 'payment_details'):
        step_have_school_payment_details(context)
    
    # Notes are already included in default payment details
    context.base_test.logger.info("Payment notes with student info are present")


@given('I have school payment details with encrypted PIN')
def step_have_payment_with_encrypted_pin(context):
    """Set school payment details with encrypted PIN"""
    step_have_school_payment_details(context)
    # PIN is already encrypted in default payment details
    context.base_test.logger.info("Payment details include encrypted PIN")


@given('I have school payment details with provider "{provider}"')
def step_have_payment_with_provider(context, provider):
    """Set school payment details with specific provider"""
    step_have_school_payment_details(context)
    context.payment_details['payerDetails']['provider'] = provider
    context.base_test.logger.info(f"Set payment provider: {provider}")


@given('I have school payment details with channel "{channel}"')
def step_have_payment_with_channel(context, channel):
    """Set school payment details with specific channel"""
    step_have_school_payment_details(context)
    context.payment_details['channel'] = channel
    context.base_test.logger.info(f"Set payment channel: {channel}")


@given('I have school payment details with subtype "{subtype}"')
def step_have_payment_with_subtype(context, subtype):
    """Set school payment details with specific subtype"""
    step_have_school_payment_details(context)
    context.payment_details['subType'] = subtype
    context.base_test.logger.info(f"Set payment subtype: {subtype}")


@given('I have school payment details with unique request ID')
def step_have_payment_with_unique_request_id(context):
    """Set school payment details with unique request ID"""
    import uuid
    step_have_school_payment_details(context)
    context.unique_request_id = str(uuid.uuid4())
    context.base_test.logger.info(f"Generated unique request ID: {context.unique_request_id}")


@given('I have school payment details with extracted token')
def step_have_payment_with_extracted_token(context):
    """Set school payment details with extracted instrument token"""
    step_have_school_payment_details(context)
    if hasattr(context, 'extracted_instrument_token'):
        context.payment_details['payerDetails']['instrumentToken'] = context.extracted_instrument_token
        context.base_test.logger.info("Using extracted instrument token in payment details")


@given('I have school payment details with extracted token and code')
def step_have_payment_with_extracted_token_and_code(context):
    """Set school payment details with extracted token and merchant code"""
    step_have_school_payment_details(context)
    if hasattr(context, 'extracted_instrument_token'):
        context.payment_details['payerDetails']['instrumentToken'] = context.extracted_instrument_token
    if hasattr(context, 'extracted_merchant_code'):
        context.payment_details['billerDetails']['Q1'] = context.extracted_merchant_code
    context.base_test.logger.info("Using extracted token and merchant code in payment details")


@given('I extract instrument token from response')
def step_extract_instrument_token_from_response(context):
    """Extract instrument token from payment options response"""
    if hasattr(context, 'response') and context.response.status_code == 200:
        response_data = context.response.json()
        if 'walletOptions' in response_data:
            wallet_options = response_data['walletOptions']
            if isinstance(wallet_options, list) and len(wallet_options) > 0:
                first_wallet = wallet_options[0]
                if 'instrumentToken' in first_wallet:
                    context.extracted_instrument_token = first_wallet['instrumentToken']
                    context.base_test.logger.info(f"Extracted instrument token: {context.extracted_instrument_token[:20]}...")
                else:
                    context.base_test.logger.warning("No instrumentToken found in wallet options")
            else:
                context.base_test.logger.warning("Wallet options list is empty")
        else:
            context.base_test.logger.warning("No walletOptions in response")


# ===========================
# When Steps - Actions
# ===========================

@when('I send school payment request to "{endpoint}"')
def step_send_school_payment_request(context, endpoint):
    """Send POST request to school payment endpoint"""
    config = context.config_loader
    url = f"{config.get('api.base_url')}{endpoint}"
    
    # Build headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {context.user_token}",
        'os': 'RM6877',
        'deviceType': 'android',
        'currentVersion': '2.2.1',
        'Accept-Encoding': 'gzip',
        'Connection': 'keep-alive',
        'appChannel': 'sasai-super-app',
        'simNumber': '03d88760-d411-11f0-9694-15a487face2d',
        'deviceId': config.get('device_id', '03d88760-d411-11f0-9694-15a487face2d'),
        'model': 'realme - RMX3741',
        'network': 'unidentified',
        'latitude': '28.4310954',
        'longitude': '77.0638722',
        'osVersion': '15',
        'appVersion': '2.2.1',
        'package': 'com.sasai.sasaipay'
    }
    
    # Add request ID if available
    if hasattr(context, 'unique_request_id'):
        headers['requestId'] = context.unique_request_id
    else:
        import uuid
        headers['requestId'] = str(uuid.uuid4())
    
    try:
        context.base_test.logger.info(f"Sending POST request to {url}")
        context.base_test.logger.info(f"Headers: {json.dumps({k: v for k, v in headers.items() if k != 'Authorization'}, indent=2)}")
        context.base_test.logger.info(f"Body: {json.dumps(context.payment_details, indent=2)}")
        
        start_time = time.time()
        context.response = requests.post(
            url,
            json=context.payment_details,
            headers=headers,
            timeout=30
        )
        context.response_time = (time.time() - start_time) * 1000
        
        context.base_test.logger.info(f"Response Status: {context.response.status_code}")
        context.base_test.logger.info(f"Response Time: {context.response_time:.2f} ms")
        
        if context.response.status_code == 200:
            context.base_test.logger.info(f"Response: {context.response.text}")
        else:
            context.base_test.logger.warning(f"Error Response: {context.response.text}")
            
    except Exception as e:
        context.base_test.logger.error(f"Request failed: {str(e)}")
        raise


@when('I send school payment request with stored token to "{endpoint}"')
def step_send_payment_with_stored_token(context, endpoint):
    """Send school payment request using stored user token"""
    if hasattr(context, 'stored_user_token'):
        context.user_token = context.stored_user_token
    step_send_school_payment_request(context, endpoint)


@when('I send the same school payment request again')
def step_send_same_payment_request_again(context):
    """Resend the same school payment request (for idempotency testing)"""
    # Reuse the same request ID and payment details
    step_send_school_payment_request(context, "/bff/v2/order/utility/payment")


# ===========================
# Then Steps - Assertions
# ===========================

@then('response should have transaction reference')
def step_response_has_transaction_reference(context):
    """Verify response has transaction reference"""
    response_data = context.response.json()
    
    reference_fields = ['referenceNumber', 'transactionId', 'reference', 'txnRef']
    has_reference = any(field in response_data for field in reference_fields)
    
    assert has_reference, \
        f"Response does not contain transaction reference. Response: {response_data}"
    
    context.base_test.logger.info("✓ Response has transaction reference")


@then('payment response should have status')
def step_payment_response_has_status(context):
    """Verify payment response has status field"""
    response_data = context.response.json()
    
    assert 'status' in response_data, \
        f"Response missing 'status' field. Response: {response_data}"
    
    context.base_test.logger.info(f"✓ Payment status: {response_data['status']}")


@then('payment response should have reference number')
def step_payment_response_has_reference_number(context):
    """Verify payment response has reference number"""
    response_data = context.response.json()
    
    reference_fields = ['referenceNumber', 'reference', 'refNumber']
    has_reference = any(field in response_data for field in reference_fields)
    
    assert has_reference, \
        f"Response missing reference number. Response: {response_data}"
    
    context.base_test.logger.info("✓ Response has reference number")


@then('payment response should have transaction ID')
def step_payment_response_has_transaction_id(context):
    """Verify payment response has transaction ID"""
    response_data = context.response.json()
    
    transaction_id_fields = ['transactionId', 'txnId', 'id']
    has_transaction_id = any(field in response_data for field in transaction_id_fields)
    
    assert has_transaction_id, \
        f"Response missing transaction ID field. Response: {response_data}"
    
    context.base_test.logger.info("✓ Response has transaction ID")


@then('payment status should be success or pending')
def step_payment_status_is_success_or_pending(context):
    """Verify payment status is success or pending"""
    response_data = context.response.json()
    
    assert 'status' in response_data, "Response missing 'status' field"
    
    status = response_data['status'].lower()
    valid_statuses = ['success', 'pending', 'completed', 'processing']
    
    assert status in valid_statuses, \
        f"Payment status '{status}' not in valid statuses: {valid_statuses}"
    
    context.base_test.logger.info(f"✓ Payment status is valid: {status}")


@then('payment response should contain amount {amount:f}')
def step_payment_response_contains_amount(context, amount):
    """Verify payment response contains specified amount"""
    response_data = context.response.json()
    
    amount_fields = ['amount', 'payerAmount', 'totalAmount']
    found_amount = None
    
    for field in amount_fields:
        if field in response_data:
            found_amount = float(response_data[field])
            break
    
    assert found_amount is not None, \
        f"Response missing amount field. Response: {response_data}"
    
    assert found_amount == amount, \
        f"Expected amount {amount}, got {found_amount}"
    
    context.base_test.logger.info(f"✓ Payment amount matches: {amount}")


@then('response should contain school details')
def step_response_contains_school_details(context):
    """Verify response contains school details"""
    response_data = context.response.json()
    
    # Check for school-related fields
    school_fields = ['operatorName', 'merchantName', 'billerName', 'schoolName']
    has_school_details = any(field in response_data for field in school_fields)
    
    # Also check in nested objects
    if not has_school_details and 'billerDetails' in response_data:
        has_school_details = any(field in response_data['billerDetails'] for field in school_fields)
    
    assert has_school_details, \
        f"Response does not contain school details. Response: {response_data}"
    
    context.base_test.logger.info("✓ Response contains school details")


@then('I store the transaction reference')
def step_store_transaction_reference(context):
    """Store transaction reference for later use"""
    response_data = context.response.json()
    
    reference_fields = ['referenceNumber', 'transactionId', 'reference', 'txnRef']
    
    for field in reference_fields:
        if field in response_data:
            context.stored_transaction_reference = response_data[field]
            context.base_test.logger.info(f"Stored transaction reference: {context.stored_transaction_reference}")
            return
    
    context.base_test.logger.warning("No transaction reference found to store")


@then('response should have receipt information')
def step_response_has_receipt_information(context):
    """Verify response has receipt information"""
    response_data = context.response.json()
    
    receipt_fields = ['receipt', 'receiptNumber', 'receiptData', 'transactionReceipt']
    has_receipt = any(field in response_data for field in receipt_fields)
    
    # Receipt info might also include transaction details that can be used for receipt
    if not has_receipt:
        # Check if we have enough info for a receipt (transaction ID, amount, date, etc.)
        has_basic_receipt_info = (
            any(f in response_data for f in ['transactionId', 'txnId', 'id']) and
            any(f in response_data for f in ['amount', 'totalAmount']) and
            any(f in response_data for f in ['timestamp', 'date', 'createdAt'])
        )
        has_receipt = has_basic_receipt_info
    
    assert has_receipt, \
        f"Response missing receipt information. Response: {response_data}"
    
    context.base_test.logger.info("✓ Response has receipt information")

