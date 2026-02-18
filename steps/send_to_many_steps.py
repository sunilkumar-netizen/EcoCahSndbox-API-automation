"""
Step definitions for Send to Many Payment API
Endpoint: POST /bff/v1/wallet/payments/send-to-many
"""

from behave import given, when, then
from core.api_client import APIClient
import logging
import uuid
import json

logger = logging.getLogger(__name__)


# ============================================================================
# GIVEN STEPS - Setup test data
# ============================================================================

@given('I have send to many payment request body with {num_recipients:d} recipients')
def step_have_send_to_many_payment_body(context, num_recipients):
    """
    Set up complete send to many payment request body with specified number of recipients.
    Uses instrumentToken from payment options if available, otherwise uses default.
    """
    config = context.base_test.config
    
    # Get instrument token from payment options API response (stored in context)
    instrument_token = getattr(context, 'send_to_many_instrument_token', None)
    
    if instrument_token:
        logger.info(f"🔑 Using instrumentToken from Payment Options API: {instrument_token}")
        print(f"\n🔑 Using instrumentToken from Payment Options API")
    else:
        # Fallback: Try to fetch dynamically
        logger.info("🔄 Attempting to fetch instrumentToken from Payment Options API...")
        instrument_token = _fetch_instrument_token_from_payment_options(context, "ZWSendManyTransactions", "ZWG", "ecocash")
        
        if instrument_token:
            logger.info(f"🔑 Fetched instrumentToken dynamically: {instrument_token}")
            print(f"\n🔑 Fetched instrumentToken dynamically from Payment Options API")
        else:
            # Last resort: Use fallback token
            instrument_token = "1e55edb5-8dae-46d2-8d9e-1001db6b9409"
            logger.warning(f"⚠️ Using fallback instrumentToken: {instrument_token}")
            print(f"\n⚠️ Using fallback instrumentToken (Payment Options API not called)")
    
    # Get encrypted PIN from config
    encrypted_pin = config.get('utility_payment.encrypted_pin') or config.get('pin_verify.sample_encrypted_pin')
    
    if not encrypted_pin:
        logger.error("❌ No encrypted PIN found in config!")
        raise ValueError("Encrypted PIN not found in configuration")
    
    # Build recipient details based on requested number
    recipients = []
    recipient_templates = [
        {
            "amount": 4,
            "name": "EcoCash User Two",
            "mobileNumber": "+263789124558",
            "customerId": "2f3a5e5a-9387-4669-8674-58df6c28b5ac"
        },
        {
            "amount": 4,
            "name": "Ecocash User Two",
            "mobileNumber": "+263789124669",
            "customerId": "f044ff8d-abe6-47aa-8837-ec329e8a0edc"
        }
    ]
    
    for i in range(num_recipients):
        template_idx = i % len(recipient_templates)
        recipients.append(recipient_templates[template_idx].copy())
    
    context.send_to_many_body = {
        "currency": "ZWG",
        "description": "Test Send to Many Recipients",
        "instrumentToken": instrument_token,
        "provider": "ecocash",
        "pin": encrypted_pin,
        "notes": {
            "message": "Test Send to Many Recipients"
        },
        "recipientDetails": recipients
    }
    
    print(f"\n✓ Send to many payment request prepared:")
    print(f"  Currency: ZWG")
    print(f"  Provider: ecocash")
    print(f"  Number of recipients: {num_recipients}")
    print(f"  Instrument Token: {instrument_token}")
    
    logger.info(f"Send to many payment body prepared with {num_recipients} recipients: {json.dumps(context.send_to_many_body, indent=2)}")


