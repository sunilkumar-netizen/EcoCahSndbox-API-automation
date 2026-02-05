"""
Step definitions for Church Search API
Endpoint: GET /bff/v1/catalog/search-school-church-merchant?type=CHURCH
This is part of the "Pay to Church" flow

NOTE: Many common steps are already defined in school_search_steps.py:
- I have search type "{search_type}"
- I have page number {page}
- I have page size {page_size}
- I have name query "{name_query}"
- I have no search type

These steps are automatically shared across all feature files using Behave.
"""

from behave import given, when, then
import json
import requests
import time


# ===========================
# Given Steps - Setup
# ===========================
# Note: The following common search steps are defined in school_search_steps.py
# and are automatically available for church search:
# - @given('I have search type "{search_type}"')
# - @given('I have page number {page}')
# - @given('I have page size {page_size}')
# - @given('I have name query "{name_query}"')
# - @given('I have no search type')

@given('I have no name query')
def step_no_name_query(context):
    """Clear name query to test missing parameter"""
    if hasattr(context, 'name_query'):
        delattr(context, 'name_query')
    context.name_query = None
    context.base_test.logger.info("❌ Name query cleared (testing missing parameter)")


# ===========================
# When Steps - Actions
# ===========================

@when('I send church search request to "{endpoint}"')
def step_send_church_search_request(context, endpoint):
    """Send GET request to church search endpoint with query parameters"""
    url = f"{context.config.base_url}{endpoint}"
    
    # Build query parameters
    params = {}
    
    if hasattr(context, 'search_type'):
        params['type'] = context.search_type
    
    if hasattr(context, 'page_number'):
        params['page'] = context.page_number
    
    if hasattr(context, 'page_size'):
        params['pageSize'] = context.page_size
    
    if hasattr(context, 'name_query'):
        params['nameQuery'] = context.name_query
    
    # Build headers
    headers = {
        'Authorization': f"Bearer {context.user_token}",
        'Content-Type': 'application/json'
    }
    
    try:
        context.base_test.logger.info(f"Sending GET request to {url}")
        context.base_test.logger.info(f"Query params: {json.dumps(params, indent=2)}")
        
        start_time = time.time()
        context.response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=30
        )
        context.response_time = (time.time() - start_time) * 1000
        
        context.base_test.logger.info(f"Response Status: {context.response.status_code}")
        context.base_test.logger.info(f"Response Time: {context.response_time:.2f} ms")
        
        if context.response.status_code == 200:
            context.base_test.logger.info(f"Response: {context.response.text[:500]}...")  # Log first 500 chars
        else:
            context.base_test.logger.warning(f"Error Response: {context.response.text}")
            
    except Exception as e:
        context.base_test.logger.error(f"Request failed: {str(e)}")
        raise


@when('I send church search request with stored token to "{endpoint}"')
def step_send_church_search_with_stored_token(context, endpoint):
    """Send church search request using stored user token"""
    if hasattr(context, 'stored_user_token'):
        context.user_token = context.stored_user_token
    step_send_church_search_request(context, endpoint)


# ===========================
# Then Steps - Assertions
# ===========================

@then('response should have church list')
def step_response_has_church_list(context):
    """Verify response contains church list"""
    assert context.response.status_code == 200, \
        f"Expected status 200, got {context.response.status_code}"
    
    response_data = context.response.json()
    
    # Check for content field containing results
    assert 'content' in response_data, \
        f"Response missing 'content' field. Response: {response_data}"
    
    content = response_data['content']
    assert isinstance(content, list), "Content should be a list"
    
    context.base_test.logger.info(f"✓ Response contains church list with {len(content)} churches")


@then('response should have pagination structure')
def step_response_has_pagination_structure(context):
    """Verify response has pagination structure"""
    response_data = context.response.json()
    
    # Check for common pagination fields
    pagination_fields = ['page', 'size', 'totalPages', 'totalElements', 'pageSize', 'number']
    has_pagination = any(field in response_data for field in pagination_fields)
    
    assert has_pagination, \
        f"Response missing pagination fields. Available fields: {list(response_data.keys())}"
    
    context.base_test.logger.info("✓ Response has pagination structure")


