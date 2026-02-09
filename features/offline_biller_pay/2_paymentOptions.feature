Feature: Get Payment Options for Bill Payment
    As a user
    I want to get available payment options for bill payment
    So that I can choose a payment method for offline biller payment

    # NOTE: Payment Options API requires user token (accessToken) from PIN Verify API
    # Endpoint: GET /bff/v2/payment/options?serviceType=sasai-app-payment
    # Query Parameters: serviceType (payment service type)
    # Response: Returns available payment instruments and options for bill payment
    # This API is called before making any bill payment to get fresh instrument tokens

    Background:
        Given API is available
        And I am authenticated with valid app token
        And I have valid user token from PIN verification

    @smoke @payment_options @offline_biller_pay @sasai
    Scenario: Get payment options with valid user token
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response body should be valid JSON
        And response should contain payment instruments
        And response should have instrument token

    @payment_options @positive @offline_biller_pay @sasai
    Scenario: Get payment options returns valid structure
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response should have payment options structure
        And response should contain available payment methods

    @payment_options @positive @offline_biller_pay @sasai
    Scenario: Extract instrument token from payment options
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And I extract instrument token from response
        And extracted instrument token should not be empty

    @payment_options @positive @offline_biller_pay @sasai
    Scenario: Verify payment options contains account information
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response should contain account details
        And response should have balance information

    @payment_options @negative @offline_biller_pay @sasai
    Scenario: Get payment options without authentication
        Given I have no authentication token
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 401

    @payment_options @negative @offline_biller_pay @sasai
    Scenario: Get payment options with invalid user token
        Given I have invalid user token
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 401

    @payment_options @negative @offline_biller_pay @sasai
    Scenario: Get payment options with expired user token
        Given I have expired user token
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 401

    @payment_options @negative @offline_biller_pay @sasai
    Scenario: Get payment options with app token only
        Given I have app token only
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 401 or 403

    @payment_options @negative @offline_biller_pay @sasai
    Scenario: Get payment options without service type
        Given I have valid user authentication
        When I send payment options request with query parameters
        Then response status code should be 400

    @payment_options @negative @offline_biller_pay @sasai
    Scenario: Get payment options with empty service type
        Given I have valid user authentication
        And I have service type ""
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 400

    @payment_options @negative @offline_biller_pay @sasai
    Scenario: Get payment options with invalid service type
        Given I have valid user authentication
        And I have service type "invalid-service-type"
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 400 or 404

    @payment_options @validation @offline_biller_pay @sasai
    Scenario: Verify payment options response contains required fields
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response should have required payment option fields
        And each payment instrument should have required fields

    @payment_options @validation @offline_biller_pay @sasai
    Scenario: Verify instrument token format is valid
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And instrument token format should be valid UUID

    @payment_options @validation @offline_biller_pay @sasai
    Scenario: Verify payment instruments have valid data
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And each instrument should have valid token
        And each instrument should have payment type

    @payment_options @headers @validation @offline_biller_pay @sasai
    Scenario: Verify payment options response headers
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response header "Content-Type" should be present
        And response header "Content-Type" should contain "application/json"

    @payment_options @security @offline_biller_pay @sasai
    Scenario: Verify payment options with missing Authorization header
        Given I have no Authorization header
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 401

    @payment_options @security @offline_biller_pay @sasai
    Scenario: Verify payment options with empty Bearer token
        Given I have empty Bearer token
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 401

    @payment_options @security @offline_biller_pay @sasai
    Scenario: Verify payment options with malformed Bearer token
        Given I have malformed Bearer token
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 401

    @payment_options @error_handling @offline_biller_pay @sasai
    Scenario: Payment options with invalid HTTP method POST
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send POST request to "/bff/v2/payment/options?serviceType=sasai-app-payment"
        Then response status code should be 405

    @payment_options @error_handling @offline_biller_pay @sasai
    Scenario: Payment options with invalid HTTP method PUT
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send PUT request to "/bff/v2/payment/options?serviceType=sasai-app-payment"
        Then response status code should be 405

    @payment_options @error_handling @offline_biller_pay @sasai
    Scenario: Payment options with invalid HTTP method DELETE
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send DELETE request to "/bff/v2/payment/options?serviceType=sasai-app-payment"
        Then response status code should be 405

    @payment_options @error_handling @offline_biller_pay @sasai
    Scenario: Payment options with wrong endpoint path
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send GET request to "/bff/v2/payment/option?serviceType=sasai-app-payment"
        Then response status code should be 404

    @payment_options @performance @offline_biller_pay @sasai
    Scenario: Verify payment options response time
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response time should be less than 3000 ms

    @payment_options @performance @offline_biller_pay @sasai
    Scenario: Verify payment options response time is acceptable
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response time should be less than 5000 ms

    @payment_options @integration @offline_biller_pay @sasai
    Scenario: Complete flow - Get payment options before biller lookup
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And I extract instrument token from response
        And I store instrument token for payment
        Given I have merchant code "8002"
        When I send offline biller lookup request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And response should contain biller details

    @payment_options @integration @offline_biller_pay @sasai
    Scenario: Complete flow - Payment options to bill payment preparation
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And I extract instrument token from response
        And I extract payment account details from response
        And stored payment details should be complete

    @payment_options @data_validation @offline_biller_pay @sasai
    Scenario: Verify payment options contains wallet information
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response should contain wallet details
        And wallet should have valid balance

    @payment_options @data_validation @offline_biller_pay @sasai
    Scenario: Verify payment instruments are not empty
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And payment instruments list should not be empty
        And each instrument should have valid data

    @payment_options @token_freshness @offline_biller_pay @sasai
    Scenario: Verify instrument token is fresh and unique
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And I extract instrument token from response
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And I extract second instrument token from response
        And second token should be different from first token

    @payment_options @service_types @offline_biller_pay @sasai
    Scenario Outline: Get payment options with different service types
        Given I have valid user authentication
        And I have service type "<serviceType>"
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be <statusCode>

        Examples:
            | serviceType             | statusCode |
            | sasai-app-payment       | 200        |
            | bill-payment            | 200 or 400 |
            | utility-payment         | 200 or 400 |

    @payment_options @extract_data @offline_biller_pay @sasai
    Scenario: Extract multiple payment instruments from options
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And I extract all instrument tokens from response
        And extracted tokens list should not be empty
        And each extracted token should be valid UUID

    @payment_options @account_info @offline_biller_pay @sasai
    Scenario: Verify payment options contains account status
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response should contain account status
        And account status should be active

    @payment_options @cache_validation @offline_biller_pay @sasai
    Scenario: Verify payment options returns fresh data
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And I extract instrument token from response
        And I wait for 2 seconds
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response should contain updated payment options