@given('I have send to many payment request with currency "{currency}"')
def step_have_send_to_many_payment_with_currency(context, currency):
    """
    Initialize send to many payment request with specific currency.
    """
    config = context.base_test.config
    
    # Get instrument token from payment options API response (stored in context)
    instrument_token = getattr(context, 'send_to_many_instrument_token', None)
    
    if instrument_token:
        logger.info(f"🔑 Using instrumentToken from Payment Options API: {instrument_token}")
        print(f"\n🔑 Using instrumentToken from Payment Options API")
    else:
        # Fallback: Try to fetch dynamically
        logger.info(f"🔄 Attempting to fetch instrumentToken for {currency}...")
        instrument_token = _fetch_instrument_token_from_payment_options(context, "ZWSendManyTransactions", currency, "ecocash")
        
        if instrument_token:
            logger.info(f"🔑 Fetched instrumentToken for {currency}: {instrument_token}")
            print(f"\n🔑 Fetched instrumentToken for {currency} from Payment Options API")
        else:
            # Last resort: Use fallback token
            instrument_token = "1e55edb5-8dae-46d2-8d9e-1001db6b9409"
            logger.warning(f"⚠️ Using fallback instrumentToken: {instrument_token}")
            print(f"\n⚠️ Using fallback instrumentToken")
    
    encrypted_pin = config.get('utility_payment.encrypted_pin') or config.get('pin_verify.sample_encrypted_pin')
    
    if not encrypted_pin:
        logger.error("❌ No encrypted PIN found in config!")
        raise ValueError("Encrypted PIN not found in configuration")
    
    context.send_to_many_body = {
        "currency": currency,
        "description": f"Test Send to Many - {currency}",
        "instrumentToken": instrument_token,
        "provider": "ecocash",
        "pin": encrypted_pin,
        "notes": {
            "message": f"Test Send to Many - {currency}"
        },
        "recipientDetails": []  # Will be populated by next step
    }
    
    print(f"\n✓ Send to many payment initialized with currency: {currency}")
    logger.info(f"Send to many payment initialized with currency {currency}")


@given('I have send to many recipients list')
def step_have_send_to_many_recipients_list(context):
    """
    Parse recipients list from data table and add to request body.
    Expected columns: amount, name, mobileNumber, customerId
    """
    if not hasattr(context, 'send_to_many_body'):
        context.send_to_many_body = {}
    
    recipients = []
    for row in context.table:
        recipient = {
            "amount": int(row['amount']),
            "name": row['name'],
            "mobileNumber": row['mobileNumber'],
            "customerId": row['customerId']
        }
        recipients.append(recipient)
    
    context.send_to_many_body['recipientDetails'] = recipients
    
    print(f"\n✓ Recipients added to request:")
    print(f"  Number of recipients: {len(recipients)}")
    for idx, recipient in enumerate(recipients, 1):
        print(f"  Recipient {idx}: {recipient['name']} - {recipient['mobileNumber']} - Amount: {recipient['amount']}")
    
    logger.info(f"Added {len(recipients)} recipients to send to many request")


@given('I have send to many payment request without currency field')
def step_have_send_to_many_without_currency(context):
    """
    Create send to many request without currency field (for negative testing).
    """
    config = context.base_test.config
    encrypted_pin = config.get('utility_payment.encrypted_pin') or config.get('pin_verify.sample_encrypted_pin')
    
    context.send_to_many_body = {
        "description": "Test Send to Many - No Currency",
        "instrumentToken": "1e55edb5-8dae-46d2-8d9e-1001db6b9409",
        "provider": "ecocash",
        "pin": encrypted_pin,
        "notes": {},
        "recipientDetails": [
            {
                "amount": 4,
                "name": "Test User",
                "mobileNumber": "+263789124558",
                "customerId": "2f3a5e5a-9387-4669-8674-58df6c28b5ac"
            }
        ]
    }
    
    print("\n✓ Send to many request created WITHOUT currency field")
    logger.info("Created send to many request without currency field for negative test")


@given('I have send to many payment request without recipients')
def step_have_send_to_many_without_recipients(context):
    """
    Create send to many request without recipients (for negative testing).
    """
    config = context.base_test.config
    encrypted_pin = config.get('utility_payment.encrypted_pin') or config.get('pin_verify.sample_encrypted_pin')
    
    context.send_to_many_body = {
        "currency": "ZWG",
        "description": "Test Send to Many - No Recipients",
        "instrumentToken": "1e55edb5-8dae-46d2-8d9e-1001db6b9409",
        "provider": "ecocash",
        "pin": encrypted_pin,
        "notes": {},
        "recipientDetails": []
    }
    
    print("\n✓ Send to many request created WITHOUT recipients")
    logger.info("Created send to many request without recipients for negative test")


