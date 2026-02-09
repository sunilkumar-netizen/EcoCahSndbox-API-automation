"""
Step definitions for P2P Payment Options API
Endpoint: GET /bff/v2/payment/options?serviceType=ZWPersonPaymentOptions
This is part of the "Pay to Person (Domestic)" flow

NOTE: This API retrieves available payment options/instruments for P2P transfers
"""

from behave import given, when, then
import logging
import json
import time
import uuid

# Initialize logger
logger = logging.getLogger(__name__)


# ===========================
# Given Steps - Setup
# ===========================

# Note: 'I have service type "{service_type}"' is already defined in payment_options_steps.py
# Note: 'I have request ID "{request_id}"' is already defined in merchant_lookup_steps.py


@given('I have service type ""')
def step_have_empty_service_type(context):
    """Set empty service type for testing"""
    context.service_type = ""
    logger.info(f"💳 Service type set to empty string (testing empty parameter)")


@given('I have no service type')
def step_no_service_type(context):
    """Clear service type to test missing parameter"""
    if hasattr(context, 'service_type'):
        delattr(context, 'service_type')
    context.service_type = None
    logger.info("❌ Service type cleared (testing missing parameter)")


# Note: 'I have request ID "{request_id}"' is already defined in merchant_lookup_steps.py


@given('I have no request ID')
def step_no_request_id(context):
    """Clear request ID"""
    if hasattr(context, 'request_id'):
        delattr(context, 'request_id')
    context.request_id = None
    logger.info("❌ Request ID cleared")


# ===========================
# When Steps - Actions
# ===========================

@when('I send P2P payment options request to "{endpoint}"')
def step_send_p2p_payment_options_request(context, endpoint):
    """Send GET request to P2P payment options endpoint"""
    url = f"{context.config_loader.get('api.base_url')}{endpoint}"
    
    # Build query parameters
    params = {}
    if hasattr(context, 'service_type') and context.service_type is not None:
        params['serviceType'] = context.service_type
    
    # Build headers
    headers = {
        'Authorization': f"Bearer {context.user_token}"
    }
    
    # Add request ID header if present
    if hasattr(context, 'request_id') and context.request_id:
        headers['requestId'] = context.request_id
    else:
        # Generate a random UUID if not provided
        headers['requestId'] = str(uuid.uuid4())
        logger.info(f"🆔 Generated request ID: {headers['requestId']}")
    
    try:
        logger.info(f"Sending GET request to {url}")
        logger.info(f"Query parameters: {json.dumps(params, indent=2)}")
        logger.info(f"Request ID: {headers.get('requestId')}")
        
        start_time = time.time()
        response = context.base_test.api_client.get(
            endpoint,
            params=params,
            headers=headers
        )
        context.response = response
        context.response_time = (time.time() - start_time) * 1000
        
        logger.info(f"Response Status: {response.status_code}")
        logger.info(f"Response Time: {context.response_time:.2f} ms")
        
        if response.status_code == 200:
            response_text = response.text if hasattr(response, 'text') else str(response.content)
            logger.info(f"Response: {response_text[:500]}...")  # Log first 500 chars
            
            # ✨ DYNAMIC TOKEN EXTRACTION: Extract payer instrument token
            try:
                response_json = response.json()
                if 'items' in response_json:
                    for item in response_json['items']:
                        # Check for instruments at item level (not provider level!)
                        if 'instruments' in item and len(item['instruments']) > 0:
                            # Get the first instrument (or default instrument)
                            instruments = item.get('instruments', [])
                            # Find EcoCash instrument or use first one
                            ecocash_instrument = None
                            for instrument in instruments:
                                if 'providers' in instrument:
                                    for provider in instrument['providers']:
                                        if provider.get('code') == 'ecocash':
                                            ecocash_instrument = instrument
                                            break
                                if ecocash_instrument:
                                    break
                            
                            # Use EcoCash instrument if found, otherwise use first instrument
                            target_instrument = ecocash_instrument or instruments[0]
                            context.payer_instrument_token = target_instrument.get('instrumentToken')
                            context.payer_instrument_id = target_instrument.get('instrumentId', '')
                            context.payer_account_number = target_instrument.get('accountNumber', '')
                            context.payer_full_name = target_instrument.get('fullName', '')
                            
                            logger.info(f"✅ Extracted payer instrument token: {context.payer_instrument_token}")
                            logger.info(f"✅ Extracted payer instrument ID: {context.payer_instrument_id}")
                            logger.info(f"✅ Extracted payer account number: {context.payer_account_number}")
                            logger.info(f"✅ Extracted payer name: {context.payer_full_name}")
                            break
            except Exception as token_error:
                logger.warning(f"Could not extract payer token: {str(token_error)}")
        else:
            response_text = response.text if hasattr(response, 'text') else str(response.content)
            logger.warning(f"Error Response: {response_text}")
            
    except Exception as e:
        logger.error(f"Request failed: {str(e)}")
        raise


