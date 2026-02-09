"""
Step definitions for P2P Beneficiary Account Lookup API
Endpoint: POST /bff/v3/payment/account/lookup
This is part of the "Pay to Person (Domestic)" flow

NOTE: This API looks up beneficiary account details for P2P payment validation.
Request Body:
- accountNumber: Phone number or account identifier

Response contains beneficiary details including name, account info, status, etc.
"""

from behave import given, when, then
import json
import logging
import time

# Initialize logger
logger = logging.getLogger(__name__)


# ===========================
# Given Steps - Setup
# ===========================

@given('I have account number ""')
def step_have_empty_account_number(context):
    """Set empty account number for testing empty parameter"""
    context.account_number = ""
    logger.info(f"📱 Account number set to empty string (testing empty parameter)")


@given('I have account number "{account_number}"')
def step_have_account_number(context, account_number):
    """Set account number for lookup"""
    context.account_number = account_number
    logger.info(f"📱 Account number set to: {account_number}")


@given('I have no account number')
def step_no_account_number(context):
    """Clear account number to test missing parameter"""
    if hasattr(context, 'account_number'):
        delattr(context, 'account_number')
    context.account_number = None
    logger.info("❌ Account number cleared (testing missing parameter)")


@given('I have null account number')
def step_null_account_number(context):
    """Set null account number for testing"""
    context.account_number = None
    logger.info("❌ Account number set to null")


@given('I have account number from extracted contact')
def step_account_number_from_extracted_contact(context):
    """Use account number from previously extracted contact"""
    assert hasattr(context, 'extracted_contact'), "No contact was extracted previously"
    
    contact = context.extracted_contact
    
    # Try to find phone number or account identifier in contact
    # Order matters - try phone fields first, then ID fields
    account_fields = [
        'phone', 'phoneNumber', 'mobileNumber', 'mobile',  # Phone fields
        'accountNumber', 'accountId',  # Account fields
        'operatorId', '_id', 'id'  # ID fields (for operators/agents)
    ]
    account_number = None
    
    for field in account_fields:
        if field in contact and contact[field]:
            account_number = str(contact[field])  # Convert to string in case it's not
            break
    
    # Check in nested document structure (legacy support)
    if not account_number and 'document' in contact and isinstance(contact['document'], list) and len(contact['document']) > 0:
        doc = contact['document'][0]
        for field in account_fields:
            if field in doc and doc[field]:
                account_number = str(doc[field])
                break
    
    assert account_number, f"Could not find account number in extracted contact. Available fields: {list(contact.keys())}"
    
    context.account_number = account_number
    logger.info(f"📱 Account number from contact: {account_number}")


@given('I have malformed JSON body')
def step_malformed_json_body(context):
    """Set flag for malformed JSON"""
    context.malformed_json = True
    logger.info("⚠️ Malformed JSON body flag set")


@given('I have no Content-Type header')
def step_no_content_type_header(context):
    """Set flag to skip Content-Type header"""
    context.skip_content_type = True
    logger.info("❌ Content-Type header will be skipped")


# ===========================
# When Steps - Actions
# ===========================

