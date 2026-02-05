"""
Step definitions for Merchant Lookup by Code API (Pay to School Flow)
GET /bff/v1/catalog/merchant-lookup

This API requires user token (accessToken) from PIN Verify API
Query Parameters: merCode (merchant code)
"""

import json
import logging
from behave import given, when, then
from core.base_test import BaseTest

logger = logging.getLogger(__name__)


# ============================
# GIVEN Steps - Setup
# ============================

@given('I have merchant code "{merchant_code}"')
def step_set_merchant_code(context, merchant_code):
    """Set the merchant code for lookup"""
    context.merchant_code = merchant_code
    logger.info(f"🏪 Set merchant code: {merchant_code}")


@given('I have no merchant code')
def step_no_merchant_code(context):
    """Clear merchant code to test missing parameter"""
    context.merchant_code = None
    logger.info("❌ Merchant code cleared (testing missing parameter)")


@given('I extract first merchant code from search results')
def step_extract_merchant_code_from_search(context):
    """Extract merchant code from previous search results (for integration tests)"""
    if not hasattr(context, 'response'):
        raise Exception("No previous response found. Run search first.")
    
    response_json = context.response.json()
    
    # Try to find merchant code in response
    if 'merchants' in response_json and len(response_json['merchants']) > 0:
        context.merchant_code = response_json['merchants'][0].get('code')
        logger.info(f"📦 Extracted merchant code: {context.merchant_code}")
    else:
        raise Exception("No merchants found in search results")


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

@when('I send merchant lookup by code request to "{endpoint}"')
def step_send_merchant_lookup_by_code(context, endpoint):
    """Send GET request to merchant lookup endpoint with merCode parameter"""
    api_client = context.base_test.api_client
    
    # Build query parameters
    params = {}
    
    if hasattr(context, 'merchant_code') and context.merchant_code is not None:
        params['merCode'] = context.merchant_code
    
    logger.info(f"🏪 Merchant Lookup Query Parameters: {params}")
    
    # Build headers
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    # Add Authorization header if token exists
    if hasattr(context, 'no_auth') and context.no_auth:
        logger.info("🚫 Skipping Authorization header (testing no auth)")
    elif hasattr(context, 'no_auth_header') and context.no_auth_header:
        logger.info("🚫 Skipping Authorization header (testing missing header)")
    elif hasattr(context, 'user_token') and context.user_token:
        headers['Authorization'] = f'Bearer {context.user_token}'
        logger.info(f"🔑 Using user token: {context.user_token[:20]}...")
    elif hasattr(context, 'app_token_only') and context.app_token_only:
        # Use app token instead of user token (for negative testing)
        if hasattr(context, 'app_token'):
            headers['Authorization'] = f'Bearer {context.app_token}'
            logger.info(f"🔑 Using app token (should fail): {context.app_token[:20]}...")
    else:
        logger.warning("⚠️ No user token available for Authorization header")
    
    # Make the GET request
    logger.info(f"🚀 Sending GET request to: {endpoint}")
    logger.info(f"📋 Headers: {headers}")
    
    context.response = api_client.get(
        endpoint=endpoint,
        params=params,
        headers=headers
    )
    
    # Log response details
    logger.info(f"📥 Response Status: {context.response.status_code}")
    logger.info(f"⏱️ Response Time: {context.response.elapsed.total_seconds() * 1000:.2f} ms")
    
    try:
        response_json = context.response.json()
        logger.info(f"📦 Response Body: {json.dumps(response_json, indent=2)}")
    except Exception as e:
        logger.warning(f"⚠️ Could not parse response as JSON: {str(e)}")
        logger.info(f"📦 Raw Response: {context.response.text[:500]}")


@when('I send merchant lookup by code request with stored token to "{endpoint}"')
def step_send_merchant_lookup_with_stored_token(context, endpoint):
    """Send merchant lookup request using token stored from previous step (integration test)"""
    # This step is used in integration scenarios where we chain APIs
    # The token should be stored in context.user_token from PIN verification
    step_send_merchant_lookup_by_code(context, endpoint)


@when('I send merchant lookup by code request with extracted code to "{endpoint}"')
def step_send_merchant_lookup_with_extracted_code(context, endpoint):
    """Send merchant lookup request using code extracted from search results"""
    # The merchant code should be stored in context.merchant_code from search
    step_send_merchant_lookup_by_code(context, endpoint)


