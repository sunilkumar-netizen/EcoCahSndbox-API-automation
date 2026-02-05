"""
Step definitions for Church Payment Options API (Pay to Church Flow)
GET /bff/v2/payment/options

This API requires user token (accessToken) from PIN Verify API
Query Parameters: serviceType (e.g., sasai-app-payment)

This file contains church-specific step definitions that delegate to school payment options steps,
as both church and school payment options use the same API endpoint and response structure.
"""

import json
from behave import given, when, then


# ============================
# WHEN Steps - Church-specific Actions
# ============================

@when('I send church payment options request to "{endpoint}"')
def step_send_church_payment_options_request(context, endpoint):
    """Send GET request to church payment options endpoint"""
    # Import the school payment options step function
    from steps.school_payment_options_steps import step_send_school_payment_options_request
    
    context.base_test.logger.info("⛪ Church Payment Options - Using payment options API")
    # Reuse the school payment options step as they use the same endpoint
    step_send_school_payment_options_request(context, endpoint)


@when('I send church payment options request with stored token to "{endpoint}"')
def step_send_church_payment_options_with_stored_token(context, endpoint):
    """Send church payment options request using token stored from previous step"""
    context.base_test.logger.info("⛪ Church Payment Options - Using stored token")
    step_send_church_payment_options_request(context, endpoint)


@when('I send {count:d} church payment options requests to "{endpoint}"')
def step_send_multiple_church_payment_options_requests(context, count, endpoint):
    """Send multiple church payment options requests"""
    context.base_test.logger.info(f"⛪ Church Payment Options - Sending {count} requests")
    
    context.multiple_responses = []
    
    for i in range(count):
        context.base_test.logger.info(f"📤 Sending request {i + 1}/{count}")
        step_send_church_payment_options_request(context, endpoint)
        
        # Store response
        context.multiple_responses.append({
            'status_code': context.response.status_code,
            'response_time': context.response.elapsed.total_seconds() * 1000,
            'body': context.response.json() if context.response.status_code == 200 else None
        })
    
    context.base_test.logger.info(f"✅ Completed {count} church payment options requests")


# ============================
# THEN Steps - Church-specific Assertions
# ============================

# NOTE: The following steps are already defined in payment_options_steps.py:
# - @then('response should have payment options')
# - @then('response should have payment options structure')
# These steps are reused for church payment options testing


@then('payment instruments should not be empty')
def step_verify_payment_instruments_not_empty(context):
    """Verify payment instruments are not empty"""
    response_json = context.response.json()
    
    instruments_count = 0
    
    if 'items' in response_json:
        for item in response_json['items']:
            if 'instruments' in item:
                instruments_count += len(item['instruments'])
    
    assert instruments_count > 0, "Payment instruments should not be empty"
    context.base_test.logger.info(f"✅ Found {instruments_count} payment instruments")


@then('wallet option should have balance information')
def step_verify_wallet_balance_info(context):
    """Verify wallet option has balance information"""
    response_json = context.response.json()
    
    balance_found = False
    
    if 'items' in response_json:
        for item in response_json['items']:
            # Check if this is wallet option
            if item.get('code') == 'wallet' or 'wallet' in str(item.get('name', '')).lower():
                # Look for balance information
                if 'instruments' in item:
                    for instrument in item['instruments']:
                        if 'balance' in instrument or 'availableBalance' in instrument or 'amount' in instrument:
                            balance_found = True
                            context.base_test.logger.info(f"✓ Found balance info in wallet instrument")
                            break
            if balance_found:
                break
    
    assert balance_found, "Wallet option should have balance information"
    context.base_test.logger.info("✅ Wallet option has balance information")


@then('I extract available payment methods from response')
def step_extract_payment_methods(context):
    """Extract available payment methods from response"""
    response_json = context.response.json()
    
    context.payment_methods = []
    
    if 'items' in response_json:
        for item in response_json['items']:
            method = {
                'code': item.get('code'),
                'name': item.get('name') or item.get('displayName'),
                'instruments_count': len(item.get('instruments', []))
            }
            context.payment_methods.append(method)
            context.base_test.logger.info(f"✓ Extracted method: {method['name']} ({method['code']}) - {method['instruments_count']} instruments")
    
    context.base_test.logger.info(f"✅ Extracted {len(context.payment_methods)} payment methods")


@then('extracted payment methods should not be empty')
def step_verify_extracted_payment_methods_not_empty(context):
    """Verify extracted payment methods are not empty"""
    assert hasattr(context, 'payment_methods'), "Payment methods not extracted"
    assert len(context.payment_methods) > 0, "Payment methods should not be empty"
    
    context.base_test.logger.info(f"✅ Extracted {len(context.payment_methods)} payment methods")


# NOTE: The following steps are already defined in merchant_lookup_code_steps.py:
# - @then('all requests should return status code {expected_status:d}')
# - @then('all responses should be consistent')
# These steps are reused for church payment options testing


# ============================
# NOTE: Reused Steps from Other Files
# ============================
# The following steps are already defined in other step files and work for church payment options:
#
# From school_payment_options_steps.py:
# - @given('I have device information headers')
# - @given('I have all required device headers')
# - @given('I have device type "{device_type}"')
# - @given('I have OS version "{os_version}"')
# - @given('I have app version "{app_version}"')
# - @given('I have latitude "{latitude}"')
# - @given('I have longitude "{longitude}"')
# - @then('response should have payment instruments')
# - @then('response should contain wallet payment option')
# - @then('payment options response should have items')
# - @then('payment options response should have instruments')
# - @then('payment instruments should have instrument tokens')
# - @then('payment instruments should have provider information')
# - @then('all instrument tokens should not be empty')
# - @then('payment instruments should have currency information')
# - @then('response should have default payment instrument')
# - @then('response should have payment menu')
# - @then('payment options should have providers list')
# - @then('providers should have health check status')
# - @then('payment providers should support balance enquiry')
# - @then('payment options should contain wallet details')
# - @then('wallet details should have masked account number')
# - @then('I extract instrument token from response')
# - @then('instrument token should be valid format')
#
# From payment_options_steps.py:
# - @given('I have service type "{service_type}"')
# - @given('I have no service type')
#
# From merchant_lookup_steps.py:
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
#
# From merchant_lookup_code_steps.py:
# - @given('I have merchant code "{merchant_code}"')
# - @when('I send merchant lookup by code request to "{endpoint}"')
# - @when('I send merchant lookup by code request with extracted code to "{endpoint}"')
# - @then('response should contain merchant details by code')
# - @then('I store response time as first_request_time')
# - @then('response should match previous response')
#
# From church_search_steps.py:
# - @given('I have search type "{search_type}"')
# - @given('I have page number {page_number:d}')
# - @given('I have page size {page_size:d}')
# - @given('I have name query "{name}"')
# - @when('I send church search request to "{endpoint}"')
# - @then('I extract first merchant code from search results')
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
# - @then('I store the user token from response')