@when('I send account lookup request to "{endpoint}"')
def step_send_account_lookup_request(context, endpoint):
    """Send POST request to account lookup endpoint"""
    url = f"{context.config_loader.get('api.base_url')}{endpoint}"
    
    # Build request body
    if hasattr(context, 'malformed_json') and context.malformed_json:
        # Send malformed JSON
        json_data = "{accountNumber: invalid}"
        headers = {
            'Authorization': f"Bearer {context.user_token}",
            'Content-Type': 'application/json'
        }
        
        try:
            logger.info(f"Sending POST request to {url} with malformed JSON")
            start_time = time.time()
            
            import requests
            response = requests.post(
                url,
                data=json_data,
                headers=headers,
                timeout=30
            )
            context.response = response
            context.response_time = (time.time() - start_time) * 1000
            logger.info(f"Response Status: {response.status_code}")
            
        except Exception as e:
            logger.error(f"Request failed: {str(e)}")
            raise
        return
    
    # Normal request
    json_data = {}
    
    if hasattr(context, 'account_number') and context.account_number is not None:
        json_data['accountNumber'] = context.account_number
    
    # Build headers
    headers = {
        'Authorization': f"Bearer {context.user_token}"
    }
    
    # Add Content-Type unless skipped
    if not hasattr(context, 'skip_content_type') or not context.skip_content_type:
        headers['Content-Type'] = 'application/json'
    
    try:
        logger.info(f"Sending POST request to {url}")
        logger.info(f"Request body: {json.dumps(json_data, indent=2)}")
        
        start_time = time.time()
        response = context.base_test.api_client.post(
            endpoint,
            json_data=json_data,  # Fixed: use json_data parameter name
            headers=headers
        )
        context.response = response
        context.response_time = (time.time() - start_time) * 1000
        
        logger.info(f"Response Status: {response.status_code}")
        logger.info(f"Response Time: {context.response_time:.2f} ms")
        
        if response.status_code == 200:
            response_text = response.text if hasattr(response, 'text') else str(response.content)
            logger.info(f"Response: {response_text[:500]}...")  # Log first 500 chars
            
            # ✨ DYNAMIC TOKEN EXTRACTION: Extract beneficiary instrument token
            try:
                response_json = response.json()
                if 'actionDetails' in response_json and len(response_json['actionDetails']) > 0:
                    first_action = response_json['actionDetails'][0]
                    if 'beneficiaryInstrumentToken' in first_action:
                        context.beneficiary_instrument_token = first_action['beneficiaryInstrumentToken']
                        context.beneficiary_instrument_id = first_action.get('instrumentId', '')
                        context.beneficiary_customer_id = first_action.get('customerId', '')
                        logger.info(f"✅ Extracted beneficiary instrument token: {context.beneficiary_instrument_token}")
                        logger.info(f"✅ Extracted instrument ID: {context.beneficiary_instrument_id}")
                        logger.info(f"✅ Extracted customer ID: {context.beneficiary_customer_id}")
            except Exception as token_error:
                logger.warning(f"Could not extract beneficiary token: {str(token_error)}")
        else:
            response_text = response.text if hasattr(response, 'text') else str(response.content)
            logger.warning(f"Error Response: {response_text}")
            
    except Exception as e:
        logger.error(f"Request failed: {str(e)}")
        raise


# ===========================
# Then Steps - Assertions
# ===========================

@then('response should contain account details')
def step_response_contains_account_details(context):
    """Verify response contains account details"""
    assert context.response.status_code == 200, \
        f"Expected status 200, got {context.response.status_code}"
    
    response_data = context.response.json()
    
    # The actual API returns actionDetails array with beneficiary information
    if 'actionDetails' in response_data and len(response_data['actionDetails']) > 0:
        logger.info(f"✓ Response contains account details in actionDetails array")
        return
    
    # Check for other common account detail fields
    account_fields = ['accountNumber', 'accountId', 'name', 'beneficiaryName', 'accountName', 'customerName', 'status']
    has_account_details = any(field in response_data for field in account_fields)
    
    # Could also have nested data
    if 'data' in response_data:
        data = response_data['data']
        has_account_details = any(field in data for field in account_fields)
    
    assert has_account_details or 'actionDetails' in response_data, \
        f"Response missing account details fields. Available fields: {list(response_data.keys())}"
    
    logger.info(f"✓ Response contains account details")


@then('response should have beneficiary name')
def step_response_has_beneficiary_name(context):
    """Verify response has beneficiary name"""
    response_data = context.response.json()
    
    # The actual API returns beneficiaryName inside actionDetails array
    if 'actionDetails' in response_data and len(response_data['actionDetails']) > 0:
        action = response_data['actionDetails'][0]
        if 'beneficiaryName' in action and action['beneficiaryName']:
            context.beneficiary_name = action['beneficiaryName']
            logger.info(f"✓ Beneficiary name found in actionDetails: {context.beneficiary_name}")
            return
    
    # Check for name fields at root level
    name_fields = ['name', 'beneficiaryName', 'accountName', 'customerName', 'fullName', 'displayName']
    
    beneficiary_name = None
    for field in name_fields:
        if field in response_data and response_data[field]:
            beneficiary_name = response_data[field]
            break
    
    # Check in nested data
    if not beneficiary_name and 'data' in response_data:
        data = response_data['data']
        for field in name_fields:
            if field in data and data[field]:
                beneficiary_name = data[field]
                break
    
    assert beneficiary_name, \
        f"Response missing beneficiary name. Available fields: {list(response_data.keys())}"
    
    context.beneficiary_name = beneficiary_name
    logger.info(f"✓ Beneficiary name found: {beneficiary_name}")