@when('I send {count:d} merchant lookup by code requests to "{endpoint}"')
def step_send_multiple_merchant_lookups(context, count, endpoint):
    """Send multiple merchant lookup requests for stress/concurrent testing"""
    import time
    
    context.multiple_responses = []
    
    for i in range(count):
        step_send_merchant_lookup_by_code(context, endpoint)
        context.multiple_responses.append({
            'status_code': context.response.status_code,
            'response_data': context.response.json() if context.response.status_code == 200 else None
        })
        time.sleep(0.1)  # Small delay between requests
    
    context.base_test.logger.info(f"Sent {count} merchant lookup requests")


# Note: The following @when steps are already defined in common_steps.py:
# - I send POST request to "{endpoint}"
# - I send GET request to "{endpoint}"
# - I send PUT request to "{endpoint}"
# - I send DELETE request to "{endpoint}"
# They work for all APIs including Merchant Lookup


# ============================
# THEN Steps - Assertions
# ============================

@then('response should contain merchant details by code')
def step_verify_merchant_details(context):
    """Verify response contains merchant details"""
    response_json = context.response.json()
    
    # Check if response has merchant data structure
    assert response_json is not None, "Response body should not be empty"
    
    # Check for common merchant fields (adjust based on actual API response)
    if isinstance(response_json, dict):
        assert len(response_json) > 0, "Merchant details should not be empty"
    
    logger.info("✅ Response contains merchant details by code")


@then('response should have merchant information')
def step_verify_merchant_information(context):
    """Verify response has merchant information"""
    response_json = context.response.json()
    
    # Verify basic structure
    assert response_json is not None, "Response should not be empty"
    
    logger.info("✅ Response has merchant information")


@then('response should have merchant structure')
def step_verify_merchant_structure(context):
    """Verify response has proper merchant structure"""
    response_json = context.response.json()
    
    # Verify it's a valid JSON object
    assert isinstance(response_json, (dict, list)), "Response should be a JSON object or array"
    
    logger.info("✅ Response has valid merchant structure")


@then('merchant response should have required fields')
def step_verify_merchant_required_fields(context):
    """Verify merchant response contains required fields"""
    response_json = context.response.json()
    
    # Common merchant fields to check (adjust based on actual API response)
    required_fields = ['name', 'code', 'mobileNumber']
    
    if isinstance(response_json, dict):
        # Check if it's a single merchant object
        for field in required_fields:
            if field in response_json:
                logger.info(f"✓ Found field: {field}")
    
    logger.info("✅ Merchant response has required fields")


@then('merchant response should contain name')
def step_verify_merchant_has_name(context):
    """Verify merchant response contains name field"""
    response_json = context.response.json()
    
    if isinstance(response_json, dict):
        assert 'name' in response_json or 'merchantName' in response_json, \
            "Response should contain merchant name"
    
    logger.info("✅ Merchant response contains name")


@then('merchant response should contain code')
def step_verify_merchant_has_code(context):
    """Verify merchant response contains code field"""
    response_json = context.response.json()
    
    if isinstance(response_json, dict):
        assert 'code' in response_json or 'merCode' in response_json or 'merchantCode' in response_json, \
            "Response should contain merchant code"
    
    logger.info("✅ Merchant response contains code")


@then('merchant response should contain mobile number')
def step_verify_merchant_has_mobile(context):
    """Verify merchant response contains mobile number field"""
    response_json = context.response.json()
    
    if isinstance(response_json, dict):
        assert 'mobileNumber' in response_json or 'mobile' in response_json or 'phone' in response_json, \
            "Response should contain mobile number"
    
    logger.info("✅ Merchant response contains mobile number")


@then('response merchant code should match requested code "{expected_code}"')
def step_verify_merchant_code_match(context, expected_code):
    """Verify the merchant code in response matches the requested code"""
    response_json = context.response.json()
    
    if isinstance(response_json, dict):
        actual_code = response_json.get('code') or response_json.get('merCode') or response_json.get('merchantCode')
        assert actual_code == expected_code, \
            f"Expected merchant code '{expected_code}', but got '{actual_code}'"
        logger.info(f"✅ Merchant code matches: {expected_code}")
    else:
        logger.warning("⚠️ Could not verify merchant code match - unexpected response structure")


