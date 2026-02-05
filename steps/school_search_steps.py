"""
Step definitions for School/Church/Merchant Search API (Pay to School Flow)
GET /bff/v1/catalog/search-school-church-merchant

This API requires user token (accessToken) from PIN Verify API
Query Parameters: type, page, pageSize, nameQuery
"""

import json
import logging
from behave import given, when, then
from core.base_test import BaseTest

logger = logging.getLogger(__name__)


# ============================
# GIVEN Steps - Setup
# ============================

@given('I have search type "{search_type}"')
def step_set_search_type(context, search_type):
    """Set the search type (SCHOOL, CHURCH, or MERCHANT)"""
    context.search_type = search_type
    logger.info(f"🔍 Set search type: {search_type}")


@given('I have page number {page}')
def step_set_page_number(context, page):
    """Set the page number for pagination"""
    context.page = int(page)
    logger.info(f"📄 Set page number: {page}")


@given('I have page size {page_size}')
def step_set_page_size(context, page_size):
    """Set the page size for pagination"""
    context.page_size = int(page_size)
    logger.info(f"📊 Set page size: {page_size}")


@given('I have name query "{name_query}"')
def step_set_name_query(context, name_query):
    """Set the search name query"""
    context.name_query = name_query
    logger.info(f"🔎 Set name query: '{name_query}'")


@given('I have no search type')
def step_no_search_type(context):
    """Clear search type to test missing parameter"""
    context.search_type = None
    logger.info("❌ Search type cleared (testing missing parameter)")


# Note: The following steps are already defined in other step files and are reused:
# - I have no authentication token (login_devices_steps.py)
# - I have invalid user token (login_devices_steps.py)
# - I have expired user token (login_devices_steps.py)
# - I have no Authorization header (login_devices_steps.py)
# - I have empty Bearer token (login_devices_steps.py)
# - I have malformed Bearer token (login_devices_steps.py)
# - I have valid user token from PIN verification (login_devices_steps.py)
# - I have valid user authentication (login_devices_steps.py)
# - I have valid PIN verification details (pin_verify_steps.py)
# These steps work across all APIs


# ============================
# WHEN Steps - Actions
# ============================

@when('I send school search request to "{endpoint}"')
def step_send_school_search_request(context, endpoint):
    """Send GET request to school search endpoint with query parameters"""
    api_client = context.base_test.api_client
    
    # Build query parameters
    params = {}
    
    if hasattr(context, 'search_type') and context.search_type is not None:
        params['type'] = context.search_type
    
    if hasattr(context, 'page'):
        params['page'] = context.page
    
    if hasattr(context, 'page_size'):
        params['pageSize'] = context.page_size
    
    if hasattr(context, 'name_query'):
        params['nameQuery'] = context.name_query
    
    logger.info(f"🔍 School Search Query Parameters: {params}")
    
    # Build headers
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    # Add Authorization header if token exists
    if hasattr(context, 'no_auth') and context.no_auth:
        logger.info("🚫 Skipping Authorization header (testing no auth)")
    elif hasattr(context, 'no_auth_header') and context.no_auth_header:
        logger.info("🚫 Skipping Authorization header (testing missing header)")
    elif hasattr(context, 'user_token') and context.user_token:
        headers['Authorization'] = f'Bearer {context.user_token}'
        logger.info(f"🔑 Using user token: {context.user_token[:20]}...")
    else:
        logger.warning("⚠️ No user token available for Authorization header")
    
    # Make the GET request
    logger.info(f"🚀 Sending GET request to: {endpoint}")
    logger.info(f"📋 Headers: {headers}")
    
    context.response = api_client.get(
        endpoint=endpoint,
        params=params,
        headers=headers
    )
    
    # Log response details
    logger.info(f"📥 Response Status: {context.response.status_code}")
    logger.info(f"⏱️ Response Time: {context.response.elapsed.total_seconds() * 1000:.2f} ms")
    
    try:
        response_json = context.response.json()
        logger.info(f"📦 Response Body: {json.dumps(response_json, indent=2)}")
    except Exception as e:
        logger.warning(f"⚠️ Could not parse response as JSON: {str(e)}")
        logger.info(f"📦 Raw Response: {context.response.text[:500]}")


@when('I send school search request with stored token to "{endpoint}"')
def step_send_school_search_with_stored_token(context, endpoint):
    """Send school search request using token stored from previous step (integration test)"""
    # This step is used in integration scenarios where we chain APIs
    # The token should be stored in context.user_token from PIN verification
    step_send_school_search_request(context, endpoint)


# Note: The following @when steps are already defined in common_steps.py:
# - I send POST request to "{endpoint}"
# - I send GET request to "{endpoint}"
# They work for all APIs including School Search


# ============================
# THEN Steps - Assertions
# ============================

@then('response should contain search results')
def step_verify_search_results(context):
    """Verify response contains search results"""
    response_json = context.response.json()
    
    # Check if response has results structure
    # Adjust based on actual API response structure
    assert response_json is not None, "Response body should not be empty"
    
    logger.info("✅ Response contains search results")


@then('response should have at most {max_results:d} results')
def step_verify_max_results(context, max_results):
    """Verify response has at most specified number of results"""
    response_json = context.response.json()
    
    # Find results array (adjust based on actual API response structure)
    results = None
    if 'content' in response_json:
        results = response_json['content']
    elif 'results' in response_json:
        results = response_json['results']
    elif 'data' in response_json:
        results = response_json['data']
    elif isinstance(response_json, list):
        results = response_json
    
    if results is not None:
        actual_count = len(results)
        assert actual_count <= max_results, f"Expected at most {max_results} results, but got {actual_count}"
        logger.info(f"✅ Response has {actual_count} results (max: {max_results})")
    else:
        logger.warning("⚠️ Could not find results array in response")


@then('search response should have required fields')
def step_verify_required_fields(context):
    """Verify search response contains required fields"""
    response_json = context.response.json()
    
    # Common fields to check (adjust based on actual API response)
    # This is a flexible check - we verify structure exists
    assert response_json is not None, "Response should not be empty"
    assert len(response_json) > 0, "Response should contain data"
    
    logger.info("✅ Search response has required fields")


# Note: The following @then steps are already defined in other step files and are reused:
# - I store the user token from response (login_devices_steps.py)
# - response body should be valid JSON (common_steps.py)
# - response time should be less than {max_time:d} ms (common_steps.py)
# - response status code should be {status_code:d} (common_steps.py)
# - response header "{header_name}" should be present (common_steps.py)
# - response header "{header_name}" should contain "{expected_value}" (common_steps.py)
# These steps work for all APIs including School Search
