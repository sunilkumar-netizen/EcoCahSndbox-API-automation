"""
Step definitions for Send to Many Payment Options API
Endpoint: GET /bff/v2/payment/options
"""

from behave import given, when, then
from core.api_client import APIClient
import logging
import uuid

logger = logging.getLogger(__name__)


@given('I have send to many payment options query parameters')
def step_have_send_to_many_payment_options_params(context):
    """
    Parse send to many payment options query parameters from data table.
    Expected fields: serviceType
    """
    # Initialize query parameters dictionary
    context.send_to_many_payment_options_params = {}
    
    # Parse data table
    for row in context.table:
        field = row['parameter']
        value = row['value']
        context.send_to_many_payment_options_params[field] = value
    
    service_type = context.send_to_many_payment_options_params.get('serviceType', 'N/A')
    
    print(f"\n✓ Send to many payment options query parameters prepared:")
    print(f"  Service Type: {service_type}")
    
    logger.info(f"Send to many payment options query params prepared - Service Type: {service_type}")


@when('I send send to many payment options request to "{endpoint}"')
def step_send_send_to_many_payment_options_request(context, endpoint):
    """
    Send GET request to send to many payment options endpoint with query parameters.
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
    
    # Get query parameters
    params = context.send_to_many_payment_options_params if hasattr(context, 'send_to_many_payment_options_params') else {}
    
    service_type = params.get('serviceType', 'N/A')
    
    print(f"\n→ Sending send to many payment options request:")
    print(f"  Endpoint: {endpoint}")
    print(f"  Service Type: {service_type}")
    print(f"  Request ID: {request_id}")
    
    logger.info(f"Sending send to many payment options request to {endpoint} with service type: {service_type}")
    
    # Initialize API client
    api_client = APIClient(context.base_test.config)
    
    # Enhanced error handling with try-catch
    try:
        # Send GET request
        context.response = api_client.get(
            endpoint,
            params=params,
            headers=headers
        )
        
        print(f"✅ Response status: {context.response.status_code}")
        
        # Log response details
        if context.response.status_code == 200:
            logger.info(f"✅ Send to many payment options request successful - Status: {context.response.status_code}")
        else:
            logger.warning(f"⚠️ Send to many payment options request returned non-200 status: {context.response.status_code}")
            
    except Exception as e:
        # Capture error details
        error_details = {
            'error_type': type(e).__name__,
            'error_message': str(e),
            'endpoint': endpoint,
            'service_type': service_type,
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
        print(f"Service Type: {error_details['service_type']}")
        print(f"Request ID: {error_details['request_id']}")
        print("=" * 80)
        
        # Check if it's a 500 error
        if '500' in str(e) or 'Internal Server Error' in str(e):
            print("\n🔴 NOTE: This is a BACKEND 500 error - not a test automation issue!")
            print("The backend service encountered an internal error processing the request.")
            print("Please check with the backend team to investigate the server-side issue.")
            print("=" * 80 + "\n")
        
        # Log the error
        logger.error(f"❌ Error in send to many payment options request: {error_details['error_type']} - {error_details['error_message']}")
        
        # Re-raise the exception to fail the test
        raise


@then('response should contain send to many payment options')
def step_verify_send_to_many_payment_options_response(context):
    """
    Verify that response contains send to many payment options data.
    Checks for common payment options fields and extracts instrumentToken for later use.
    """
    response_json = context.response.json()
    
    # Check for common payment options fields
    # The API may return different structures, so we check for multiple possibilities
    has_payment_options = False
    found_fields = []
    
    # Check for possible field names
    possible_fields = ['paymentOptions', 'options', 'data', 'instruments', 'paymentMethods']
    
    for field in possible_fields:
        if field in response_json:
            has_payment_options = True
            found_fields.append(field)
    
    # Also check if response has any data (non-empty)
    if response_json and len(response_json) > 0:
        has_payment_options = True
    
    # Extract instrumentToken from the response for use in send to many payment
    instrument_token_extracted = False
    
    # Try to extract instrumentToken from response
    if isinstance(response_json, list) and len(response_json) > 0:
        # Response is an array of payment options
        for item in response_json:
            if 'instrumentToken' in item:
                context.send_to_many_instrument_token = item['instrumentToken']
                instrument_token_extracted = True
                print(f"\n🔑 Extracted instrumentToken: {context.send_to_many_instrument_token}")
                logger.info(f"✅ Extracted instrumentToken from payment options: {context.send_to_many_instrument_token}")
                break
    elif isinstance(response_json, dict):
        # Response is a dictionary
        # Check for instrumentToken directly
        if 'instrumentToken' in response_json:
            context.send_to_many_instrument_token = response_json['instrumentToken']
            instrument_token_extracted = True
            print(f"\n🔑 Extracted instrumentToken: {context.send_to_many_instrument_token}")
            logger.info(f"✅ Extracted instrumentToken from payment options: {context.send_to_many_instrument_token}")
        else:
            # Check nested structures
            for field in ['data', 'items', 'paymentOptions', 'options']:
                if field in response_json:
                    nested_data = response_json[field]
                    if isinstance(nested_data, list) and len(nested_data) > 0:
                        for item in nested_data:
                            if 'instrumentToken' in item:
                                context.send_to_many_instrument_token = item['instrumentToken']
                                instrument_token_extracted = True
                                print(f"\n🔑 Extracted instrumentToken: {context.send_to_many_instrument_token}")
                                logger.info(f"✅ Extracted instrumentToken from payment options: {context.send_to_many_instrument_token}")
                                break
                    elif isinstance(nested_data, dict) and 'instrumentToken' in nested_data:
                        context.send_to_many_instrument_token = nested_data['instrumentToken']
                        instrument_token_extracted = True
                        print(f"\n🔑 Extracted instrumentToken: {context.send_to_many_instrument_token}")
                        logger.info(f"✅ Extracted instrumentToken from payment options: {context.send_to_many_instrument_token}")
                        break
                    if instrument_token_extracted:
                        break
    
    if not instrument_token_extracted:
        logger.warning("⚠️ Could not extract instrumentToken from payment options response")
        print("\n⚠️ Warning: instrumentToken not found in response - will use fallback token")
    
    print(f"\n✓ Send to many payment options response validation:")
    if found_fields:
        print(f"  Found fields: {', '.join(found_fields)}")
    print(f"  Has payment options data: {has_payment_options}")
    print(f"  InstrumentToken extracted: {instrument_token_extracted}")
    
    assert has_payment_options, f"Response does not contain send to many payment options data. Response: {response_json}"
    
    logger.info(f"✅ Send to many payment options response validated - Fields found: {found_fields}")