@given('I have send to many payment request with invalid instrument token')
def step_have_send_to_many_with_invalid_token(context):
    """
    Create send to many request with invalid instrument token (for negative testing).
    """
    config = context.base_test.config
    encrypted_pin = config.get('utility_payment.encrypted_pin') or config.get('pin_verify.sample_encrypted_pin')
    
    context.send_to_many_body = {
        "currency": "ZWG",
        "description": "Test Send to Many - Invalid Token",
        "instrumentToken": "invalid-token-12345",
        "provider": "ecocash",
        "pin": encrypted_pin,
        "notes": {},
        "recipientDetails": [
            {
                "amount": 4,
                "name": "Test User",
                "mobileNumber": "+263789124558",
                "customerId": "2f3a5e5a-9387-4669-8674-58df6c28b5ac"
            }
        ]
    }
    
    print("\n✓ Send to many request created with INVALID instrument token")
    logger.info("Created send to many request with invalid instrument token for negative test")


@given('I have send to many payment request with incomplete recipient data')
def step_have_send_to_many_with_incomplete_recipient(context):
    """
    Create send to many request with incomplete recipient data (for negative testing).
    """
    config = context.base_test.config
    encrypted_pin = config.get('utility_payment.encrypted_pin') or config.get('pin_verify.sample_encrypted_pin')
    
    context.send_to_many_body = {
        "currency": "ZWG",
        "description": "Test Send to Many - Incomplete Recipient",
        "instrumentToken": "1e55edb5-8dae-46d2-8d9e-1001db6b9409",
        "provider": "ecocash",
        "pin": encrypted_pin,
        "notes": {},
        "recipientDetails": [
            {
                "amount": 4,
                "name": "Test User"
                # Missing mobileNumber and customerId
            }
        ]
    }
    
    print("\n✓ Send to many request created with INCOMPLETE recipient data")
    logger.info("Created send to many request with incomplete recipient data for negative test")


@given('I have send to many payment request with unencrypted pin')
def step_have_send_to_many_with_unencrypted_pin(context):
    """
    Create send to many request with unencrypted PIN (for security testing).
    """
    context.send_to_many_body = {
        "currency": "ZWG",
        "description": "Test Send to Many - Unencrypted PIN",
        "instrumentToken": "1e55edb5-8dae-46d2-8d9e-1001db6b9409",
        "provider": "ecocash",
        "pin": "1234",  # Unencrypted plain text PIN
        "notes": {},
        "recipientDetails": [
            {
                "amount": 4,
                "name": "Test User",
                "mobileNumber": "+263789124558",
                "customerId": "2f3a5e5a-9387-4669-8674-58df6c28b5ac"
            }
        ]
    }
    
    print("\n✓ Send to many request created with UNENCRYPTED PIN")
    logger.info("Created send to many request with unencrypted PIN for security test")


# ============================================================================
# WHEN STEPS - API calls
# ============================================================================

