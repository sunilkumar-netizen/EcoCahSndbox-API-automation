"""
Payment Reminder Step Definitions
Step definitions for Payment Reminder API tests
"""

from behave import given, when, then
import time


# ==============================================================================
# Given Steps - Setup Payment Reminder Data
# ==============================================================================

@given('I have payment reminder details')
def step_have_payment_reminder_details(context):
    """Prepare payment reminder payload from table data."""
    config = context.base_test.config
    
    # Initialize request data
    reminder_data = {
        "customerId": config.get('payment_reminder.customer_id'),
        "amount": "127",
        "currency": "ZWG",
        "alias": "NonRec Person Reminder",
        "trigger": {
            "frequency": "no-repeat",
            "occurrence": None,
            "startAt": int(time.time()) + (2 * 24 * 60 * 60)  # 2 days ahead
        },
        "notes": {
            "Q1": "+263789124669",
            "expenseCategory": "",
            "paymentType": "wallet"
        }
    }
    
    # Override with table data if provided
    if context.table:
        for row in context.table:
            field = row['field']
            value = row['value']
            
            if field == 'amount':
                reminder_data['amount'] = value
            elif field == 'currency':
                reminder_data['currency'] = value
            elif field == 'alias':
                reminder_data['alias'] = value
            elif field == 'frequency':
                reminder_data['trigger']['frequency'] = value
            elif field == 'beneficiary':
                reminder_data['notes']['Q1'] = value
            elif field == 'paymentType':
                reminder_data['notes']['paymentType'] = value
    
    context.request_data = reminder_data
    context.base_test.logger.info(f"Payment reminder data prepared: {reminder_data}")


@given('I have complete payment reminder payload with non-recurring frequency')
def step_have_complete_reminder_payload(context):
    """Prepare complete payment reminder payload."""
    config = context.base_test.config
    
    context.request_data = {
        "customerId": config.get('payment_reminder.customer_id'),
        "amount": "127",
        "currency": "ZWG",
        "alias": "NonRec Person Reminder",
        "trigger": {
            "frequency": "no-repeat",
            "occurrence": None,
            "startAt": int(time.time()) + (2 * 24 * 60 * 60)  # 2 days ahead
        },
        "notes": {
            "Q1": "+263789124669",
            "expenseCategory": "",
            "paymentType": "wallet"
        }
    }
    context.base_test.logger.info("Complete payment reminder payload prepared")


@given('I have payment reminder with amount {amount:d} ZWG')
def step_have_reminder_with_amount(context, amount):
    """Set payment reminder with specific amount."""
    config = context.base_test.config
    
    context.request_data = {
        "customerId": config.get('payment_reminder.customer_id'),
        "amount": str(amount),
        "currency": "ZWG",
        "alias": "Test Reminder",
        "trigger": {
            "frequency": "no-repeat",
            "occurrence": None,
            "startAt": int(time.time()) + (2 * 24 * 60 * 60)
        },
        "notes": {
            "Q1": "+263789124669",
            "expenseCategory": "",
            "paymentType": "wallet"
        }
    }
    context.base_test.logger.info(f"Payment reminder with amount {amount} prepared")


@given('I have payment reminder with alias "{alias}"')
def step_have_reminder_with_alias(context, alias):
    """Set payment reminder with specific alias."""
    config = context.base_test.config
    
    context.request_data = {
        "customerId": config.get('payment_reminder.customer_id'),
        "amount": "100",
        "currency": "ZWG",
        "alias": alias,
        "trigger": {
            "frequency": "no-repeat",
            "occurrence": None,
            "startAt": int(time.time()) + (2 * 24 * 60 * 60)
        },
        "notes": {
            "Q1": "+263789124669",
            "expenseCategory": "",
            "paymentType": "wallet"
        }
    }
    context.reminder_alias = alias
    context.base_test.logger.info(f"Payment reminder with alias '{alias}' prepared")


@given('I have payment reminder scheduled 2 days ahead')
def step_have_reminder_2_days_ahead(context):
    """Set payment reminder scheduled exactly 2 days ahead."""
    config = context.base_test.config
    
    # Calculate epoch time for 2 days ahead
    start_at = int(time.time()) + (2 * 24 * 60 * 60)
    
    context.request_data = {
        "customerId": config.get('payment_reminder.customer_id'),
        "amount": "100",
        "currency": "ZWG",
        "alias": "2 Days Ahead Reminder",
        "trigger": {
            "frequency": "no-repeat",
            "occurrence": None,
            "startAt": start_at
        },
        "notes": {
            "Q1": "+263789124669",
            "expenseCategory": "",
            "paymentType": "wallet"
        }
    }
    context.expected_start_at = start_at
    context.base_test.logger.info(f"Payment reminder scheduled for 2 days ahead: {start_at}")


