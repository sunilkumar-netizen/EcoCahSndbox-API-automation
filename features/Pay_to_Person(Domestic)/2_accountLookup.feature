Feature: Beneficiary Account Lookup for P2P Payment
    As a user
    I want to lookup beneficiary account details
    So that I can verify the recipient before making a P2P payment

    # NOTE: Account Lookup API requires user token (accessToken) from PIN Verify API
    # Endpoint: POST /bff/v3/payment/account/lookup
    # Request Body: {"accountNumber": "+263789124669"}
    # Response: Returns beneficiary account details including name, account info, etc.
    # This API is used to validate recipient accounts before Person-to-Person payments

    Background:
        Given API is available
        And I am authenticated with valid app token
        And I have valid user token from PIN verification

    @smoke @p2p_lookup @account_lookup @sasai
    Scenario: Lookup beneficiary account with valid phone number
        Given I have valid user authentication
        And I have account number "+263789124669"
        When I send account lookup request to "/bff/v3/payment/account/lookup"
        Then response status code should be 200
        And response body should be valid JSON
        And response should contain account details
        And response should have beneficiary name
        And response should have account status

    @p2p_lookup @positive @account_lookup @sasai
    Scenario: Lookup account and verify response structure
        Given I have valid user authentication
        And I have account number "+263789124669"
        When I send account lookup request to "/bff/v3/payment/account/lookup"
        Then response status code should be 200
        And response should have complete beneficiary details
        And response should have required account fields
        And beneficiary account should be valid

    @p2p_lookup @positive @account_lookup @sasai
    Scenario: Lookup account with different phone number format
        Given I have valid user authentication
        And I have account number "263789124669"
        When I send account lookup request to "/bff/v3/payment/account/lookup"
        Then response status code should be 200
        And response should contain account details

    @p2p_lookup @positive @account_lookup @sasai
    Scenario: Lookup account and extract beneficiary details
        Given I have valid user authentication
        And I have account number "+263789124669"
        When I send account lookup request to "/bff/v3/payment/account/lookup"
        Then response status code should be 200
        And I extract beneficiary name from response
        And I extract account identifier from response
        And extracted beneficiary details should be valid

    @p2p_lookup @positive @account_lookup @sasai
    Scenario: Complete flow - Search then lookup account
        Given I have valid user authentication
        And I have search query "EcoCash User Five"
        And I have country code "ZW"
        And I have page number 1
        And I have page count 20
        When I send contact search request to "/search/v3/collection/search"
        Then response status code should be 200
        And I extract first contact from search results
        Given I have account number from extracted contact
        When I send account lookup request to "/bff/v3/payment/account/lookup"
        Then response status code should be 200
        And response should contain account details

    @p2p_lookup @negative @account_lookup @sasai
    Scenario: Lookup account without authentication
        Given I have no authentication token
        And I have account number "+263789124669"
        When I send account lookup request to "/bff/v3/payment/account/lookup"
        Then response status code should be 401

    @p2p_lookup @negative @account_lookup @sasai
    Scenario: Lookup account with invalid user token
        Given I have invalid user token
        And I have account number "+263789124669"
        When I send account lookup request to "/bff/v3/payment/account/lookup"
        Then response status code should be 401

    @p2p_lookup @negative @account_lookup @sasai
    Scenario: Lookup account with expired user token
        Given I have expired user token
        And I have account number "+263789124669"
        When I send account lookup request to "/bff/v3/payment/account/lookup"
        Then response status code should be 401

    @p2p_lookup @negative @account_lookup @sasai
    Scenario: Lookup account without account number
        Given I have valid user authentication
        And I have no account number
        When I send account lookup request to "/bff/v3/payment/account/lookup"
        Then response status code should be 400

    @p2p_lookup @negative @account_lookup @sasai
    Scenario: Lookup account with empty account number
        Given I have valid user authentication
        And I have account number ""
        When I send account lookup request to "/bff/v3/payment/account/lookup"
        Then response status code should be 400

    @p2p_lookup @negative @account_lookup @sasai
    Scenario: Lookup account with invalid phone number format
        Given I have valid user authentication
        And I have account number "invalid123"
        When I send account lookup request to "/bff/v3/payment/account/lookup"
        Then response status code should be 400 or 404

    @p2p_lookup @negative @account_lookup @sasai
    Scenario: Lookup account with non-existent account number
        Given I have valid user authentication
        And I have account number "+263999999999"
        When I send account lookup request to "/bff/v3/payment/account/lookup"
        Then response status code should be 404

    @p2p_lookup @negative @account_lookup @sasai
    Scenario: Lookup account with special characters in account number
        Given I have valid user authentication
        And I have account number "+263@#$%^&*()"
        When I send account lookup request to "/bff/v3/payment/account/lookup"
        Then response status code should be 400

    @p2p_lookup @negative @account_lookup @sasai
    Scenario: Lookup account with very short number
        Given I have valid user authentication
        And I have account number "123"
        When I send account lookup request to "/bff/v3/payment/account/lookup"
        Then response status code should be 400 or 404

    @p2p_lookup @negative @account_lookup @sasai
    Scenario: Lookup account with very long number
        Given I have valid user authentication
        And I have account number "+2637891246691234567890"
        When I send account lookup request to "/bff/v3/payment/account/lookup"
        Then response status code should be 400 or 404

    @p2p_lookup @negative @account_lookup @sasai
    Scenario: Lookup account with null account number
        Given I have valid user authentication
        And I have null account number
        When I send account lookup request to "/bff/v3/payment/account/lookup"
        Then response status code should be 400

    @p2p_lookup @validation @account_lookup @sasai
    Scenario: Verify account lookup response contains required fields
        Given I have valid user authentication
        And I have account number "+263789124669"
        When I send account lookup request to "/bff/v3/payment/account/lookup"
        Then response status code should be 200
        And response should have account metadata
        And response should have beneficiary information

    @p2p_lookup @validation @account_lookup @sasai
    Scenario: Verify beneficiary name format
        Given I have valid user authentication
        And I have account number "+263789124669"
        When I send account lookup request to "/bff/v3/payment/account/lookup"
        Then response status code should be 200
        And beneficiary name should not be empty
        And beneficiary name should be valid string

    @p2p_lookup @validation @account_lookup @sasai
    Scenario: Verify account identifier format
        Given I have valid user authentication
        And I have account number "+263789124669"
        When I send account lookup request to "/bff/v3/payment/account/lookup"
        Then response status code should be 200
        And account identifier should be present
        And account identifier should match requested number

    @p2p_lookup @headers @validation @account_lookup @sasai
    Scenario: Verify account lookup response headers
        Given I have valid user authentication
        And I have account number "+263789124669"
        When I send account lookup request to "/bff/v3/payment/account/lookup"
        Then response status code should be 200
        And response header "Content-Type" should be present
        And response header "Content-Type" should contain "application/json"

    @p2p_lookup @security @account_lookup @sasai
    Scenario: Verify lookup with missing Authorization header
        Given I have no Authorization header
        And I have account number "+263789124669"
        When I send account lookup request to "/bff/v3/payment/account/lookup"
        Then response status code should be 401

    @p2p_lookup @security @account_lookup @sasai
    Scenario: Verify lookup with empty Bearer token
        Given I have empty Bearer token
        And I have account number "+263789124669"
        When I send account lookup request to "/bff/v3/payment/account/lookup"
        Then response status code should be 401

    @p2p_lookup @security @account_lookup @sasai
    Scenario: Verify lookup with malformed Bearer token
        Given I have malformed Bearer token
        And I have account number "+263789124669"
        When I send account lookup request to "/bff/v3/payment/account/lookup"
        Then response status code should be 401

    @p2p_lookup @security @account_lookup @sasai
    Scenario: Verify lookup with missing Content-Type header
        Given I have valid user authentication
        And I have no Content-Type header
        And I have account number "+263789124669"
        When I send account lookup request to "/bff/v3/payment/account/lookup"
        Then response status code should be 400 or 415

    @p2p_lookup @error_handling @account_lookup @sasai
    Scenario: Lookup with invalid HTTP method GET
        Given I have valid user authentication
        When I send GET request to "/bff/v3/payment/account/lookup"
        Then response status code should be 405

    @p2p_lookup @error_handling @account_lookup @sasai
    Scenario: Lookup with invalid HTTP method PUT
        Given I have valid user authentication
        When I send PUT request to "/bff/v3/payment/account/lookup"
        Then response status code should be 405

    @p2p_lookup @error_handling @account_lookup @sasai
    Scenario: Lookup with wrong endpoint path
        Given I have valid user authentication
        And I have account number "+263789124669"
        When I send account lookup request to "/bff/v3/payment/account/lookups"
        Then response status code should be 404

    @p2p_lookup @error_handling @account_lookup @sasai
    Scenario: Lookup with malformed JSON body
        Given I have valid user authentication
        And I have malformed JSON body
        When I send account lookup request to "/bff/v3/payment/account/lookup"
        Then response status code should be 400

    @p2p_lookup @performance @account_lookup @sasai
    Scenario: Verify account lookup response time
        Given I have valid user authentication
        And I have account number "+263789124669"
        When I send account lookup request to "/bff/v3/payment/account/lookup"
        Then response status code should be 200
        And response time should be less than 3000 ms

    @p2p_lookup @performance @account_lookup @sasai
    Scenario: Verify account lookup response time is acceptable
        Given I have valid user authentication
        And I have account number "+263789124669"
        When I send account lookup request to "/bff/v3/payment/account/lookup"
        Then response status code should be 200
        And response time should be less than 5000 ms

    @p2p_lookup @data_validation @account_lookup @sasai
    Scenario: Verify lookup with international format
        Given I have valid user authentication
        And I have account number "+263789124669"
        When I send account lookup request to "/bff/v3/payment/account/lookup"
        Then response status code should be 200

    @p2p_lookup @data_validation @account_lookup @sasai
    Scenario: Verify lookup with local format
        Given I have valid user authentication
        And I have account number "0789124669"
        When I send account lookup request to "/bff/v3/payment/account/lookup"
        Then response status code should be 200 or 400

    @p2p_lookup @data_validation @account_lookup @sasai
    Scenario: Verify same account looked up multiple times
        Given I have valid user authentication
        And I have account number "+263789124669"
        When I send account lookup request to "/bff/v3/payment/account/lookup"
        Then response status code should be 200
        And I store first lookup response
        When I send account lookup request to "/bff/v3/payment/account/lookup"
        Then response status code should be 200
        And second lookup response should match first lookup

    @p2p_lookup @phone_formats @account_lookup @sasai
    Scenario Outline: Lookup accounts with different phone number formats
        Given I have valid user authentication
        And I have account number "<phoneNumber>"
        When I send account lookup request to "/bff/v3/payment/account/lookup"
        Then response status code should be <statusCode>

        Examples:
            | phoneNumber       | statusCode |
            | +263789124669     | 200        |
            | 263789124669      | 200        |
            | 0789124669        | 200 or 400 |
            | 789124669         | 200 or 400 |

    @p2p_lookup @country_codes @account_lookup @sasai
    Scenario Outline: Lookup accounts with different country code formats
        Given I have valid user authentication
        And I have account number "<phoneNumber>"
        When I send account lookup request to "/bff/v3/payment/account/lookup"
        Then response status code should be <statusCode>

        Examples:
            | phoneNumber       | statusCode |
            | +263789124669     | 200        |
            | +27789124669      | 200 or 404 |
            | +254789124669     | 200 or 404 |
            | +234789124669     | 200 or 404 |