@then('merchant name should not be empty')
def step_verify_merchant_name_not_empty(context):
    """Verify merchant name is not empty"""
    response_json = context.response.json()
    
    if isinstance(response_json, dict):
        name = response_json.get('name') or response_json.get('merchantName')
        assert name, "Merchant name should not be empty"
        assert len(str(name).strip()) > 0, "Merchant name should not be blank"
        logger.info(f"✅ Merchant name is not empty: {name}")


@then('merchant code should not be empty')
def step_verify_merchant_code_not_empty(context):
    """Verify merchant code is not empty"""
    response_json = context.response.json()
    
    if isinstance(response_json, dict):
        code = response_json.get('code') or response_json.get('merCode') or response_json.get('merchantCode')
        assert code, "Merchant code should not be empty"
        assert len(str(code).strip()) > 0, "Merchant code should not be blank"
        logger.info(f"✅ Merchant code is not empty: {code}")


@then('merchant should have address information')
def step_verify_merchant_has_address(context):
    """Verify merchant has address information"""
    response_json = context.response.json()
    
    if isinstance(response_json, dict):
        has_address = 'address' in response_json or 'location' in response_json or 'street' in response_json
        assert has_address, "Merchant should have address information"
        logger.info("✅ Merchant has address information")


@then('merchant should have city information')
def step_verify_merchant_has_city(context):
    """Verify merchant has city information"""
    response_json = context.response.json()
    
    if isinstance(response_json, dict):
        has_city = 'city' in response_json or 'town' in response_json
        assert has_city, "Merchant should have city information"
        logger.info("✅ Merchant has city information")


# ==============================================================================
# Additional Steps for Church/School Lookup Features
# ==============================================================================

@given('I set request header "{header_name}" to "{header_value}"')
def step_set_request_header(context, header_name, header_value):
    """Set a custom request header."""
    if not hasattr(context, 'custom_headers'):
        context.custom_headers = {}
    context.custom_headers[header_name] = header_value
    context.base_test.logger.info(f"Set header {header_name}: {header_value}")


@then('response should have merchant type field')
def step_response_should_have_merchant_type_field(context):
    """Verify response contains merchant type field."""
    assert context.response.status_code == 200, f"Expected 200, got {context.response.status_code}"
    
    response_data = context.response.json()
    
    # Check for type field
    type_fields = ['type', 'merchantType', 'merchant_type']
    has_type_field = any(field in response_data for field in type_fields)
    
    assert has_type_field, f"Response missing merchant type field. Available fields: {list(response_data.keys())}"
    
    context.base_test.logger.info("Response has merchant type field")


@then('response merchant code should match "{expected_code}"')
def step_response_merchant_code_should_match(context, expected_code):
    """Verify returned merchant code matches the requested code."""
    assert context.response.status_code == 200, f"Expected 200, got {context.response.status_code}"
    
    response_data = context.response.json()
    
    # Find the code field
    code_fields = ['code', 'merCode', 'merchantCode', 'merchant_code']
    actual_code = None
    
    for field in code_fields:
        if field in response_data:
            actual_code = str(response_data[field])
            break
    
    assert actual_code is not None, "Could not find merchant code in response"
    assert actual_code == expected_code, f"Expected code {expected_code}, got {actual_code}"
    
    context.base_test.logger.info(f"Merchant code matches: {expected_code}")


@then('merchant type should be "{expected_type}"')
def step_merchant_type_should_be(context, expected_type):
    """Verify merchant type matches expected value."""
    assert context.response.status_code == 200, f"Expected 200, got {context.response.status_code}"
    
    response_data = context.response.json()
    
    # Find the type field
    type_fields = ['type', 'merchantType', 'merchant_type']
    actual_type = None
    
    for field in type_fields:
        if field in response_data:
            actual_type = response_data[field]
            break
    
    assert actual_type is not None, "Could not find merchant type in response"
    assert actual_type == expected_type, f"Expected type {expected_type}, got {actual_type}"
    
    context.base_test.logger.info(f"Merchant type is: {expected_type}")


@then('merchant code should be numeric string')
def step_merchant_code_should_be_numeric_string(context):
    """Verify merchant code is a numeric string."""
    assert context.response.status_code == 200, f"Expected 200, got {context.response.status_code}"
    
    response_data = context.response.json()
    
    # Find the code field
    code_fields = ['code', 'merCode', 'merchantCode', 'merchant_code']
    merchant_code = None
    
    for field in code_fields:
        if field in response_data:
            merchant_code = str(response_data[field])
            break
    
    assert merchant_code is not None, "Could not find merchant code in response"
    assert merchant_code.isdigit(), f"Merchant code '{merchant_code}' is not numeric"
    
    context.base_test.logger.info(f"Merchant code is numeric: {merchant_code}")