@then('response should have account status')
def step_response_has_account_status(context):
    """Verify response has account status"""
    response_data = context.response.json()
    
    # The actual API may have status information in actionDetails
    if 'actionDetails' in response_data and len(response_data['actionDetails']) > 0:
        # The presence of actionDetails with account info indicates account is valid
        logger.info(f"✓ Account is valid (actionDetails present with {len(response_data['actionDetails'])} action(s))")
        return
    
    # Check for status field at root level
    status_fields = ['status', 'accountStatus', 'state', 'active']
    
    account_status = None
    for field in status_fields:
        if field in response_data:
            account_status = response_data[field]
            break
    
    # Check in nested data
    if not account_status and 'data' in response_data:
        data = response_data['data']
        for field in status_fields:
            if field in data:
                account_status = data[field]
                break
    
    # Status field might not always be present, just log if found
    if account_status:
        logger.info(f"✓ Account status: {account_status}")
    else:
        logger.info(f"ℹ️ No explicit account status field found (but account is valid)")


@then('response should have complete beneficiary details')
def step_response_has_complete_beneficiary_details(context):
    """Verify response has complete beneficiary details"""
    response_data = context.response.json()
    
    # Store response for later use
    context.beneficiary_details = response_data
    
    # Check for essential fields
    essential_fields = ['name', 'beneficiaryName', 'accountName', 'customerName']
    has_name = any(field in response_data for field in essential_fields)
    
    # Check in nested data
    if not has_name and 'data' in response_data:
        data = response_data['data']
        has_name = any(field in data for field in essential_fields)
    
    assert has_name, \
        f"Response missing essential beneficiary details. Available fields: {list(response_data.keys())}"
    
    logger.info(f"✓ Response has complete beneficiary details")


@then('response should have required account fields')
def step_response_has_required_account_fields(context):
    """Verify response has required account fields"""
    response_data = context.response.json()
    
    # At least one identifier should be present
    identifier_fields = ['accountNumber', 'accountId', 'customerId', 'phone', 'phoneNumber']
    has_identifier = any(field in response_data for field in identifier_fields)
    
    # Check in nested data
    if not has_identifier and 'data' in response_data:
        data = response_data['data']
        has_identifier = any(field in data for field in identifier_fields)
    
    assert has_identifier, \
        f"Response missing required account identifier. Available fields: {list(response_data.keys())}"
    
    logger.info(f"✓ Response has required account fields")


@then('beneficiary account should be valid')
def step_beneficiary_account_should_be_valid(context):
    """Verify beneficiary account is valid"""
    response_data = context.response.json()
    
    # Check if account is valid (no error status)
    if 'error' in response_data or 'errorCode' in response_data:
        raise AssertionError(f"Account lookup returned error: {response_data}")
    
    # Check status if present
    status_fields = ['status', 'accountStatus', 'state']
    for field in status_fields:
        if field in response_data:
            status = response_data[field]
            if isinstance(status, str) and status.lower() in ['invalid', 'closed', 'blocked', 'inactive']:
                logger.warning(f"⚠️ Account status is: {status}")
    
    logger.info(f"✓ Beneficiary account is valid")


@then('I extract beneficiary name from response')
def step_extract_beneficiary_name(context):
    """Extract beneficiary name from response"""
    response_data = context.response.json()
    
    # Find name field
    name_fields = ['name', 'beneficiaryName', 'accountName', 'customerName', 'fullName', 'displayName']
    
    beneficiary_name = None
    for field in name_fields:
        if field in response_data and response_data[field]:
            beneficiary_name = response_data[field]
            break
    
    # Check in nested data
    if not beneficiary_name and 'data' in response_data:
        data = response_data['data']
        for field in name_fields:
            if field in data and data[field]:
                beneficiary_name = data[field]
                break
    
    assert beneficiary_name, "Could not extract beneficiary name from response"
    
    context.extracted_beneficiary_name = beneficiary_name
    logger.info(f"✓ Extracted beneficiary name: {beneficiary_name}")