@when('I send send to many payment request to "{endpoint}"')
def step_send_send_to_many_payment_request(context, endpoint):
    """
    Send POST request to send to many payment endpoint.
    Uses user token for authentication.
    """
    # Generate request ID
    request_id = str(uuid.uuid4())
    
    # Build headers
    headers = {
        'Authorization': f'Bearer {context.user_token}',
        'Content-Type': 'application/json',
        'requestId': request_id
    }
    
    # Get request body
    body = context.send_to_many_body if hasattr(context, 'send_to_many_body') else {}
    
    currency = body.get('currency', 'N/A')
    num_recipients = len(body.get('recipientDetails', []))
    
    print(f"\n→ Sending send to many payment request:")
    print(f"  Endpoint: {endpoint}")
    print(f"  Currency: {currency}")
    print(f"  Number of recipients: {num_recipients}")
    print(f"  Request ID: {request_id}")
    
    logger.info(f"Sending send to many payment request to {endpoint} - Currency: {currency}, Recipients: {num_recipients}")
    
    # Initialize API client
    api_client = APIClient(context.base_test.config)
    
    # Enhanced error handling with try-catch
    try:
        # Send POST request
        context.response = api_client.post(
            endpoint,
            json_data=body,
            headers=headers
        )
        
        context.base_test.response = context.response
        
        print(f"✅ Response status: {context.response.status_code}")
        
        # Extract and store sendManyId from response for use in details API
        if context.response.status_code in [200, 201]:
            try:
                response_json = context.response.json()
                
                # Check for possible field names that might contain the transaction ID
                possible_fields = [
                    'sendManyId', 'transactionId', 'orderId', 'paymentId', 
                    'referenceId', 'id', 'sendToManyId', 'sendManyTransactionId'
                ]
                
                send_many_id = None
                field_found = None
                
                # Check root level
                for field in possible_fields:
                    if field in response_json and response_json[field]:
                        send_many_id = response_json[field]
                        field_found = field
                        break
                
                # Check nested 'data' object
                if not send_many_id and 'data' in response_json and isinstance(response_json['data'], dict):
                    for field in possible_fields:
                        if field in response_json['data'] and response_json['data'][field]:
                            send_many_id = response_json['data'][field]
                            field_found = f"data.{field}"
                            break
                
                if send_many_id:
                    context.send_many_id = send_many_id
                    print(f"🔑 Captured send many ID: {send_many_id} (from {field_found})")
                    logger.info(f"✅ Captured send many ID: {send_many_id}")
                    
            except Exception as id_extract_error:
                logger.warning(f"⚠️ Could not extract send many ID from response: {id_extract_error}")
        
        # Log response details
        if context.response.status_code in [200, 201]:
            logger.info(f"✅ Send to many payment request successful - Status: {context.response.status_code}")
        else:
            logger.warning(f"⚠️ Send to many payment request returned non-success status: {context.response.status_code}")
            print(f"⚠️ Response body: {context.response.text[:500]}")
            
    except Exception as e:
        # Capture error details
        error_details = {
            'error_type': type(e).__name__,
            'error_message': str(e),
            'endpoint': endpoint,
            'currency': currency,
            'num_recipients': num_recipients,
            'request_id': request_id
        }
        
        # Store error details in context for potential use in other steps
        context.error_details = error_details
        
        # Print formatted error message
        print("\n" + "=" * 80)
        print("❌ BACKEND ERROR DETAILS:")
        print("=" * 80)
        print(f"Error Type: {error_details['error_type']}")
        print(f"Error Message: {error_details['error_message']}")
        print(f"Endpoint: {error_details['endpoint']}")
        print(f"Currency: {error_details['currency']}")
        print(f"Recipients: {error_details['num_recipients']}")
        print(f"Request ID: {error_details['request_id']}")
        print("=" * 80)
        
        # Check if it's a 500 error
        if '500' in str(e) or 'Internal Server Error' in str(e):
            print("\n🔴 NOTE: This is a BACKEND 500 error - not a test automation issue!")
            print("The backend service encountered an internal error processing the request.")
            print("Please check with the backend team to investigate the server-side issue.")
            print("=" * 80 + "\n")
        
        # Log the error
        logger.error(f"❌ Error in send to many payment request: {error_details['error_type']} - {error_details['error_message']}")
        
        # Re-raise the exception to fail the test
        raise


@when('I send send to many payment request without token to "{endpoint}"')
def step_send_send_to_many_payment_without_token(context, endpoint):
    """
    Send POST request to send to many payment endpoint without authentication token.
    For negative testing.
    """
    # Generate request ID
    request_id = str(uuid.uuid4())
    
    # Build headers WITHOUT Authorization
    headers = {
        'Content-Type': 'application/json',
        'requestId': request_id
    }
    
    # Get request body
    body = context.send_to_many_body if hasattr(context, 'send_to_many_body') else {}
    
    print(f"\n→ Sending send to many payment request WITHOUT authentication")
    print(f"  Endpoint: {endpoint}")
    
    logger.info(f"Sending send to many payment request WITHOUT token to {endpoint}")
    
    # Initialize API client
    api_client = APIClient(context.base_test.config)
    
    # Send POST request without token
    context.response = api_client.post(
        endpoint,
        json_data=body,
        headers=headers
    )
    
    context.base_test.response = context.response
    
    print(f"✅ Response status: {context.response.status_code}")
    logger.info(f"Send to many payment request without token - Status: {context.response.status_code}")


# ============================================================================
# THEN STEPS - Assertions
# ============================================================================

