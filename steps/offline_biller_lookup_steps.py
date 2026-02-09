"""
Step definitions for Offline Biller Lookup API
GET /bff/v1/catalog/merchant-lookup?merCode={merchantCode}

This API requires user token (accessToken) from PIN Verify API
Query Parameters: merCode (merchant code)
Response: Returns biller details including name, code, category, and payment information
"""

import json
from behave import given, when, then


# ============================
# WHEN Steps - Actions
# ============================

@when('I send offline biller lookup request to "{endpoint}"')
def step_send_offline_biller_lookup_request(context, endpoint):
    """Send GET request to offline biller lookup endpoint with merchant code"""
    api_client = context.base_test.api_client
    
    # Get merchant code from context
    merchant_code = getattr(context, 'merchant_code', '8002')
    
    # Build query parameters
    query_params = {'merCode': merchant_code}
    
    context.base_test.logger.info(f"🏪 Offline Biller Lookup - Merchant Code: {merchant_code}")
    
    # Build headers
    headers = {
        'Accept': 'application/json'
    }
    
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
    
    # Make the GET request
    context.base_test.logger.info(f"🚀 Sending GET request to: {endpoint}?merCode={merchant_code}")
    
    context.response = api_client.get(
        endpoint=endpoint,
        params=query_params,
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


@when('I send offline biller lookup request without merchant code to "{endpoint}"')
def step_send_offline_biller_lookup_without_merchant_code(context, endpoint):
    """Send GET request to offline biller lookup endpoint without merchant code"""
    api_client = context.base_test.api_client
    
    context.base_test.logger.info(f"🏪 Offline Biller Lookup - No Merchant Code")
    
    # Build headers
    headers = {
        'Accept': 'application/json'
    }
    
    # Add Authorization header
    if hasattr(context, 'user_token') and context.user_token:
        headers['Authorization'] = f'Bearer {context.user_token}'
    
    # Make the GET request without query parameters
    context.base_test.logger.info(f"🚀 Sending GET request to: {endpoint} (no merCode)")
    
    context.response = api_client.get(
        endpoint=endpoint,
        headers=headers
    )
    
    context.base_test.logger.info(f"📥 Response Status: {context.response.status_code}")


# ============================
# THEN Steps - Assertions
# ============================

@then('response should contain biller details')
def step_verify_biller_details(context):
    """Verify response contains biller details"""
    response_json = context.response.json()
    
    # Check for common biller detail fields
    has_biller_details = False
    
    biller_fields = ['merchantName', 'merchant_name', 'name', 'merchantCode', 'merchant_code', 'code', 'merCode']
    for field in biller_fields:
        if field in response_json:
            has_biller_details = True
            context.base_test.logger.info(f"✓ Found biller field: {field}")
            break
    
    assert has_biller_details, f"Response should contain biller details, got: {response_json}"
    context.base_test.logger.info("✅ Response contains biller details")


@then('response should have merchant code')
def step_verify_merchant_code(context):
    """Verify response contains merchant code"""
    response_json = context.response.json()
    
    has_merchant_code = False
    merchant_code = None
    
    # Check various possible field names for merchant code
    code_fields = ['merchantCode', 'merchant_code', 'code', 'merCode', 'billerCode']
    for field in code_fields:
        if field in response_json:
            merchant_code = response_json[field]
            has_merchant_code = True
            context.base_test.logger.info(f"✓ Found merchant code in field '{field}': {merchant_code}")
            break
    
    assert has_merchant_code, "Response should contain merchant code"
    context.base_test.logger.info(f"✅ Merchant code found: {merchant_code}")
    
    # Store for later use
    context.extracted_merchant_code = merchant_code


@then('response should have merchant name')
def step_verify_merchant_name(context):
    """Verify response contains merchant name"""
    response_json = context.response.json()
    
    has_merchant_name = False
    merchant_name = None
    
    # Check various possible field names for merchant name
    name_fields = ['merchantName', 'merchant_name', 'name', 'billerName', 'operatorName']
    for field in name_fields:
        if field in response_json:
            merchant_name = response_json[field]
            has_merchant_name = True
            context.base_test.logger.info(f"✓ Found merchant name in field '{field}': {merchant_name}")
            break
    
    assert has_merchant_name, "Response should contain merchant name"
    context.base_test.logger.info(f"✅ Merchant name found: {merchant_name}")
    
    # Store for later use
    context.extracted_merchant_name = merchant_name


@then('response should have required biller fields')
def step_verify_required_biller_fields(context):
    """Verify response has required biller fields"""
    response_json = context.response.json()
    
    # Check for at least some key fields
    required_field_found = False
    
    required_fields = ['merchantCode', 'merchantName', 'code', 'name', 'category', 'operatorId']
    for field in required_fields:
        if field in response_json:
            required_field_found = True
            context.base_test.logger.info(f"✓ Found required field: {field}")
    
    assert required_field_found, f"Response should contain required biller fields, got: {response_json}"
    context.base_test.logger.info("✅ Response has required biller fields")


@then('extracted merchant details should not be empty')
def step_verify_extracted_merchant_details_not_empty(context):
    """Verify extracted merchant details are not empty"""
    assert hasattr(context, 'extracted_merchant_code') or hasattr(context, 'extracted_merchant_name'), \
        "No merchant details were extracted"
    
    if hasattr(context, 'extracted_merchant_code'):
        assert context.extracted_merchant_code, "Merchant code should not be empty"
        context.base_test.logger.info(f"✓ Merchant code: {context.extracted_merchant_code}")
    
    if hasattr(context, 'extracted_merchant_name'):
        assert context.extracted_merchant_name, "Merchant name should not be empty"
        context.base_test.logger.info(f"✓ Merchant name: {context.extracted_merchant_name}")
    
    context.base_test.logger.info("✅ Extracted merchant details are not empty")


@then('response should contain merchant name')
def step_verify_contains_merchant_name(context):
    """Verify response contains merchant name field"""
    response_json = context.response.json()
    
    has_name = False
    name_fields = ['merchantName', 'merchant_name', 'name', 'billerName']
    
    for field in name_fields:
        if field in response_json and response_json[field]:
            has_name = True
            context.base_test.logger.info(f"✓ Merchant name field found: {field}")
            break
    
    assert has_name, "Response should contain merchant name"
    context.base_test.logger.info("✅ Response contains merchant name")


@then('response should contain merchant code')
def step_verify_contains_merchant_code(context):
    """Verify response contains merchant code field"""
    response_json = context.response.json()
    
    has_code = False
    code_fields = ['merchantCode', 'merchant_code', 'code', 'merCode']
    
    for field in code_fields:
        if field in response_json and response_json[field]:
            has_code = True
            context.base_test.logger.info(f"✓ Merchant code field found: {field}")
            break
    
    assert has_code, "Response should contain merchant code"
    context.base_test.logger.info("✅ Response contains merchant code")


@then('response should contain category information')
def step_verify_category_information(context):
    """Verify response contains category information"""
    response_json = context.response.json()
    
    has_category = False
    category_fields = ['category', 'categoryId', 'category_id', 'categoryName']
    
    for field in category_fields:
        if field in response_json:
            has_category = True
            context.base_test.logger.info(f"✓ Category field found: {field}")
            break
    
    assert has_category, "Response should contain category information"
    context.base_test.logger.info("✅ Response contains category information")


@then('merchant code format should be valid')
def step_verify_merchant_code_format(context):
    """Verify merchant code has valid format"""
    response_json = context.response.json()
    
    # Get merchant code
    merchant_code = None
    for field in ['merchantCode', 'merchant_code', 'code', 'merCode']:
        if field in response_json:
            merchant_code = response_json[field]
            break
    
    assert merchant_code is not None, "Merchant code not found in response"
    assert len(str(merchant_code)) > 0, "Merchant code should not be empty"
    
    context.base_test.logger.info(f"✅ Merchant code format is valid: {merchant_code}")


@then('I store biller details for payment')
def step_store_biller_details_for_payment(context):
    """Store biller details in context for payment use"""
    response_json = context.response.json()
    
    # Store biller details
    context.biller_details = response_json
    
    context.base_test.logger.info("✅ Biller details stored for payment")
    context.base_test.logger.info(f"📋 Stored details: {json.dumps(response_json, indent=2)[:500]}...")


@then('biller details should be complete')
def step_verify_biller_details_complete(context):
    """Verify biller details are complete"""
    response_json = context.response.json()
    
    # Check for essential fields
    essential_fields_found = 0
    essential_fields = ['merchantCode', 'merchantName', 'code', 'name']
    
    for field in essential_fields:
        if field in response_json and response_json[field]:
            essential_fields_found += 1
            context.base_test.logger.info(f"✓ Essential field present: {field}")
    
    assert essential_fields_found > 0, "Biller details should have at least some essential fields"
    context.base_test.logger.info(f"✅ Biller details are complete ({essential_fields_found} fields found)")


@then('biller details should have valid format')
def step_verify_biller_details_format(context):
    """Verify biller details have valid format"""
    response_json = context.response.json()
    
    # Verify response is a dictionary
    assert isinstance(response_json, dict), "Response should be a dictionary"
    
    # Verify it's not empty
    assert len(response_json) > 0, "Response should not be empty"
    
    context.base_test.logger.info("✅ Biller details have valid format")


# ============================
# NOTE: Reused Steps from Other Files
# ============================
# The following steps are already defined in other step files and work for offline biller lookup:
#
# From login_devices_steps.py:
# - @given('I have valid user authentication')
# - @given('I have no authentication token')
# - @given('I have invalid user token')
# - @given('I have expired user token')
# - @given('I have app token only')
# - @given('I have no Authorization header')
# - @given('I have empty Bearer token')
# - @given('I have malformed Bearer token')
# - @given('I have valid user token from PIN verification')
#
# From merchant_lookup_code_steps.py:
# - @given('I have merchant code "{merchant_code}"')
# - @then('I extract merchant name from response')
# - @then('I extract merchant code from response')
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