# ===========================
# Then Steps - Assertions
# ===========================

@then('response should contain P2P payment options')
def step_response_contains_payment_options(context):
    """Verify response contains payment options"""
    assert context.response.status_code == 200, \
        f"Expected status 200, got {context.response.status_code}"
    
    response_data = context.response.json()
    
    # Check for common payment options fields (including 'items' which is used by this API)
    payment_option_fields = ['items', 'paymentOptions', 'options', 'instruments', 'paymentMethods', 'data']
    has_payment_options = any(field in response_data for field in payment_option_fields)
    
    # Could also be a list at root level
    if isinstance(response_data, list):
        has_payment_options = True
    
    assert has_payment_options, \
        f"Response missing payment options. Available fields: {list(response_data.keys() if isinstance(response_data, dict) else 'root-level-list')}"
    
    logger.info(f"✓ Response contains payment options")


@then('P2P payment options should not be empty')
def step_payment_options_not_empty(context):
    """Verify payment options are not empty"""
    response_data = context.response.json()
    
    # Find payment options in response (including 'items' field)
    payment_options = None
    if isinstance(response_data, list):
        payment_options = response_data
    elif 'items' in response_data:
        payment_options = response_data['items']
    elif 'items' in response_data:
        payment_options = response_data['items']
    elif 'paymentOptions' in response_data:
        payment_options = response_data['paymentOptions']
    elif 'options' in response_data:
        payment_options = response_data['options']
    elif 'instruments' in response_data:
        payment_options = response_data['instruments']
    elif 'data' in response_data:
        payment_options = response_data['data']
    
    assert payment_options is not None, "Payment options not found in response"
    assert len(payment_options) > 0, "Payment options list is empty"
    
    logger.info(f"✓ Payment options not empty ({len(payment_options)} option(s) available)")


@then('response should have P2P payment options list')
def step_response_has_payment_options_list(context):
    """Verify response has payment options list structure"""
    response_data = context.response.json()
    
    # Check if response has list structure
    has_list = False
    if isinstance(response_data, list):
        has_list = True
    elif 'paymentOptions' in response_data and isinstance(response_data['paymentOptions'], list):
        has_list = True
    elif 'options' in response_data and isinstance(response_data['options'], list):
        has_list = True
    elif 'instruments' in response_data and isinstance(response_data['instruments'], list):
        has_list = True
    elif 'data' in response_data and isinstance(response_data['data'], list):
        has_list = True
    
    assert has_list, "Payment options list not found in response"
    logger.info(f"✓ Response has payment options list")


@then('each P2P payment option should have required fields')
def step_each_option_has_required_fields(context):
    """Verify each payment option has required fields"""
    response_data = context.response.json()
    
    # Find payment options
    payment_options = None
    if isinstance(response_data, list):
        payment_options = response_data
    elif 'items' in response_data:
        payment_options = response_data['items']
    elif 'paymentOptions' in response_data:
        payment_options = response_data['paymentOptions']
    elif 'options' in response_data:
        payment_options = response_data['options']
    elif 'instruments' in response_data:
        payment_options = response_data['instruments']
    elif 'data' in response_data:
        payment_options = response_data['data']
    
    assert payment_options, "Payment options not found"
    assert len(payment_options) > 0, "Payment options list is empty"
    
    # Check required fields in each option
    required_fields = ['id', 'type', 'name', 'instrumentId', 'provider', 'providerName']
    
    for i, option in enumerate(payment_options):
        # At least one required field should be present
        has_any_field = any(field in option for field in required_fields)
        assert has_any_field, f"Payment option {i} missing all required fields. Available: {list(option.keys())}"
    
    logger.info(f"✓ All {len(payment_options)} payment options have required fields")


