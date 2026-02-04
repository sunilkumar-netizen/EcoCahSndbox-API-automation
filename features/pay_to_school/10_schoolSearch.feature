Feature: Pay to School- search
    As a user
    I want to search for schools, churches, and merchants
    So that I can make payments to these institutions

    # NOTE: School Search API requires user token (accessToken) from PIN Verify API
    # This is part of the "Pay to School" flow
    # Endpoint: GET /bff/v1/catalog/search-school-church-merchant
    # Query Parameters: type, page, pageSize, nameQuery

    Background:
        Given API is available
        And I am authenticated with valid app token
        And I have valid user token from PIN verification

    @smoke @school_search @pay_to_school @sasai
    Scenario: Search for schools with valid parameters
        Given I have valid user authentication
        And I have search type "SCHOOL"
        And I have page number 0
        And I have page size 10
        And I have name query "school"
        When I send school search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 200
        And response should contain search results
        And response should have pagination info

    @school_search @positive @pay_to_school @sasai
    Scenario: Search for churches with valid parameters
        Given I have valid user authentication
        And I have search type "CHURCH"
        And I have page number 0
        And I have page size 10
        And I have name query "church"
        When I send school search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 200
        And response should contain search results

    @school_search @positive @pay_to_school @sasai
    Scenario: Search for merchants with valid parameters
        Given I have valid user authentication
        And I have search type "MERCHANT"
        And I have page number 0
        And I have page size 10
        And I have name query "merchant"
        When I send school search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 200
        And response should contain search results

    @school_search @pagination @pay_to_school @sasai
    Scenario: Search with different page sizes
        Given I have valid user authentication
        And I have search type "SCHOOL"
        And I have page number 0
        And I have page size 5
        And I have name query "school"
        When I send school search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 200
        And response should contain search results
        And response should have at most 5 results

    @school_search @pagination @pay_to_school @sasai
    Scenario: Search with pagination - page 2
        Given I have valid user authentication
        And I have search type "SCHOOL"
        And I have page number 1
        And I have page size 10
        And I have name query "school"
        When I send school search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 200

    @school_search @positive @pay_to_school @sasai
    Scenario: Search with minimum query length
        Given I have valid user authentication
        And I have search type "SCHOOL"
        And I have page number 0
        And I have page size 10
        And I have name query "a"
        When I send school search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 200

    @school_search @positive @pay_to_school @sasai
    Scenario: Search with numeric query
        Given I have valid user authentication
        And I have search type "SCHOOL"
        And I have page number 0
        And I have page size 10
        And I have name query "123"
        When I send school search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 200

    @school_search @negative @pay_to_school @sasai
    Scenario: Search without authentication
        Given I have no authentication token
        And I have search type "SCHOOL"
        And I have page number 0
        And I have page size 10
        And I have name query "school"
        When I send school search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 401

    @school_search @negative @pay_to_school @sasai
    Scenario: Search with invalid user token
        Given I have invalid user token
        And I have search type "SCHOOL"
        And I have page number 0
        And I have page size 10
        And I have name query "school"
        When I send school search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 401

    @school_search @negative @pay_to_school @sasai
    Scenario: Search with expired user token
        Given I have expired user token
        And I have search type "SCHOOL"
        And I have page number 0
        And I have page size 10
        And I have name query "school"
        When I send school search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 401

    @school_search @negative @pay_to_school @sasai
    Scenario: Search with invalid type
        Given I have valid user authentication
        And I have search type "INVALID_TYPE"
        And I have page number 0
        And I have page size 10
        And I have name query "school"
        When I send school search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 400

    @school_search @negative @pay_to_school @sasai
    Scenario: Search with negative page number
        Given I have valid user authentication
        And I have search type "SCHOOL"
        And I have page number -1
        And I have page size 10
        And I have name query "school"
        When I send school search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 400

    @school_search @negative @pay_to_school @sasai
    Scenario: Search with zero page size
        Given I have valid user authentication
        And I have search type "SCHOOL"
        And I have page number 0
        And I have page size 0
        And I have name query "school"
        When I send school search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 400

    @school_search @negative @pay_to_school @sasai
    Scenario: Search with negative page size
        Given I have valid user authentication
        And I have search type "SCHOOL"
        And I have page number 0
        And I have page size -10
        And I have name query "school"
        When I send school search request to "/bff/v1/catalog/search-school-merchant"
        Then response status code should be 400

    @school_search @negative @pay_to_school @sasai
    Scenario: Search with excessive page size
        Given I have valid user authentication
        And I have search type "SCHOOL"
        And I have page number 0
        And I have page size 1000
        And I have name query "school"
        When I send school search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 400

    @school_search @negative @pay_to_school @sasai
    Scenario: Search with empty name query
        Given I have valid user authentication
        And I have search type "SCHOOL"
        And I have page number 0
        And I have page size 10
        And I have name query ""
        When I send school search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 400

    @school_search @negative @pay_to_school @sasai
    Scenario: Search with missing type parameter
        Given I have valid user authentication
        And I have no search type
        And I have page number 0
        And I have page size 10
        And I have name query "school"
        When I send school search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 400

    @school_search @validation @pay_to_school @sasai
    Scenario: Verify search response structure
        Given I have valid user authentication
        And I have search type "SCHOOL"
        And I have page number 0
        And I have page size 10
        And I have name query "school"
        When I send school search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 200
        And response body should be valid JSON
        And response should have search structure

    @school_search @validation @pay_to_school @sasai
    Scenario: Verify search response contains required fields
        Given I have valid user authentication
        And I have search type "SCHOOL"
        And I have page number 0
        And I have page size 10
        And I have name query "school"
        When I send school search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 200
        And search response should have required fields

    @school_search @headers @validation @pay_to_school @sasai
    Scenario: Verify search response headers
        Given I have valid user authentication
        And I have search type "SCHOOL"
        And I have page number 0
        And I have page size 10
        And I have name query "school"
        When I send school search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 200
        And response header "Content-Type" should be present
        And response header "Content-Type" should contain "application/json"

    @school_search @security @pay_to_school @sasai
    Scenario: Verify search with missing Authorization header
        Given I have no Authorization header
        And I have search type "SCHOOL"
        And I have page number 0
        And I have page size 10
        And I have name query "school"
        When I send school search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 401

    @school_search @security @pay_to_school @sasai
    Scenario: Verify search with empty Bearer token
        Given I have empty Bearer token
        And I have search type "SCHOOL"
        And I have page number 0
        And I have page size 10
        And I have name query "school"
        When I send school search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 401

    @school_search @security @pay_to_school @sasai
    Scenario: Verify search with malformed Bearer token
        Given I have malformed Bearer token
        And I have search type "SCHOOL"
        And I have page number 0
        And I have page size 10
        And I have name query "school"
        When I send school search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 401

    @school_search @error_handling @pay_to_school @sasai
    Scenario: Search with invalid HTTP method
        Given I have valid user authentication
        And I have search type "SCHOOL"
        And I have page number 0
        And I have page size 10
        And I have name query "school"
        When I send POST request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 405

    @school_search @error_handling @pay_to_school @sasai
    Scenario: Search with wrong endpoint path
        Given I have valid user authentication
        And I have search type "SCHOOL"
        And I have page number 0
        And I have page size 10
        And I have name query "school"
        When I send GET request to "/bff/v1/catalog/search-school"
        Then response status code should be 404

    @school_search @performance @pay_to_school @sasai
    Scenario: Verify search response time
        Given I have valid user authentication
        And I have search type "SCHOOL"
        And I have page number 0
        And I have page size 10
        And I have name query "school"
        When I send school search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 200
        And response time should be less than 5000 ms

    @school_search @integration @pay_to_school @sasai
    Scenario: Complete flow - PIN Verify to School Search
        Given I have valid PIN verification details
        When I send PIN verification request to "/bff/v4/auth/pin/verify"
        Then response status code should be 200
        And I store the user token from response
        Given I have search type "SCHOOL"
        And I have page number 0
        And I have page size 10
        And I have name query "school"
        When I send school search request with stored token to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 200
        And response should contain search results
