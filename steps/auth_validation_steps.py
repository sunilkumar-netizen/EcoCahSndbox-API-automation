"""
Authentication Flow Validation Step Definitions
Validates that global authentication cache is working correctly.
"""

from behave import given, when, then
from core.logger import Logger

logger = Logger.get_logger(__name__)


@then('I should have cached app token from global authentication')
def step_should_have_cached_app_token(context):
    """Verify that app token exists in global cache."""
    assert hasattr(context, 'global_auth_cache'), "Global auth cache not initialized"
    assert context.global_auth_cache.get('authenticated'), "Global authentication not completed"
    
    app_token = context.global_auth_cache.get('app_token')
    assert app_token is not None, "App token not found in global cache"
    assert len(app_token) > 0, "App token is empty"
    
    logger.info(f"✅ Cached app token found: {app_token[:50]}...")


@then('I should have cached user token from global authentication')
def step_should_have_cached_user_token(context):
    """Verify that user token exists in global cache."""
    assert hasattr(context, 'global_auth_cache'), "Global auth cache not initialized"
    assert context.global_auth_cache.get('authenticated'), "Global authentication not completed"
    
    user_token = context.global_auth_cache.get('user_token')
    assert user_token is not None, "User token not found in global cache"
    assert len(user_token) > 0, "User token is empty"
    
    logger.info(f"✅ Cached user token found: {user_token[:50]}...")


@then('cached tokens should be valid and not expired')
def step_cached_tokens_should_be_valid(context):
    """Verify that cached tokens are valid JWT tokens."""
    import base64
    import json
    
    app_token = context.global_auth_cache.get('app_token')
    user_token = context.global_auth_cache.get('user_token')
    
    # Basic JWT structure validation (should have 3 parts separated by dots)
    assert app_token.count('.') == 2, "App token is not a valid JWT format"
    assert user_token.count('.') == 2, "User token is not a valid JWT format"
    
    # Decode the payload (middle part) to check it's valid JSON
    try:
        app_payload = app_token.split('.')[1]
        # Add padding if needed
        app_payload += '=' * (4 - len(app_payload) % 4)
        app_decoded = base64.b64decode(app_payload)
        app_data = json.loads(app_decoded)
        logger.info(f"✅ App token payload decoded successfully")
        
        user_payload = user_token.split('.')[1]
        user_payload += '=' * (4 - len(user_payload) % 4)
        user_decoded = base64.b64decode(user_payload)
        user_data = json.loads(user_decoded)
        logger.info(f"✅ User token payload decoded successfully")
        
        # Check expiration (exp field should exist and be in the future)
        import time
        current_time = int(time.time())
        
        if 'exp' in app_data:
            assert app_data['exp'] > current_time, "App token has expired"
            logger.info(f"✅ App token is not expired")
        
        if 'exp' in user_data:
            assert user_data['exp'] > current_time, "User token has expired"
            logger.info(f"✅ User token is not expired")
            
    except Exception as e:
        raise AssertionError(f"Failed to validate token structure: {str(e)}")


@given('I have cached app token from global authentication')
def step_have_cached_app_token(context):
    """Get cached app token from global authentication."""
    assert hasattr(context, 'global_auth_cache'), "Global auth cache not initialized"
    assert context.global_auth_cache.get('authenticated'), "Global authentication not completed"
    
    context.test_app_token = context.global_auth_cache.get('app_token')
    assert context.test_app_token is not None, "App token not found in global cache"
    logger.info(f"✅ Using cached app token: {context.test_app_token[:50]}...")


@when('I use the cached app token for API request')
def step_use_cached_app_token(context):
    """Make a simple API request using cached app token."""
    api_client = context.base_test.api_client
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {context.test_app_token}'
    }
    
    # Make a lightweight request to validate token works
    # Using OTP request as a simple test (won't actually request OTP, just validates auth)
    config = context.base_test.config
    test_data = {
        'senderId': config.get('otp.sender_id'),
        'countryCode': config.get('otp.country_code'),
        'purpose': '0',
        'otpMode': '0'
    }
    
    try:
        response = api_client.post(
            endpoint='/bff/v2/auth/otp/request',
            json_data=test_data,
            headers=headers
        )
        context.token_validation_response = response
        logger.info(f"✅ API request with cached app token completed: {response.status_code}")
    except Exception as e:
        context.token_validation_error = str(e)
        logger.error(f"❌ API request with cached app token failed: {str(e)}")


@then('the cached app token should be accepted by the API')
def step_cached_app_token_should_be_accepted(context):
    """Verify that the API accepted the cached app token."""
    assert hasattr(context, 'token_validation_response'), "No response from token validation"
    
    # Token should be accepted (not 401 Unauthorized)
    response = context.token_validation_response
    assert response.status_code != 401, f"App token was rejected (401 Unauthorized)"
    
    # Even if we get 400 (because of duplicate OTP request), the token was accepted
    # 401 = token rejected, 400 = token accepted but request invalid
    if response.status_code in [200, 400]:
        logger.info(f"✅ Cached app token accepted by API (status: {response.status_code})")
    else:
        logger.warning(f"⚠️  Unexpected status code: {response.status_code}")


@given('I have cached user token from global authentication')
def step_have_cached_user_token(context):
    """Get cached user token from global authentication."""
    assert hasattr(context, 'global_auth_cache'), "Global auth cache not initialized"
    assert context.global_auth_cache.get('authenticated'), "Global authentication not completed"
    
    context.test_user_token = context.global_auth_cache.get('user_token')
    assert context.test_user_token is not None, "User token not found in global cache"
    logger.info(f"✅ Using cached user token: {context.test_user_token[:50]}...")


@when('I use the cached user token for API request')
def step_use_cached_user_token(context):
    """Make a simple API request using cached user token."""
    api_client = context.base_test.api_client
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {context.test_user_token}'
    }
    
    # Make a lightweight request to validate token works
    # Using login devices endpoint as a simple test
    try:
        response = api_client.get(
            endpoint='/bff/v1/auth/login-devices',
            headers=headers
        )
        context.token_validation_response = response
        logger.info(f"✅ API request with cached user token completed: {response.status_code}")
    except Exception as e:
        context.token_validation_error = str(e)
        logger.error(f"❌ API request with cached user token failed: {str(e)}")


@then('the cached user token should be accepted by the API')
def step_cached_user_token_should_be_accepted(context):
    """Verify that the API accepted the cached user token."""
    assert hasattr(context, 'token_validation_response'), "No response from token validation"
    
    # Token should be accepted (not 401 Unauthorized)
    response = context.token_validation_response
    assert response.status_code != 401, f"User token was rejected (401 Unauthorized)"
    
    # 200 or 4xx (except 401) means token was accepted
    if response.status_code in [200, 400, 404]:
        logger.info(f"✅ Cached user token accepted by API (status: {response.status_code})")
    else:
        logger.warning(f"⚠️  Unexpected status code: {response.status_code}")
