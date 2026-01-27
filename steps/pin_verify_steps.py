"""
PIN Verify Step Definitions
Implements step definitions for PIN verification API scenarios.
"""

from behave import given, when, then
import uuid


@given('I have valid PIN verification details')
def step_have_valid_pin_verification(context):
    """Prepare valid PIN verification data."""
    config = context.base_test.config
    
    # Get user reference ID from OTP verification or use default
    if not hasattr(context, 'user_reference_id'):
        # Try to get from OTP API first
        api_client = context.base_test.api_client
        access_token = getattr(context, 'access_token', '')
        config = context.base_test.config
        
        otp_request_data = {
            'senderId': config.get('otp.sender_id'),
            'countryCode': config.get('otp.country_code'),
            'purpose': config.get('otp.default_purpose'),
            'otpMode': config.get('otp.default_mode')
        }
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        
        try:
            otp_response = api_client.post(
                endpoint='/bff/v2/auth/otp/request',
                json_data=otp_request_data,
                headers=headers
            )
            
            if otp_response.status_code == 200:
                otp_data = otp_response.json()
                context.user_reference_id = otp_data.get('userReferenceId', 
                    config.get('pin_verify.default_user_reference_id'))
            else:
                context.user_reference_id = config.get('pin_verify.default_user_reference_id')
        except:
            context.user_reference_id = config.get('pin_verify.default_user_reference_id')
    
    # Prepare PIN verification data
    context.request_data = {
        'pin': config.get('pin_verify.sample_encrypted_pin'),
        'userReferenceId': context.user_reference_id
    }
    
    # Set default query params
    context.query_params = {
        'tenantId': config.get('pin_verify.default_tenant_id'),
        'azp': config.get('pin_verify.default_azp')
    }
    
    # Set default custom headers
    context.custom_headers = {
        'model': config.get('pin_verify.default_device_model')
    }
    
    context.base_test.logger.info("Valid PIN verification details prepared")


@given('I have encrypted PIN')
def step_have_encrypted_pin(context):
    """Set encrypted PIN for verification."""
    if not hasattr(context, 'request_data'):
        context.request_data = {}
    
    config = context.base_test.config
    context.request_data['pin'] = config.get('pin_verify.sample_encrypted_pin')
    context.base_test.logger.info("Encrypted PIN set")


@given('I have user reference ID for PIN')
def step_have_user_reference_for_pin(context):
    """Set user reference ID for PIN verification."""
    if not hasattr(context, 'request_data'):
        context.request_data = {}
    
    config = context.base_test.config
    # Try to get from previous OTP request or use default
    if not hasattr(context, 'user_reference_id'):
        context.user_reference_id = config.get('pin_verify.default_user_reference_id')
    
    context.request_data['userReferenceId'] = context.user_reference_id
    context.base_test.logger.info(f"User reference ID set for PIN: {context.user_reference_id[:20]}...")


@given('I have tenant ID "{tenant_id}"')
def step_have_tenant_id(context, tenant_id):
    """Set tenant ID for query parameters."""
    if not hasattr(context, 'query_params'):
        context.query_params = {}
    context.query_params['tenantId'] = tenant_id
    context.base_test.logger.info(f"Tenant ID set: {tenant_id}")


@given('I have azp "{azp}"')
def step_have_azp(context, azp):
    """Set azp (authorized party) for query parameters."""
    if not hasattr(context, 'query_params'):
        context.query_params = {}
    context.query_params['azp'] = azp
    context.base_test.logger.info(f"AZP set: {azp}")


@given('I have invalid tenant ID "{tenant_id}"')
def step_have_invalid_tenant_id(context, tenant_id):
    """Set invalid tenant ID for testing."""
    if not hasattr(context, 'query_params'):
        context.query_params = {}
    context.query_params['tenantId'] = tenant_id
    context.base_test.logger.info(f"Invalid tenant ID set: {tenant_id}")


@given('I have invalid encrypted PIN')
def step_have_invalid_encrypted_pin(context):
    """Set invalid encrypted PIN."""
    if not hasattr(context, 'request_data'):
        context.request_data = {}
    config = context.base_test.config
    context.request_data['pin'] = config.get('pin_verify.invalid_encrypted_pin')
    context.base_test.logger.info("Invalid encrypted PIN set")


@given('I have empty PIN')
def step_have_empty_pin(context):
    """Set empty PIN."""
    if not hasattr(context, 'request_data'):
        context.request_data = {}
    config = context.base_test.config
    context.request_data['pin'] = config.get('pin_verify.empty_pin')
    context.base_test.logger.info("Empty PIN set")


@given('I have PIN verification without PIN')
def step_have_pin_verification_without_pin(context):
    """Prepare PIN verification without PIN field."""
    config = context.base_test.config
    context.request_data = {
        'userReferenceId': config.get('pin_verify.default_user_reference_id')
    }
    context.base_test.logger.info("PIN verification without PIN prepared")


