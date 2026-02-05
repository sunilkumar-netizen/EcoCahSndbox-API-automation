"""
Step definitions for School Payment Options API (Pay to School Flow)
GET /bff/v2/payment/options

This API requires user token (accessToken) from PIN Verify API
Query Parameters: serviceType (e.g., sasai-app-payment)

NOTE: The following steps are shared with payment_options_steps.py:
- @given('I have service type "{service_type}"')
- @given('I have no service type')
These steps are automatically available for school payment options.
"""

import json
import uuid
from behave import given, when, then


# ============================
# GIVEN Steps - Setup
# ============================
# NOTE: The following steps are shared with other step files:
# - service type steps (payment_options_steps.py)
# - request ID step (merchant_lookup_steps.py)
# These steps are automatically available.

@given('I have device information headers')
def step_set_device_headers(context):
    """Set basic device information headers"""
    if not hasattr(context, 'custom_headers'):
        context.custom_headers = {}
    
    context.custom_headers.update({
        'deviceType': 'android',
        'os': 'RM6877',
        'osVersion': '15',
        'appVersion': '2.2.1',
        'model': 'realme - RMX3741',
        'package': 'com.sasai.sasaipay'
    })
    context.base_test.logger.info("📱 Set basic device information headers")


@given('I have all required device headers')
def step_set_all_device_headers(context):
    """Set all required device headers"""
    if not hasattr(context, 'custom_headers'):
        context.custom_headers = {}
    
    context.custom_headers.update({
        'os': 'RM6877',
        'deviceType': 'android',
        'currentVersion': '2.2.1',
        'Accept-Encoding': 'gzip',
        'Connection': 'keep-alive',
        'requestId': str(uuid.uuid4()),
        'appChannel': 'sasai-super-app',
        'simNumber': str(uuid.uuid4()),
        'deviceId': str(uuid.uuid4()),
        'model': 'realme - RMX3741',
        'network': 'unidentified',
        'latitude': '28.508632',
        'longitude': '77.092242',
        'osVersion': '15',
        'appVersion': '2.2.1',
        'package': 'com.sasai.sasaipay'
    })
    context.base_test.logger.info("📱 Set all required device headers")


@given('I have device type "{device_type}"')
def step_set_device_type(context, device_type):
    """Set device type header"""
    if not hasattr(context, 'custom_headers'):
        context.custom_headers = {}
    context.custom_headers['deviceType'] = device_type
    context.base_test.logger.info(f"📱 Set device type: {device_type}")


@given('I have OS version "{os_version}"')
def step_set_os_version(context, os_version):
    """Set OS version header"""
    if not hasattr(context, 'custom_headers'):
        context.custom_headers = {}
    context.custom_headers['osVersion'] = os_version
    context.base_test.logger.info(f"💻 Set OS version: {os_version}")


@given('I have app version "{app_version}"')
def step_set_app_version(context, app_version):
    """Set app version header"""
    if not hasattr(context, 'custom_headers'):
        context.custom_headers = {}
    context.custom_headers['appVersion'] = app_version
    context.base_test.logger.info(f"📲 Set app version: {app_version}")


@given('I have latitude "{latitude}"')
def step_set_latitude(context, latitude):
    """Set latitude header"""
    if not hasattr(context, 'custom_headers'):
        context.custom_headers = {}
    context.custom_headers['latitude'] = latitude
    context.base_test.logger.info(f"📍 Set latitude: {latitude}")


@given('I have longitude "{longitude}"')
def step_set_longitude(context, longitude):
    """Set longitude header"""
    if not hasattr(context, 'custom_headers'):
        context.custom_headers = {}
    context.custom_headers['longitude'] = longitude
    context.base_test.logger.info(f"📍 Set longitude: {longitude}")


# Note: The following steps are already defined in other step files and are reused:
# - I have no authentication token (login_devices_steps.py)
# - I have invalid user token (login_devices_steps.py)
# - I have expired user token (login_devices_steps.py)
# - I have app token only (login_devices_steps.py)
# - I have no Authorization header (login_devices_steps.py)
# - I have empty Bearer token (login_devices_steps.py)
# - I have malformed Bearer token (login_devices_steps.py)
# - I have token without Bearer prefix (login_devices_steps.py)
# - I have valid user token from PIN verification (login_devices_steps.py)
# - I have valid user authentication (login_devices_steps.py)
# - I have valid PIN verification details (pin_verify_steps.py)
# These steps work across all APIs


