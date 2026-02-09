Feature: Church Search by Name
    As a user
    I want to search for churches by name
    So that I can find churches for making donations or payments

    # NOTE: Church Search API requires user token (accessToken) from PIN Verify API
    # This is part of the "Pay to Church" flow
    # Endpoint: GET /bff/v1/catalog/search-school-church-merchant
    # Query Parameters: type=CHURCH, page, pageSize, nameQuery

    Background:
        Given API is available
        And I am authenticated with valid app token
        And I have valid user token from PIN verification

    @smoke @church_search @pay_to_church @sasai
    Scenario: Search churches with valid query
        Given I have valid user authentication
        And I have search type "CHURCH"
        And I have page number 0
        And I have page size 10
        And I have name query "church"
        When I send church search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 200
        And response should contain search results
       # And response should have church list

    @church_search @positive @pay_to_church @sasai
    Scenario: Search churches returns correct structure
        Given I have valid user authentication
        And I have search type "CHURCH"
        And I have page number 0
        And I have page size 10
        And I have name query "church"
        When I send church search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 200
        And response body should be valid JSON
        And response should have pagination structure

    @church_search @positive @pay_to_church @sasai
    Scenario: Search churches with specific name
        Given I have valid user authentication
        And I have search type "CHURCH"
        And I have page number 0
        And I have page size 10
        And I have name query "baptist"
        When I send church search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 200
        And response should contain search results

    @church_search @positive @pay_to_church @sasai
    Scenario: Search churches with different page size
        Given I have valid user authentication
        And I have search type "CHURCH"
        And I have page number 0
        And I have page size 20
        And I have name query "church"
        When I send church search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 200
        And response should contain search results

    @church_search @positive @pay_to_church @sasai
    Scenario: Search churches with pagination
        Given I have valid user authentication
        And I have search type "CHURCH"
        And I have page number 1
        And I have page size 10
        And I have name query "church"
        When I send church search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 200
        And response should have pagination info

    @church_search @negative @pay_to_church @sasai
    Scenario: Search churches without authentication
        Given I have no authentication token
        And I have search type "CHURCH"
        And I have page number 0
        And I have page size 10
        And I have name query "church"
        When I send church search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 401

    @church_search @negative @pay_to_church @sasai
    Scenario: Search churches with invalid user token
        Given I have invalid user token
        And I have search type "CHURCH"
        And I have page number 0
        And I have page size 10
        And I have name query "church"
        When I send church search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 401

    @church_search @negative @pay_to_church @sasai
    Scenario: Search churches with expired user token
        Given I have expired user token
        And I have search type "CHURCH"
        And I have page number 0
        And I have page size 10
        And I have name query "church"
        When I send church search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 401

    @church_search @negative @pay_to_church @sasai
    Scenario: Search churches with app token instead of user token
        Given I have app token only
        And I have search type "CHURCH"
        And I have page number 0
        And I have page size 10
        And I have name query "church"
        When I send church search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 401 or 403

    @church_search @negative @pay_to_church @sasai
    Scenario: Search churches without type parameter
        Given I have valid user authentication
        And I have no search type
        And I have page number 0
        And I have page size 10
        And I have name query "church"
        When I send church search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 400

    @church_search @negative @pay_to_church @sasai
    Scenario: Search churches with invalid type
        Given I have valid user authentication
        And I have search type "INVALID"
        And I have page number 0
        And I have page size 10
        And I have name query "church"
        When I send church search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 400

    @church_search @negative @pay_to_church @sasai
    Scenario: Search churches without name query
        Given I have valid user authentication
        And I have search type "CHURCH"
        And I have page number 0
        And I have page size 10
        And I have no name query
        When I send church search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 400

    @church_search @negative @pay_to_church @sasai
    Scenario: Search churches with empty name query
        Given I have valid user authentication
        And I have search type "CHURCH"
        And I have page number 0
        And I have page size 10
        And I have name query ""
        When I send church search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 400

    @church_search @negative @pay_to_church @sasai
    Scenario: Search churches with negative page number
        Given I have valid user authentication
        And I have search type "CHURCH"
        And I have page number -1
        And I have page size 10
        And I have name query "church"
        When I send church search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 400

    @church_search @negative @pay_to_church @sasai
    Scenario: Search churches with zero page size
        Given I have valid user authentication
        And I have search type "CHURCH"
        And I have page number 0
        And I have page size 0
        And I have name query "church"
        When I send church search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 400

    @church_search @negative @pay_to_church @sasai
    Scenario: Search churches with excessive page size
        Given I have valid user authentication
        And I have search type "CHURCH"
        And I have page number 0
        And I have page size 1000
        And I have name query "church"
        When I send church search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 400

    @church_search @validation @pay_to_church @sasai
    Scenario: Verify church search response contains required fields
        Given I have valid user authentication
        And I have search type "CHURCH"
        And I have page number 0
        And I have page size 10
        And I have name query "church"
        When I send church search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 200
        And response should have content field
        And response should have pagination fields

    @church_search @validation @pay_to_church @sasai
    Scenario: Verify church search response structure
        Given I have valid user authentication
        And I have search type "CHURCH"
        And I have page number 0
        And I have page size 10
        And I have name query "church"
        When I send church search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 200
        And response body should be valid JSON
        And response should have search structure

    @church_search @validation @pay_to_church @sasai
    Scenario: Verify church items have required fields
        Given I have valid user authentication
        And I have search type "CHURCH"
        And I have page number 0
        And I have page size 10
        And I have name query "church"
        When I send church search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 200
        And each church should have name field
        And each church should have code field

    @church_search @headers @validation @pay_to_church @sasai
    Scenario: Verify church search response headers
        Given I have valid user authentication
        And I have search type "CHURCH"
        And I have page number 0
        And I have page size 10
        And I have name query "church"
        When I send church search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 200
        And response header "Content-Type" should be present
        And response header "Content-Type" should contain "application/json"

    @church_search @security @pay_to_church @sasai
    Scenario: Verify church search with missing Authorization header
        Given I have no Authorization header
        And I have search type "CHURCH"
        And I have page number 0
        And I have page size 10
        And I have name query "church"
        When I send church search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 401

    @church_search @security @pay_to_church @sasai
    Scenario: Verify church search with empty Bearer token
        Given I have empty Bearer token
        And I have search type "CHURCH"
        And I have page number 0
        And I have page size 10
        And I have name query "church"
        When I send church search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 401

    @church_search @security @pay_to_church @sasai
    Scenario: Verify church search with malformed Bearer token
        Given I have malformed Bearer token
        And I have search type "CHURCH"
        And I have page number 0
        And I have page size 10
        And I have name query "church"
        When I send church search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 401

    @church_search @error_handling @pay_to_church @sasai
    Scenario: Church search with invalid HTTP method POST
        Given I have valid user authentication
        And I have search type "CHURCH"
        When I send POST request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 405

    @church_search @error_handling @pay_to_church @sasai
    Scenario: Church search with wrong endpoint path
        Given I have valid user authentication
        And I have search type "CHURCH"
        When I send GET request to "/bff/v1/catalog/search-church"
        Then response status code should be 404

    @church_search @performance @pay_to_church @sasai
    Scenario: Verify church search response time
        Given I have valid user authentication
        And I have search type "CHURCH"
        And I have page number 0
        And I have page size 10
        And I have name query "church"
        When I send church search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 200
        And response time should be less than 3000 ms

    @church_search @performance @pay_to_church @sasai
    Scenario: Verify church search response time is acceptable
        Given I have valid user authentication
        And I have search type "CHURCH"
        And I have page number 0
        And I have page size 10
        And I have name query "church"
        When I send church search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 200
        And response time should be less than 5000 ms

    @church_search @integration @pay_to_church @sasai
    Scenario: Complete flow - PIN Verify to Church Search
        Given I have valid PIN verification details
        When I send PIN verification request to "/bff/v4/auth/pin/verify"
        Then response status code should be 200
        And I store the user token from response
        Given I have search type "CHURCH"
        And I have page number 0
        And I have page size 10
        And I have name query "church"
        When I send church search request with stored token to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 200
        And response should contain search results

    @church_search @data_validation @pay_to_church @sasai
    Scenario: Verify church search results are churches only
        Given I have valid user authentication
        And I have search type "CHURCH"
        And I have page number 0
        And I have page size 10
        And I have name query "church"
        When I send church search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 200
        And all results should be of type church

    @church_search @data_validation @pay_to_church @sasai
    Scenario: Verify church search returns correct page size
        Given I have valid user authentication
        And I have search type "CHURCH"
        And I have page number 0
        And I have page size 5
        And I have name query "church"
        When I send church search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 200
        And response should contain at most 5 results

    @church_search @data_validation @pay_to_church @sasai
    Scenario: Verify church names contain search query
        Given I have valid user authentication
        And I have search type "CHURCH"
        And I have page number 0
        And I have page size 10
        And I have name query "baptist"
        When I send church search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 200
        And church names should contain "baptist"

    @church_search @special_chars @pay_to_church @sasai
    Scenario: Search churches with special characters in query
        Given I have valid user authentication
        And I have search type "CHURCH"
        And I have page number 0
        And I have page size 10
        And I have name query "st. mary's"
        When I send church search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 200

    @church_search @case_sensitivity @pay_to_church @sasai
    Scenario: Search churches is case insensitive
        Given I have valid user authentication
        And I have search type "CHURCH"
        And I have page number 0
        And I have page size 10
        And I have name query "CHURCH"
        When I send church search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 200
        And response should contain search results

    @church_search @partial_match @pay_to_church @sasai
    Scenario: Search churches with partial name match
        Given I have valid user authentication
        And I have search type "CHURCH"
        And I have page number 0
        And I have page size 10
        And I have name query "chr"
        When I send church search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 200
        And response should contain search results

    @church_search @no_results @pay_to_church @sasai
    Scenario: Search churches with no matching results
        Given I have valid user authentication
        And I have search type "CHURCH"
        And I have page number 0
        And I have page size 10
        And I have name query "xyzabc123nonexistent"
        When I send church search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 200
        And response should have empty results

    @church_search @pagination @pay_to_church @sasai
    Scenario Outline: Search churches with different page numbers
        Given I have valid user authentication
        And I have search type "CHURCH"
        And I have page number <pageNumber>
        And I have page size 10
        And I have name query "church"
        When I send church search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 200

        Examples:
            | pageNumber |
            | 0          |
            | 1          |
            | 2          |

    @church_search @page_sizes @pay_to_church @sasai
    Scenario Outline: Search churches with different page sizes
        Given I have valid user authentication
        And I have search type "CHURCH"
        And I have page number 0
        And I have page size <pageSize>
        And I have name query "church"
        When I send church search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 200
        And response should contain at most <pageSize> results

        Examples:
            | pageSize |
            | 5        |
            | 10       |
            | 15       |
            | 20       |

    @church_search @name_queries @pay_to_church @sasai
    Scenario Outline: Search churches with different name queries
        Given I have valid user authentication
        And I have search type "CHURCH"
        And I have page number 0
        And I have page size 10
        And I have name query "<nameQuery>"
        When I send church search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 200

        Examples:
            | nameQuery  |
            | church     |
            | baptist    |
            | catholic   |
            | methodist  |
            | apostolic  |

    @church_search @extract_data @pay_to_church @sasai
    Scenario: Extract church code from search results
        Given I have valid user authentication
        And I have search type "CHURCH"
        And I have page number 0
        And I have page size 10
        And I have name query "church"
        When I send church search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 200
        And response should contain search results
        And I extract first merchant code from search results
        And extracted code should not be empty

    @church_search @sort_order @pay_to_church @sasai
    Scenario: Verify church search results are sorted
        Given I have valid user authentication
        And I have search type "CHURCH"
        And I have page number 0
        And I have page size 10
        And I have name query "church"
        When I send church search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 200
        And response should contain search results
        And results should be in alphabetical order
