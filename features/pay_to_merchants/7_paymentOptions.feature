Feature: Pay to Merchant- Payment Options
    As a user
    I want to verify payment options from Sasai Payment Gateway API
    So that I can see available payment methods before making a merchant payment

    # NOTE: Payment Options API requires user token (accessToken) from PIN Verify API
    # This is part of the "Merchant Payment" flow (after Merchant Lookup)
    # Endpoint: GET /bff/v1/payment/options

    Background:
        Given API is available
        And I am authenticated with valid app token
        And I have valid user token from PIN verification

    @smoke @payment_options @merchant_payment @sasai
    Scenario: Verify payment options with valid parameters
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v1/payment/options"
        Then response status code should be 200
        And response time should be less than 5000 ms
        And response should contain payment options

    @payment_options @positive @merchant_payment @sasai
    Scenario: Get payment options with sasai-app-payment service type
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        And I have request ID "bdefac7b-bbc0-48b4-9ef0-84e6b9b34a6f"
        When I send payment options request with query parameters
        Then response status code should be 200
        And response should contain payment options
        And response should contain payment methods

    @payment_options @positive @merchant_payment @sasai
    Scenario: Get payment options with valid requestId header
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        And I have request ID "bdefac7b-bbc0-48b4-9ef0-84e6b9b34a6f"
        When I send payment options request to "/bff/v1/payment/options"
        Then response status code should be 200
        And response header "Content-Type" should contain "application/json"
        And response should contain payment options

    @payment_options @negative @merchant_payment @sasai
    Scenario: Get payment options without authentication
        Given I have no authentication token
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v1/payment/options"
        Then response status code should be 401

    @payment_options @negative @merchant_payment @sasai
    Scenario: Get payment options with app token instead of user token
        Given I have app token only
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v1/payment/options"
        Then response status code should be 401 or 403

    @payment_options @negative @merchant_payment @sasai
    Scenario: Get payment options with expired user token
        Given I have expired user token
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v1/payment/options"
        Then response status code should be 401

    @payment_options @negative @merchant_payment @sasai
    Scenario: Get payment options with invalid user token
        Given I have invalid user token
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v1/payment/options"
        Then response status code should be 401

    @payment_options @negative @merchant_payment @sasai
    Scenario: Get payment options with missing service type
        Given I have valid user authentication
        And I have no service type parameter
        When I send payment options request to "/bff/v1/payment/options"
        Then response status code should be 400

    @payment_options @negative @merchant_payment @sasai
    Scenario: Get payment options with invalid service type
        Given I have valid user authentication
        And I have invalid service type "invalid-service"
        When I send payment options request with query parameters
        Then response status code should be 400

    @payment_options @negative @merchant_payment @sasai
    Scenario: Get payment options with empty service type
        Given I have valid user authentication
        And I have empty service type
        When I send payment options request with query parameters
        Then response status code should be 400

    @payment_options @validation @merchant_payment @sasai
    Scenario: Verify payment options response structure
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v1/payment/options"
        Then response status code should be 200
        And response body should be valid JSON
        And response should have payment options structure

    @payment_options @validation @merchant_payment @sasai
    Scenario: Verify payment options contains required fields
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v1/payment/options"
        Then response status code should be 200
        And payment options should have required fields

    @payment_options @validation @merchant_payment @sasai
    Scenario: Verify payment methods are available
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v1/payment/options"
        Then response status code should be 200
        And response should contain at least one payment method

    @payment_options @headers @validation @merchant_payment @sasai
    Scenario: Verify payment options response headers
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v1/payment/options"
        Then response status code should be 200
        And response header "Content-Type" should be present
        And response header "Content-Type" should contain "application/json"

    @payment_options @headers @validation @merchant_payment @sasai
    Scenario: Verify payment options has required headers
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v1/payment/options"
        Then response status code should be 200
        And response header "Content-Type" should not be empty
        And response header "Date" should be present

    @payment_options @security @merchant_payment @sasai
    Scenario: Verify payment options with missing Authorization header
        Given I have no Authorization header
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v1/payment/options"
        Then response status code should be 401

    @payment_options @security @merchant_payment @sasai
    Scenario: Verify payment options with empty Bearer token
        Given I have empty Bearer token
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v1/payment/options"
        Then response status code should be 401

    @payment_options @security @merchant_payment @sasai
    Scenario: Verify payment options without Bearer prefix
        Given I have token without Bearer prefix
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v1/payment/options"
        Then response status code should be 401

    @payment_options @security @merchant_payment @sasai
    Scenario: Verify payment options with malformed Bearer token
        Given I have malformed Bearer token
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v1/payment/options"
        Then response status code should be 401

    @payment_options @error_handling @merchant_payment @sasai
    Scenario: Get payment options with invalid HTTP method
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send POST request to "/bff/v1/payment/options"
        Then response status code should be 405

    @payment_options @error_handling @merchant_payment @sasai
    Scenario: Get payment options with wrong endpoint path
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send GET request to "/bff/v1/payment/option"
        Then response status code should be 404

    @payment_options @performance @merchant_payment @sasai
    Scenario: Verify payment options response time
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v1/payment/options"
        Then response status code should be 200
        And response time should be less than 3000 ms

    @payment_options @integration @merchant_payment @sasai
    Scenario: Complete flow - PIN Verify to Payment Options
        Given I have valid PIN verification details
        When I send PIN verification request to "/bff/v4/auth/pin/verify"
        Then response status code should be 200
        And I store the user token from response
        Given I have service type "sasai-app-payment"
        When I send payment options request with stored token to "/bff/v1/payment/options"
        Then response status code should be 200
        And response should contain payment options

    @payment_options @integration @merchant_payment @sasai
    Scenario: Complete merchant payment flow - Merchant Lookup to Payment Options
        Given I have valid user authentication
        And I have merchant lookup parameters
        When I send merchant lookup request to "/catalog/v1/categories/SZWC10002/operators/SZWOM00001/lookup"
        Then response status code should be 200
        And response should contain merchant details
        Given I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v1/payment/options"
        Then response status code should be 200
        And response should contain payment options
        And response should contain payment methods
