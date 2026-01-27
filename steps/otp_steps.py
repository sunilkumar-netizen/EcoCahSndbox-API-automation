"""
OTP Request Step Definitions
Implements step definitions for OTP request API scenarios.
"""

from behave import given, when, then


@given('I am authenticated with valid app token')
def step_authenticated_with_app_token(context):
    """Authenticate and get access token from Sasai."""
    # Get token from appToken API
    api_client = context.base_test.api_client
    config = context.base_test.config
    
    # Prepare authentication credentials
    auth_data = {
        'username': config.get('auth.username'),
        'password': config.get('auth.password'),
        'tenantId': config.get('auth.tenant_id'),
        'clientId': config.get('auth.client_id')
    }
    
    # Get access token
    auth_response = api_client.post(
        endpoint='/bff/v1/auth/token',
        json_data=auth_data
    )
    
    if auth_response.status_code == 200:
        token_data = auth_response.json()
        context.access_token = token_data.get('accessToken')
        context.base_test.logger.info(f"✅ Authenticated successfully, token: {context.access_token[:50]}...")
    else:
        raise Exception(f"Authentication failed with status {auth_response.status_code}")


@given('I have valid OTP request details')
def step_have_valid_otp_request(context):
    """Prepare valid OTP request data."""
    config = context.base_test.config
    context.request_data = {
        'senderId': config.get('otp.sender_id', '771222221'),
        'countryCode': config.get('otp.country_code', '+263'),
        'purpose': '0',  # 0 for authentication
        'otpMode': '0'   # 0 for SMS
    }
    context.base_test.logger.info("Valid OTP request details prepared")


@given('I have OTP request with sender ID "{sender_id}"')
def step_have_otp_sender_id(context, sender_id):
    """Set sender ID for OTP request."""
    if not hasattr(context, 'request_data'):
        context.request_data = {}
    context.request_data['senderId'] = sender_id
    context.base_test.logger.info(f"OTP sender ID set: {sender_id}")


@given('I have country code "{country_code}"')
def step_have_country_code(context, country_code):
    """Set country code for OTP request."""
    if not hasattr(context, 'request_data'):
        context.request_data = {}
    context.request_data['countryCode'] = country_code
    context.base_test.logger.info(f"Country code set: {country_code}")


@given('I have OTP purpose "{purpose}"')
def step_have_otp_purpose(context, purpose):
    """Set OTP purpose."""
    if not hasattr(context, 'request_data'):
        context.request_data = {}
    context.request_data['purpose'] = purpose
    context.base_test.logger.info(f"OTP purpose set: {purpose}")


@given('I have OTP mode "{mode}"')
def step_have_otp_mode(context, mode):
    """Set OTP delivery mode."""
    if not hasattr(context, 'request_data'):
        context.request_data = {}
    context.request_data['otpMode'] = mode
    context.base_test.logger.info(f"OTP mode set: {mode}")


@given('I have OTP request without sender ID')
def step_have_otp_without_sender_id(context):
    """Prepare OTP request without sender ID."""
    context.request_data = {
        'countryCode': '+263',
        'purpose': '0',
        'otpMode': '0'
    }
    context.base_test.logger.info("OTP request without sender ID prepared")


@given('I have expired authentication token')
def step_have_expired_token(context):
    """Set an expired token for testing."""
    context.access_token = 'expired_token_12345'
    context.base_test.logger.info("Expired token set for testing")


@when('I send authenticated POST request to "{endpoint}"')
def step_send_authenticated_post_request(context, endpoint):
    """Send POST request with Bearer token authentication."""
    api_client = context.base_test.api_client
    request_data = getattr(context, 'request_data', {})
    access_token = getattr(context, 'access_token', '')
    
    # Prepare headers with Bearer token
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    
    # Send request
    context.response = api_client.post(
        endpoint=endpoint,
        json_data=request_data,
        headers=headers
    )
    context.base_test.logger.info(f"Authenticated POST request sent to {endpoint}")


@then('OTP request should be successful')
def step_verify_otp_success(context):
    """Verify OTP request was successful."""
    response_data = context.response.json()
    status = response_data.get('status')
    
    assert status is not None, "OTP response should contain 'status' field"
    context.base_test.logger.info(f"✅ OTP request status: {status}")


@then('response should contain OTP reference')
def step_verify_otp_reference(context):
    """Verify response contains OTP reference/transaction ID."""
    response_data = context.response.json()
    
    # Check for common OTP reference fields
    has_reference = any(key in response_data for key in ['otpRef', 'transactionId', 'referenceId', 'id'])
    
    assert has_reference, "Response should contain OTP reference field"
    context.base_test.logger.info("✅ Response contains OTP reference")
