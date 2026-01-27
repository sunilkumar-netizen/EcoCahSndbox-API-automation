"""
OTP Verify Step Definitions
Implements step definitions for OTP verification API scenarios.
"""

from behave import given, when, then
import uuid


@given('I have valid OTP verification details')
def step_have_valid_otp_verification(context):
    """Prepare valid OTP verification data."""
    # First, request an OTP to get reference IDs
    api_client = context.base_test.api_client
    config = context.base_test.config
    access_token = getattr(context, 'access_token', '')
    
    # Step 1: Request OTP first
    otp_request_data = {
        'senderId': config.get('otp.sender_id', '771222221'),
        'countryCode': config.get('otp.country_code', '+263'),
        'purpose': '0',
        'otpMode': '0'
    }
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    
    otp_response = api_client.post(
        endpoint='/bff/v2/auth/otp/request',
        json_data=otp_request_data,
        headers=headers
    )
    
    if otp_response.status_code == 200:
        otp_data = otp_response.json()
        context.otp_reference_id = otp_data.get('otpReferenceId', str(uuid.uuid4()))
        context.user_reference_id = otp_data.get('userReferenceId', str(uuid.uuid4()))
        context.base_test.logger.info(f"✅ OTP requested, reference ID: {context.otp_reference_id[:20]}...")
    else:
        # Fallback to mock data if OTP request fails
        context.otp_reference_id = str(uuid.uuid4())
        context.user_reference_id = str(uuid.uuid4())
        context.base_test.logger.warning(f"⚠️ OTP request failed, using mock data")
    
    # Prepare verification data
    context.request_data = {
        'otpReferenceId': context.otp_reference_id,
        'otp': 123456,  # Default test OTP
        'userReferenceId': context.user_reference_id
    }
    context.base_test.logger.info("Valid OTP verification details prepared")


@given('I have OTP reference ID from previous request')
def step_have_otp_reference_from_request(context):
    """Get OTP reference ID from previous OTP request."""
    api_client = context.base_test.api_client
    access_token = getattr(context, 'access_token', '')
    config = context.base_test.config
    
    # Request OTP to get reference ID
    otp_request_data = {
        'senderId': config.get('otp.sender_id', '771222221'),
        'countryCode': config.get('otp.country_code', '+263'),
        'purpose': '0',
        'otpMode': '0'
    }
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    
    otp_response = api_client.post(
        endpoint='/bff/v2/auth/otp/request',
        json_data=otp_request_data,
        headers=headers
    )
    
    if otp_response.status_code == 200:
        otp_data = otp_response.json()
        context.otp_reference_id = otp_data.get('otpReferenceId', str(uuid.uuid4()))
        context.base_test.logger.info(f"✅ OTP reference ID obtained: {context.otp_reference_id[:20]}...")
    else:
        context.otp_reference_id = str(uuid.uuid4())
        context.base_test.logger.warning(f"⚠️ Using mock OTP reference ID")
    
    if not hasattr(context, 'request_data'):
        context.request_data = {}
    context.request_data['otpReferenceId'] = context.otp_reference_id


@given('I have valid OTP code "{otp_code}"')
def step_have_valid_otp_code(context, otp_code):
    """Set valid OTP code for verification."""
    if not hasattr(context, 'request_data'):
        context.request_data = {}
    context.request_data['otp'] = int(otp_code)
    context.base_test.logger.info(f"OTP code set: {otp_code}")


@given('I have user reference ID')
def step_have_user_reference_id(context):
    """Set user reference ID from previous request or generate new."""
    if not hasattr(context, 'user_reference_id'):
        # Get from previous OTP request or generate
        api_client = context.base_test.api_client
        access_token = getattr(context, 'access_token', '')
        config = context.base_test.config
        
        otp_request_data = {
            'senderId': config.get('otp.sender_id', '771222221'),
            'countryCode': config.get('otp.country_code', '+263'),
            'purpose': '0',
            'otpMode': '0'
        }
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        
        otp_response = api_client.post(
            endpoint='/bff/v2/auth/otp/request',
            json_data=otp_request_data,
            headers=headers
        )
        
        if otp_response.status_code == 200:
            otp_data = otp_response.json()
            context.user_reference_id = otp_data.get('userReferenceId', str(uuid.uuid4()))
        else:
            context.user_reference_id = str(uuid.uuid4())
    
    if not hasattr(context, 'request_data'):
        context.request_data = {}
    context.request_data['userReferenceId'] = context.user_reference_id
    context.base_test.logger.info(f"User reference ID set: {context.user_reference_id[:20]}...")


