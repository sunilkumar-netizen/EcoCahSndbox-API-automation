Feature: P2P Payment Options API
    As a user
    I want to get available payment options for P2P transfers
    So that I can choose how to send money to another person

    # NOTE: Payment Options API requires user token (accessToken) from PIN Verify API
    # Endpoint: GET /bff/v2/payment/options?serviceType=ZWPersonPaymentOptions
    # Query Parameters: serviceType (required) - e.g., "ZWPersonPaymentOptions"
    # Headers: requestId (UUID), Authorization (Bearer token)
    # Response: Returns available payment options/instruments for P2P payments
    # This API is used after account lookup to present payment method choices to the user

    Background:
        Given API is available
        And I am authenticated with valid app token
        And I have valid user token from PIN verification

    @smoke @p2p_payment_options @payment_options @p2p @sasai
    Scenario: Get payment options for P2P transfer
        Given I have valid user authentication
        And I have service type "ZWPersonPaymentOptions"
        And I have request ID "bdefac7b-bbc0-48b4-9ef0-84e6b9b34a6f"
        When I send P2P payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response body should be valid JSON
        And response should contain P2P payment options
        And P2P payment options should not be empty

    @p2p_payment_options @positive @payment_options @p2p @sasai
    Scenario: Verify payment options response structure
        Given I have valid user authentication
        And I have service type "ZWPersonPaymentOptions"
        And I have request ID "bdefac7b-bbc0-48b4-9ef0-84e6b9b34a6f"
        When I send P2P payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response should have P2P payment options list
        And each P2P payment option should have required fields
        And P2P payment options should have valid structure

    @p2p_payment_options @positive @payment_options @p2p @sasai
    Scenario: Get payment options without request ID
        Given I have valid user authentication
        And I have service type "ZWPersonPaymentOptions"
        When I send P2P payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response should contain P2P payment options

    @p2p_payment_options @positive @payment_options @p2p @sasai
    Scenario: Get payment options and extract first option
        Given I have valid user authentication
        And I have service type "ZWPersonPaymentOptions"
        And I have request ID "bdefac7b-bbc0-48b4-9ef0-84e6b9b34a6f"
        When I send P2P payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And I extract first P2P payment option
        And extracted P2P payment option should be valid

    @p2p_payment_options @integration @payment_options @p2p @sasai
    Scenario: Complete P2P flow - Search, Lookup, Get Payment Options
        Given I have valid user authentication
        # Step 1: Search for contact
        And I have search query "EcoCash User Five"
        And I have country code "ZW"
        And I have page number 1
        And I have page count 20
        When I send contact search request to "/search/v3/collection/search"
        Then response status code should be 200
        And I extract first contact from search results
        # Step 2: Lookup beneficiary account
        Given I have account number from extracted contact
        When I send account lookup request to "/bff/v3/payment/account/lookup"
        Then response status code should be 200
        And response should contain account details
        # Step 3: Get payment options
        Given I have service type "ZWPersonPaymentOptions"
        And I have request ID "bdefac7b-bbc0-48b4-9ef0-84e6b9b34a6f"
        When I send P2P payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response should contain P2P payment options

    @p2p_payment_options @negative @payment_options @p2p @sasai
    Scenario: Get payment options without authentication
        Given I have no authentication token
        And I have service type "ZWPersonPaymentOptions"
        When I send P2P payment options request to "/bff/v2/payment/options"
        Then response status code should be 401

    @p2p_payment_options @negative @payment_options @p2p @sasai
    Scenario: Get payment options with invalid user token
        Given I have invalid user token
        And I have service type "ZWPersonPaymentOptions"
        When I send P2P payment options request to "/bff/v2/payment/options"
        Then response status code should be 401

    @p2p_payment_options @negative @payment_options @p2p @sasai
    Scenario: Get payment options with expired user token
        Given I have expired user token
        And I have service type "ZWPersonPaymentOptions"
        When I send P2P payment options request to "/bff/v2/payment/options"
        Then response status code should be 401

    @p2p_payment_options @negative @payment_options @p2p @sasai
    Scenario: Get payment options without service type
        Given I have valid user authentication
        And I have no service type
        When I send P2P payment options request to "/bff/v2/payment/options"
        Then response status code should be 400

    @p2p_payment_options @negative @payment_options @p2p @sasai
    Scenario: Get payment options with empty service type
        Given I have valid user authentication
        And I have service type ""
        When I send P2P payment options request to "/bff/v2/payment/options"
        Then response status code should be 400

    @p2p_payment_options @negative @payment_options @p2p @sasai
    Scenario: Get payment options with invalid service type
        Given I have valid user authentication
        And I have service type "InvalidServiceType"
        When I send P2P payment options request to "/bff/v2/payment/options"
        Then response status code should be 400 or 404

    @p2p_payment_options @negative @payment_options @p2p @sasai
    Scenario: Get payment options with malformed service type
        Given I have valid user authentication
        And I have service type "!@#$%^&*()"
        When I send P2P payment options request to "/bff/v2/payment/options"
        Then response status code should be 400

    @p2p_payment_options @validation @payment_options @p2p @sasai
    Scenario: Verify payment options contain instrument details
        Given I have valid user authentication
        And I have service type "ZWPersonPaymentOptions"
        When I send P2P payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And P2P payment options should contain instrument information
        And each P2P instrument should have valid details

    @p2p_payment_options @validation @payment_options @p2p @sasai
    Scenario: Verify payment options have provider information
        Given I have valid user authentication
        And I have service type "ZWPersonPaymentOptions"
        When I send P2P payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And P2P payment options should have provider details
        And P2P provider names should be valid

    @p2p_payment_options @validation @payment_options @p2p @sasai
    Scenario: Verify request ID is properly handled
        Given I have valid user authentication
        And I have service type "ZWPersonPaymentOptions"
        And I have request ID "550e8400-e29b-41d4-a716-446655440000"
        When I send P2P payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response should contain P2P payment options

    @p2p_payment_options @headers @validation @payment_options @p2p @sasai
    Scenario: Verify payment options response headers
        Given I have valid user authentication
        And I have service type "ZWPersonPaymentOptions"
        When I send P2P payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response header "Content-Type" should be present
        And response header "Content-Type" should contain "application/json"

    @p2p_payment_options @security @payment_options @p2p @sasai
    Scenario: Verify payment options with missing Authorization header
        Given I have no Authorization header
        And I have service type "ZWPersonPaymentOptions"
        When I send P2P payment options request to "/bff/v2/payment/options"
        Then response status code should be 401

    @p2p_payment_options @security @payment_options @p2p @sasai
    Scenario: Verify payment options with empty Bearer token
        Given I have empty Bearer token
        And I have service type "ZWPersonPaymentOptions"
        When I send P2P payment options request to "/bff/v2/payment/options"
        Then response status code should be 401

    @p2p_payment_options @security @payment_options @p2p @sasai
    Scenario: Verify payment options with malformed Bearer token
        Given I have malformed Bearer token
        And I have service type "ZWPersonPaymentOptions"
        When I send P2P payment options request to "/bff/v2/payment/options"
        Then response status code should be 401

    @p2p_payment_options @error_handling @payment_options @p2p @sasai
    Scenario: Payment options with invalid HTTP method POST
        Given I have valid user authentication
        And I have service type "ZWPersonPaymentOptions"
        When I send POST request to "/bff/v2/payment/options?serviceType=ZWPersonPaymentOptions"
        Then response status code should be 405

    @p2p_payment_options @error_handling @payment_options @p2p @sasai
    Scenario: Payment options with invalid HTTP method PUT
        Given I have valid user authentication
        And I have service type "ZWPersonPaymentOptions"
        When I send PUT request to "/bff/v2/payment/options?serviceType=ZWPersonPaymentOptions"
        Then response status code should be 405

    @p2p_payment_options @error_handling @payment_options @p2p @sasai
    Scenario: Payment options with wrong endpoint path
        Given I have valid user authentication
        And I have service type "ZWPersonPaymentOptions"
        When I send P2P payment options request to "/bff/v2/payment/option"
        Then response status code should be 404

    @p2p_payment_options @performance @payment_options @p2p @sasai
    Scenario: Verify payment options response time
        Given I have valid user authentication
        And I have service type "ZWPersonPaymentOptions"
        When I send P2P payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response time should be less than 2000 ms

    @p2p_payment_options @performance @payment_options @p2p @sasai
    Scenario: Verify payment options response time is acceptable
        Given I have valid user authentication
        And I have service type "ZWPersonPaymentOptions"
        When I send P2P payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response time should be less than 3000 ms

    @p2p_payment_options @data_validation @payment_options @p2p @sasai
    Scenario: Verify multiple calls return consistent results
        Given I have valid user authentication
        And I have service type "ZWPersonPaymentOptions"
        When I send P2P payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And I store first P2P payment options response
        When I send P2P payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And second P2P payment options should match first

    @p2p_payment_options @service_types @payment_options @p2p @sasai
    Scenario Outline: Get payment options with different service types
        Given I have valid user authentication
        And I have service type "<serviceType>"
        When I send P2P payment options request to "/bff/v2/payment/options"
        Then response status code should be <statusCode>

        Examples:
            | serviceType                | statusCode |
            | ZWPersonPaymentOptions     | 200        |
            | ZWPersonPayment            | 200 or 400 |
            | PersonPaymentOptions       | 200 or 400 |
            | ZWPaymentOptions           | 200 or 400 |

    @p2p_payment_options @request_ids @payment_options @p2p @sasai
    Scenario Outline: Get payment options with different request ID formats
        Given I have valid user authentication
        And I have service type "ZWPersonPaymentOptions"
        And I have request ID "<requestId>"
        When I send P2P payment options request to "/bff/v2/payment/options"
        Then response status code should be <statusCode>

        Examples:
            | requestId                              | statusCode |
            | 550e8400-e29b-41d4-a716-446655440000   | 200        |
            | bdefac7b-bbc0-48b4-9ef0-84e6b9b34a6f   | 200        |
            | 123e4567-e89b-12d3-a456-426614174000   | 200        |
