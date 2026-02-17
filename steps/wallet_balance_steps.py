"""
Step definitions for Wallet Balance API tests
Endpoint: POST /bff/v1/wallet/balance
"""

from behave import given, when, then
from core.api_client import APIClient
import json
import logging
import uuid

logger = logging.getLogger(__name__)


@given('I have wallet balance request payload with currency "{currency}"')
def step_have_wallet_balance_payload_with_currency(context, currency):
    """Prepare wallet balance request payload with specified currency"""
    # Get instrument token from payment options if available
    instrument_token = getattr(context, 'instrument_token', None)
    
    # If no instrument token from payment options, try to get it dynamically
    if not instrument_token:
        # First, get payment options to retrieve valid instrument token
        api_client = APIClient(context.base_test.config)
        headers = {
            'Authorization': f'Bearer {context.user_token}',
            'requestId': str(uuid.uuid4())
        }
        params = {'serviceType': 'ZWAllPaymentOptions'}
        
        try:
            payment_options_response = api_client.get('/bff/v1/payment/options', params=params, headers=headers)
            if payment_options_response.status_code == 200:
                po_data = payment_options_response.json()
                # Extract instrument token from the first wallet instrument
                if 'items' in po_data and len(po_data['items']) > 0:
                    items = po_data['items']
                    for item in items:
                        if 'instruments' in item and len(item['instruments']) > 0:
                            for instrument in item['instruments']:
                                # Match currency
                                if 'currency' in instrument:
                                    currencies = instrument['currency']
                                    if isinstance(currencies, list):
                                        currency_codes = [c.get('key') for c in currencies if isinstance(c, dict)]
                                        if currency in currency_codes:
                                            instrument_token = instrument.get('instrumentToken')
                                            print(f"\n✓ Retrieved instrument token for {currency}: {instrument_token}")
                                            break
                            if instrument_token:
                                break
        except Exception as e:
            logger.warning(f"Failed to get instrument token from payment options: {e}")
    
    # Fallback to hardcoded token if still not found
    if not instrument_token:
        instrument_token = "52ecc218-f1c8-4a70-821e-614e7b2bbf67"
        print(f"\n⚠️  Using fallback instrument token")
    
    # Default encrypted PIN (this should match the test user's encrypted PIN)
    encrypted_pin = "Z9jXnPVARjr+J5ZHBlMIw93wMCzEmuXv6jpbl7dXQ7PcHcEiiywjyrO3DqSLGT/g1XyKTj7AzYOdgRfSoGbAOBeBefi5dhK+KIvEu+2e+pxHbj4vcKdJEZEwuv0XlnT7XWCioCAkZdqn+edZZIyAYxa4yux7fnt+Ek2HRNT1ic0Rh46buOoXngjxlu3VIFRh1KvVB7DcnjdtOH9u9qMEDgIFLNKiB3YOHwzYNlu+YbcrToH01xGJEUZ5dWy+Hc9pTOB8dQ+lvGsHZ+u4dzkCf09avVWlP9ljnEgefNPDVtoe51Z1abFVm2Bptdw8vW2DsuqP5HpH8rROu6vr7W9mjg=="
    
    context.wallet_balance_payload = {
        "country": "ZW",
        "currency": currency,
        "providerName": "ecocash",
        "providerCode": "ecocash",
        "pin": encrypted_pin,
        "instrumentToken": instrument_token
    }
    logger.info(f"Wallet balance payload prepared for currency: {currency}")
    print(f"\n✓ Wallet balance payload prepared for {currency}")


@given('I have wallet balance request payload with invalid currency "{currency}"')
def step_have_wallet_balance_payload_with_invalid_currency(context, currency):
    """Prepare wallet balance request payload with invalid currency"""
    encrypted_pin = "Z9jXnPVARjr+J5ZHBlMIw93wMCzEmuXv6jpbl7dXQ7PcHcEiiywjyrO3DqSLGT/g1XyKTj7AzYOdgRfSoGbAOBeBefi5dhK+KIvEu+2e+pxHbj4vcKdJEZEwuv0XlnT7XWCioCAkZdqn+edZZIyAYxa4yux7fnt+Ek2HRNT1ic0Rh46buOoXngjxlu3VIFRh1KvVB7DcnjdtOH9u9qMEDgIFLNKiB3YOHwzYNlu+YbcrToH01xGJEUZ5dWy+Hc9pTOB8dQ+lvGsHZ+u4dzkCf09avVWlP9ljnEgefNPDVtoe51Z1abFVm2Bptdw8vW2DsuqP5HpH8rROu6vr7W9mjg=="
    instrument_token = "52ecc218-f1c8-4a70-821e-614e7b2bbf67"
    
    context.wallet_balance_payload = {
        "country": "ZW",
        "currency": currency,
        "providerName": "ecocash",
        "providerCode": "ecocash",
        "pin": encrypted_pin,
        "instrumentToken": instrument_token
    }
    logger.info(f"Wallet balance payload prepared with invalid currency: {currency}")


@given('I have incomplete wallet balance request payload')
def step_have_incomplete_wallet_balance_payload(context):
    """Prepare incomplete wallet balance request payload (missing required fields)"""
    context.wallet_balance_payload = {
        "country": "ZW",
        "currency": "ZWG"
        # Missing: providerName, providerCode, pin, instrumentToken
    }
    logger.info("Incomplete wallet balance payload prepared")