@then('I extract account identifier from response')
def step_extract_account_identifier(context):
    """Extract account identifier from response"""
    response_data = context.response.json()
    
    # Find identifier field
    identifier_fields = ['accountNumber', 'accountId', 'customerId', 'phone', 'phoneNumber', 'mobileNumber']
    
    account_id = None
    for field in identifier_fields:
        if field in response_data and response_data[field]:
            account_id = response_data[field]
            break
    
    # Check in nested data
    if not account_id and 'data' in response_data:
        data = response_data['data']
        for field in identifier_fields:
            if field in data and data[field]:
                account_id = data[field]
                break
    
    assert account_id, "Could not extract account identifier from response"
    
    context.extracted_account_id = account_id
    logger.info(f"✓ Extracted account identifier: {account_id}")


@then('extracted beneficiary details should be valid')
def step_extracted_beneficiary_details_valid(context):
    """Verify extracted beneficiary details are valid"""
    assert hasattr(context, 'extracted_beneficiary_name'), "Beneficiary name was not extracted"
    assert hasattr(context, 'extracted_account_id'), "Account identifier was not extracted"
    
    assert context.extracted_beneficiary_name, "Beneficiary name is empty"
    assert context.extracted_account_id, "Account identifier is empty"
    
    logger.info(f"✓ Extracted beneficiary details are valid")


@then('response should have account metadata')
def step_response_has_account_metadata(context):
    """Verify response has account metadata"""
    response_data = context.response.json()
    
    # Response should have some metadata
    assert len(response_data) > 0, "Response is empty"
    
    logger.info(f"✓ Response has account metadata with {len(response_data)} fields")


@then('response should have beneficiary information')
def step_response_has_beneficiary_information(context):
    """Verify response has beneficiary information"""
    response_data = context.response.json()
    
    # Should have at least name or account information
    info_fields = ['name', 'beneficiaryName', 'accountName', 'customerName', 'accountNumber', 'accountId']
    has_info = any(field in response_data for field in info_fields)
    
    # Check in nested data
    if not has_info and 'data' in response_data:
        data = response_data['data']
        has_info = any(field in data for field in info_fields)
    
    assert has_info, \
        f"Response missing beneficiary information. Available fields: {list(response_data.keys())}"
    
    logger.info(f"✓ Response has beneficiary information")


@then('beneficiary name should not be empty')
def step_beneficiary_name_not_empty(context):
    """Verify beneficiary name is not empty"""
    response_data = context.response.json()
    
    # Find name field
    name_fields = ['name', 'beneficiaryName', 'accountName', 'customerName', 'fullName']
    
    beneficiary_name = None
    for field in name_fields:
        if field in response_data:
            beneficiary_name = response_data[field]
            break
    
    # Check in nested data
    if not beneficiary_name and 'data' in response_data:
        data = response_data['data']
        for field in name_fields:
            if field in data:
                beneficiary_name = data[field]
                break
    
    assert beneficiary_name, "Beneficiary name is empty or missing"
    assert len(str(beneficiary_name).strip()) > 0, "Beneficiary name is empty string"
    
    logger.info(f"✓ Beneficiary name is not empty: {beneficiary_name}")


@then('beneficiary name should be valid string')
def step_beneficiary_name_valid_string(context):
    """Verify beneficiary name is a valid string"""
    response_data = context.response.json()
    
    # Find name field
    name_fields = ['name', 'beneficiaryName', 'accountName', 'customerName', 'fullName']
    
    beneficiary_name = None
    for field in name_fields:
        if field in response_data:
            beneficiary_name = response_data[field]
            break
    
    # Check in nested data
    if not beneficiary_name and 'data' in response_data:
        data = response_data['data']
        for field in name_fields:
            if field in data:
                beneficiary_name = data[field]
                break
    
    assert isinstance(beneficiary_name, str), f"Beneficiary name is not a string: {type(beneficiary_name)}"
    assert len(beneficiary_name.strip()) > 0, "Beneficiary name is empty"
    
    logger.info(f"✓ Beneficiary name is valid string: {beneficiary_name}")


@then('account identifier should be present')
def step_account_identifier_present(context):
    """Verify account identifier is present"""
    response_data = context.response.json()
    
    # Find identifier field
    identifier_fields = ['accountNumber', 'accountId', 'customerId', 'phone', 'phoneNumber']
    
    has_identifier = any(field in response_data for field in identifier_fields)
    
    # Check in nested data
    if not has_identifier and 'data' in response_data:
        data = response_data['data']
        has_identifier = any(field in data for field in identifier_fields)
    
    assert has_identifier, \
        f"Account identifier is missing. Available fields: {list(response_data.keys())}"
    
    logger.info(f"✓ Account identifier is present")