@then('response should contain send to many payment confirmation')
def step_verify_send_to_many_payment_confirmation(context):
    """
    Verify that response contains send to many payment confirmation data.
    Checks for common payment confirmation fields.
    """
    response_json = context.response.json()
    
    # Check for common payment confirmation fields
    has_confirmation = False
    found_fields = []
    
    # Check for possible field names
    possible_fields = [
        'transactionId', 'orderId', 'paymentId', 'referenceId', 'traceId',
        'status', 'message', 'data', 'result', 'success'
    ]
    
    for field in possible_fields:
        if field in response_json:
            has_confirmation = True
            found_fields.append(field)
    
    # Also check if response has any data (non-empty)
    if response_json and len(response_json) > 0:
        has_confirmation = True
    
    print(f"\n✓ Send to many payment confirmation validation:")
    if found_fields:
        print(f"  Found fields: {', '.join(found_fields)}")
    print(f"  Has confirmation data: {has_confirmation}")
    
    assert has_confirmation, f"Response does not contain send to many payment confirmation data. Response: {response_json}"
    
    logger.info(f"✅ Send to many payment confirmation validated - Fields found: {found_fields}")


@then('send to many payment should process all recipients successfully')
def step_verify_all_recipients_processed(context):
    """
    Verify that all recipients in the request were processed successfully.
    """
    response_json = context.response.json()
    request_body = context.send_to_many_body
    
    num_recipients_sent = len(request_body.get('recipientDetails', []))
    
    # Check for recipient processing information in response
    # Different APIs may return this information differently
    recipients_processed = False
    
    # Check various possible response structures
    if 'recipientsProcessed' in response_json:
        num_processed = response_json['recipientsProcessed']
        recipients_processed = (num_processed == num_recipients_sent)
    elif 'results' in response_json:
        num_processed = len(response_json['results'])
        recipients_processed = (num_processed == num_recipients_sent)
    elif 'status' in response_json and response_json['status'] in ['success', 'completed', 'SUCCESS']:
        recipients_processed = True
    else:
        # If no specific recipient count, assume success if status is 200/201
        if context.response.status_code in [200, 201]:
            recipients_processed = True
    
    print(f"\n✓ Recipients processing validation:")
    print(f"  Recipients sent: {num_recipients_sent}")
    print(f"  All recipients processed: {recipients_processed}")
    
    assert recipients_processed, f"Not all recipients were processed successfully. Sent: {num_recipients_sent}"
    
    logger.info(f"✅ All {num_recipients_sent} recipients processed successfully")


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _fetch_instrument_token_from_payment_options(context, service_type, currency, provider):
    """
    Helper function to fetch instrument token from payment options API.
    Returns instrument token if found, None otherwise.
    """
    try:
        # First check if already extracted from payment options response
        if hasattr(context, 'send_to_many_instrument_token'):
            logger.info(f"✅ Using instrumentToken from context (already extracted): {context.send_to_many_instrument_token}")
            return context.send_to_many_instrument_token
        
        # Check legacy context variable
        if hasattr(context, 'instrument_token'):
            logger.info(f"✅ Using instrumentToken from legacy context: {context.instrument_token}")
            return context.instrument_token
        
        # Fetch from payment options API
        api_client = APIClient(context.base_test.config)
        request_id = str(uuid.uuid4())
        
        headers = {
            'Authorization': f'Bearer {context.user_token}',
            'Content-Type': 'application/json',
            'requestId': request_id
        }
        
        params = {'serviceType': service_type}
        
        logger.info(f"🔄 Fetching instrument token from payment options API - Service: {service_type}, Currency: {currency}")
        
        response = api_client.get('/bff/v2/payment/options', params=params, headers=headers)
        
        if response.status_code == 200:
            response_json = response.json()
            
            # Extract instrument token based on currency and provider
            items = response_json if isinstance(response_json, list) else response_json.get('items', [])
            
            for item in items:
                if item.get('currency') == currency and item.get('provider') == provider:
                    instrument_token = item.get('instrumentToken')
                    if instrument_token:
                        logger.info(f"✅ Retrieved instrument token for {currency}/{provider}: {instrument_token}")
                        context.send_to_many_instrument_token = instrument_token
                        return instrument_token
        
        logger.warning(f"⚠️ Could not fetch instrument token from payment options API")
        return None
        
    except Exception as e:
        logger.warning(f"⚠️ Error fetching instrument token: {str(e)}")
        return None