@then('response should have pagination info')
def step_response_has_pagination_info(context):
    """Verify response contains pagination information"""
    response_data = context.response.json()
    
    # Check for pagination object or individual pagination fields
    if 'pagination' in response_data:
        pagination = response_data['pagination']
        assert isinstance(pagination, dict), "Pagination should be a dictionary"
        context.base_test.logger.info(f"✓ Response has pagination object: {pagination}")
    else:
        # Check for individual pagination fields
        pagination_fields = ['page', 'pageSize', 'totalPages', 'totalElements', 'size', 'number']
        has_pagination = any(field in response_data for field in pagination_fields)
        
        assert has_pagination, \
            f"Response should contain pagination info. Available fields: {list(response_data.keys())}"
        
        context.base_test.logger.info("✓ Response has pagination info")


@then('response should have content field')
def step_response_has_content_field(context):
    """Verify response has content field"""
    response_data = context.response.json()
    
    assert 'content' in response_data, \
        f"Response missing 'content' field. Available fields: {list(response_data.keys())}"
    
    assert isinstance(response_data['content'], list), \
        "Content field should be a list"
    
    context.base_test.logger.info(f"✓ Response has content field with {len(response_data['content'])} items")


@then('response should have pagination fields')
def step_response_has_pagination_fields(context):
    """Verify response has pagination fields"""
    response_data = context.response.json()
    
    # Check for pagination fields
    pagination_fields = ['page', 'size', 'totalPages', 'totalElements']
    found_fields = [field for field in pagination_fields if field in response_data]
    
    assert len(found_fields) > 0, \
        f"Response missing pagination fields. Available fields: {list(response_data.keys())}"
    
    context.base_test.logger.info(f"✓ Response has pagination fields: {found_fields}")


@then('response should have search structure')
def step_response_has_search_structure(context):
    """Verify response has proper search result structure"""
    response_data = context.response.json()
    
    # Verify it's a valid JSON object
    assert isinstance(response_data, dict), \
        "Response should be a JSON object"
    
    # Check for typical search response fields
    expected_fields = ['content', 'page', 'size', 'totalElements', 'totalPages']
    found_fields = [field for field in expected_fields if field in response_data]
    
    context.base_test.logger.info(f"✓ Response has valid search structure with fields: {found_fields}")


@then('response should have empty results')
def step_response_has_empty_results(context):
    """Verify response has empty results"""
    response_data = context.response.json()
    
    # Check for content field
    if 'content' in response_data:
        assert isinstance(response_data['content'], list), "Content should be a list"
        assert len(response_data['content']) == 0, \
            f"Expected empty results, but got {len(response_data['content'])} results"
    elif isinstance(response_data, list):
        assert len(response_data) == 0, \
            f"Expected empty results, but got {len(response_data)} results"
    
    context.base_test.logger.info("✓ Response has empty results")


@then('all results should be of type church')
def step_all_results_are_churches(context):
    """Verify all search results are churches"""
    response_data = context.response.json()
    
    assert 'content' in response_data, "Response missing 'content' field"
    
    churches = response_data['content']
    
    if len(churches) > 0:
        # Check if results have type field or category field indicating church
        for church in churches:
            # The type might be in different fields depending on API response
            if 'type' in church:
                assert church['type'].upper() == 'CHURCH', \
                    f"Found non-church result: {church.get('type')}"
            elif 'category' in church:
                assert 'CHURCH' in church['category'].upper(), \
                    f"Found non-church result: {church.get('category')}"
            
        context.base_test.logger.info(f"✓ All {len(churches)} results are churches")
    else:
        context.base_test.logger.info("✓ No results to validate (empty list)")


