Feature: School Search by Code
    As a user
    I want to search for schools by merchant code
    So that I can get school/church/merchant details for payments

    # NOTE: School Search by Code API requires user token (accessToken) from PIN Verify API
    # This is part of the "Pay to School" flow
    # Endpoint: GET /bff/v1/catalog/merchant-lookup
    # Query Parameters: merCode (merchant code)

    Background:
        Given API is available
        And I am authenticated with valid app token
        And I have valid user token from PIN verification

    @smoke @merchant_lookup_code @pay_to_school @sasai
    Scenario: Lookup merchant by valid code
        Given I have valid user authentication
        And I have merchant code "054329"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And response should contain merchant details by code
        And response should have merchant information

    @merchant_lookup_code @positive @pay_to_school @sasai
    Scenario: Lookup merchant by code returns correct structure
        Given I have valid user authentication
        And I have merchant code "054329"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And response body should be valid JSON
        And response should have merchant structure

    @merchant_lookup_code @positive @pay_to_school @sasai
    Scenario: Lookup merchant with different valid code
        Given I have valid user authentication
        And I have merchant code "149017"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And response should contain merchant details by code

    @merchant_lookup_code @positive @pay_to_school @sasai
    Scenario: Lookup merchant code with leading zeros
        Given I have valid user authentication
        And I have merchant code "0043"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And response should contain merchant details by code

    @merchant_lookup_code @negative @pay_to_school @sasai
    Scenario: Lookup merchant without authentication
        Given I have no authentication token
        And I have merchant code "054329"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 401

    @merchant_lookup_code @negative @pay_to_school @sasai
    Scenario: Lookup merchant with invalid user token
        Given I have invalid user token
        And I have merchant code "054329"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 401

    @merchant_lookup_code @negative @pay_to_school @sasai
    Scenario: Lookup merchant with expired user token
        Given I have expired user token
        And I have merchant code "054329"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 401

    @merchant_lookup_code @negative @pay_to_school @sasai
    Scenario: Lookup merchant with app token instead of user token
        Given I have app token only
        And I have merchant code "054329"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 401 or 403

    @merchant_lookup_code @negative @pay_to_school @sasai
    Scenario: Lookup merchant with invalid merchant code
        Given I have valid user authentication
        And I have merchant code "999999999"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 404

    @merchant_lookup_code @negative @pay_to_school @sasai
    Scenario: Lookup merchant with empty merchant code
        Given I have valid user authentication
        And I have merchant code ""
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 400

    @merchant_lookup_code @negative @pay_to_school @sasai
    Scenario: Lookup merchant without merchant code parameter
        Given I have valid user authentication
        And I have no merchant code
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 400

    @merchant_lookup_code @negative @pay_to_school @sasai
    Scenario: Lookup merchant with special characters in code
        Given I have valid user authentication
        And I have merchant code "054@329"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 400 or 404

    @merchant_lookup_code @negative @pay_to_school @sasai
    Scenario: Lookup merchant with alphabetic characters in code
        Given I have valid user authentication
        And I have merchant code "ABC123"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 400 or 404

    @merchant_lookup_code @validation @pay_to_school @sasai
    Scenario: Verify merchant lookup response contains required fields
        Given I have valid user authentication
        And I have merchant code "054329"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And merchant response should have required fields
        And merchant response should contain name
        And merchant response should contain code
        And merchant response should contain mobile number

    @merchant_lookup_code @validation @pay_to_school @sasai
    Scenario: Verify merchant lookup response structure
        Given I have valid user authentication
        And I have merchant code "054329"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And response body should be valid JSON
        And response should have merchant structure

    @merchant_lookup_code @headers @validation @pay_to_school @sasai
    Scenario: Verify merchant lookup response headers
        Given I have valid user authentication
        And I have merchant code "054329"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And response header "Content-Type" should be present
        And response header "Content-Type" should contain "application/json"

    @merchant_lookup_code @headers @validation @pay_to_school @sasai
    Scenario: Verify merchant lookup has required headers
        Given I have valid user authentication
        And I have merchant code "054329"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And response header "Content-Type" should not be empty
        And response header "Date" should be present

    @merchant_lookup_code @security @pay_to_school @sasai
    Scenario: Verify merchant lookup with missing Authorization header
        Given I have no Authorization header
        And I have merchant code "054329"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 401

    @merchant_lookup_code @security @pay_to_school @sasai
    Scenario: Verify merchant lookup with empty Bearer token
        Given I have empty Bearer token
        And I have merchant code "054329"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 401

    @merchant_lookup_code @security @pay_to_school @sasai
    Scenario: Verify merchant lookup with malformed Bearer token
        Given I have malformed Bearer token
        And I have merchant code "054329"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 401

    @merchant_lookup_code @security @pay_to_school @sasai
    Scenario: Verify merchant lookup without Bearer prefix
        Given I have token without Bearer prefix
        And I have merchant code "054329"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 401

    @merchant_lookup_code @error_handling @pay_to_school @sasai
    Scenario: Merchant lookup with invalid HTTP method POST
        Given I have valid user authentication
        And I have merchant code "054329"
        When I send POST request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 405

    @merchant_lookup_code @error_handling @pay_to_school @sasai
    Scenario: Merchant lookup with invalid HTTP method PUT
        Given I have valid user authentication
        And I have merchant code "054329"
        When I send PUT request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 405

    @merchant_lookup_code @error_handling @pay_to_school @sasai
    Scenario: Merchant lookup with invalid HTTP method DELETE
        Given I have valid user authentication
        And I have merchant code "054329"
        When I send DELETE request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 405

    @merchant_lookup_code @error_handling @pay_to_school @sasai
    Scenario: Merchant lookup with wrong endpoint path
        Given I have valid user authentication
        And I have merchant code "054329"
        When I send GET request to "/bff/v1/catalog/merchant-search"
        Then response status code should be 404

    @merchant_lookup_code @performance @pay_to_school @sasai
    Scenario: Verify merchant lookup response time
        Given I have valid user authentication
        And I have merchant code "054329"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And response time should be less than 3000 ms

    @merchant_lookup_code @performance @pay_to_school @sasai
    Scenario: Verify merchant lookup response time is acceptable
        Given I have valid user authentication
        And I have merchant code "054329"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And response time should be less than 5000 ms

    @merchant_lookup_code @integration @pay_to_school @sasai
    Scenario: Complete flow - PIN Verify to Merchant Lookup by Code
        Given I have valid PIN verification details
        When I send PIN verification request to "/bff/v4/auth/pin/verify"
        Then response status code should be 200
        And I store the user token from response
        Given I have merchant code "054329"
        When I send merchant lookup by code request with stored token to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And response should contain merchant details by code

    @merchant_lookup_code @integration @pay_to_school @sasai
    Scenario: Search then lookup - School Search to Merchant Lookup by Code
        Given I have valid user authentication
        And I have search type "SCHOOL"
        And I have page number 0
        And I have page size 10
        And I have name query "school"
        When I send school search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 200
        And response should contain search results
        And I extract first merchant code from search results
        When I send merchant lookup by code request with extracted code to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And response should contain merchant details by code

    @merchant_lookup_code @data_validation @pay_to_school @sasai
    Scenario: Verify merchant code matches in response
        Given I have valid user authentication
        And I have merchant code "054329"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And response merchant code should match requested code "054329"

    @merchant_lookup_code @data_validation @pay_to_school @sasai
    Scenario: Verify merchant name is not empty
        Given I have valid user authentication
        And I have merchant code "054329"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And merchant name should not be empty
        And merchant code should not be empty

    @merchant_lookup_code @data_validation @pay_to_school @sasai
    Scenario: Verify merchant address information
        Given I have valid user authentication
        And I have merchant code "054329"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And merchant should have address information
        And merchant should have city information

    @merchant_lookup_code @multiple_codes @pay_to_school @sasai
    Scenario Outline: Lookup different merchant codes
        Given I have valid user authentication
        And I have merchant code "<merchantCode>"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And response should contain merchant details by code

        Examples:
            | merchantCode |
            | 054329       |
            | 149017       |
            | 164575       |
            | 123540       |
            | 0043         |

    @merchant_lookup_code @negative @multiple_codes @pay_to_school @sasai
    Scenario Outline: Lookup with invalid merchant codes
        Given I have valid user authentication
        And I have merchant code "<merchantCode>"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 400 or 404

        Examples:
            | merchantCode |
            | INVALID      |
            | 99999999     |
            | -12345       |
            | @#$%^&       |

    @merchant_lookup_code @case_sensitivity @pay_to_school @sasai
    Scenario: Verify merchant code is case insensitive (numeric)
        Given I have valid user authentication
        And I have merchant code "054329"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And response should contain merchant details by code