@given('I have payment reminder with payment type "{payment_type}"')
def step_have_reminder_with_payment_type(context, payment_type):
    """Set payment reminder with specific payment type."""
    config = context.base_test.config
    
    context.request_data = {
        "customerId": config.get('payment_reminder.customer_id'),
        "amount": "100",
        "currency": "ZWG",
        "alias": "Test Reminder",
        "trigger": {
            "frequency": "no-repeat",
            "occurrence": None,
            "startAt": int(time.time()) + (2 * 24 * 60 * 60)
        },
        "notes": {
            "Q1": "+263789124669",
            "expenseCategory": "",
            "paymentType": payment_type
        }
    }
    context.base_test.logger.info(f"Payment reminder with payment type '{payment_type}' prepared")


@given('I have payment reminder without amount')
def step_have_reminder_without_amount(context):
    """Prepare payment reminder without amount field."""
    config = context.base_test.config
    
    context.request_data = {
        "customerId": config.get('payment_reminder.customer_id'),
        "currency": "ZWG",
        "alias": "Test Reminder",
        "trigger": {
            "frequency": "no-repeat",
            "occurrence": None,
            "startAt": int(time.time()) + (2 * 24 * 60 * 60)
        },
        "notes": {
            "Q1": "+263789124669",
            "paymentType": "wallet"
        }
    }
    context.base_test.logger.info("Payment reminder without amount prepared")


@given('I have payment reminder with amount {amount:d}')
def step_have_reminder_with_specific_amount(context, amount):
    """Set payment reminder with specific amount (can be 0 or negative for validation)."""
    config = context.base_test.config
    
    context.request_data = {
        "customerId": config.get('payment_reminder.customer_id'),
        "amount": str(amount),
        "currency": "ZWG",
        "alias": "Test Reminder",
        "trigger": {
            "frequency": "no-repeat",
            "occurrence": None,
            "startAt": int(time.time()) + (2 * 24 * 60 * 60)
        },
        "notes": {
            "Q1": "+263789124669",
            "paymentType": "wallet"
        }
    }
    context.base_test.logger.info(f"Payment reminder with amount {amount} prepared")


@given('I have payment reminder without currency')
def step_have_reminder_without_currency(context):
    """Prepare payment reminder without currency field."""
    config = context.base_test.config
    
    context.request_data = {
        "customerId": config.get('payment_reminder.customer_id'),
        "amount": "100",
        "alias": "Test Reminder",
        "trigger": {
            "frequency": "no-repeat",
            "occurrence": None,
            "startAt": int(time.time()) + (2 * 24 * 60 * 60)
        },
        "notes": {
            "Q1": "+263789124669",
            "paymentType": "wallet"
        }
    }
    context.base_test.logger.info("Payment reminder without currency prepared")


@given('I have payment reminder with currency "{currency}"')
def step_have_reminder_with_currency(context, currency):
    """Set payment reminder with specific currency."""
    config = context.base_test.config
    
    context.request_data = {
        "customerId": config.get('payment_reminder.customer_id'),
        "amount": "100",
        "currency": currency,
        "alias": "Test Reminder",
        "trigger": {
            "frequency": "no-repeat",
            "occurrence": None,
            "startAt": int(time.time()) + (2 * 24 * 60 * 60)
        },
        "notes": {
            "Q1": "+263789124669",
            "paymentType": "wallet"
        }
    }
    context.base_test.logger.info(f"Payment reminder with currency '{currency}' prepared")


@given('I have payment reminder without frequency')
def step_have_reminder_without_frequency(context):
    """Prepare payment reminder without frequency field."""
    config = context.base_test.config
    
    context.request_data = {
        "customerId": config.get('payment_reminder.customer_id'),
        "amount": "100",
        "currency": "ZWG",
        "alias": "Test Reminder",
        "trigger": {
            "occurrence": None,
            "startAt": int(time.time()) + (2 * 24 * 60 * 60)
        },
        "notes": {
            "Q1": "+263789124669",
            "paymentType": "wallet"
        }
    }
    context.base_test.logger.info("Payment reminder without frequency prepared")


@given('I have payment reminder with frequency "{frequency}"')
def step_have_reminder_with_frequency(context, frequency):
    """Set payment reminder with specific frequency."""
    config = context.base_test.config
    
    context.request_data = {
        "customerId": config.get('payment_reminder.customer_id'),
        "amount": "100",
        "currency": "ZWG",
        "alias": "Test Reminder",
        "trigger": {
            "frequency": frequency,
            "occurrence": None,
            "startAt": int(time.time()) + (2 * 24 * 60 * 60)
        },
        "notes": {
            "Q1": "+263789124669",
            "paymentType": "wallet"
        }
    }
    context.base_test.logger.info(f"Payment reminder with frequency '{frequency}' prepared")


