"""
Step definitions for Payment Request Account Lookup API
Note: This file only contains unique steps for Payment Request.
Common assertion steps are reused from p2p_account_lookup_steps.py
"""

from behave import given, when
import logging

logger = logging.getLogger(__name__)


@given('I have payment request account lookup details')
def step_have_payment_request_account_lookup_details(context):
    """Prepare payment request account lookup data from table"""
    data = {}
    
    for row in context.table:
        field = row['field']
        value = row['value']
        
        # Map fields to request body
        if field == 'accountNumber':
            data['accountNumber'] = value
        elif field == 'origin':
            data['origin'] = value
    
    # Store in context
    context.payment_request_lookup_data = data
    context.account_lookup_data = data  # For compatibility with common steps
    logger.info(f"Payment request account lookup data prepared: {data}")


@given('I have payment request account lookup without account number')
def step_have_payment_request_lookup_without_account_number(context):
    """Prepare payment request lookup data without accountNumber field"""
    context.payment_request_lookup_data = {
        'origin': 'requestPay'
    }
    context.account_lookup_data = context.payment_request_lookup_data
    logger.info("Payment request lookup without account number prepared")


@given('I have payment request account lookup without origin')
def step_have_payment_request_lookup_without_origin(context):
    """Prepare payment request lookup data without origin field"""
    context.payment_request_lookup_data = {
        'accountNumber': '+263789124669'
    }
    context.account_lookup_data = context.payment_request_lookup_data
    logger.info("Payment request lookup without origin prepared")


@when('I send payment request account lookup to "{endpoint}"')
def step_send_payment_request_account_lookup(context, endpoint):
    """Send POST request to payment request account lookup endpoint"""
    # Get the payload
    payload = context.payment_request_lookup_data
    
    # Build headers with user token
    headers = {
        'Authorization': f"Bearer {context.user_token}",
        'Content-Type': 'application/json'
    }
    
    # Build full URL
    url = f"{context.config_loader.get('api.base_url')}{endpoint}"
    
    # Send POST request using requests directly (like P2P does)
    import requests
    import time
    
    try:
        logger.info(f"Sending POST request to {url}")
        logger.info(f"Request payload: {payload}")
        start_time = time.time()
        
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=30
        )
        
        context.response = response
        context.response_time = (time.time() - start_time) * 1000
        
        logger.info(f"Payment request account lookup sent to {endpoint}")
        logger.info(f"Response status: {response.status_code}")
        if response.text:
            logger.info(f"Response body: {response.text[:500]}")
            
    except Exception as e:
        logger.error(f"Request failed: {str(e)}")
        raise

