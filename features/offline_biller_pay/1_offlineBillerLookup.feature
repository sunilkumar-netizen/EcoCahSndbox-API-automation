Feature: Offline Biller Lookup
    As a user
    I want to lookup offline billers by merchant code
    So that I can get biller details for bill payments

    # NOTE: Offline Biller Lookup API requires user token (accessToken) from PIN Verify API
    # Endpoint: GET /bff/v1/catalog/merchant-lookup?merCode={merchantCode}
    # Query Parameters: merCode (merchant code)
    # Response: Returns biller details including name, code, category, and payment information

    Background:
        Given API is available
        And I am authenticated with valid app token
        And I have valid user token from PIN verification

    @smoke @offline_biller_lookup @offline_biller_pay @sasai
    Scenario: Lookup offline biller with valid merchant code
        Given I have valid user authentication
        And I have merchant code "8002"
        When I send offline biller lookup request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And response body should be valid JSON
        And response should contain biller details
        And response should have merchant code
        And response should have merchant name

    @offline_biller_lookup @positive @offline_biller_pay @sasai
    Scenario: Lookup offline biller with different valid merchant codes
        Given I have valid user authentication
        And I have merchant code "8002"
        When I send offline biller lookup request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And response should contain biller details

    @offline_biller_lookup @positive @offline_biller_pay @sasai
    Scenario: Verify offline biller response structure
        Given I have valid user authentication
        And I have merchant code "8002"
        When I send offline biller lookup request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And response body should be valid JSON
        And response should have required biller fields

    @offline_biller_lookup @positive @offline_biller_pay @sasai
    Scenario: Extract offline biller details for payment
        Given I have valid user authentication
        And I have merchant code "8002"
        When I send offline biller lookup request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And I extract merchant name from response
        And I extract merchant code from response
        And extracted merchant details should not be empty

    @offline_biller_lookup @negative @offline_biller_pay @sasai
    Scenario: Lookup offline biller without authentication
        Given I have no authentication token
        And I have merchant code "8002"
        When I send offline biller lookup request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 401

    @offline_biller_lookup @negative @offline_biller_pay @sasai
    Scenario: Lookup offline biller with invalid user token
        Given I have invalid user token
        And I have merchant code "8002"
        When I send offline biller lookup request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 401

    @offline_biller_lookup @negative @offline_biller_pay @sasai
    Scenario: Lookup offline biller with expired user token
        Given I have expired user token
        And I have merchant code "8002"
        When I send offline biller lookup request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 401

    @offline_biller_lookup @negative @offline_biller_pay @sasai
    Scenario: Lookup offline biller with app token only
        Given I have app token only
        And I have merchant code "8002"
        When I send offline biller lookup request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 401 or 403

    @offline_biller_lookup @negative @offline_biller_pay @sasai
    Scenario: Lookup offline biller without merchant code
        Given I have valid user authentication
        When I send offline biller lookup request without merchant code to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 400

    @offline_biller_lookup @negative @offline_biller_pay @sasai
    Scenario: Lookup offline biller with empty merchant code
        Given I have valid user authentication
        And I have merchant code ""
        When I send offline biller lookup request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 400

    @offline_biller_lookup @negative @offline_biller_pay @sasai
    Scenario: Lookup offline biller with invalid merchant code
        Given I have valid user authentication
        And I have merchant code "INVALID999"
        When I send offline biller lookup request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 404

    @offline_biller_lookup @negative @offline_biller_pay @sasai
    Scenario: Lookup offline biller with non-existent merchant code
        Given I have valid user authentication
        And I have merchant code "999999"
        When I send offline biller lookup request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 404

    @offline_biller_lookup @negative @offline_biller_pay @sasai
    Scenario: Lookup offline biller with special characters in merchant code
        Given I have valid user authentication
        And I have merchant code "@#$%^&"
        When I send offline biller lookup request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 400 or 404

    @offline_biller_lookup @validation @offline_biller_pay @sasai
    Scenario: Verify offline biller response contains merchant information
        Given I have valid user authentication
        And I have merchant code "8002"
        When I send offline biller lookup request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And response should contain merchant name
        And response should contain merchant code
        And response should contain category information

    @offline_biller_lookup @validation @offline_biller_pay @sasai
    Scenario: Verify offline biller response format
        Given I have valid user authentication
        And I have merchant code "8002"
        When I send offline biller lookup request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And merchant code format should be valid
        And merchant name should not be empty

    @offline_biller_lookup @headers @validation @offline_biller_pay @sasai
    Scenario: Verify offline biller lookup response headers
        Given I have valid user authentication
        And I have merchant code "8002"
        When I send offline biller lookup request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And response header "Content-Type" should be present
        And response header "Content-Type" should contain "application/json"

    @offline_biller_lookup @security @offline_biller_pay @sasai
    Scenario: Verify offline biller lookup with missing Authorization header
        Given I have no Authorization header
        And I have merchant code "8002"
        When I send offline biller lookup request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 401

    @offline_biller_lookup @security @offline_biller_pay @sasai
    Scenario: Verify offline biller lookup with empty Bearer token
        Given I have empty Bearer token
        And I have merchant code "8002"
        When I send offline biller lookup request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 401

    @offline_biller_lookup @security @offline_biller_pay @sasai
    Scenario: Verify offline biller lookup with malformed Bearer token
        Given I have malformed Bearer token
        And I have merchant code "8002"
        When I send offline biller lookup request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 401

    @offline_biller_lookup @error_handling @offline_biller_pay @sasai
    Scenario: Offline biller lookup with invalid HTTP method POST
        Given I have valid user authentication
        And I have merchant code "8002"
        When I send POST request to "/bff/v1/catalog/merchant-lookup?merCode=8002"
        Then response status code should be 405

    @offline_biller_lookup @error_handling @offline_biller_pay @sasai
    Scenario: Offline biller lookup with invalid HTTP method PUT
        Given I have valid user authentication
        And I have merchant code "8002"
        When I send PUT request to "/bff/v1/catalog/merchant-lookup?merCode=8002"
        Then response status code should be 405

    @offline_biller_lookup @error_handling @offline_biller_pay @sasai
    Scenario: Offline biller lookup with invalid HTTP method DELETE
        Given I have valid user authentication
        And I have merchant code "8002"
        When I send DELETE request to "/bff/v1/catalog/merchant-lookup?merCode=8002"
        Then response status code should be 405

    @offline_biller_lookup @error_handling @offline_biller_pay @sasai
    Scenario: Offline biller lookup with wrong endpoint path
        Given I have valid user authentication
        And I have merchant code "8002"
        When I send GET request to "/bff/v1/catalog/merchant-search?merCode=8002"
        Then response status code should be 404

    @offline_biller_lookup @performance @offline_biller_pay @sasai
    Scenario: Verify offline biller lookup response time
        Given I have valid user authentication
        And I have merchant code "8002"
        When I send offline biller lookup request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And response time should be less than 3000 ms

    @offline_biller_lookup @performance @offline_biller_pay @sasai
    Scenario: Verify offline biller lookup response time is acceptable
        Given I have valid user authentication
        And I have merchant code "8002"
        When I send offline biller lookup request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And response time should be less than 5000 ms

    @offline_biller_lookup @integration @offline_biller_pay @sasai
    Scenario: Complete flow - Offline biller lookup to payment preparation
        Given I have valid user authentication
        And I have merchant code "8002"
        When I send offline biller lookup request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And I extract merchant name from response
        And I extract merchant code from response
        And I store biller details for payment

    @offline_biller_lookup @data_validation @offline_biller_pay @sasai
    Scenario: Verify offline biller details completeness
        Given I have valid user authentication
        And I have merchant code "8002"
        When I send offline biller lookup request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And biller details should be complete
        And biller details should have valid format

    @offline_biller_lookup @merchant_code @offline_biller_pay @sasai
    Scenario Outline: Lookup offline biller with different merchant codes
        Given I have valid user authentication
        And I have merchant code "<merchantCode>"
        When I send offline biller lookup request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be <statusCode>

        Examples:
            | merchantCode | statusCode |
            | 8002         | 200        |
            | 8001         | 200 or 404 |
            | 8003         | 200 or 404 |
            | 0001         | 200 or 404 |