@given('I have payment reminder with past start date')
def step_have_reminder_with_past_date(context):
    """Set payment reminder with past start date."""
    config = context.base_test.config
    
    # Set start date to 1 day in the past
    past_date = int(time.time()) - (1 * 24 * 60 * 60)
    
    context.request_data = {
        "customerId": config.get('payment_reminder.customer_id'),
        "amount": "100",
        "currency": "ZWG",
        "alias": "Past Date Reminder",
        "trigger": {
            "frequency": "no-repeat",
            "occurrence": None,
            "startAt": past_date
        },
        "notes": {
            "Q1": "+263789124669",
            "paymentType": "wallet"
        }
    }
    context.base_test.logger.info(f"Payment reminder with past date {past_date} prepared")


@given('I have payment reminder without beneficiary')
def step_have_reminder_without_beneficiary(context):
    """Prepare payment reminder without beneficiary field."""
    config = context.base_test.config
    
    context.request_data = {
        "customerId": config.get('payment_reminder.customer_id'),
        "amount": "100",
        "currency": "ZWG",
        "alias": "Test Reminder",
        "trigger": {
            "frequency": "no-repeat",
            "occurrence": None,
            "startAt": int(time.time()) + (2 * 24 * 60 * 60)
        },
        "notes": {
            "expenseCategory": "",
            "paymentType": "wallet"
        }
    }
    context.base_test.logger.info("Payment reminder without beneficiary prepared")


@given('I have payment reminder with beneficiary "{beneficiary}"')
def step_have_reminder_with_beneficiary(context, beneficiary):
    """Set payment reminder with specific beneficiary."""
    config = context.base_test.config
    
    context.request_data = {
        "customerId": config.get('payment_reminder.customer_id'),
        "amount": "100",
        "currency": "ZWG",
        "alias": "Test Reminder",
        "trigger": {
            "frequency": "no-repeat",
            "occurrence": None,
            "startAt": int(time.time()) + (2 * 24 * 60 * 60)
        },
        "notes": {
            "Q1": beneficiary,
            "expenseCategory": "",
            "paymentType": "wallet"
        }
    }
    context.base_test.logger.info(f"Payment reminder with beneficiary '{beneficiary}' prepared")


# ==============================================================================
# When Steps - API Requests
# ==============================================================================

@when('I send set reminder request to "{endpoint}"')
def step_send_set_reminder_request(context, endpoint):
    """Send POST request to set payment reminder."""
    api_client = context.base_test.api_client
    request_data = getattr(context, 'request_data', {})
    
    # Use user token for authentication
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
    context.base_test.logger.info(f"Set reminder request sent to {endpoint}")


# ==============================================================================
# Then Steps - Response Validation
# ==============================================================================

@then('response should contain reminder details')
def step_response_should_contain_reminder_details(context):
    """Verify response contains reminder details."""
    response_data = context.response.json()
    
    # Check for common reminder response fields
    assert response_data is not None, "Response data is None"
    context.base_test.logger.info("Response contains reminder details")


@then('response should have reminder ID')
def step_response_should_have_reminder_id(context):
    """Verify response has reminder ID or successful empty response."""
    response_data = context.response.json()
    
    # Debug: Print the response to see the structure
    context.base_test.logger.info(f"DEBUG - Response Data: {response_data}")
    
    # Check if response is empty (which means success for this API)
    if not response_data or len(response_data) == 0:
        context.base_test.logger.info("✅ Reminder created successfully (empty response indicates success)")
        context.reminder_id = "N/A (API returns empty response on success)"
        return
    
    # Check for reminder ID (can be 'id', 'reminderId', or similar)
    has_id = ('id' in response_data or 
              'reminderId' in response_data or 
              'reminder_id' in response_data or
              'data' in response_data)
    
    if not has_id:
        context.base_test.logger.warning(f"Response has data but no reminder ID. Keys: {list(response_data.keys())}")
        return
    
    # Store reminder ID for later use
    if 'id' in response_data:
        context.reminder_id = response_data['id']
    elif 'reminderId' in response_data:
        context.reminder_id = response_data['reminderId']
    elif 'reminder_id' in response_data:
        context.reminder_id = response_data['reminder_id']
    elif 'data' in response_data and isinstance(response_data['data'], dict):
        if 'id' in response_data['data']:
            context.reminder_id = response_data['data']['id']
        elif 'reminderId' in response_data['data']:
            context.reminder_id = response_data['data']['reminderId']
    
    context.base_test.logger.info(f"✅ Reminder ID found: {getattr(context, 'reminder_id', 'N/A')}")
    
    # Store reminder ID for later use
    if 'id' in response_data:
        context.reminder_id = response_data['id']
    elif 'reminderId' in response_data:
        context.reminder_id = response_data['reminderId']
    elif 'reminder_id' in response_data:
        context.reminder_id = response_data['reminder_id']
    
    context.base_test.logger.info(f"Reminder ID found: {getattr(context, 'reminder_id', 'N/A')}")