@given('I have PIN verification without user reference ID')
def step_have_pin_verification_without_user_ref(context):
    """Prepare PIN verification without user reference ID."""
    if not hasattr(context, 'request_data'):
        context.request_data = {}
    # Remove userReferenceId if present
    context.request_data.pop('userReferenceId', None)
    context.base_test.logger.info("PIN verification without user reference ID prepared")


@given('I have invalid user reference ID for PIN')
def step_have_invalid_user_reference_for_pin(context):
    """Set invalid user reference ID."""
    if not hasattr(context, 'request_data'):
        context.request_data = {}
    config = context.base_test.config
    context.request_data['userReferenceId'] = config.get('pin_verify.invalid_user_reference_id')
    context.base_test.logger.info("Invalid user reference ID set")


@given('I have invalid device model "{model}"')
def step_have_invalid_device_model(context, model):
    """Set invalid device model header."""
    if not hasattr(context, 'custom_headers'):
        context.custom_headers = {}
    context.custom_headers['model'] = model
    context.base_test.logger.info(f"Invalid device model set: {model}")


@given('I have malformed PIN verification data')
def step_have_malformed_pin_data(context):
    """Prepare malformed PIN verification data."""
    config = context.base_test.config
    context.request_data = {
        'invalid_field': config.get('pin_verify.malformed_test_string'),
        'pin': config.get('pin_verify.malformed_pin'),  # PIN should be string
        'userReferenceId': config.get('pin_verify.malformed_user_ref')  # Should be string UUID
    }
    context.base_test.logger.info("Malformed PIN verification data prepared")


@when('I send PIN verification request to "{endpoint}"')
def step_send_pin_verification_request(context, endpoint):
    """Send PIN verification POST request with Bearer token and custom headers."""
    api_client = context.base_test.api_client
    request_data = getattr(context, 'request_data', {})
    access_token = getattr(context, 'access_token', '')
    query_params = getattr(context, 'query_params', {})
    custom_headers = getattr(context, 'custom_headers', {})
    
    # Prepare headers with Bearer token and custom headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    
    # Add custom headers (like model)
    headers.update(custom_headers)
    
    # Build URL with query parameters
    url = endpoint
    if query_params:
        query_string = '&'.join([f"{k}={v}" for k, v in query_params.items()])
        url = f"{endpoint}?{query_string}"
    
    # Send request
    context.response = api_client.post(
        endpoint=url,
        json_data=request_data,
        headers=headers
    )
    context.base_test.logger.info(f"PIN verification request sent to {url}")


@when('I send PIN verification request with query params to "{endpoint}"')
def step_send_pin_verification_with_query_params(context, endpoint):
    """Send PIN verification request with query parameters."""
    step_send_pin_verification_request(context, endpoint)


@when('I send PIN verification request without model header to "{endpoint}"')
def step_send_pin_verification_without_model(context, endpoint):
    """Send PIN verification request without model header."""
    api_client = context.base_test.api_client
    request_data = getattr(context, 'request_data', {})
    access_token = getattr(context, 'access_token', '')
    query_params = getattr(context, 'query_params', {})
    
    # Prepare headers WITHOUT model header
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    
    # Build URL with query parameters
    url = endpoint
    if query_params:
        query_string = '&'.join([f"{k}={v}" for k, v in query_params.items()])
        url = f"{endpoint}?{query_string}"
    
    # Send request
    context.response = api_client.post(
        endpoint=url,
        json_data=request_data,
        headers=headers
    )
    context.base_test.logger.info(f"PIN verification request sent without model header to {url}")


@then('response should contain PIN verification status')
def step_verify_pin_verification_status(context):
    """Verify response contains PIN verification status or authentication tokens."""
    response_data = context.response.json()
    
    # PIN Verify API returns authentication tokens (like App Token API)
    # Check for status fields OR authentication tokens
    has_status = any(key in response_data for key in ['message', 'status', 'verified', 'success', 'isValid', 'pinVerified', 'accessToken'])
    
    assert has_status, f"Response should contain verification status or accessToken, got: {response_data}"
    context.base_test.logger.info(f"✅ Response contains PIN verification status/tokens: {list(response_data.keys())}")


@then('PIN verification should be successful')
def step_verify_pin_verification_success(context):
    """Verify PIN verification was successful."""
    response_data = context.response.json()
    
    # PIN Verify API returns accessToken when PIN is verified successfully (like App Token API)
    # Check for success indicators OR authentication tokens
    message = response_data.get('message', '')
    status = response_data.get('status')
    verified = response_data.get('verified')
    success = response_data.get('success')
    pin_verified = response_data.get('pinVerified')
    has_access_token = 'accessToken' in response_data
    
    is_successful = (
        'verified' in message.lower() or
        'success' in message.lower() or
        status in ['success', 'verified', 'valid'] or
        verified is True or
        success is True or
        pin_verified is True or
        has_access_token  # accessToken indicates successful PIN verification
    )
    
    assert is_successful, f"PIN verification should be successful (with accessToken or status), got: {response_data}"
    context.base_test.logger.info(f"✅ PIN verification successful (received {'accessToken' if has_access_token else 'status'})")
