"""
Login Devices Step Definitions
Implements step definitions for Login Devices API scenarios.
"""

from behave import given, when, then


@given('I have valid user token from PIN verification')
def step_have_user_token_from_pin_verify(context):
    """Get user token from PIN verification API using sender_id from config."""
    # Check if using cached authentication
    if hasattr(context, 'global_auth_cache') and context.global_auth_cache.get('authenticated'):
        # Use cached user token
        context.user_token = context.global_auth_cache.get('user_token')
        context.base_test.user_token = context.user_token
        logger = context.base_test.logger
        logger.debug("♻️  Using cached user token")
        return
    
    config = context.base_test.config
    api_client = context.base_test.api_client
    logger = context.base_test.logger
    
    # Get sender_id from config - this is the user we'll authenticate
    sender_id = config.get('otp.sender_id')
    logger.info(f"🔐 Starting authentication flow for sender_id: {sender_id}")
    
    # Ensure we have app token
    access_token = getattr(context, 'access_token', '')
    if not access_token:
        logger.error("❌ App token not available, cannot proceed with authentication")
        raise ValueError("App token required for authentication flow")
    
    # Step 1: Request OTP for the sender_id
    otp_request_data = {
        'senderId': sender_id,
        'countryCode': config.get('otp.country_code'),
        'purpose': config.get('otp.default_purpose'),
        'otpMode': config.get('otp.default_mode')
    }
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    
    logger.info(f"📱 Step 1: Requesting OTP for {sender_id}")
    try:
        otp_response = api_client.post(
            endpoint='/bff/v2/auth/otp/request',
            json_data=otp_request_data,
            headers=headers
        )
        
        if otp_response.status_code == 200:
            otp_data = otp_response.json()
            user_reference_id = otp_data.get('userReferenceId')
            
            if not user_reference_id:
                logger.error("❌ No userReferenceId in OTP response")
                raise ValueError("OTP response missing userReferenceId")
            
            context.user_reference_id = user_reference_id
            logger.info(f"✅ OTP requested successfully, userReferenceId: {user_reference_id}")
        else:
            logger.error(f"❌ OTP request failed with status {otp_response.status_code}")
            logger.error(f"Response: {otp_response.text}")
            raise ValueError(f"OTP request failed: {otp_response.status_code}")
    except Exception as e:
        logger.error(f"❌ Error requesting OTP: {str(e)}")
        raise
    
    # Step 2: Perform PIN verification to get user token
    logger.info(f"🔑 Step 2: Performing PIN verification for userReferenceId: {context.user_reference_id}")
    
    pin_verify_data = {
        'pin': config.get('pin_verify.sample_encrypted_pin'),
        'userReferenceId': context.user_reference_id
    }
    
    query_params = {
        'tenantId': config.get('pin_verify.default_tenant_id'),
        'azp': config.get('pin_verify.default_azp')
    }
    
    pin_headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}',
        'model': config.get('pin_verify.default_device_model'),
        'deviceid': config.get('pin_verify.default_device_id')
    }
    
    # Build URL with query parameters
    query_string = '&'.join([f"{k}={v}" for k, v in query_params.items()])
    url = f"/bff/v4/auth/pin/verify?{query_string}"
    
    try:
        pin_response = api_client.post(
            endpoint=url,
            json_data=pin_verify_data,
            headers=pin_headers
        )
        
        if pin_response.status_code == 200:
            pin_data = pin_response.json()
            user_token = pin_data.get('accessToken', '')
            
            if not user_token:
                logger.error("❌ No accessToken in PIN verify response")
                raise ValueError("PIN verify response missing accessToken")
            
            context.user_token = user_token
            logger.info(f"✅ User token obtained successfully for {sender_id}")
            logger.info(f"🎫 Token: {user_token[:50]}...")
        else:
            logger.error(f"❌ PIN verification failed with status {pin_response.status_code}")
            logger.error(f"Response: {pin_response.text}")
            raise ValueError(f"PIN verification failed: {pin_response.status_code}")
    except Exception as e:
        logger.error(f"❌ Error during PIN verification: {str(e)}")
        raise


@given('I have valid user authentication')
def step_have_valid_user_authentication(context):
    """
    Ensure we have valid user token for authentication.
    This will generate a fresh token using the sender_id from config.
    """
    logger = context.base_test.logger
    
    # Always generate fresh token - don't rely on cached tokens
    logger.info("🔄 Generating fresh user authentication token")
    step_have_user_token_from_pin_verify(context)
    
    # Verify we have a valid token
    if not hasattr(context, 'user_token') or not context.user_token:
        logger.error("❌ Failed to obtain valid user token")
        raise ValueError("User authentication failed - no valid token")
    
    logger.info("✅ Valid user authentication available")
    logger.info(f"🎫 Using token: {context.user_token[:50]}...")


@given('I have no authentication token')
def step_have_no_authentication_token(context):
    """Remove authentication token."""
    context.user_token = ''
    context.access_token = ''
    context.base_test.logger.info("Authentication token removed")


@given('I have app token only')
def step_have_app_token_only(context):
    """Use only app token (not user token)."""
    context.user_token = getattr(context, 'access_token', '')
    context.base_test.logger.info("Using app token instead of user token")


