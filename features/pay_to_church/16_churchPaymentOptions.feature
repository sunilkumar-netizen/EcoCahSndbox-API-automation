Feature: Church Payment Options
    As a user
    I want to get available payment options for church payments
    So that I can choose how to make my church donation

    # NOTE: Church Payment Options API requires user token (accessToken) from PIN Verify API
    # This is part of the "Pay to Church" flow - Step 3 after church lookup
    # Endpoint: GET /bff/v2/payment/options
    # Query Parameter: serviceType=sasai-app-payment
    # Required Headers: Device information, location, authorization

    Background:
        Given API is available
        And I am authenticated with valid app token
        And I have valid user token from PIN verification

    @smoke @church_payment_options @pay_to_church @sasai
    Scenario: Get church payment options with valid authentication
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        And I have device information headers
        When I send church payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response should have payment options
        And response should have payment instruments

    @church_payment_options @positive @pay_to_church @sasai
    Scenario: Get church payment options returns correct structure
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        And I have device information headers
        When I send church payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response body should be valid JSON
        And response should have payment options structure

    @church_payment_options @positive @pay_to_church @sasai
    Scenario: Get church payment options with all required headers
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        And I have all required device headers
        When I send church payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response should contain wallet payment option

    @church_payment_options @positive @pay_to_church @sasai
    Scenario: Get church payment options with location headers
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        And I have device information headers
        And I have latitude "28.508632"
        And I have longitude "77.092242"
        When I send church payment options request to "/bff/v2/payment/options"
        Then response status code should be 200

    @church_payment_options @negative @pay_to_church @sasai
    Scenario: Get church payment options without authentication
        Given I have no authentication token
        And I have service type "sasai-app-payment"
        And I have device information headers
        When I send church payment options request to "/bff/v2/payment/options"
        Then response status code should be 401

    @church_payment_options @negative @pay_to_church @sasai
    Scenario: Get church payment options with invalid user token
        Given I have invalid user token
        And I have service type "sasai-app-payment"
        And I have device information headers
        When I send church payment options request to "/bff/v2/payment/options"
        Then response status code should be 401

    @church_payment_options @negative @pay_to_church @sasai
    Scenario: Get church payment options with expired user token
        Given I have expired user token
        And I have service type "sasai-app-payment"
        And I have device information headers
        When I send church payment options request to "/bff/v2/payment/options"
        Then response status code should be 401

    @church_payment_options @negative @pay_to_church @sasai
    Scenario: Get church payment options with app token instead of user token
        Given I have app token only
        And I have service type "sasai-app-payment"
        And I have device information headers
        When I send church payment options request to "/bff/v2/payment/options"
        Then response status code should be 401 or 403

    @church_payment_options @negative @pay_to_church @sasai
    Scenario: Get church payment options without service type parameter
        Given I have valid user authentication
        And I have no service type
        And I have device information headers
        When I send church payment options request to "/bff/v2/payment/options"
        Then response status code should be 400

    @church_payment_options @negative @pay_to_church @sasai
    Scenario: Get church payment options with empty service type
        Given I have valid user authentication
        And I have service type ""
        And I have device information headers
        When I send church payment options request to "/bff/v2/payment/options"
        Then response status code should be 400

    @church_payment_options @negative @pay_to_church @sasai
    Scenario: Get church payment options with invalid service type
        Given I have valid user authentication
        And I have service type "invalid-service-type"
        And I have device information headers
        When I send church payment options request to "/bff/v2/payment/options"
        Then response status code should be 400 or 404

    @church_payment_options @validation @pay_to_church @sasai
    Scenario: Verify church payment options response contains required fields
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        And I have device information headers
        When I send church payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response should have payment options
        And response should have payment instruments

    @church_payment_options @validation @pay_to_church @sasai
    Scenario: Verify church payment options response structure
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        And I have device information headers
        When I send church payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response body should be valid JSON
        And response should have payment options structure

    @church_payment_options @headers @validation @pay_to_church @sasai
    Scenario: Verify church payment options response headers
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        And I have device information headers
        When I send church payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response header "Content-Type" should be present
        And response header "Content-Type" should contain "application/json"

    @church_payment_options @headers @validation @pay_to_church @sasai
    Scenario: Church payment options with request ID header
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        And I have request ID "43843e90-d1c8-11f0-a41e-95f35da604e5"
        And I have device information headers
        When I send church payment options request to "/bff/v2/payment/options"
        Then response status code should be 200

    @church_payment_options @device_headers @pay_to_church @sasai
    Scenario: Church payment options with device type header
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        And I have device type "android"
        And I have device information headers
        When I send church payment options request to "/bff/v2/payment/options"
        Then response status code should be 200

    @church_payment_options @device_headers @pay_to_church @sasai
    Scenario: Church payment options with OS version header
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        And I have OS version "15"
        And I have device information headers
        When I send church payment options request to "/bff/v2/payment/options"
        Then response status code should be 200

    @church_payment_options @device_headers @pay_to_church @sasai
    Scenario: Church payment options with app version header
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        And I have app version "2.2.1"
        And I have device information headers
        When I send church payment options request to "/bff/v2/payment/options"
        Then response status code should be 200

    @church_payment_options @security @pay_to_church @sasai
    Scenario: Verify church payment options with missing Authorization header
        Given I have no Authorization header
        And I have service type "sasai-app-payment"
        And I have device information headers
        When I send church payment options request to "/bff/v2/payment/options"
        Then response status code should be 401

    @church_payment_options @security @pay_to_church @sasai
    Scenario: Verify church payment options with empty Bearer token
        Given I have empty Bearer token
        And I have service type "sasai-app-payment"
        And I have device information headers
        When I send church payment options request to "/bff/v2/payment/options"
        Then response status code should be 401

    @church_payment_options @security @pay_to_church @sasai
    Scenario: Verify church payment options with malformed Bearer token
        Given I have malformed Bearer token
        And I have service type "sasai-app-payment"
        And I have device information headers
        When I send church payment options request to "/bff/v2/payment/options"
        Then response status code should be 401

    @church_payment_options @error_handling @pay_to_church @sasai
    Scenario: Church payment options with invalid HTTP method POST
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send POST request to "/bff/v2/payment/options"
        Then response status code should be 405

    @church_payment_options @error_handling @pay_to_church @sasai
    Scenario: Church payment options with invalid HTTP method PUT
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send PUT request to "/bff/v2/payment/options"
        Then response status code should be 405

    @church_payment_options @error_handling @pay_to_church @sasai
    Scenario: Church payment options with invalid HTTP method DELETE
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send DELETE request to "/bff/v2/payment/options"
        Then response status code should be 405

    @church_payment_options @error_handling @pay_to_church @sasai
    Scenario: Church payment options with wrong endpoint path
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send GET request to "/bff/v2/payment/option"
        Then response status code should be 404

    @church_payment_options @performance @pay_to_church @sasai
    Scenario: Verify church payment options response time
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        And I have device information headers
        When I send church payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response time should be less than 3000 ms

    @church_payment_options @performance @pay_to_church @sasai
    Scenario: Verify church payment options response time is acceptable
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        And I have device information headers
        When I send church payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response time should be less than 5000 ms

    @church_payment_options @integration @pay_to_church @sasai
    Scenario: Complete flow - Church Lookup to Payment Options
        Given I have valid user authentication
        And I have merchant code "394875"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And response should contain merchant details by code
        Given I have service type "sasai-app-payment"
        And I have device information headers
        When I send church payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response should have payment options

    @church_payment_options @integration @pay_to_church @sasai
    Scenario: Complete flow - PIN Verify to Church Payment Options
        Given I have valid PIN verification details
        When I send PIN verification request to "/bff/v4/auth/pin/verify"
        Then response status code should be 200
        And I store the user token from response
        Given I have service type "sasai-app-payment"
        And I have device information headers
        When I send church payment options request with stored token to "/bff/v2/payment/options"
        Then response status code should be 200
        And response should have payment options

    @church_payment_options @integration @pay_to_church @sasai
    Scenario: Complete flow - Church Search to Lookup to Payment Options
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
        Given I have service type "sasai-app-payment"
        And I have device information headers
        When I send church payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response should have payment options

    @church_payment_options @data_validation @pay_to_church @sasai
    Scenario: Verify payment options contains wallet option
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        And I have device information headers
        When I send church payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response should contain wallet payment option

    @church_payment_options @data_validation @pay_to_church @sasai
    Scenario: Verify payment instruments are not empty
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        And I have device information headers
        When I send church payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And payment instruments should not be empty

    @church_payment_options @cache @pay_to_church @sasai
    Scenario: Verify church payment options caching behavior
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        And I have device information headers
        When I send church payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And I store response time as first_request_time
        When I send church payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response should match previous response

    @church_payment_options @concurrent @pay_to_church @sasai
    Scenario: Multiple church payment options requests with same token
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        And I have device information headers
        When I send church payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        When I send church payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        When I send church payment options request to "/bff/v2/payment/options"
        Then response status code should be 200

    @church_payment_options @service_types @pay_to_church @sasai
    Scenario Outline: Church payment options with different service types
        Given I have valid user authentication
        And I have service type "<serviceType>"
        And I have device information headers
        When I send church payment options request to "/bff/v2/payment/options"
        Then response status code should be <statusCode>

        Examples:
            | serviceType          | statusCode |
            | sasai-app-payment    | 200        |
            | invalid-service      | 400 or 404 |
            | ""                   | 400        |

    @church_payment_options @location @pay_to_church @sasai
    Scenario Outline: Church payment options with different locations
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        And I have device information headers
        And I have latitude "<latitude>"
        And I have longitude "<longitude>"
        When I send church payment options request to "/bff/v2/payment/options"
        Then response status code should be 200

        Examples:
            | latitude   | longitude  |
            | 28.508632  | 77.092242  |
            | -17.829773 | 31.054028  |
            | 0.0        | 0.0        |

    @church_payment_options @extract_data @pay_to_church @sasai
    Scenario: Extract payment options for church donation
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        And I have device information headers
        When I send church payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And I extract available payment methods from response
        And extracted payment methods should not be empty

    @church_payment_options @wallet_validation @pay_to_church @sasai
    Scenario: Verify wallet balance in payment options
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        And I have device information headers
        When I send church payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response should contain wallet payment option
        And wallet option should have balance information

    @church_payment_options @stress @pay_to_church @sasai
    Scenario: Rapid church payment options requests
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        And I have device information headers
        When I send 5 church payment options requests to "/bff/v2/payment/options"
        Then all requests should return status code 200
        And all responses should be consistent

    @church_payment_options @headers_missing @pay_to_church @sasai
    Scenario: Church payment options without device headers
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send church payment options request to "/bff/v2/payment/options"
        Then response status code should be 200 or 400

    @church_payment_options @headers_optional @pay_to_church @sasai
    Scenario: Church payment options with minimal headers
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        And I have device type "android"
        When I send church payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
