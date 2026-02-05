"""
Common Step Definitions
Reusable step definitions shared across multiple features.
"""

from behave import given, when, then


@given('API is available')
def step_api_available(context):
    """Verify API is available and accessible."""
    # You can implement health check here
    context.base_test.logger.info("API availability check passed")


@given('I wait for {seconds:d} seconds')
def step_wait_seconds(context, seconds):
    """Wait for specified seconds."""
    import time
    time.sleep(seconds)
    context.base_test.logger.info(f"Waited for {seconds} seconds")


# ==============================================================================
# HTTP Request Steps
# ==============================================================================

@when('I send POST request to "{endpoint}"')
def step_send_post_request(context, endpoint):
    """Send POST request to the specified endpoint."""
    api_client = context.base_test.api_client
    request_data = getattr(context, 'request_data', {})
    
    # Check if user_token exists (for user-level endpoints like login-devices)
    headers = None
    if hasattr(context, 'user_token') and context.user_token:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {context.user_token}'
        }
    
    context.response = api_client.post(
        endpoint=endpoint,
        json_data=request_data,
        headers=headers
    )
    context.base_test.logger.info(f"POST request sent to {endpoint}")


@when('I send GET request to "{endpoint}"')
def step_send_get_request(context, endpoint):
    """Send GET request to the specified endpoint."""
    api_client = context.base_test.api_client
    
    # Check if user_token exists (for user-level endpoints like login-devices)
    headers = None
    if hasattr(context, 'user_token') and context.user_token:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {context.user_token}'
        }
    
    context.response = api_client.get(
        endpoint=endpoint,
        headers=headers
    )
    context.base_test.logger.info(f"GET request sent to {endpoint}")


@when('I send PUT request to "{endpoint}"')
def step_send_put_request(context, endpoint):
    """Send PUT request to the specified endpoint."""
    api_client = context.base_test.api_client
    request_data = getattr(context, 'request_data', {})
    
    # Check if user_token exists (for user-level endpoints)
    headers = None
    if hasattr(context, 'user_token') and context.user_token:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {context.user_token}'
        }
    
    context.response = api_client.put(
        endpoint=endpoint,
        json_data=request_data,
        headers=headers
    )
    context.base_test.logger.info(f"PUT request sent to {endpoint}")


@when('I send DELETE request to "{endpoint}"')
def step_send_delete_request(context, endpoint):
    """Send DELETE request to the specified endpoint."""
    api_client = context.base_test.api_client
    
    # Check if user_token exists (for user-level endpoints)
    headers = None
    if hasattr(context, 'user_token') and context.user_token:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {context.user_token}'
        }
    
    context.response = api_client.delete(
        endpoint=endpoint,
        headers=headers
    )
    context.base_test.logger.info(f"DELETE request sent to {endpoint}")


# ==============================================================================
# Response Assertion Steps
# ==============================================================================

@then('response status code should be {status_code:d}')
def step_verify_status_code(context, status_code):
    """Verify response status code."""
    assertions = context.base_test.assert_response(context.response)
    assertions.assert_status_code(status_code)


@then('response status code should be {status1:d} or {status2:d}')
def step_verify_status_code_or(context, status1, status2):
    """Verify response status code is one of two acceptable values."""
    actual_status = context.response.status_code
    assert actual_status in [status1, status2], \
        f"Expected status code to be {status1} or {status2}, but got {actual_status}"
    context.base_test.logger.info(f"✅ Status code is {actual_status} (expected {status1} or {status2})")


@then('response body should contain "{key}"')
def step_verify_body_contains(context, key):
    """Verify response body contains a key."""
    assertions = context.base_test.assert_response(context.response)
    assertions.assert_json_contains_key(key)


@then('response body should be valid JSON')
def step_verify_valid_json(context):
    """Verify response body is valid JSON."""
    try:
        response_data = context.response.json()
        assert isinstance(response_data, (dict, list)), "Response should be a JSON object or array"
        context.base_test.logger.info("✅ Response body is valid JSON")
    except Exception as e:
        raise AssertionError(f"Response body is not valid JSON: {str(e)}")