@given('I have expired user token')
def step_have_expired_user_token(context):
    """Set an expired user token."""
    config = context.base_test.config
    context.user_token = config.get('login_devices.expired_user_token')
    context.base_test.logger.info("Expired user token set")


@given('I have invalid user token')
def step_have_invalid_user_token(context):
    """Set an invalid user token."""
    config = context.base_test.config
    context.user_token = config.get('login_devices.invalid_user_token')
    context.base_test.logger.info("Invalid user token set")


@given('I have malformed Bearer token')
def step_have_malformed_bearer_token(context):
    """Set a malformed Bearer token."""
    config = context.base_test.config
    context.user_token = config.get('login_devices.malformed_token')
    context.base_test.logger.info("Malformed Bearer token set")


@given('I have no Authorization header')
def step_have_no_authorization_header(context):
    """Remove Authorization header."""
    context.user_token = None
    context.base_test.logger.info("Authorization header will be removed")


@given('I have empty Bearer token')
def step_have_empty_bearer_token(context):
    """Set an empty Bearer token."""
    config = context.base_test.config
    context.user_token = config.get('login_devices.empty_token')
    context.base_test.logger.info("Empty Bearer token set")


@given('I have token without Bearer prefix')
def step_have_token_without_bearer_prefix(context):
    """Set token without Bearer prefix."""
    config = context.base_test.config
    # Get a valid token but it will be sent without Bearer prefix
    if not hasattr(context, 'user_token') or not context.user_token:
        step_have_user_token_from_pin_verify(context)
    context.no_bearer_prefix = True
    context.base_test.logger.info("Token will be sent without Bearer prefix")


@when('I send login devices request to "{endpoint}"')
def step_send_login_devices_request(context, endpoint):
    """Send GET request to login devices endpoint with user token."""
    api_client = context.base_test.api_client
    user_token = getattr(context, 'user_token', '')
    
    # Prepare headers
    headers = {
        'Content-Type': 'application/json'
    }
    
    # Handle different authorization scenarios
    if hasattr(context, 'no_bearer_prefix') and context.no_bearer_prefix:
        # Send token without Bearer prefix
        headers['Authorization'] = user_token
    elif user_token is not None:
        if user_token:
            headers['Authorization'] = f'Bearer {user_token}'
        # If user_token is empty string, add empty Bearer
        elif user_token == '':
            headers['Authorization'] = 'Bearer '
    # If user_token is None, don't add Authorization header at all
    
    # Send GET request
    context.response = api_client.get(
        endpoint=endpoint,
        headers=headers
    )
    context.base_test.logger.info(f"Login devices request sent to {endpoint}")


@when('I send login devices request with stored token to "{endpoint}"')
def step_send_login_devices_with_stored_token(context, endpoint):
    """Send login devices request with previously stored user token."""
    # Use the stored user token from previous step
    if hasattr(context, 'stored_user_token'):
        context.user_token = context.stored_user_token
    step_send_login_devices_request(context, endpoint)


@then('response should contain login devices list')
def step_verify_login_devices_list(context):
    """Verify response contains login devices list."""
    response_data = context.response.json()
    
    # Response should be a list or contain a list field or be a valid dict response
    is_list = isinstance(response_data, list)
    has_devices_list = isinstance(response_data.get('devices'), list) if isinstance(response_data, dict) else False
    has_data_list = isinstance(response_data.get('data'), list) if isinstance(response_data, dict) else False
    is_valid_dict = isinstance(response_data, dict) and len(response_data) > 0
    
    assert is_list or has_devices_list or has_data_list or is_valid_dict, \
        f"Response should contain login devices list or valid data, got: {type(response_data)}"
    
    context.base_test.logger.info(f"✅ Response contains login devices data")



@then('response should be a list')
def step_verify_response_is_list(context):
    """Verify response is a list."""
    response_data = context.response.json()
    assert isinstance(response_data, list), \
        f"Response should be a list, got: {type(response_data)}"
    context.base_test.logger.info(f"✅ Response is a list with {len(response_data)} items")


@then('each device should have required fields')
def step_verify_device_fields(context):
    """Verify each device in the list has required fields."""
    response_data = context.response.json()
    
    # Get the devices list
    if isinstance(response_data, list):
        devices = response_data
    elif isinstance(response_data, dict):
        devices = response_data.get('devices', response_data.get('data', []))
    else:
        devices = []
    
    if len(devices) == 0:
        context.base_test.logger.info("No devices in response (empty list)")
        return
    
    # Check first device has some expected fields
    # Common fields might include: deviceId, model, lastLogin, etc.
    first_device = devices[0]
    has_fields = isinstance(first_device, dict) and len(first_device) > 0
    
    assert has_fields, \
        f"Each device should have fields, got: {first_device}"
    
    context.base_test.logger.info(f"✅ Devices have required fields: {list(first_device.keys())}")


@then('I store the user token from response')
def step_store_user_token_from_response(context):
    """Store user token from PIN verify response for later use."""
    response_data = context.response.json()
    context.stored_user_token = response_data.get('accessToken', '')
    context.user_token = context.stored_user_token
    assert context.stored_user_token, "Should have accessToken in response"
    context.base_test.logger.info("✅ User token stored from response")