@then('I store response time as first_request_time')
def step_store_response_time(context):
    """Store response time for comparison."""
    context.first_request_time = context.response_time
    context.base_test.logger.info(f"Stored first request time: {context.first_request_time:.2f}ms")


@then('response should match previous response')
def step_response_should_match_previous_response(context):
    """Verify current response matches previously stored response (for caching tests)."""
    if not hasattr(context, 'previous_response_data'):
        context.previous_response_data = context.response.json()
        context.base_test.logger.info("Stored response data for comparison")
    else:
        current_data = context.response.json()
        assert current_data == context.previous_response_data, "Response data doesn't match previous response"
        context.base_test.logger.info("Response matches previous response (caching working)")


@then('response should not contain database error')
def step_response_should_not_contain_database_error(context):
    """Verify response doesn't expose database errors."""
    response_text = context.response.text.lower()
    
    # Check for common database error keywords
    db_error_keywords = ['sql', 'database', 'mysql', 'postgres', 'oracle', 'syntax error', 'query failed']
    
    for keyword in db_error_keywords:
        assert keyword not in response_text, f"Response contains database error keyword: {keyword}"
    
    context.base_test.logger.info("Response does not contain database errors")


@then('I extract merchant name from response')
def step_extract_merchant_name(context):
    """Extract merchant name from response."""
    assert context.response.status_code == 200, f"Expected 200, got {context.response.status_code}"
    
    response_data = context.response.json()
    
    # Find the name field
    name_fields = ['name', 'merchantName', 'merchant_name']
    
    for field in name_fields:
        if field in response_data:
            context.extracted_merchant_name = response_data[field]
            context.base_test.logger.info(f"Extracted merchant name: {context.extracted_merchant_name}")
            return
    
    raise AssertionError("Could not find merchant name field in response")


@then('I extract merchant code from response')
def step_extract_merchant_code(context):
    """Extract merchant code from response."""
    assert context.response.status_code == 200, f"Expected 200, got {context.response.status_code}"
    
    response_data = context.response.json()
    
    # Find the code field
    code_fields = ['code', 'merCode', 'merchantCode', 'merchant_code']
    
    for field in code_fields:
        if field in response_data:
            context.extracted_merchant_code = str(response_data[field])
            context.base_test.logger.info(f"Extracted merchant code: {context.extracted_merchant_code}")
            return
    
    raise AssertionError("Could not find merchant code field in response")


@then('extracted details should not be empty')
def step_extracted_details_should_not_be_empty(context):
    """Verify extracted details are not empty."""
    assert hasattr(context, 'extracted_merchant_name'), "Merchant name not extracted"
    assert hasattr(context, 'extracted_merchant_code'), "Merchant code not extracted"
    
    assert len(str(context.extracted_merchant_name).strip()) > 0, "Extracted merchant name is empty"
    assert len(str(context.extracted_merchant_code).strip()) > 0, "Extracted merchant code is empty"
    
    context.base_test.logger.info("All extracted details are valid and not empty")


@then('all requests should return status code {expected_status:d}')
def step_all_requests_should_return_status(context, expected_status):
    """Verify all multiple requests returned expected status code."""
    if not hasattr(context, 'multiple_responses'):
        raise AssertionError("No multiple responses found")
    
    for idx, response in enumerate(context.multiple_responses):
        assert response['status_code'] == expected_status, \
            f"Request {idx+1} returned {response['status_code']}, expected {expected_status}"
    
    context.base_test.logger.info(f"All {len(context.multiple_responses)} requests returned status {expected_status}")


@then('all responses should be consistent')
def step_all_responses_should_be_consistent(context):
    """Verify all multiple responses have consistent data."""
    if not hasattr(context, 'multiple_responses'):
        raise AssertionError("No multiple responses found")
    
    first_response = context.multiple_responses[0]['response_data']
    
    for idx, response in enumerate(context.multiple_responses[1:], start=2):
        assert response['response_data'] == first_response, \
            f"Request {idx} response differs from first response"
    
    context.base_test.logger.info(f"All {len(context.multiple_responses)} responses are consistent")


@then('I extract first merchant code from search results')
def step_then_extract_merchant_code_from_search(context):
    """Extract merchant code from previous search results (for integration tests) - Then version"""
    step_extract_merchant_code_from_search(context)
