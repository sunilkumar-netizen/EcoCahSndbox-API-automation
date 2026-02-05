Feature: School Payment Options
    As a user
    I want to get available payment options for school payments
    So that I can choose how to pay for school/church/merchant services

    # NOTE: Payment Options API requires user token (accessToken) from PIN Verify API
    # This is part of the "Pay to School" flow
    # Endpoint: GET /bff/v2/payment/options
    # Query Parameters: serviceType=sasai-app-payment

    Background:
        Given API is available
        And I am authenticated with valid app token
        And I have valid user token from PIN verification

    @smoke @school_payment_options @pay_to_school @sasai
    Scenario: Get payment options for school payment
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send school payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response should contain payment options
        And response should have payment instruments

    @school_payment_options @positive @pay_to_school @sasai
    Scenario: Get payment options returns correct structure
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send school payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response body should be valid JSON
        And response should have payment options structure

    @school_payment_options @positive @pay_to_school @sasai
    Scenario: Get payment options with device headers
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        And I have device information headers
        When I send school payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response should contain payment options

    @school_payment_options @positive @pay_to_school @sasai
    Scenario: Get payment options includes wallet option
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send school payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response should contain wallet payment option

    @school_payment_options @positive @pay_to_school @sasai
    Scenario: Get payment options with request ID
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        And I have request ID "43843e90-d1c8-11f0-a41e-95f35da604e5"
        When I send school payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response should contain payment options

    @school_payment_options @negative @pay_to_school @sasai
    Scenario: Get payment options without authentication
        Given I have no authentication token
        And I have service type "sasai-app-payment"
        When I send school payment options request to "/bff/v2/payment/options"
        Then response status code should be 401

    @school_payment_options @negative @pay_to_school @sasai
    Scenario: Get payment options with invalid user token
        Given I have invalid user token
        And I have service type "sasai-app-payment"
        When I send school payment options request to "/bff/v2/payment/options"
        Then response status code should be 401

    @school_payment_options @negative @pay_to_school @sasai
    Scenario: Get payment options with expired user token
        Given I have expired user token
        And I have service type "sasai-app-payment"
        When I send school payment options request to "/bff/v2/payment/options"
        Then response status code should be 401

    @school_payment_options @negative @pay_to_school @sasai
    Scenario: Get payment options with app token instead of user token
        Given I have app token only
        And I have service type "sasai-app-payment"
        When I send school payment options request to "/bff/v2/payment/options"
        Then response status code should be 401 or 403

    @school_payment_options @negative @pay_to_school @sasai
    Scenario: Get payment options without service type
        Given I have valid user authentication
        And I have no service type
        When I send school payment options request to "/bff/v2/payment/options"
        Then response status code should be 400

    @school_payment_options @negative @pay_to_school @sasai
    Scenario: Get payment options with invalid service type
        Given I have valid user authentication
        And I have service type "invalid-service-type"
        When I send school payment options request to "/bff/v2/payment/options"
        Then response status code should be 400

    @school_payment_options @negative @pay_to_school @sasai
    Scenario: Get payment options with empty service type
        Given I have valid user authentication
        And I have service type ""
        When I send school payment options request to "/bff/v2/payment/options"
        Then response status code should be 400

    @school_payment_options @validation @pay_to_school @sasai
    Scenario: Verify payment options response contains required fields
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send school payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And payment options response should have items
        And payment options response should have instruments

    @school_payment_options @validation @pay_to_school @sasai
    Scenario: Verify payment options instruments have required details
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send school payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And payment instruments should have instrument tokens
        And payment instruments should have provider information

    @school_payment_options @validation @pay_to_school @sasai
    Scenario: Verify payment options response structure
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send school payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response body should be valid JSON
        And response should have payment options structure

    @school_payment_options @headers @validation @pay_to_school @sasai
    Scenario: Verify payment options response headers
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send school payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response header "Content-Type" should be present
        And response header "Content-Type" should contain "application/json"

    @school_payment_options @headers @validation @pay_to_school @sasai
    Scenario: Verify payment options with all device headers
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        And I have all required device headers
        When I send school payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response should contain payment options

    @school_payment_options @security @pay_to_school @sasai
    Scenario: Verify payment options with missing Authorization header
        Given I have no Authorization header
        And I have service type "sasai-app-payment"
        When I send school payment options request to "/bff/v2/payment/options"
        Then response status code should be 401

    @school_payment_options @security @pay_to_school @sasai
    Scenario: Verify payment options with empty Bearer token
        Given I have empty Bearer token
        And I have service type "sasai-app-payment"
        When I send school payment options request to "/bff/v2/payment/options"
        Then response status code should be 401

    @school_payment_options @security @pay_to_school @sasai
    Scenario: Verify payment options with malformed Bearer token
        Given I have malformed Bearer token
        And I have service type "sasai-app-payment"
        When I send school payment options request to "/bff/v2/payment/options"
        Then response status code should be 401

    @school_payment_options @security @pay_to_school @sasai
    Scenario: Verify payment options without Bearer prefix
        Given I have token without Bearer prefix
        And I have service type "sasai-app-payment"
        When I send school payment options request to "/bff/v2/payment/options"
        Then response status code should be 401

    @school_payment_options @error_handling @pay_to_school @sasai
    Scenario: Payment options with invalid HTTP method POST
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send POST request to "/bff/v2/payment/options"
        Then response status code should be 405

    @school_payment_options @error_handling @pay_to_school @sasai
    Scenario: Payment options with invalid HTTP method PUT
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send PUT request to "/bff/v2/payment/options"
        Then response status code should be 405

    @school_payment_options @error_handling @pay_to_school @sasai
    Scenario: Payment options with invalid HTTP method DELETE
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send DELETE request to "/bff/v2/payment/options"
        Then response status code should be 405

    @school_payment_options @error_handling @pay_to_school @sasai
    Scenario: Payment options with wrong endpoint path
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send GET request to "/bff/v2/payment/option"
        Then response status code should be 404

    @school_payment_options @performance @pay_to_school @sasai
    Scenario: Verify payment options response time
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send school payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response time should be less than 3000 ms

    @school_payment_options @performance @pay_to_school @sasai
    Scenario: Verify payment options response time is acceptable
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send school payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response time should be less than 5000 ms

    @school_payment_options @integration @pay_to_school @sasai
    Scenario: Complete flow - PIN Verify to Payment Options
        Given I have valid PIN verification details
        When I send PIN verification request to "/bff/v4/auth/pin/verify"
        Then response status code should be 200
        And I store the user token from response
        Given I have service type "sasai-app-payment"
        When I send school payment options request with stored token to "/bff/v2/payment/options"
        Then response status code should be 200
        And response should contain payment options

    @school_payment_options @integration @pay_to_school @sasai
    Scenario: Complete flow - School Search to Payment Options
        Given I have valid user authentication
        And I have search type "SCHOOL"
        And I have page number 0
        And I have page size 10
        And I have name query "school"
        When I send school search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 200
        And response should contain search results
        Given I have service type "sasai-app-payment"
        When I send school payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response should contain payment options
        And payment instruments should have instrument tokens

    @school_payment_options @data_validation @pay_to_school @sasai
    Scenario: Verify instrument tokens are not empty
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send school payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And all instrument tokens should not be empty

    @school_payment_options @data_validation @pay_to_school @sasai
    Scenario: Verify payment options contains EcoCash provider
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send school payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And payment options should contain provider "ecocash"

    @school_payment_options @data_validation @pay_to_school @sasai
    Scenario: Verify payment instruments have currency information
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send school payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And payment instruments should have currency information

    @school_payment_options @data_validation @pay_to_school @sasai
    Scenario: Verify default payment instrument is marked
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send school payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response should have default payment instrument

    @school_payment_options @service_types @pay_to_school @sasai
    Scenario Outline: Get payment options with different service types
        Given I have valid user authentication
        And I have service type "<serviceType>"
        When I send school payment options request to "/bff/v2/payment/options"
        Then response status code should be <statusCode>

        Examples:
            | serviceType           | statusCode |
            | sasai-app-payment     | 200        |
            | sasai-super-app       | 200        |
            | merchant-payment      | 200        |

    @school_payment_options @device_headers @pay_to_school @sasai
    Scenario: Payment options with Android device headers
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        And I have device type "android"
        And I have OS version "15"
        And I have app version "2.2.1"
        When I send school payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response should contain payment options

    @school_payment_options @device_headers @pay_to_school @sasai
    Scenario: Payment options with location headers
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        And I have latitude "28.508632"
        And I have longitude "77.092242"
        When I send school payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response should contain payment options

    @school_payment_options @wallet_details @pay_to_school @sasai
    Scenario: Verify wallet details in payment options
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send school payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And payment options should contain wallet details
        And wallet details should have masked account number

    @school_payment_options @extract_token @pay_to_school @sasai
    Scenario: Extract instrument token for payment
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send school payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And I extract instrument token from response
        And instrument token should be valid format

    @school_payment_options @cache @pay_to_school @sasai
    Scenario: Verify payment options can be called multiple times
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send school payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response should contain payment options
        When I send school payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response should contain payment options

    @school_payment_options @payment_menu @pay_to_school @sasai
    Scenario: Verify payment menu in response
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send school payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response should have payment menu

    @school_payment_options @providers @pay_to_school @sasai
    Scenario: Verify payment providers information
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send school payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And payment options should have providers list
        And providers should have health check status

    @school_payment_options @balance_enquiry @pay_to_school @sasai
    Scenario: Verify balance enquiry capability in payment options
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send school payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And payment providers should support balance enquiry