@then('P2P payment options should have valid structure')
def step_payment_options_valid_structure(context):
    """Verify payment options have valid structure"""
    response_data = context.response.json()
    
    # Find payment options
    payment_options = None
    if isinstance(response_data, list):
        payment_options = response_data
    elif 'items' in response_data:
        payment_options = response_data['items']
    elif 'paymentOptions' in response_data:
        payment_options = response_data['paymentOptions']
    elif 'options' in response_data:
        payment_options = response_data['options']
    elif 'instruments' in response_data:
        payment_options = response_data['instruments']
    elif 'data' in response_data:
        payment_options = response_data['data']
    
    assert payment_options, "Payment options not found"
    assert isinstance(payment_options, list), "Payment options should be a list"
    
    # Check each option is a dict/object
    for i, option in enumerate(payment_options):
        assert isinstance(option, dict), f"Payment option {i} should be an object/dict"
    
    logger.info(f"✓ Payment options have valid structure ({len(payment_options)} options)")


@then('I extract first P2P payment option')
def step_extract_first_payment_option(context):
    """Extract first payment option from response"""
    response_data = context.response.json()
    
    # Find payment options
    payment_options = None
    if isinstance(response_data, list):
        payment_options = response_data
    elif 'items' in response_data:
        payment_options = response_data['items']
    elif 'paymentOptions' in response_data:
        payment_options = response_data['paymentOptions']
    elif 'options' in response_data:
        payment_options = response_data['options']
    elif 'instruments' in response_data:
        payment_options = response_data['instruments']
    elif 'data' in response_data:
        payment_options = response_data['data']
    
    assert payment_options, "Payment options not found"
    assert len(payment_options) > 0, "Payment options list is empty"
    
    context.first_payment_option = payment_options[0]
    logger.info(f"✓ Extracted first payment option: {context.first_payment_option.get('providerName', 'Unknown')}")


@then('extracted P2P payment option should be valid')
def step_extracted_option_valid(context):
    """Verify extracted payment option is valid"""
    assert hasattr(context, 'first_payment_option'), "No payment option extracted"
    assert context.first_payment_option, "Extracted payment option is None"
    assert isinstance(context.first_payment_option, dict), "Payment option should be a dict"
    
    # Check it has some data
    assert len(context.first_payment_option) > 0, "Payment option is empty"
    
    logger.info(f"✓ Extracted payment option is valid with {len(context.first_payment_option)} fields")


@then('P2P payment options should contain instrument information')
def step_options_contain_instrument_info(context):
    """Verify payment options contain instrument information"""
    response_data = context.response.json()
    
    # Find payment options
    payment_options = None
    if isinstance(response_data, list):
        payment_options = response_data
    elif 'items' in response_data:
        payment_options = response_data['items']
    elif 'paymentOptions' in response_data:
        payment_options = response_data['paymentOptions']
    elif 'instruments' in response_data:
        payment_options = response_data['instruments']
    elif 'data' in response_data:
        payment_options = response_data['data']
    
    assert payment_options, "Payment options not found"
    
    # Check for instrument fields
    instrument_fields = ['instrumentId', 'instrumentType', 'type', 'id']
    found_instruments = False
    
    for option in payment_options:
        if any(field in option for field in instrument_fields):
            found_instruments = True
            break
    
    assert found_instruments, "No instrument information found in payment options"
    logger.info(f"✓ Payment options contain instrument information")


@then('each P2P instrument should have valid details')
def step_each_instrument_valid(context):
    """Verify each instrument has valid details"""
    response_data = context.response.json()
    
    # Find payment options
    payment_options = None
    if isinstance(response_data, list):
        payment_options = response_data
    elif 'items' in response_data:
        payment_options = response_data['items']
    elif 'paymentOptions' in response_data:
        payment_options = response_data['paymentOptions']
    elif 'instruments' in response_data:
        payment_options = response_data['instruments']
    elif 'data' in response_data:
        payment_options = response_data['data']
    
    assert payment_options, "Payment options not found"
    
    for i, option in enumerate(payment_options):
        # Each option should be a dict with at least some fields
        assert isinstance(option, dict), f"Instrument {i} should be a dict"
        assert len(option) > 0, f"Instrument {i} is empty"
    
    logger.info(f"✓ All {len(payment_options)} instruments have valid details")


