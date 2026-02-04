Feature: Sasai Payment Gateway - Merchant Lookup API Testing (Pay to Merchant)
    As a user
    I want to lookup merchant details from Sasai Payment Gateway API
    So that I can verify merchant information before making a payment

    # NOTE: Merchant Lookup API requires user token (accessToken) from PIN Verify API
    # This is part of the "Pay to Merchant" flow
    # Endpoint: GET /catalog/v1/categories/{categoryId}/operators/{operatorId}/lookup

    Background:
        Given API is available
        And I am authenticated with valid app token
        And I have valid user token from PIN verification

    @smoke @merchant_lookup @pay_to_merchant @sasai
    Scenario: Lookup merchant with valid parameters
        Given I have valid user authentication
        And I have merchant lookup parameters
        When I send merchant lookup request to "/catalog/v1/categories/SZWC10002/operators/SZWOM00001/lookup"
        Then response status code should be 200
        And response time should be less than 5000 ms
        And response should contain merchant details

    @merchant_lookup @positive @pay_to_merchant @sasai
    Scenario: Lookup merchant with all required query parameters
        Given I have valid user authentication
        And I have merchant category "SZWC10002"
        And I have operator ID "SZWOM00001"
        And I have country code "ZW"
        And I have merchant ID "52869750-4e6f-4bb9-9d45-cc401f0da123"
        And I have currency "USD"
        And I have Q1 value "001535"
        When I send merchant lookup request with query parameters
        Then response status code should be 200
        And response should contain merchant details

    @merchant_lookup @positive @pay_to_merchant @sasai
    Scenario: Lookup merchant with valid requestId header
        Given I have valid user authentication
        And I have merchant lookup parameters
        And I have request ID "bdefac7b-bbc0-48b4-9ef0-84e6b9b34a6f"
        When I send merchant lookup request to "/catalog/v1/categories/SZWC10002/operators/SZWOM00001/lookup"
        Then response status code should be 200
        And response should contain merchant details

    @merchant_lookup @negative @pay_to_merchant @sasai
    Scenario: Lookup merchant without authentication
        Given I have no authentication token
        And I have merchant lookup parameters
        When I send merchant lookup request to "/catalog/v1/categories/SZWC10002/operators/SZWOM00001/lookup"
        Then response status code should be 401

    @merchant_lookup @negative @pay_to_merchant @sasai
    Scenario: Lookup merchant with app token instead of user token
        Given I have app token only
        And I have merchant lookup parameters
        When I send merchant lookup request to "/catalog/v1/categories/SZWC10002/operators/SZWOM00001/lookup"
        Then response status code should be 401 or 403

    @merchant_lookup @negative @pay_to_merchant @sasai
    Scenario: Lookup merchant with expired user token
        Given I have expired user token
        And I have merchant lookup parameters
        When I send merchant lookup request to "/catalog/v1/categories/SZWC10002/operators/SZWOM00001/lookup"
        Then response status code should be 401

    @merchant_lookup @negative @pay_to_merchant @sasai
    Scenario: Lookup merchant with invalid user token
        Given I have invalid user token
        And I have merchant lookup parameters
        When I send merchant lookup request to "/catalog/v1/categories/SZWC10002/operators/SZWOM00001/lookup"
        Then response status code should be 401

    @merchant_lookup @negative @pay_to_merchant @sasai
    Scenario: Lookup merchant with invalid category ID
        Given I have valid user authentication
        And I have invalid merchant category "INVALID_CAT"
        And I have operator ID "SZWOM00001"
        When I send merchant lookup request with query parameters
        Then response status code should be 400 or 404

    @merchant_lookup @negative @pay_to_merchant @sasai
    Scenario: Lookup merchant with invalid operator ID
        Given I have valid user authentication
        And I have merchant category "SZWC10002"
        And I have invalid operator ID "INVALID_OP"
        When I send merchant lookup request with query parameters
        Then response status code should be 400 or 404

    @merchant_lookup @negative @pay_to_merchant @sasai
    Scenario: Lookup merchant with missing country code
        Given I have valid user authentication
        And I have merchant lookup parameters without country code
        When I send merchant lookup request to "/catalog/v1/categories/SZWC10002/operators/SZWOM00001/lookup"
        Then response status code should be 400

    @merchant_lookup @negative @pay_to_merchant @sasai
    Scenario: Lookup merchant with invalid country code
        Given I have valid user authentication
        And I have merchant lookup parameters
        And I have invalid country code "XX"
        When I send merchant lookup request to "/catalog/v1/categories/SZWC10002/operators/SZWOM00001/lookup"
        Then response status code should be 400

    @merchant_lookup @negative @pay_to_merchant @sasai
    Scenario: Lookup merchant with missing merchant ID
        Given I have valid user authentication
        And I have merchant lookup parameters without merchant ID
        When I send merchant lookup request to "/catalog/v1/categories/SZWC10002/operators/SZWOM00001/lookup"
        Then response status code should be 400

    @merchant_lookup @negative @pay_to_merchant @sasai
    Scenario: Lookup merchant with invalid merchant ID
        Given I have valid user authentication
        And I have merchant lookup parameters
        And I have invalid merchant ID "invalid-merchant-id"
        When I send merchant lookup request to "/catalog/v1/categories/SZWC10002/operators/SZWOM00001/lookup"
        Then response status code should be 400 or 404

    @merchant_lookup @negative @pay_to_merchant @sasai
    Scenario: Lookup merchant with missing currency
        Given I have valid user authentication
        And I have merchant lookup parameters without currency
        When I send merchant lookup request to "/catalog/v1/categories/SZWC10002/operators/SZWOM00001/lookup"
        Then response status code should be 400

    @merchant_lookup @negative @pay_to_merchant @sasai
    Scenario: Lookup merchant with invalid currency
        Given I have valid user authentication
        And I have merchant lookup parameters
        And I have invalid currency "XXX"
        When I send merchant lookup request to "/catalog/v1/categories/SZWC10002/operators/SZWOM00001/lookup"
        Then response status code should be 400

    @merchant_lookup @negative @pay_to_merchant @sasai
    Scenario: Lookup merchant with missing Q1 parameter
        Given I have valid user authentication
        And I have merchant lookup parameters without Q1
        When I send merchant lookup request to "/catalog/v1/categories/SZWC10002/operators/SZWOM00001/lookup"
        Then response status code should be 400

    @merchant_lookup @validation @pay_to_merchant @sasai
    Scenario: Verify merchant lookup response structure
        Given I have valid user authentication
        And I have merchant lookup parameters
        When I send merchant lookup request to "/catalog/v1/categories/SZWC10002/operators/SZWOM00001/lookup"
        Then response status code should be 200
        And response body should be valid JSON
        And response should contain merchant information fields

    @merchant_lookup @validation @pay_to_merchant @sasai
    Scenario: Verify merchant lookup response contains required fields
        Given I have valid user authentication
        And I have merchant lookup parameters
        When I send merchant lookup request to "/catalog/v1/categories/SZWC10002/operators/SZWOM00001/lookup"
        Then response status code should be 200
        And merchant details should have required fields

    @merchant_lookup @headers @validation @pay_to_merchant @sasai
    Scenario: Verify merchant lookup response headers
        Given I have valid user authentication
        And I have merchant lookup parameters
        When I send merchant lookup request to "/catalog/v1/categories/SZWC10002/operators/SZWOM00001/lookup"
        Then response status code should be 200
        And response header "Content-Type" should be present
        And response header "Content-Type" should contain "application/json"

    @merchant_lookup @headers @validation @pay_to_merchant @sasai
    Scenario: Verify merchant lookup has required headers
        Given I have valid user authentication
        And I have merchant lookup parameters
        When I send merchant lookup request to "/catalog/v1/categories/SZWC10002/operators/SZWOM00001/lookup"
        Then response status code should be 200
        And response header "Content-Type" should not be empty
        And response header "Date" should be present

    @merchant_lookup @security @pay_to_merchant @sasai
    Scenario: Verify merchant lookup with missing Authorization header
        Given I have no Authorization header
        And I have merchant lookup parameters
        When I send merchant lookup request to "/catalog/v1/categories/SZWC10002/operators/SZWOM00001/lookup"
        Then response status code should be 401

    @merchant_lookup @security @pay_to_merchant @sasai
    Scenario: Verify merchant lookup with empty Bearer token
        Given I have empty Bearer token
        And I have merchant lookup parameters
        When I send merchant lookup request to "/catalog/v1/categories/SZWC10002/operators/SZWOM00001/lookup"
        Then response status code should be 401

    @merchant_lookup @security @pay_to_merchant @sasai
    Scenario: Verify merchant lookup without Bearer prefix
        Given I have token without Bearer prefix
        And I have merchant lookup parameters
        When I send merchant lookup request to "/catalog/v1/categories/SZWC10002/operators/SZWOM00001/lookup"
        Then response status code should be 401

    @merchant_lookup @security @pay_to_merchant @sasai
    Scenario: Verify merchant lookup with malformed Bearer token
        Given I have malformed Bearer token
        And I have merchant lookup parameters
        When I send merchant lookup request to "/catalog/v1/categories/SZWC10002/operators/SZWOM00001/lookup"
        Then response status code should be 401

    @merchant_lookup @error_handling @pay_to_merchant @sasai
    Scenario: Lookup merchant with invalid HTTP method
        Given I have valid user authentication
        And I have merchant lookup parameters
        When I send POST request to "/catalog/v1/categories/SZWC10002/operators/SZWOM00001/lookup"
        Then response status code should be 405

    @merchant_lookup @error_handling @pay_to_merchant @sasai
    Scenario: Lookup merchant with wrong endpoint path
        Given I have valid user authentication
        And I have merchant lookup parameters
        When I send GET request to "/catalog/v1/categories/SZWC10002/operators/SZWOM00001/lookups"
        Then response status code should be 404

    @merchant_lookup @performance @pay_to_merchant @sasai
    Scenario: Verify merchant lookup response time
        Given I have valid user authentication
        And I have merchant lookup parameters
        When I send merchant lookup request to "/catalog/v1/categories/SZWC10002/operators/SZWOM00001/lookup"
        Then response status code should be 200
        And response time should be less than 3000 ms

    @merchant_lookup @integration @pay_to_merchant @sasai
    Scenario: Complete flow - PIN Verify to Merchant Lookup
        Given I have valid PIN verification details
        When I send PIN verification request to "/bff/v4/auth/pin/verify"
        Then response status code should be 200
        And I store the user token from response
        Given I have merchant lookup parameters
        When I send merchant lookup request with stored token to "/catalog/v1/categories/SZWC10002/operators/SZWOM00001/lookup"
        Then response status code should be 200
        And response should contain merchant details
