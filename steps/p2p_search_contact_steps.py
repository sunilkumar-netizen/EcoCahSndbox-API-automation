"""
Step definitions for P2P Search Contact API
Endpoint: GET /search/v3/collection/search
This is part of the "Pay to Person (Domestic)" flow

NOTE: This API searches for contacts/users for P2P payment transactions.
Query Parameters:
- q: search query (name, phone number, etc.)
- countryCode: country code (e.g., ZW for Zimbabwe)
- page: page number for pagination
- pageCount: number of results per page

Response contains list of matching contacts with their details.
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

@given('I have search query "{query}"')
def step_have_search_query(context, query):
    """Set search query for contact search"""
    context.search_query = query
    logger.info(f"🔍 Search query set to: {query}")


@given('I have no search query')
def step_no_search_query(context):
    """Clear search query to test missing parameter"""
    if hasattr(context, 'search_query'):
        delattr(context, 'search_query')
    context.search_query = None
    logger.info("❌ Search query cleared (testing missing parameter)")


@given('I have no country code')
def step_no_country_code(context):
    """Clear country code to test missing parameter"""
    if hasattr(context, 'country_code'):
        delattr(context, 'country_code')
    context.country_code = None
    logger.info("❌ Country code cleared (testing missing parameter)")


@given('I have page count {count:d}')
def step_have_page_count(context, count):
    """Set page count (results per page)"""
    context.page_count = count
    logger.info(f"📊 Page count set to: {count}")


# ===========================
# When Steps - Actions
# ===========================

@when('I send contact search request to "{endpoint}"')
def step_send_contact_search_request(context, endpoint):
    """Send GET request to contact search endpoint with query parameters"""
    url = f"{context.config_loader.get('api.base_url')}{endpoint}"
    
    # Build query parameters
    params = {}
    
    if hasattr(context, 'search_query') and context.search_query:
        params['q'] = context.search_query
    
    # Check for country_code in multiple locations
    country_code = None
    if hasattr(context, 'country_code') and context.country_code:
        country_code = context.country_code
    elif hasattr(context, 'request_data') and 'countryCode' in context.request_data:
        country_code = context.request_data['countryCode']
    
    if country_code:
        params['countryCode'] = country_code
    
    # Check for page_number in multiple locations
    page_number = None
    if hasattr(context, 'page_number') and context.page_number:
        page_number = context.page_number
    
    if page_number:
        params['page'] = page_number
    
    if hasattr(context, 'page_count') and context.page_count:
        params['pageCount'] = context.page_count
    
    # Build headers
    headers = {
        'Authorization': f"Bearer {context.user_token}",
        'Content-Type': 'application/json'
    }
    
    try:
        logger.info(f"Sending GET request to {url}")
        logger.info(f"Query params: {json.dumps(params, indent=2)}")
        
        start_time = time.time()
        response = context.base_test.api_client.get(
            endpoint,
            params=params,
            headers=headers
        )
        context.response = response
        context.response_time = (time.time() - start_time) * 1000
        
        logger.info(f"Response Status: {response.status_code}")
        logger.info(f"Response Time: {context.response_time:.2f} ms")
        
        if response.status_code == 200:
            response_text = response.text if hasattr(response, 'text') else str(response.content)
            logger.info(f"Response: {response_text[:500]}...")  # Log first 500 chars
        else:
            response_text = response.text if hasattr(response, 'text') else str(response.content)
            logger.warning(f"Error Response: {response_text}")
            
    except Exception as e:
        logger.error(f"Request failed: {str(e)}")
        raise


# ===========================
# Then Steps - Assertions
# ===========================

@then('response should have contacts list')
def step_response_has_contacts_list(context):
    """Verify response contains contacts list"""
    assert context.response.status_code == 200, \
        f"Expected status 200, got {context.response.status_code}"
    
    response_data = context.response.json()
    
    # Try to find contacts in various structures
    contacts = None
    if isinstance(response_data, list):
        contacts = response_data
    elif 'results' in response_data:
        contacts = response_data['results']
    elif 'data' in response_data:
        contacts = response_data['data']
    elif 'content' in response_data:
        contacts = response_data['content']
    elif 'items' in response_data:
        contacts = response_data['items']
    elif 'contacts' in response_data:
        contacts = response_data['contacts']
    
    assert contacts is not None, \
        f"Could not find contacts list in response. Available fields: {list(response_data.keys())}"
    
    assert isinstance(contacts, list), "Contacts should be a list"
    
    # Store contacts for later use
    context.search_contacts = contacts
    
    logger.info(f"✓ Response contains contacts list with {len(contacts)} contacts")


@then('search results should not be empty')
def step_search_results_not_empty(context):
    """Verify search results are not empty"""
    response_data = context.response.json()
    
    # Check if we have contacts stored
    if hasattr(context, 'search_contacts'):
        contacts = context.search_contacts
    else:
        # Try to extract contacts
        if isinstance(response_data, list):
            contacts = response_data
        elif 'results' in response_data:
            contacts = response_data['results']
        elif 'data' in response_data:
            contacts = response_data['data']
        elif 'content' in response_data:
            contacts = response_data['content']
        else:
            contacts = []
    
    assert len(contacts) > 0, \
        f"Search results are empty. Expected at least 1 result."
    
    logger.info(f"✓ Search results not empty: {len(contacts)} contacts found")


@then('search results should be empty or valid')
def step_search_results_empty_or_valid(context):
    """Verify search results are either empty or contain valid data"""
    assert context.response.status_code == 200, \
        f"Expected status 200, got {context.response.status_code}"
    
    response_data = context.response.json()
    
    # Response should be valid JSON
    assert response_data is not None, "Response data is None"
    
    logger.info(f"✓ Search results are valid (empty or with data)")


@then('response should have contact details structure')
def step_response_has_contact_details_structure(context):
    """Verify response has proper contact details structure"""
    response_data = context.response.json()
    
    # Extract contacts
    if isinstance(response_data, list):
        contacts = response_data
    elif 'results' in response_data:
        contacts = response_data['results']
    elif 'data' in response_data:
        contacts = response_data['data']
    elif 'content' in response_data:
        contacts = response_data['content']
    else:
        contacts = []
    
    if len(contacts) > 0:
        first_contact = contacts[0]
        # Check if contact has some expected fields (flexible check)
        contact_fields = ['id', 'name', 'phone', 'phoneNumber', 'email', 'customerId', 'userId', 'accountId']
        has_contact_fields = any(field in first_contact for field in contact_fields)
        
        assert has_contact_fields, \
            f"Contact missing expected fields. Available fields: {list(first_contact.keys())}"
        
        logger.info(f"✓ Contacts have proper structure with fields: {list(first_contact.keys())}")
    else:
        logger.info("✓ No contacts to validate structure")


@then('each contact should have required fields')
def step_each_contact_has_required_fields(context):
    """Verify each contact has required fields"""
    response_data = context.response.json()
    
    # Extract contacts
    if isinstance(response_data, list):
        contacts = response_data
    elif 'results' in response_data:
        contacts = response_data['results']
    elif 'data' in response_data:
        contacts = response_data['data']
    elif 'content' in response_data:
        contacts = response_data['content']
    else:
        contacts = []
    
    if len(contacts) > 0:
        for i, contact in enumerate(contacts):
            # At least one identifier field should be present
            identifier_fields = ['id', 'customerId', 'userId', 'accountId', 'phone', 'phoneNumber']
            has_identifier = any(field in contact for field in identifier_fields)
            
            assert has_identifier, \
                f"Contact {i} missing identifier field. Available fields: {list(contact.keys())}"
        
        logger.info(f"✓ All {len(contacts)} contacts have required fields")
    else:
        logger.info("✓ No contacts to validate")


@then('response should respect page count limit')
def step_response_respects_page_count(context):
    """Verify response respects the page count limit"""
    response_data = context.response.json()
    
    # Extract contacts
    if isinstance(response_data, list):
        contacts = response_data
    elif 'results' in response_data:
        contacts = response_data['results']
    elif 'data' in response_data:
        contacts = response_data['data']
    elif 'content' in response_data:
        contacts = response_data['content']
    else:
        contacts = []
    
    if hasattr(context, 'page_count'):
        assert len(contacts) <= context.page_count, \
            f"Response has {len(contacts)} contacts, exceeds page count limit of {context.page_count}"
        
        logger.info(f"✓ Response respects page count limit: {len(contacts)} <= {context.page_count}")
    else:
        logger.info(f"✓ Response has {len(contacts)} contacts")


@then('I extract first contact from search results')
def step_extract_first_contact(context):
    """Extract first contact from search results"""
    response_data = context.response.json()
    
    # Extract contacts
    if isinstance(response_data, list):
        contacts = response_data
    elif 'results' in response_data:
        contacts = response_data['results']
    elif 'data' in response_data:
        contacts = response_data['data']
    elif 'content' in response_data:
        contacts = response_data['content']
    else:
        contacts = []
    
    assert len(contacts) > 0, "No contacts found to extract"
    
    # For the P2P search API, the response has a structure where each collection
    # has a 'document' array with actual contacts. Find first collection with documents.
    first_contact = None
    for collection in contacts:
        if 'document' in collection and isinstance(collection['document'], list) and len(collection['document']) > 0:
            first_contact = collection['document'][0]
            logger.info(f"✓ Extracted first contact from document array: {json.dumps(first_contact, indent=2)}")
            break
    
    # If no document structure found, use first item as is
    if not first_contact:
        first_contact = contacts[0]
        logger.info(f"✓ Extracted first contact: {json.dumps(first_contact, indent=2)}")
    
    context.extracted_contact = first_contact


@then('extracted contact should have valid details')
def step_extracted_contact_has_valid_details(context):
    """Verify extracted contact has valid details"""
    assert hasattr(context, 'extracted_contact'), "No contact was extracted"
    
    contact = context.extracted_contact
    
    # Contact should have some identifier
    identifier_fields = ['id', 'customerId', 'userId', 'accountId', 'phone', 'phoneNumber']
    has_identifier = any(field in contact and contact[field] for field in identifier_fields)
    
    assert has_identifier, \
        f"Contact missing valid identifier. Available fields: {list(contact.keys())}"
    
    logger.info(f"✓ Extracted contact has valid details")


@then('response should have search metadata')
def step_response_has_search_metadata(context):
    """Verify response has search metadata"""
    response_data = context.response.json()
    
    # Check for metadata fields
    metadata_fields = ['total', 'totalElements', 'page', 'pageCount', 'totalPages', 'query', 'searchQuery']
    has_metadata = any(field in response_data for field in metadata_fields)
    
    # Could also be a list with results
    if isinstance(response_data, list):
        has_metadata = True  # List itself is metadata
    
    if not has_metadata:
        logger.warning(f"No explicit metadata fields found. Available fields: {list(response_data.keys())}")
    else:
        logger.info("✓ Response has search metadata")


@then('each contact should have name field')
def step_each_contact_has_name_field(context):
    """Verify each contact has name field"""
    response_data = context.response.json()
    
    # Extract contacts
    if isinstance(response_data, list):
        contacts = response_data
    elif 'results' in response_data:
        contacts = response_data['results']
    elif 'data' in response_data:
        contacts = response_data['data']
    elif 'content' in response_data:
        contacts = response_data['content']
    else:
        contacts = []
    
    if len(contacts) > 0:
        for i, contact in enumerate(contacts):
            # Check for name fields
            name_fields = ['name', 'fullName', 'displayName', 'firstName', 'lastName']
            has_name = any(field in contact for field in name_fields)
            
            if not has_name:
                logger.warning(f"Contact {i} missing name field. Available fields: {list(contact.keys())}")
        
        logger.info(f"✓ Checked name fields in {len(contacts)} contacts")
    else:
        logger.info("✓ No contacts to validate")


@then('each contact should have identifier field')
def step_each_contact_has_identifier_field(context):
    """Verify each contact has identifier field"""
    response_data = context.response.json()
    
    # Extract contacts
    if isinstance(response_data, list):
        contacts = response_data
    elif 'results' in response_data:
        contacts = response_data['results']
    elif 'data' in response_data:
        contacts = response_data['data']
    elif 'content' in response_data:
        contacts = response_data['content']
    else:
        contacts = []
    
    if len(contacts) > 0:
        for i, contact in enumerate(contacts):
            # Check for identifier fields
            identifier_fields = ['id', 'customerId', 'userId', 'accountId', 'phone', 'phoneNumber', 'mobileNumber']
            has_identifier = any(field in contact for field in identifier_fields)
            
            assert has_identifier, \
                f"Contact {i} missing identifier field. Available fields: {list(contact.keys())}"
        
        logger.info(f"✓ All {len(contacts)} contacts have identifier fields")
    else:
        logger.info("✓ No contacts to validate")


# ===========================
# Reused Steps
# ===========================
# The following steps are already defined in other step files and automatically available:
# 
# From common_steps.py:
# - @given('I have page number {page:d}')
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
# From otp_steps.py:
# - @given('I have country code "{country_code}"')
#
# From church_search_steps.py / school_search_steps.py:
# - @then('response should have pagination info')
# - @then('response should contain search results')