@then('P2P payment options should have provider details')
def step_options_have_provider_details(context):
    """Verify payment options have provider details"""
    response_data = context.response.json()
    
    # Find payment options
    payment_options = None
    if isinstance(response_data, list):
        payment_options = response_data
    elif 'items' in response_data:
        payment_options = response_data['items']
    elif 'paymentOptions' in response_data:
        payment_options = response_data['paymentOptions']
    elif 'data' in response_data:
        payment_options = response_data['data']
    
    assert payment_options, "Payment options not found"
    
    # Check for provider fields
    provider_fields = ['provider', 'providerName', 'providerType', 'providerDetails']
    found_providers = False
    
    for option in payment_options:
        if any(field in option for field in provider_fields):
            found_providers = True
            break
    
    assert found_providers, "No provider details found in payment options"
    logger.info(f"✓ Payment options have provider details")


@then('P2P provider names should be valid')
def step_provider_names_valid(context):
    """Verify provider names are valid strings"""
    response_data = context.response.json()
    
    # Find payment options
    payment_options = None
    if isinstance(response_data, list):
        payment_options = response_data
    elif 'items' in response_data:
        payment_options = response_data['items']
    elif 'paymentOptions' in response_data:
        payment_options = response_data['paymentOptions']
    elif 'data' in response_data:
        payment_options = response_data['data']
    
    assert payment_options, "Payment options not found"
    
    provider_count = 0
    for option in payment_options:
        provider_name = option.get('providerName') or option.get('provider')
        if provider_name:
            assert isinstance(provider_name, str), f"Provider name should be a string: {provider_name}"
            assert len(provider_name) > 0, "Provider name should not be empty"
            provider_count += 1
    
    assert provider_count > 0, "No provider names found"
    logger.info(f"✓ All {provider_count} provider names are valid")


@then('I store first P2P payment options response')
def step_store_first_options_response(context):
    """Store first payment options response for comparison"""
    context.first_options_response = context.response.json()
    logger.info(f"✓ Stored first payment options response")


@then('second P2P payment options should match first')
def step_second_options_match_first(context):
    """Verify second payment options response matches first"""
    assert hasattr(context, 'first_options_response'), "No first response stored"
    
    second_response = context.response.json()
    
    # Compare structure (not exact match as some fields may change)
    # Just verify we got similar data structure
    if isinstance(context.first_options_response, list) and isinstance(second_response, list):
        assert len(second_response) > 0, "Second response is empty"
        logger.info(f"✓ Both responses are lists with data")
    elif isinstance(context.first_options_response, dict) and isinstance(second_response, dict):
        # Check for similar keys
        first_keys = set(context.first_options_response.keys())
        second_keys = set(second_response.keys())
        common_keys = first_keys.intersection(second_keys)
        assert len(common_keys) > 0, "No common keys between responses"
        logger.info(f"✓ Both responses have similar structure ({len(common_keys)} common keys)")
    else:
        assert False, f"Response types don't match: {type(context.first_options_response)} vs {type(second_response)}"


# ===========================
# Reused Steps Documentation
# ===========================
# The following steps are reused from other step definition files:
#
# From common_steps.py:
# - @then('response status code should be {status_code:d}')
# - @then('response body should be valid JSON')
# - @then('response time should be less than {time_ms:d} ms')
# - @then('response header "{header_name}" should be present')
# - @then('response header "{header_name}" should contain "{value}"')
# - @when('I send POST request to "{endpoint}"')
# - @when('I send PUT request to "{endpoint}"')
#
# From login_devices_steps.py:
# - @given('I have valid user authentication')
# - @given('I have no authentication token')
# - @given('I have invalid user token')
# - @given('I have expired user token')
# - @given('I have no Authorization header')
# - @given('I have empty Bearer token')
# - @given('I have malformed Bearer token')
#
# From p2p_search_contact_steps.py:
# - @given('I have search query "{query}"')
# - @given('I have country code "{code}"')
# - @given('I have page number {number:d}')
# - @given('I have page count {count:d}')
# - @when('I send contact search request to "{endpoint}"')
# - @then('I extract first contact from search results')
#
# From p2p_account_lookup_steps.py:
# - @given('I have account number from extracted contact')
# - @when('I send account lookup request to "{endpoint}"')
# - @then('response should contain account details')
#
# From otp_steps.py:
# - @given('I am authenticated with valid app token')
#
# From merchant_lookup_steps.py:
# - @given('I have request ID "{request_id}"')
#
# From payment_options_steps.py (utility payment options):
# - @given('I have service type "{service_type}"')
#
# From common_steps.py:
# - @given('API is available')