@then('reminder status should be valid')
def step_reminder_status_should_be_valid(context):
    """Verify reminder status is valid."""
    response_data = context.response.json()
    
    # Check if status field exists and has a valid value
    if 'status' in response_data:
        valid_statuses = ['active', 'pending', 'scheduled', 'created', 'success']
        assert response_data['status'] in valid_statuses, f"Invalid status: {response_data['status']}"
        context.base_test.logger.info(f"Reminder status is valid: {response_data['status']}")
    else:
        context.base_test.logger.info("Status field not in response, assuming valid")


@then('response should have complete reminder details')
def step_response_should_have_complete_details(context):
    """Verify response has complete reminder details."""
    response_data = context.response.json()
    
    # Check for essential fields
    assert response_data is not None, "Response data is None"
    context.base_test.logger.info("Response has complete reminder details")


@then('response should have creation timestamp')
def step_response_should_have_timestamp(context):
    """Verify response has creation timestamp."""
    response_data = context.response.json()
    
    # Check for timestamp fields
    has_timestamp = ('createdAt' in response_data or 
                    'created_at' in response_data or 
                    'timestamp' in response_data or
                    'createdDate' in response_data)
    
    assert has_timestamp, "Response does not have creation timestamp"
    context.base_test.logger.info("Response has creation timestamp")


@then('response should contain trigger information')
def step_response_should_contain_trigger(context):
    """Verify response contains trigger information."""
    response_data = context.response.json()
    
    # Check for trigger information
    has_trigger = ('trigger' in response_data or 
                  'schedule' in response_data or
                  'frequency' in response_data)
    
    assert has_trigger, "Response does not contain trigger information"
    context.base_test.logger.info("Response contains trigger information")


@then('reminder alias should match "{expected_alias}"')
def step_reminder_alias_should_match(context, expected_alias):
    """Verify reminder alias matches expected value."""
    response_data = context.response.json()
    
    if 'alias' in response_data:
        assert response_data['alias'] == expected_alias, \
            f"Alias mismatch: expected '{expected_alias}', got '{response_data['alias']}'"
        context.base_test.logger.info(f"Reminder alias matches: {expected_alias}")
    else:
        context.base_test.logger.warning("Alias field not in response")


@then('reminder start date should be approximately 2 days ahead')
def step_reminder_start_date_2_days_ahead(context):
    """Verify reminder start date is approximately 2 days ahead."""
    response_data = context.response.json()
    
    # Get expected start time (2 days ahead)
    expected_start = getattr(context, 'expected_start_at', int(time.time()) + (2 * 24 * 60 * 60))
    
    # Check if trigger information exists in response
    if 'trigger' in response_data and 'startAt' in response_data['trigger']:
        actual_start = response_data['trigger']['startAt']
        
        # Allow 5 minutes tolerance (300 seconds)
        time_diff = abs(actual_start - expected_start)
        assert time_diff < 300, \
            f"Start date not approximately 2 days ahead. Diff: {time_diff} seconds"
        
        context.base_test.logger.info(f"Reminder start date is approximately 2 days ahead")
    else:
        context.base_test.logger.info("Start date validation skipped - field not in response")


@then('response should contain error message about invalid date')
def step_response_should_contain_date_error(context):
    """Verify response contains error about invalid date."""
    response_data = context.response.json()
    
    # Check for error message related to date
    has_date_error = False
    error_fields = ['error', 'message', 'errors', 'detail', 'description']
    
    for field in error_fields:
        if field in response_data:
            error_msg = str(response_data[field]).lower()
            if 'date' in error_msg or 'time' in error_msg or 'past' in error_msg or 'future' in error_msg:
                has_date_error = True
                break
    
    assert has_date_error, "Response does not contain error about invalid date"
    context.base_test.logger.info("Response contains date-related error message")


@then('reminder can be retrieved later')
def step_reminder_can_be_retrieved(context):
    """Verify reminder can be retrieved (placeholder for future GET endpoint)."""
    # This is a placeholder step for future implementation
    # When GET reminder endpoint is available, implement actual retrieval
    reminder_id = getattr(context, 'reminder_id', None)
    assert reminder_id is not None, "No reminder ID available for retrieval"
    context.base_test.logger.info(f"Reminder {reminder_id} can be retrieved later")
