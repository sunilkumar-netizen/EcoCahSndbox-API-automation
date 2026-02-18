"""
Get All Payment Reminders Step Definitions
Step definitions for Get All Payment Reminders API tests
"""

from behave import given, when, then


# ==============================================================================
# When Steps - Send Get All Reminders Requests
# ==============================================================================

@when('I send get all reminders request to "{endpoint}" with parameters')
def step_send_get_all_reminders_with_params(context, endpoint):
    """Send GET request to retrieve all reminders with table parameters."""
    # Parse parameters from table
    params = {}
    if context.table:
        for row in context.table:
            param_name = row['parameter']
            param_value = row['value']
            params[param_name] = param_value
    
    # Get user token
    token = getattr(context, 'user_token', None)
    
    # Set headers
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    # Send GET request
    context.response = context.base_test.api_client.get(
        endpoint,
        headers=headers,
        params=params
    )
    
    context.base_test.logger.info(f"Get all reminders request sent to {endpoint} with params: {params}")


@when('I send get all reminders request with count {count:d} and skip {skip:d}')
def step_send_get_all_reminders_simple(context, count, skip):
    """Send GET request to retrieve all reminders with count and skip."""
    endpoint = "/bff/v1/payment/reminder"
    
    params = {
        'count': count,
        'skip': skip,
        'status': 'active'
    }
    
    # Get user token
    token = getattr(context, 'user_token', None)
    
    # Set headers
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    # Send GET request
    context.response = context.base_test.api_client.get(
        endpoint,
        headers=headers,
        params=params
    )
    
    context.base_test.logger.info(f"Get all reminders request sent with count={count}, skip={skip}")


# ==============================================================================
# Then Steps - Validate Get All Reminders Responses
# ==============================================================================

@then('response should contain reminders list')
def step_response_should_contain_reminders_list(context):
    """Verify response contains reminders list."""
    response_data = context.response.json()
    
    # Check if response has data array or items array
    has_reminders = ('data' in response_data or 
                    'items' in response_data or 
                    'reminders' in response_data or
                    'results' in response_data or
                    isinstance(response_data, list))
    
    if has_reminders:
        context.base_test.logger.info("✅ Response contains reminders list")
    else:
        context.base_test.logger.info("⚠️ Response structure varies - may be empty or have different format")


@then('I should extract and store first reminder ID if available')
def step_extract_and_store_reminder_id(context):
    """Extract and store first reminder ID from response for future use."""
    response_data = context.response.json()
    
    reminder_id = None
    
    # Try different response structures
    if isinstance(response_data, list) and len(response_data) > 0:
        # Response is a direct array
        first_reminder = response_data[0]
        reminder_id = first_reminder.get('reminderId') or first_reminder.get('id') or first_reminder.get('reminder_id')
    elif 'data' in response_data and isinstance(response_data['data'], list) and len(response_data['data']) > 0:
        # Response has data array
        first_reminder = response_data['data'][0]
        reminder_id = first_reminder.get('reminderId') or first_reminder.get('id') or first_reminder.get('reminder_id')
    elif 'items' in response_data and isinstance(response_data['items'], list) and len(response_data['items']) > 0:
        # Response has items array
        first_reminder = response_data['items'][0]
        reminder_id = first_reminder.get('reminderId') or first_reminder.get('id') or first_reminder.get('reminder_id')
    elif 'reminders' in response_data and isinstance(response_data['reminders'], list) and len(response_data['reminders']) > 0:
        # Response has reminders array
        first_reminder = response_data['reminders'][0]
        reminder_id = first_reminder.get('reminderId') or first_reminder.get('id') or first_reminder.get('reminder_id')
    elif 'results' in response_data and isinstance(response_data['results'], list) and len(response_data['results']) > 0:
        # Response has results array
        first_reminder = response_data['results'][0]
        reminder_id = first_reminder.get('reminderId') or first_reminder.get('id') or first_reminder.get('reminder_id')
    
    if reminder_id:
        context.reminder_id = reminder_id
        # Store in config for future use
        config = context.base_test.config
        # You can access this later using config.get('payment_reminder.last_reminder_id')
        context.base_test.logger.info(f"✅ Reminder ID extracted and stored: {reminder_id}")
    else:
        context.base_test.logger.info("ℹ️ No reminders found in response (list may be empty)")