@given('I have invalid OTP code "{otp_code}"')
def step_have_invalid_otp_code(context, otp_code):
    """Set invalid OTP code for verification."""
    if not hasattr(context, 'request_data'):
        context.request_data = {}
    context.request_data['otp'] = int(otp_code)
    context.base_test.logger.info(f"Invalid OTP code set: {otp_code}")


@given('I have expired OTP reference ID')
def step_have_expired_otp_reference(context):
    """Set an expired/invalid OTP reference ID."""
    if not hasattr(context, 'request_data'):
        context.request_data = {}
    # Use a fixed UUID that represents an expired/non-existent OTP
    config = context.base_test.config
    context.request_data['otpReferenceId'] = config.get('otp_verify.expired_otp_reference_id')
    context.base_test.logger.info("Expired OTP reference ID set")


@given('I have OTP verification without reference ID')
def step_have_verification_without_reference(context):
    """Prepare OTP verification without reference ID."""
    context.request_data = {
        'otp': 123456,
        'userReferenceId': str(uuid.uuid4())
    }
    context.base_test.logger.info("OTP verification without reference ID prepared")


@given('I have OTP verification without OTP code')
def step_have_verification_without_otp_code(context):
    """Prepare OTP verification without OTP code."""
    if not hasattr(context, 'request_data'):
        context.request_data = {}
    # Remove OTP code if present
    context.request_data.pop('otp', None)
    context.base_test.logger.info("OTP verification without OTP code prepared")


@given('I have invalid user reference ID')
def step_have_invalid_user_reference(context):
    """Set invalid user reference ID."""
    if not hasattr(context, 'request_data'):
        context.request_data = {}
    config = context.base_test.config
    context.request_data['userReferenceId'] = config.get('otp_verify.invalid_user_reference_id')
    context.base_test.logger.info("Invalid user reference ID set")


@given('I have invalid authentication token')
def step_have_invalid_auth_token(context):
    """Set an invalid authentication token."""
    context.access_token = 'invalid_token_xyz123'
    context.base_test.logger.info("Invalid authentication token set")


@given('I have malformed OTP verification data')
def step_have_malformed_verification_data(context):
    """Prepare malformed OTP verification data."""
    context.request_data = {
        'invalid_field': 'test',
        'otp': 'not_a_number',  # OTP should be integer
        'otpReferenceId': 12345  # Should be string UUID
    }
    context.base_test.logger.info("Malformed OTP verification data prepared")


@when('I send OTP verification request to "{endpoint}"')
def step_send_otp_verification_request(context, endpoint):
    """Send OTP verification POST request with Bearer token."""
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
    context.base_test.logger.info(f"OTP verification request sent to {endpoint}")


@then('response should contain OTP verification status')
def step_verify_verification_status(context):
    """Verify response contains OTP verification status."""
    response_data = context.response.json()
    
    # Check for common status fields - API returns 'message' field
    has_status = any(key in response_data for key in ['message', 'status', 'verified', 'success', 'isValid'])
    
    assert has_status, f"Response should contain verification status field, got: {response_data}"
    context.base_test.logger.info(f"✅ Response contains OTP verification status: {response_data.get('message', 'verified')}")


@then('OTP verification should be successful')
def step_verify_otp_verification_success(context):
    """Verify OTP verification was successful."""
    response_data = context.response.json()
    
    # API returns 'message' field with success message: "Your OTP has been verified!"
    message = response_data.get('message', '')
    status = response_data.get('status')
    verified = response_data.get('verified')
    success = response_data.get('success')
    
    is_successful = (
        'verified' in message.lower() or
        status in ['success', 'verified', 'valid'] or
        verified is True or
        success is True
    )
    
    assert is_successful, f"OTP verification should be successful, got: {response_data}"
    context.base_test.logger.info(f"✅ OTP verification successful: {message}")


@then('response should contain verification status')
def step_verify_has_verification_status(context):
    """Verify response contains verification status field or authentication tokens."""
    response_data = context.response.json()
    
    assert isinstance(response_data, dict), "Response should be a JSON object"
    
    # Check for common verification status fields OR authentication tokens (for PIN Verify API)
    # PIN Verify API returns accessToken/refreshToken instead of simple status
    has_verification_field = any(
        key in response_data 
        for key in ['message', 'status', 'verified', 'verificationStatus', 'isVerified', 'success', 
                    'accessToken', 'refreshToken', 'username']  # Added for PIN Verify API
    )
    
    assert has_verification_field, f"Response should contain verification status or authentication data, got: {list(response_data.keys())}"
    
    # Log appropriate message based on response type
    if 'accessToken' in response_data:
        context.base_test.logger.info(f"✅ Response contains authentication tokens (PIN Verify API)")
    else:
        context.base_test.logger.info(f"✅ Response contains verification status: {response_data.get('message', 'verified')}")