@given('I have wallet balance request payload with invalid instrument token')
def step_have_wallet_balance_payload_with_invalid_token(context):
    """Prepare wallet balance request payload with invalid instrument token"""
    encrypted_pin = "Z9jXnPVARjr+J5ZHBlMIw93wMCzEmuXv6jpbl7dXQ7PcHcEiiywjyrO3DqSLGT/g1XyKTj7AzYOdgRfSoGbAOBeBefi5dhK+KIvEu+2e+pxHbj4vcKdJEZEwuv0XlnT7XWCioCAkZdqn+edZZIyAYxa4yux7fnt+Ek2HRNT1ic0Rh46buOoXngjxlu3VIFRh1KvVB7DcnjdtOH9u9qMEDgIFLNKiB3YOHwzYNlu+YbcrToH01xGJEUZ5dWy+Hc9pTOB8dQ+lvGsHZ+u4dzkCf09avVWlP9ljnEgefNPDVtoe51Z1abFVm2Bptdw8vW2DsuqP5HpH8rROu6vr7W9mjg=="
    
    context.wallet_balance_payload = {
        "country": "ZW",
        "currency": "ZWG",
        "providerName": "ecocash",
        "providerCode": "ecocash",
        "pin": encrypted_pin,
        "instrumentToken": "invalid-token-" + str(uuid.uuid4())
    }
    logger.info("Wallet balance payload prepared with invalid instrument token")


@when('I send wallet balance request to "{endpoint}"')
def step_send_wallet_balance_request(context, endpoint):
    """Send POST request to wallet balance endpoint with authentication"""
    print(f"\nSending POST request to {endpoint}")
    print(f"Full payload: {json.dumps(context.wallet_balance_payload, indent=2)}")
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {context.user_token}'
    }
    print(f"Headers: {list(headers.keys())}")
    
    api_client = APIClient(context.base_test.config)
    
    # Log the request details
    logger.info(f"Sending wallet balance request with payload: {context.wallet_balance_payload}")
    
    context.response = api_client.post(
        endpoint, 
        json_data=context.wallet_balance_payload,  # Changed from json to json_data
        headers=headers
    )
    
    print(f"Response status: {context.response.status_code}")
    if context.response.status_code != 200:
        print(f"Response body: {context.response.text}")
    
    logger.info(f"Wallet balance request sent - Status: {context.response.status_code}")


@when('I send wallet balance request without token to "{endpoint}"')
def step_send_wallet_balance_request_without_token(context, endpoint):
    """Send POST request to wallet balance endpoint without authentication token"""
    print(f"\nSending POST request to {endpoint} WITHOUT authentication")
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    api_client = APIClient(context.base_test.config)
    context.response = api_client.post(
        endpoint, 
        json_data=context.wallet_balance_payload,  # Changed from json to json_data
        headers=headers
    )
    
    print(f"Response status: {context.response.status_code}")
    logger.info(f"Wallet balance request sent without token - Status: {context.response.status_code}")


@then('response should contain wallet balance information')
def step_response_should_contain_wallet_balance_info(context):
    """Verify response contains wallet balance information"""
    response_json = context.response.json()
    
    # Check for balance information in response (various possible field names)
    has_balance = ('balance' in response_json or 
                   'balanceAmount' in response_json or 
                   'availableBalance' in response_json or 
                   'amount' in response_json)
    
    assert has_balance, \
        f"Response does not contain balance information. Response: {json.dumps(response_json, indent=2)}"
    
    logger.info("✓ Response contains wallet balance information")
    print("\n✓ Wallet balance information found in response")
    
    # Store balance for later validations
    context.balance_amount = (response_json.get('balanceAmount') or 
                             response_json.get('balance') or 
                             response_json.get('availableBalance') or 
                             response_json.get('amount'))
    context.balance_currency = (response_json.get('balanceCurrency') or 
                               response_json.get('currency') or 
                               response_json.get('currencyCode'))
    
    print(f"Balance: {context.balance_amount} {context.balance_currency}")


@then('response should contain currency "{expected_currency}"')
def step_response_should_contain_currency(context, expected_currency):
    """Verify response contains the expected currency"""
    response_json = context.response.json()
    
    # Check currency in different possible locations
    currency = (response_json.get('balanceCurrency') or 
               response_json.get('currency') or 
               response_json.get('currencyCode'))
    
    assert currency == expected_currency, \
        f"Expected currency '{expected_currency}' but got '{currency}'"
    
    logger.info(f"✓ Response contains expected currency: {expected_currency}")
    print(f"\n✓ Currency verified: {expected_currency}")


@then('wallet balance amount should be numeric')
def step_wallet_balance_amount_should_be_numeric(context):
    """Verify wallet balance amount is numeric"""
    response_json = context.response.json()
    
    # Get balance from different possible field names
    balance = (response_json.get('balanceAmount') or 
              response_json.get('balance') or 
              response_json.get('availableBalance') or 
              response_json.get('amount'))
    
    assert balance is not None, "Balance field not found in response"
    
    # Check if balance is numeric (int, float, or string that can be converted)
    try:
        if isinstance(balance, str):
            float(balance)
        else:
            assert isinstance(balance, (int, float)), "Balance is not numeric"
        logger.info(f"✓ Balance amount is numeric: {balance}")
        print(f"\n✓ Balance amount is numeric: {balance}")
    except ValueError:
        raise AssertionError(f"Balance amount is not numeric: {balance}")


@then('request should contain encrypted PIN')
def step_request_should_contain_encrypted_pin(context):
    """Verify request contains encrypted PIN (security check)"""
    payload = context.wallet_balance_payload
    
    assert 'pin' in payload, "PIN field not found in request payload"
    
    pin = payload['pin']
    
    # Check that PIN is encrypted (should be base64 encoded and long)
    assert len(pin) > 50, "PIN does not appear to be encrypted (too short)"
    assert '==' in pin or pin.isalnum(), "PIN does not appear to be base64 encoded"
    
    logger.info("✓ Request contains encrypted PIN")
    print("\n✓ Request contains encrypted PIN (security validated)")