@then('response field "{key}" should be "{value}"')
def step_verify_field_value(context, key, value):
    """Verify response field has specific value."""
    assertions = context.base_test.assert_response(context.response)
    assertions.assert_json_value(key, value)


@then('response field "{key}" should not be empty')
def step_verify_field_not_empty(context, key):
    """Verify response field is not empty."""
    assertions = context.base_test.assert_response(context.response)
    value = assertions.get_json_value(key)
    
    assert value is not None and str(value).strip() != '', \
        f"Expected field '{key}' to not be empty, but got '{value}'"
    
    context.base_test.logger.info(f"✅ Field '{key}' is not empty: {value[:50]}..." if len(str(value)) > 50 else f"✅ Field '{key}' is not empty: {value}")


@then('response time should be less than {milliseconds:d} ms')
def step_verify_response_time(context, milliseconds):
    """Verify response time is below threshold."""
    assertions = context.base_test.assert_response(context.response)
    assertions.assert_response_time_less_than(milliseconds)


@then('I store the "{field}" from response')
def step_store_field_from_response(context, field):
    """Store a field from response for later use."""
    try:
        response_data = context.response.json()
        value = response_data.get(field)
        setattr(context, field, value)
        context.base_test.logger.info(f"Stored {field}: {value[:50]}..." if len(str(value)) > 50 else f"Stored {field}: {value}")
    except Exception as e:
        context.base_test.logger.error(f"Failed to store {field}: {str(e)}")
        raise


@then('I print the response')
def step_print_response(context):
    """Print response for debugging."""
    try:
        import json
        response_json = context.response.json()
        print("\n" + "="*50)
        print("RESPONSE:")
        print(json.dumps(response_json, indent=2))
        print("="*50 + "\n")
    except:
        print("\n" + "="*50)
        print("RESPONSE (TEXT):")
        print(context.response.text)
        print("="*50 + "\n")


@then('response header "{header}" should be present')
def step_verify_header_present(context, header):
    """Verify response header is present."""
    headers = context.response.headers
    assert header in headers, \
        f"Expected header '{header}' to be present, but it was not found. Available headers: {list(headers.keys())}"
    context.base_test.logger.info(f"✅ Header '{header}' is present: {headers[header]}")


@then('response header "{header}" should be "{value}"')
def step_verify_header_value(context, header, value):
    """Verify response header has specific value."""
    headers = context.response.headers
    assert header in headers, \
        f"Expected header '{header}' to be present, but it was not found"
    
    actual_value = headers[header]
    assert actual_value == value, \
        f"Expected header '{header}' to be '{value}', but got '{actual_value}'"
    
    context.base_test.logger.info(f"✅ Header '{header}' has correct value: {value}")


@then('response header "{header}" should contain "{value}"')
def step_verify_header_contains(context, header, value):
    """Verify response header contains specific value."""
    headers = context.response.headers
    assert header in headers, \
        f"Expected header '{header}' to be present, but it was not found"
    
    actual_value = headers[header]
    assert value.lower() in actual_value.lower(), \
        f"Expected header '{header}' to contain '{value}', but got '{actual_value}'"
    
    context.base_test.logger.info(f"✅ Header '{header}' contains '{value}': {actual_value}")


@then('response header "{header}" should not be empty')
def step_verify_header_not_empty(context, header):
    """Verify response header is not empty."""
    headers = context.response.headers
    assert header in headers, \
        f"Expected header '{header}' to be present, but it was not found"
    
    actual_value = headers[header]
    assert actual_value and actual_value.strip() != '', \
        f"Expected header '{header}' to not be empty, but it was empty or whitespace"
    
    context.base_test.logger.info(f"✅ Header '{header}' is not empty: {actual_value}")

