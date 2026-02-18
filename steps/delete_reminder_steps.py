"""
Step definitions for Delete Payment Reminder API
Endpoint: DELETE /bff/v1/payment/reminder/{reminderId}
"""

from behave import given, when, then
import logging

logger = logging.getLogger(__name__)


@given('I have a valid reminder ID from config')
def step_have_valid_reminder_id_from_config(context):
    """
    Load reminder ID from config or use previously stored reminder ID
    """
    # First check if we have a reminder ID stored in context from previous steps
    if hasattr(context, 'reminder_id') and context.reminder_id:
        logger.info(f"Using reminder ID from context: {context.reminder_id}")
        return
    
    # Otherwise, try to get from config
    config = context.config_loader
    reminder_id = config.get('payment_reminder.reminder_id')
    
    if reminder_id:
        context.reminder_id = reminder_id
        logger.info(f"Loaded reminder ID from config: {reminder_id}")
    else:
        # Use a default test reminder ID if not available in config
        context.reminder_id = "698c43199d9bea2a8e44ef6d"
        logger.warning(f"No reminder ID in config, using default: {context.reminder_id}")


@when('I send delete reminder request to "{endpoint}"')
def step_send_delete_reminder_request(context, endpoint):
    """
    Send DELETE request to delete a payment reminder
    Supports path parameter replacement with {reminderId}
    Priority: 1) Context reminder_id (from Get All Reminders), 2) Config, 3) Default
    """
    # Replace {reminderId} placeholder with actual reminder ID
    if '{reminderId}' in endpoint:
        # Priority 1: Check if reminder ID is already stored in context from previous steps (e.g., Get All Reminders)
        if hasattr(context, 'reminder_id') and context.reminder_id:
            endpoint = endpoint.replace('{reminderId}', context.reminder_id)
            context.base_test.logger.info(f"✅ Using reminder ID from context: {context.reminder_id}")
        else:
            # Priority 2: Try to get from config
            config = context.config_loader
            reminder_id = config.get('payment_reminder.reminder_id')
            
            if reminder_id:
                context.reminder_id = reminder_id
                endpoint = endpoint.replace('{reminderId}', reminder_id)
                context.base_test.logger.info(f"✅ Using reminder ID from config: {reminder_id}")
            else:
                # Priority 3: Use default test reminder ID
                context.reminder_id = "698c43199d9bea2a8e44ef6d"
                endpoint = endpoint.replace('{reminderId}', context.reminder_id)
                context.base_test.logger.warning(f"⚠️  No reminder ID found, using default: {context.reminder_id}")
    
    # Get API client and user token
    api_client = context.base_test.api_client
    user_token = context.user_token
    
    # Prepare headers with user token (Bearer authentication)
    headers = {
        'Authorization': f'Bearer {user_token}',
        'Content-Type': 'application/json'
    }
    
    context.base_test.logger.info(f"Sending DELETE request to {endpoint}")
    
    # Send DELETE request (no body required)
    response = api_client.delete(
        endpoint=endpoint,
        headers=headers
    )
    
    context.response = response
    context.base_test.logger.info(f"Delete reminder request sent to {endpoint}")
    context.base_test.logger.info(f"Response status: {response.status_code}")
    
    # Log response body if present
    if response.text:
        context.base_test.logger.info(f"Response body: {response.text[:200]}")  # First 200 chars


@then('response status code should be {code1:d} or {code2:d}')
def step_response_status_should_be_either(context, code1, code2):
    """
    Verify response status code is one of two expected codes
    Useful for APIs that can return multiple success codes (e.g., 200 or 204)
    """
    actual_status = context.response.status_code
    
    if actual_status not in [code1, code2]:
        error_msg = f"Expected status code {code1} or {code2}, but got {actual_status}"
        logger.error(error_msg)
        
        # Log response details for debugging
        if context.response.text:
            logger.error(f"Response body: {context.response.text}")
        
        raise AssertionError(error_msg)
    
    logger.info(f"✅ Response status code {actual_status} is valid (expected {code1} or {code2})")


@then('response status code should be {code1:d}, {code2:d} or {code3:d}')
def step_response_status_should_be_one_of_three(context, code1, code2, code3):
    """
    Verify response status code is one of three expected codes
    Useful for edge cases with multiple possible responses
    """
    actual_status = context.response.status_code
    
    if actual_status not in [code1, code2, code3]:
        error_msg = f"Expected status code {code1}, {code2} or {code3}, but got {actual_status}"
        logger.error(error_msg)
        
        # Log response details for debugging
        if context.response.text:
            logger.error(f"Response body: {context.response.text}")
        
        raise AssertionError(error_msg)
    
    logger.info(f"✅ Response status code {actual_status} is valid (expected {code1}, {code2} or {code3})")

