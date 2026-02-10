Feature: Search Contact for P2P Payment
    As a user
    I want to search for contacts
    So that I can send money to them via P2P payment

    # NOTE: Search Contact API requires user token (accessToken) from PIN Verify API
    # Endpoint: GET /search/v3/collection/search
    # Query Parameters: countryCode, page, pageCount, q (search query)
    # Response: Returns list of matching contacts/users with their details
    # This API is used to find recipients for Person-to-Person (Domestic) payments

    Background:
        Given API is available
        And I am authenticated with valid app token
        And I have valid user token from PIN verification

    @smoke @p2p_search @search_contact @sasai @p2p
    Scenario: Search for contact with valid query
        Given I have valid user authentication
        And I have search query "EcoCash User Five"
        And I have country code "ZW"
        And I have page number 1
        And I have page count 20
        When I send contact search request to "/search/v3/collection/search"
        Then response status code should be 200
        And response body should be valid JSON
        And response should contain search results
        And response should have contacts list
        And search results should not be empty

    @p2p_search @positive @search_contact @sasai
    Scenario: Search contact and verify response structure
        Given I have valid user authentication
        And I have search query "EcoCash User"
        And I have country code "ZW"
        And I have page number 1
        And I have page count 20
        When I send contact search request to "/search/v3/collection/search"
        Then response status code should be 200
        And response should have contact details structure
        And each contact should have required fields
        And response should have pagination info

    @p2p_search @positive @search_contact @sasai
    Scenario: Search with partial name
        Given I have valid user authentication
        And I have search query "EcoCash"
        And I have country code "ZW"
        And I have page number 1
        And I have page count 20
        When I send contact search request to "/search/v3/collection/search"
        Then response status code should be 200
        And response should contain search results

    @p2p_search @positive @search_contact @sasai
    Scenario: Search with phone number
        Given I have valid user authentication
        And I have search query "263"
        And I have country code "ZW"
        And I have page number 1
        And I have page count 20
        When I send contact search request to "/search/v3/collection/search"
        Then response status code should be 200
        And response should contain search results

    @p2p_search @positive @search_contact @sasai
    Scenario: Search with different page sizes
        Given I have valid user authentication
        And I have search query "EcoCash User"
        And I have country code "ZW"
        And I have page number 1
        And I have page count 10
        When I send contact search request to "/search/v3/collection/search"
        Then response status code should be 200
        And response should contain search results
        And response should respect page count limit

    @p2p_search @positive @search_contact @sasai
    Scenario: Search with pagination - page 2
        Given I have valid user authentication
        And I have search query "EcoCash"
        And I have country code "ZW"
        And I have page number 2
        And I have page count 10
        When I send contact search request to "/search/v3/collection/search"
        Then response status code should be 200
        And response should contain search results

    @p2p_search @positive @search_contact @sasai
    Scenario: Search and extract contact details
        Given I have valid user authentication
        And I have search query "EcoCash User Five"
        And I have country code "ZW"
        And I have page number 1
        And I have page count 20
        When I send contact search request to "/search/v3/collection/search"
        Then response status code should be 200
        And I extract first contact from search results
        And extracted contact should have valid details

    @p2p_search @negative @search_contact @sasai
    Scenario: Search without authentication
        Given I have no authentication token
        And I have search query "EcoCash User"
        And I have country code "ZW"
        And I have page number 1
        And I have page count 20
        When I send contact search request to "/search/v3/collection/search"
        Then response status code should be 401

    @p2p_search @negative @search_contact @sasai
    Scenario: Search with invalid user token
        Given I have invalid user token
        And I have search query "EcoCash User"
        And I have country code "ZW"
        And I have page number 1
        And I have page count 20
        When I send contact search request to "/search/v3/collection/search"
        Then response status code should be 401

    @p2p_search @negative @search_contact @sasai
    Scenario: Search with expired user token
        Given I have expired user token
        And I have search query "EcoCash User"
        And I have country code "ZW"
        And I have page number 1
        And I have page count 20
        When I send contact search request to "/search/v3/collection/search"
        Then response status code should be 401

    @p2p_search @negative @search_contact @sasai
    Scenario: Search without country code
        Given I have valid user authentication
        And I have search query "EcoCash User"
        And I have no country code
        And I have page number 1
        And I have page count 20
        When I send contact search request to "/search/v3/collection/search"
        Then response status code should be 400

    @p2p_search @negative @search_contact @sasai
    Scenario: Search with invalid country code
        Given I have valid user authentication
        And I have search query "EcoCash User"
        And I have country code "INVALID"
        And I have page number 1
        And I have page count 20
        When I send contact search request to "/search/v3/collection/search"
        Then response status code should be 400

    @p2p_search @negative @search_contact @sasai
    Scenario: Search without search query
        Given I have valid user authentication
        And I have no search query
        And I have country code "ZW"
        And I have page number 1
        And I have page count 20
        When I send contact search request to "/search/v3/collection/search"
        Then response status code should be 400

    @p2p_search @negative @search_contact @sasai
    Scenario: Search with empty search query
        Given I have valid user authentication
        And I have search query ""
        And I have country code "ZW"
        And I have page number 1
        And I have page count 20
        When I send contact search request to "/search/v3/collection/search"
        Then response status code should be 400

    @p2p_search @negative @search_contact @sasai
    Scenario: Search with invalid page number
        Given I have valid user authentication
        And I have search query "EcoCash User"
        And I have country code "ZW"
        And I have page number -1
        And I have page count 20
        When I send contact search request to "/search/v3/collection/search"
        Then response status code should be 400

    @p2p_search @negative @search_contact @sasai
    Scenario: Search with zero page number
        Given I have valid user authentication
        And I have search query "EcoCash User"
        And I have country code "ZW"
        And I have page number 0
        And I have page count 20
        When I send contact search request to "/search/v3/collection/search"
        Then response status code should be 400

    @p2p_search @negative @search_contact @sasai
    Scenario: Search with invalid page count
        Given I have valid user authentication
        And I have search query "EcoCash User"
        And I have country code "ZW"
        And I have page number 1
        And I have page count -5
        When I send contact search request to "/search/v3/collection/search"
        Then response status code should be 400

    @p2p_search @negative @search_contact @sasai
    Scenario: Search with excessive page count
        Given I have valid user authentication
        And I have search query "EcoCash User"
        And I have country code "ZW"
        And I have page number 1
        And I have page count 1000
        When I send contact search request to "/search/v3/collection/search"
        Then response status code should be 400

    @p2p_search @negative @search_contact @sasai
    Scenario: Search with special characters in query
        Given I have valid user authentication
        And I have search query "@#$%^&*()"
        And I have country code "ZW"
        And I have page number 1
        And I have page count 20
        When I send contact search request to "/search/v3/collection/search"
        Then response status code should be 200
        And search results should be empty or valid

    @p2p_search @validation @search_contact @sasai
    Scenario: Verify contact search response contains required fields
        Given I have valid user authentication
        And I have search query "EcoCash User"
        And I have country code "ZW"
        And I have page number 1
        And I have page count 20
        When I send contact search request to "/search/v3/collection/search"
        Then response status code should be 200
        And response should have search metadata

    @p2p_search @validation @search_contact @sasai
    Scenario: Verify contact details structure
        Given I have valid user authentication
        And I have search query "EcoCash User Five"
        And I have country code "ZW"
        And I have page number 1
        And I have page count 20
        When I send contact search request to "/search/v3/collection/search"
        Then response status code should be 200
        And each contact should have name field
        And each contact should have identifier field

    @p2p_search @headers @validation @search_contact @sasai
    Scenario: Verify search response headers
        Given I have valid user authentication
        And I have search query "EcoCash User"
        And I have country code "ZW"
        And I have page number 1
        And I have page count 20
        When I send contact search request to "/search/v3/collection/search"
        Then response status code should be 200
        And response header "Content-Type" should be present
        And response header "Content-Type" should contain "application/json"

    @p2p_search @security @search_contact @sasai
    Scenario: Verify search with missing Authorization header
        Given I have no Authorization header
        And I have search query "EcoCash User"
        And I have country code "ZW"
        And I have page number 1
        And I have page count 20
        When I send contact search request to "/search/v3/collection/search"
        Then response status code should be 401

    @p2p_search @security @search_contact @sasai
    Scenario: Verify search with empty Bearer token
        Given I have empty Bearer token
        And I have search query "EcoCash User"
        And I have country code "ZW"
        And I have page number 1
        And I have page count 20
        When I send contact search request to "/search/v3/collection/search"
        Then response status code should be 401

    @p2p_search @security @search_contact @sasai
    Scenario: Verify search with malformed Bearer token
        Given I have malformed Bearer token
        And I have search query "EcoCash User"
        And I have country code "ZW"
        And I have page number 1
        And I have page count 20
        When I send contact search request to "/search/v3/collection/search"
        Then response status code should be 401

    @p2p_search @error_handling @search_contact @sasai
    Scenario: Search with invalid HTTP method POST
        Given I have valid user authentication
        When I send POST request to "/search/v3/collection/search"
        Then response status code should be 405

    @p2p_search @error_handling @search_contact @sasai
    Scenario: Search with invalid HTTP method PUT
        Given I have valid user authentication
        When I send PUT request to "/search/v3/collection/search"
        Then response status code should be 405

    @p2p_search @error_handling @search_contact @sasai
    Scenario: Search with wrong endpoint path
        Given I have valid user authentication
        And I have search query "EcoCash User"
        And I have country code "ZW"
        And I have page number 1
        And I have page count 20
        When I send contact search request to "/search/v3/collection/searches"
        Then response status code should be 404

    @p2p_search @performance @search_contact @sasai
    Scenario: Verify search response time
        Given I have valid user authentication
        And I have search query "EcoCash User"
        And I have country code "ZW"
        And I have page number 1
        And I have page count 20
        When I send contact search request to "/search/v3/collection/search"
        Then response status code should be 200
        And response time should be less than 3000 ms

    @p2p_search @performance @search_contact @sasai
    Scenario: Verify search response time with large page count
        Given I have valid user authentication
        And I have search query "EcoCash"
        And I have country code "ZW"
        And I have page number 1
        And I have page count 100
        When I send contact search request to "/search/v3/collection/search"
        Then response status code should be 200 or 400
        And response time should be less than 5000 ms

    @p2p_search @data_validation @search_contact @sasai
    Scenario: Verify search results are case insensitive
        Given I have valid user authentication
        And I have search query "ecocash user"
        And I have country code "ZW"
        And I have page number 1
        And I have page count 20
        When I send contact search request to "/search/v3/collection/search"
        Then response status code should be 200

    @p2p_search @data_validation @search_contact @sasai
    Scenario: Verify search with numeric query
        Given I have valid user authentication
        And I have search query "123456789"
        And I have country code "ZW"
        And I have page number 1
        And I have page count 20
        When I send contact search request to "/search/v3/collection/search"
        Then response status code should be 200

    @p2p_search @country_codes @search_contact @sasai
    Scenario Outline: Search contacts with different country codes
        Given I have valid user authentication
        And I have search query "User"
        And I have country code "<countryCode>"
        And I have page number 1
        And I have page count 20
        When I send contact search request to "/search/v3/collection/search"
        Then response status code should be <statusCode>

        Examples:
            | countryCode | statusCode |
            | ZW          | 200        |
            | ZA          | 200 or 400 |
            | KE          | 200 or 400 |
            | NG          | 200 or 400 |

    @p2p_search @page_sizes @search_contact @sasai
    Scenario Outline: Search with different page sizes
        Given I have valid user authentication
        And I have search query "EcoCash User"
        And I have country code "ZW"
        And I have page number 1
        And I have page count <pageCount>
        When I send contact search request to "/search/v3/collection/search"
        Then response status code should be <statusCode>

        Examples:
            | pageCount | statusCode |
            | 5         | 200        |
            | 10        | 200        |
            | 20        | 200        |
            | 50        | 200        |
            | 100       | 200 or 400 |