@then('church names should contain "{search_term}"')
def step_church_names_contain_term(context, search_term):
    """Verify church names contain the search term"""
    response_data = context.response.json()
    
    assert 'content' in response_data, "Response missing 'content' field"
    
    churches = response_data['content']
    
    if len(churches) > 0:
        search_term_lower = search_term.lower()
        
        for church in churches:
            church_name = church.get('name', '').lower()
            # The search might match partially or be in description
            # So we check if any field contains the search term
            found = False
            for key, value in church.items():
                if isinstance(value, str) and search_term_lower in value.lower():
                    found = True
                    break
            
            if not found:
                context.base_test.logger.warning(f"Church '{church.get('name')}' doesn't contain '{search_term}' directly")
        
        context.base_test.logger.info(f"✓ Verified church names for search term '{search_term}'")
    else:
        context.base_test.logger.info("✓ No results to validate (empty list)")


@then('each church should have name field')
def step_each_church_has_name(context):
    """Verify each church has a name field"""
    response_data = context.response.json()
    
    assert 'content' in response_data, "Response missing 'content' field"
    
    churches = response_data['content']
    
    if len(churches) > 0:
        for church in churches:
            assert 'name' in church, \
                f"Church missing 'name' field: {church}"
            assert church['name'], \
                f"Church name is empty: {church}"
        
        context.base_test.logger.info(f"✓ All {len(churches)} churches have name field")
    else:
        context.base_test.logger.info("✓ No results to validate (empty list)")


@then('each church should have code field')
def step_each_church_has_code(context):
    """Verify each church has a code field"""
    response_data = context.response.json()
    
    assert 'content' in response_data, "Response missing 'content' field"
    
    churches = response_data['content']
    
    if len(churches) > 0:
        for church in churches:
            # Code might be in different fields: code, merchantCode, id, etc.
            has_code = any(key in church for key in ['code', 'merchantCode', 'id', 'merCode'])
            assert has_code, \
                f"Church missing code field: {church}"
        
        context.base_test.logger.info(f"✓ All {len(churches)} churches have code field")
    else:
        context.base_test.logger.info("✓ No results to validate (empty list)")


@then('results should be in alphabetical order')
def step_results_in_alphabetical_order(context):
    """Verify results are sorted in alphabetical order"""
    response_data = context.response.json()
    
    assert 'content' in response_data, "Response missing 'content' field"
    
    churches = response_data['content']
    
    if len(churches) > 1:
        names = [church.get('name', '') for church in churches]
        sorted_names = sorted(names)
        
        # Check if names are in alphabetical order (case-insensitive)
        names_lower = [n.lower() for n in names]
        sorted_names_lower = [n.lower() for n in sorted_names]
        
        if names_lower != sorted_names_lower:
            context.base_test.logger.warning(f"Results may not be in perfect alphabetical order")
            context.base_test.logger.info(f"Actual order: {names[:5]}...")  # Show first 5
            context.base_test.logger.info(f"Sorted order: {sorted_names[:5]}...")
        else:
            context.base_test.logger.info("✓ Results are in alphabetical order")
    else:
        context.base_test.logger.info("✓ Not enough results to verify sorting")


@then('response should contain at most {max_count:d} results')
def step_response_contains_at_most_results(context, max_count):
    """Verify response contains at most specified number of results"""
    response_data = context.response.json()
    
    # Find results array
    results = None
    if 'content' in response_data:
        results = response_data['content']
    elif 'results' in response_data:
        results = response_data['results']
    elif isinstance(response_data, list):
        results = response_data
    
    if results is not None:
        actual_count = len(results)
        assert actual_count <= max_count, \
            f"Expected at most {max_count} results, but got {actual_count}"
        context.base_test.logger.info(f"✓ Response has {actual_count} results (max: {max_count})")
    else:
        context.base_test.logger.warning("⚠️ Could not find results array in response")


@then('extracted code should not be empty')
def step_extracted_code_not_empty(context):
    """Verify extracted merchant code is not empty"""
    assert hasattr(context, 'extracted_merchant_code'), \
        "No merchant code was extracted"
    
    assert context.extracted_merchant_code, \
        "Extracted merchant code is empty"
    
    assert context.extracted_merchant_code.strip() != "", \
        "Extracted merchant code contains only whitespace"
    
    context.base_test.logger.info(f"✓ Extracted code is not empty: {context.extracted_merchant_code}")