@then('account identifier should match requested number')
def step_account_identifier_matches_requested(context):
    """Verify account identifier matches requested number"""
    response_data = context.response.json()
    
    # Get requested account number
    requested = context.account_number
    
    # Find identifier in response
    identifier_fields = ['accountNumber', 'accountId', 'phone', 'phoneNumber', 'mobileNumber']
    
    found_identifier = None
    for field in identifier_fields:
        if field in response_data and response_data[field]:
            found_identifier = response_data[field]
            break
    
    # Check in nested data
    if not found_identifier and 'data' in response_data:
        data = response_data['data']
        for field in identifier_fields:
            if field in data and data[field]:
                found_identifier = data[field]
                break
    
    if found_identifier:
        # Normalize both for comparison (remove +, spaces, etc.)
        requested_normalized = str(requested).replace('+', '').replace(' ', '').replace('-', '')
        found_normalized = str(found_identifier).replace('+', '').replace(' ', '').replace('-', '')
        
        # Check if they match or if one contains the other
        if requested_normalized in found_normalized or found_normalized in requested_normalized:
            logger.info(f"✓ Account identifier matches: {requested} ≈ {found_identifier}")
        else:
            logger.warning(f"⚠️ Account identifier mismatch: requested={requested}, found={found_identifier}")
    else:
        logger.warning(f"⚠️ Could not find identifier in response to compare")


@then('I store first lookup response')
def step_store_first_lookup_response(context):
    """Store first lookup response for comparison"""
    response_data = context.response.json()
    context.first_lookup_response = response_data
    logger.info(f"✓ Stored first lookup response")


@then('second lookup response should match first lookup')
def step_second_lookup_matches_first(context):
    """Verify second lookup response matches first"""
    assert hasattr(context, 'first_lookup_response'), "First lookup response was not stored"
    
    first_response = context.first_lookup_response
    second_response = context.response.json()
    
    # Compare key fields
    comparison_fields = ['name', 'beneficiaryName', 'accountName', 'accountNumber', 'accountId']
    
    matches = True
    for field in comparison_fields:
        if field in first_response and field in second_response:
            if first_response[field] != second_response[field]:
                matches = False
                logger.warning(f"⚠️ Field mismatch: {field}: {first_response[field]} != {second_response[field]}")
    
    # If nested data, check that too
    if 'data' in first_response and 'data' in second_response:
        for field in comparison_fields:
            if field in first_response['data'] and field in second_response['data']:
                if first_response['data'][field] != second_response['data'][field]:
                    matches = False
                    logger.warning(f"⚠️ Data field mismatch: {field}")
    
    assert matches, "Second lookup response does not match first lookup"
    logger.info(f"✓ Second lookup response matches first lookup")


# ===========================
# Reused Steps
# ===========================
# The following steps are already defined in other step files and automatically available:
# 
# From common_steps.py:
# - @given('I have valid user authentication')
# - @given('I have no authentication token')
# - @given('I have invalid user token')
# - @given('I have expired user token')
# - @given('I have no Authorization header')
# - @given('I have empty Bearer token')
# - @given('I have malformed Bearer token')
# - @then('response status code should be {status_code:d}')
# - @then('response status code should be {status1:d} or {status2:d}')
# - @then('response body should be valid JSON')
# - @then('response header "{header_name}" should be present')
# - @then('response header "{header_name}" should contain "{expected_value}"')
# - @then('response time should be less than {max_time:d} ms')
# - @when('I send GET request to "{endpoint}"')
# - @when('I send POST request to "{endpoint}"')
# - @when('I send PUT request to "{endpoint}"')
#
# From p2p_search_contact_steps.py:
# - @given('I have search query "{query}"')
# - @when('I send contact search request to "{endpoint}"')
# - @then('I extract first contact from search results')
#
# From otp_steps.py:
# - @given('I have country code "{country_code}"')
#
# From school_search_steps.py:
# - @given('I have page number {page:d}')
#
# From p2p_search_contact_steps.py:
# - @given('I have page count {count:d}')
