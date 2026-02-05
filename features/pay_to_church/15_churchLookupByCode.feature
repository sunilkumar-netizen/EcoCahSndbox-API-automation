Feature: Church Lookup by Code
    As a user
    I want to lookup church details by merchant code
    So that I can verify church information before making payments

    # NOTE: Church Lookup API requires user token (accessToken) from PIN Verify API
    # This is part of the "Pay to Church" flow - Step 2 after searching churches
    # Endpoint: GET /bff/v1/catalog/merchant-lookup
    # Query Parameter: merCode (merchant code obtained from church search)

    Background:
        Given API is available
        And I am authenticated with valid app token
        And I have valid user token from PIN verification

    @smoke @church_lookup @pay_to_church @sasai
    Scenario: Lookup church with valid merchant code
        Given I have valid user authentication
        And I have merchant code "394875"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And response should contain merchant details by code
        And merchant response should contain code

    @church_lookup @positive @pay_to_church @sasai
    Scenario: Lookup church returns correct structure
        Given I have valid user authentication
        And I have merchant code "394875"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And response body should be valid JSON
        And response should have merchant structure

    @church_lookup @positive @pay_to_church @sasai
    Scenario: Lookup church returns complete details
        Given I have valid user authentication
        And I have merchant code "394875"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And merchant response should contain name
        And response should have merchant type field

    @church_lookup @positive @pay_to_church @sasai
    Scenario: Lookup church with different valid code
        Given I have valid user authentication
        And I have merchant code "123456"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200 or 404

    @church_lookup @negative @pay_to_church @sasai
    Scenario: Lookup church without authentication
        Given I have no authentication token
        And I have merchant code "394875"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 401

    @church_lookup @negative @pay_to_church @sasai
    Scenario: Lookup church with invalid user token
        Given I have invalid user token
        And I have merchant code "394875"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 401

    @church_lookup @negative @pay_to_church @sasai
    Scenario: Lookup church with expired user token
        Given I have expired user token
        And I have merchant code "394875"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 401

    @church_lookup @negative @pay_to_church @sasai
    Scenario: Lookup church with app token instead of user token
        Given I have app token only
        And I have merchant code "394875"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 401 or 403

    @church_lookup @negative @pay_to_church @sasai
    Scenario: Lookup church without merchant code parameter
        Given I have valid user authentication
        And I have no merchant code
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 400

    @church_lookup @negative @pay_to_church @sasai
    Scenario: Lookup church with empty merchant code
        Given I have valid user authentication
        And I have merchant code ""
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 400

    @church_lookup @negative @pay_to_church @sasai
    Scenario: Lookup church with non-existent code
        Given I have valid user authentication
        And I have merchant code "999999999"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 404

    @church_lookup @negative @pay_to_church @sasai
    Scenario: Lookup church with invalid code format - letters
        Given I have valid user authentication
        And I have merchant code "ABCDEF"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 400 or 404

    @church_lookup @negative @pay_to_church @sasai
    Scenario: Lookup church with invalid code format - special chars
        Given I have valid user authentication
        And I have merchant code "123@#$"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 400

    @church_lookup @negative @pay_to_church @sasai
    Scenario: Lookup church with negative merchant code
        Given I have valid user authentication
        And I have merchant code "-123456"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 400 or 404

    @church_lookup @negative @pay_to_church @sasai
    Scenario: Lookup church with zero merchant code
        Given I have valid user authentication
        And I have merchant code "0"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 404

    @church_lookup @validation @pay_to_church @sasai
    Scenario: Verify church lookup response contains required fields
        Given I have valid user authentication
        And I have merchant code "394875"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And merchant response should contain code
        And merchant response should contain name

    @church_lookup @validation @pay_to_church @sasai
    Scenario: Verify church lookup response structure
        Given I have valid user authentication
        And I have merchant code "394875"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And response body should be valid JSON
        And response should have merchant structure

    @church_lookup @validation @pay_to_church @sasai
    Scenario: Verify returned code matches requested code
        Given I have valid user authentication
        And I have merchant code "394875"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And response merchant code should match "394875"

    @church_lookup @headers @validation @pay_to_church @sasai
    Scenario: Verify church lookup response headers
        Given I have valid user authentication
        And I have merchant code "394875"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And response header "Content-Type" should be present
        And response header "Content-Type" should contain "application/json"

    @church_lookup @headers @validation @pay_to_church @sasai
    Scenario: Verify church lookup accepts JSON
        Given I have valid user authentication
        And I have merchant code "394875"
        And I set request header "Accept" to "application/json"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200

    @church_lookup @security @pay_to_church @sasai
    Scenario: Verify church lookup with missing Authorization header
        Given I have no Authorization header
        And I have merchant code "394875"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 401

    @church_lookup @security @pay_to_church @sasai
    Scenario: Verify church lookup with empty Bearer token
        Given I have empty Bearer token
        And I have merchant code "394875"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 401

    @church_lookup @security @pay_to_church @sasai
    Scenario: Verify church lookup with malformed Bearer token
        Given I have malformed Bearer token
        And I have merchant code "394875"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 401

    @church_lookup @error_handling @pay_to_church @sasai
    Scenario: Church lookup with invalid HTTP method POST
        Given I have valid user authentication
        And I have merchant code "394875"
        When I send POST request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 405

    @church_lookup @error_handling @pay_to_church @sasai
    Scenario: Church lookup with invalid HTTP method PUT
        Given I have valid user authentication
        And I have merchant code "394875"
        When I send PUT request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 405

    @church_lookup @error_handling @pay_to_church @sasai
    Scenario: Church lookup with invalid HTTP method DELETE
        Given I have valid user authentication
        And I have merchant code "394875"
        When I send DELETE request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 405

    @church_lookup @error_handling @pay_to_church @sasai
    Scenario: Church lookup with wrong endpoint path
        Given I have valid user authentication
        And I have merchant code "394875"
        When I send GET request to "/bff/v1/catalog/merchant-details"
        Then response status code should be 404

    @church_lookup @performance @pay_to_church @sasai
    Scenario: Verify church lookup response time
        Given I have valid user authentication
        And I have merchant code "394875"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And response time should be less than 2000 ms

    @church_lookup @performance @pay_to_church @sasai
    Scenario: Verify church lookup response time is acceptable
        Given I have valid user authentication
        And I have merchant code "394875"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And response time should be less than 3000 ms

    @church_lookup @integration @pay_to_church @sasai
    Scenario: Complete flow - Search Church to Lookup Details
        Given I have valid user authentication
        And I have search type "CHURCH"
        And I have page number 0
        And I have page size 10
        And I have name query "church"
        When I send church search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 200
        And I extract first merchant code from search results
        When I send merchant lookup by code request with extracted code to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And response should contain merchant details by code

    @church_lookup @integration @pay_to_church @sasai
    Scenario: Complete flow - PIN Verify to Church Lookup
        Given I have valid PIN verification details
        When I send PIN verification request to "/bff/v4/auth/pin/verify"
        Then response status code should be 200
        And I store the user token from response
        Given I have merchant code "394875"
        When I send merchant lookup by code request with stored token to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And response should contain merchant details by code

    @church_lookup @data_validation @pay_to_church @sasai
    Scenario: Verify church type in lookup response
        Given I have valid user authentication
        And I have merchant code "394875"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And merchant type should be "CHURCH"

    @church_lookup @data_validation @pay_to_church @sasai
    Scenario: Verify church name is not empty
        Given I have valid user authentication
        And I have merchant code "394875"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And merchant name should not be empty

    @church_lookup @data_validation @pay_to_church @sasai
    Scenario: Verify church code format in response
        Given I have valid user authentication
        And I have merchant code "394875"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And merchant code should be numeric string

    @church_lookup @cache @pay_to_church @sasai
    Scenario: Verify church lookup caching behavior
        Given I have valid user authentication
        And I have merchant code "394875"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And I store response time as first_request_time
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And response should match previous response

    @church_lookup @special_codes @pay_to_church @sasai
    Scenario Outline: Lookup church with different merchant codes
        Given I have valid user authentication
        And I have merchant code "<merchantCode>"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be <statusCode>

        Examples:
            | merchantCode | statusCode |
            | 394875       | 200        |
            | 123456       | 200 or 404 |
            | 111111       | 200 or 404 |
            | 999999       | 200 or 404 |

    @church_lookup @concurrent @pay_to_church @sasai
    Scenario: Multiple church lookups with same token
        Given I have valid user authentication
        And I have merchant code "394875"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200

    @church_lookup @code_length @pay_to_church @sasai
    Scenario Outline: Lookup church with different code lengths
        Given I have valid user authentication
        And I have merchant code "<code>"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be <statusCode>

        Examples:
            | code      | statusCode |
            | 1         | 200 or 404 |
            | 12        | 200 or 404 |
            | 123       | 200 or 404 |
            | 1234      | 200 or 404 |
            | 12345     | 200 or 404 |
            | 123456    | 200 or 404 |
            | 1234567   | 200 or 404 |
            | 12345678  | 200 or 404 |

    @church_lookup @sql_injection @security @pay_to_church @sasai
    Scenario: Church lookup with SQL injection attempt
        Given I have valid user authentication
        And I have merchant code "394875' OR '1'='1"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 400 or 404
        And response should not contain database error

    @church_lookup @xss @security @pay_to_church @sasai
    Scenario: Church lookup with XSS attempt
        Given I have valid user authentication
        And I have merchant code "<script>alert('xss')</script>"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 400 or 404

    @church_lookup @extract_data @pay_to_church @sasai
    Scenario: Extract church details for payment
        Given I have valid user authentication
        And I have merchant code "394875"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And I extract merchant name from response
        And I extract merchant code from response
        And extracted details should not be empty

    @church_lookup @boundary @pay_to_church @sasai
    Scenario: Lookup church with maximum length code
        Given I have valid user authentication
        And I have merchant code "99999999999999999999"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 400 or 404

    @church_lookup @whitespace @pay_to_church @sasai
    Scenario: Lookup church with code containing whitespace
        Given I have valid user authentication
        And I have merchant code "394 875"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 400

    @church_lookup @leading_zeros @pay_to_church @sasai
    Scenario: Lookup church with leading zeros in code
        Given I have valid user authentication
        And I have merchant code "0000394875"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200 or 404

    @church_lookup @unicode @pay_to_church @sasai
    Scenario: Lookup church with unicode characters
        Given I have valid user authentication
        And I have merchant code "①②③④⑤⑥"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 400

    @church_lookup @stress @pay_to_church @sasai
    Scenario: Rapid church lookup requests
        Given I have valid user authentication
        And I have merchant code "394875"
        When I send 5 merchant lookup by code requests to "/bff/v1/catalog/merchant-lookup"
        Then all requests should return status code 200
        And all responses should be consistent