# ============================
# WHEN Steps - Actions
# ============================

@when('I send school payment options request to "{endpoint}"')
def step_send_school_payment_options_request(context, endpoint):
    """Send GET request to school payment options endpoint"""
    api_client = context.base_test.api_client
    
    # Build query parameters
    params = {}
    
    if hasattr(context, 'service_type') and context.service_type is not None:
        params['serviceType'] = context.service_type
    
    context.base_test.logger.info(f"💳 School Payment Options Query Parameters: {params}")
    
    # Build headers
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    # Add custom headers if set
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
        # Use app token instead of user token (for negative testing)
        if hasattr(context, 'app_token'):
            headers['Authorization'] = f'Bearer {context.app_token}'
            context.base_test.logger.info(f"🔑 Using app token (should fail): {context.app_token[:20]}...")
    else:
        context.base_test.logger.warning("⚠️ No user token available for Authorization header")
    
    # Make the GET request
    context.base_test.logger.info(f"🚀 Sending GET request to: {endpoint}")
    
    context.response = api_client.get(
        endpoint=endpoint,
        params=params,
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


@when('I send school payment options request with stored token to "{endpoint}"')
def step_send_school_payment_options_with_stored_token(context, endpoint):
    """Send school payment options request using token stored from previous step"""
    step_send_school_payment_options_request(context, endpoint)


# Note: The following @when steps are already defined in common_steps.py:
# - I send POST request to "{endpoint}"
# - I send GET request to "{endpoint}"
# - I send PUT request to "{endpoint}"
# - I send DELETE request to "{endpoint}"


# ============================
# THEN Steps - Assertions
# ============================

@then('response should have payment instruments')
def step_verify_payment_instruments(context):
    """Verify response contains payment instruments"""
    response_json = context.response.json()
    
    # Check for payment instruments
    has_instruments = False
    
    if 'items' in response_json:
        items = response_json['items']
        if isinstance(items, list) and len(items) > 0:
            for item in items:
                if 'instruments' in item and len(item['instruments']) > 0:
                    has_instruments = True
                    break
    
    assert has_instruments, "Response should contain payment instruments"
    context.base_test.logger.info("✅ Response has payment instruments")


# NOTE: 'response should have payment options structure' is defined in payment_options_steps.py

@then('response should contain wallet payment option')
def step_verify_wallet_payment_option(context):
    """Verify response contains wallet payment option"""
    response_json = context.response.json()
    
    has_wallet = False
    
    if 'items' in response_json:
        for item in response_json['items']:
            if item.get('code') == 'wallet' or 'wallet' in str(item).lower():
                has_wallet = True
                break
    
    assert has_wallet, "Response should contain wallet payment option"
    context.base_test.logger.info("✅ Response contains wallet payment option")


@then('payment options response should have items')
def step_verify_payment_options_has_items(context):
    """Verify payment options response has items"""
    response_json = context.response.json()
    
    assert 'items' in response_json, "Response should contain 'items' field"
    assert isinstance(response_json['items'], list), "'items' should be a list"
    assert len(response_json['items']) > 0, "'items' should not be empty"
    
    context.base_test.logger.info(f"✅ Payment options has {len(response_json['items'])} items")


@then('payment options response should have instruments')
def step_verify_payment_options_has_instruments(context):
    """Verify payment options has instruments"""
    response_json = context.response.json()
    
    instruments_found = False
    
    if 'items' in response_json:
        for item in response_json['items']:
            if 'instruments' in item:
                instruments_found = True
                break
    
    assert instruments_found, "Payment options should contain instruments"
    context.base_test.logger.info("✅ Payment options has instruments")


@then('payment instruments should have instrument tokens')
def step_verify_instruments_have_tokens(context):
    """Verify payment instruments have instrument tokens"""
    response_json = context.response.json()
    
    tokens_found = False
    
    if 'items' in response_json:
        for item in response_json['items']:
            if 'instruments' in item:
                for instrument in item['instruments']:
                    if 'instrumentToken' in instrument:
                        tokens_found = True
                        context.base_test.logger.info(f"✓ Found instrument token: {instrument['instrumentToken'][:20]}...")
                        break
            if tokens_found:
                break
    
    assert tokens_found, "Payment instruments should have instrument tokens"
    context.base_test.logger.info("✅ Payment instruments have tokens")


@then('payment instruments should have provider information')
def step_verify_instruments_have_providers(context):
    """Verify payment instruments have provider information"""
    response_json = context.response.json()
    
    providers_found = False
    
    if 'items' in response_json:
        for item in response_json['items']:
            if 'providers' in item or ('instruments' in item and any('providers' in i for i in item['instruments'])):
                providers_found = True
                break
    
    assert providers_found, "Payment instruments should have provider information"
    context.base_test.logger.info("✅ Payment instruments have provider information")


@then('all instrument tokens should not be empty')
def step_verify_instrument_tokens_not_empty(context):
    """Verify all instrument tokens are not empty"""
    response_json = context.response.json()
    
    token_count = 0
    
    if 'items' in response_json:
        for item in response_json['items']:
            if 'instruments' in item:
                for instrument in item['instruments']:
                    if 'instrumentToken' in instrument:
                        token = instrument['instrumentToken']
                        assert token and len(str(token).strip()) > 0, \
                            "Instrument token should not be empty"
                        token_count += 1
    
    assert token_count > 0, "Should have at least one instrument token"
    context.base_test.logger.info(f"✅ All {token_count} instrument tokens are not empty")


@then('payment options should contain provider "{provider_code}"')
def step_verify_payment_options_has_provider(context, provider_code):
    """Verify payment options contain specific provider"""
    response_json = context.response.json()
    
    provider_found = False
    
    if 'items' in response_json:
        for item in response_json['items']:
            if 'providers' in item:
                for provider in item['providers']:
                    if provider.get('code') == provider_code:
                        provider_found = True
                        context.base_test.logger.info(f"✓ Found provider: {provider.get('name')}")
                        break
            if provider_found:
                break
    
    assert provider_found, f"Payment options should contain provider '{provider_code}'"
    context.base_test.logger.info(f"✅ Payment options contain provider {provider_code}")


@then('payment instruments should have currency information')
def step_verify_instruments_have_currency(context):
    """Verify payment instruments have currency information"""
    response_json = context.response.json()
    
    currency_found = False
    
    if 'items' in response_json:
        for item in response_json['items']:
            if 'instruments' in item:
                for instrument in item['instruments']:
                    if 'currency' in instrument:
                        currency_found = True
                        context.base_test.logger.info(f"✓ Found currency: {instrument['currency']}")
                        break
            if currency_found:
                break
    
    assert currency_found, "Payment instruments should have currency information"
    context.base_test.logger.info("✅ Payment instruments have currency information")


@then('response should have default payment instrument')
def step_verify_default_instrument(context):
    """Verify response has a default payment instrument"""
    response_json = context.response.json()
    
    default_found = False
    
    if 'items' in response_json:
        for item in response_json['items']:
            if 'instruments' in item:
                for instrument in item['instruments']:
                    if instrument.get('isDefault') == True:
                        default_found = True
                        context.base_test.logger.info("✓ Found default payment instrument")
                        break
            if default_found:
                break
    
    assert default_found, "Response should have a default payment instrument"
    context.base_test.logger.info("✅ Response has default payment instrument")


@then('response should have payment menu')
def step_verify_payment_menu(context):
    """Verify response contains payment menu"""
    response_json = context.response.json()
    
    assert 'paymentMenu' in response_json, "Response should contain payment menu"
    context.base_test.logger.info("✅ Response has payment menu")


@then('payment options should have providers list')
def step_verify_providers_list(context):
    """Verify payment options have providers list"""
    response_json = context.response.json()
    
    providers_found = False
    
    if 'items' in response_json:
        for item in response_json['items']:
            if 'providers' in item and isinstance(item['providers'], list):
                providers_found = True
                break
    
    assert providers_found, "Payment options should have providers list"
    context.base_test.logger.info("✅ Payment options have providers list")


@then('providers should have health check status')
def step_verify_providers_health_check(context):
    """Verify providers have health check status"""
    response_json = context.response.json()
    
    health_check_found = False
    
    if 'items' in response_json:
        for item in response_json['items']:
            if 'providers' in item:
                for provider in item['providers']:
                    if 'healthCheck' in provider:
                        health_check_found = True
                        context.base_test.logger.info(f"✓ Provider {provider.get('name')} has health check: {provider['healthCheck']}")
                        break
            if health_check_found:
                break
    
    assert health_check_found, "Providers should have health check status"
    context.base_test.logger.info("✅ Providers have health check status")


@then('payment providers should support balance enquiry')
def step_verify_balance_enquiry_support(context):
    """Verify payment providers support balance enquiry"""
    response_json = context.response.json()
    
    balance_enquiry_found = False
    
    if 'items' in response_json:
        for item in response_json['items']:
            if 'providers' in item:
                for provider in item['providers']:
                    if 'balanceEnquiryEnabled' in provider:
                        balance_enquiry_found = True
                        context.base_test.logger.info(f"✓ Provider {provider.get('name')} balance enquiry: {provider['balanceEnquiryEnabled']}")
                        break
            if balance_enquiry_found:
                break
    
    assert balance_enquiry_found, "Payment providers should have balance enquiry capability"
    context.base_test.logger.info("✅ Payment providers support balance enquiry")


@then('payment options should contain wallet details')
def step_verify_wallet_details(context):
    """Verify payment options contain wallet details"""
    response_json = context.response.json()
    
    wallet_details_found = False
    
    if 'items' in response_json:
        for item in response_json['items']:
            if 'instruments' in item:
                for instrument in item['instruments']:
                    if 'walletDetails' in instrument:
                        wallet_details_found = True
                        context.base_test.logger.info("✓ Found wallet details")
                        break
            if wallet_details_found:
                break
    
    assert wallet_details_found, "Payment options should contain wallet details"
    context.base_test.logger.info("✅ Payment options contain wallet details")


@then('wallet details should have masked account number')
def step_verify_masked_account_number(context):
    """Verify wallet details have masked account number"""
    response_json = context.response.json()
    
    masked_account_found = False
    
    if 'items' in response_json:
        for item in response_json['items']:
            if 'instruments' in item:
                for instrument in item['instruments']:
                    wallet_details = instrument.get('walletDetails', {})
                    if 'maskedAccountNumber' in wallet_details:
                        masked_account_found = True
                        context.base_test.logger.info(f"✓ Found masked account: {wallet_details['maskedAccountNumber']}")
                        break
                    # Also check at instrument level
                    if 'maskedNumber' in instrument:
                        masked_account_found = True
                        context.base_test.logger.info(f"✓ Found masked number: {instrument['maskedNumber']}")
                        break
            if masked_account_found:
                break
    
    assert masked_account_found, "Wallet details should have masked account number"
    context.base_test.logger.info("✅ Wallet details have masked account number")


@then('I extract instrument token from response')
def step_extract_instrument_token(context):
    """Extract instrument token from payment options response"""
    response_json = context.response.json()
    
    token_extracted = False
    
    if 'items' in response_json:
        for item in response_json['items']:
            if 'instruments' in item and len(item['instruments']) > 0:
                instrument = item['instruments'][0]  # Get first instrument
                if 'instrumentToken' in instrument:
                    context.instrument_token = instrument['instrumentToken']
                    token_extracted = True
                    context.base_test.logger.info(f"✅ Extracted instrument token: {context.instrument_token[:20]}...")
                    break
    
    assert token_extracted, "Could not extract instrument token from response"


@then('instrument token should be valid format')
def step_verify_instrument_token_format(context):
    """Verify extracted instrument token has valid format"""
    assert hasattr(context, 'instrument_token'), "Instrument token not extracted"
    assert context.instrument_token, "Instrument token should not be empty"
    assert len(context.instrument_token) > 10, "Instrument token should have valid length"
    
    context.base_test.logger.info(f"✅ Instrument token has valid format: {context.instrument_token[:20]}...")


# Note: The following @then steps are already defined in other step files and are reused:
# - I store the user token from response (login_devices_steps.py)
# - response body should be valid JSON (common_steps.py)
# - response time should be less than {max_time:d} ms (common_steps.py)
# - response status code should be {status_code:d} (common_steps.py)
# - response status code should be {code1:d} or {code2:d} (common_steps.py)
# - response header "{header_name}" should be present (common_steps.py)
# - response header "{header_name}" should contain "{expected_value}" (common_steps.py)
# - response should contain payment options (payment_options_steps.py)
# These steps work for all APIs including School Payment Options
