Feature: Pay to Merchant- Payment
    As a user
    I want to make utility payments through Sasai Payment Gateway API
    So that I can complete merchant payments for utility services

    # NOTE: Utility Payment API requires user token (accessToken) from PIN Verify API
    # This is part of the "Merchant Payment" flow (after Payment Options)
    # Endpoint: POST /bff/v2/order/utility/payment

    Background:
        Given API is available
        And I am authenticated with valid app token
        And I have valid user token from PIN verification
        And I have valid user authentication
        And I have service type "sasai-app-payment"
        And I have request ID "bdefac7b-bbc0-48b4-9ef0-84e6b9b34a6f"
        When I send payment options request to "/bff/v1/payment/options"
        Then response status code should be 200
        And response should contain payment options

    @smoke @utility_payment @merchant_payment @sasai
    Scenario: Create utility payment with valid parameters
        Given I have valid user authentication
        And I have utility payment request body
        When I send utility payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response time should be less than 10000 ms
        And response should contain payment confirmation

    @utility_payment @positive @merchant_payment @sasai
    Scenario: Create utility payment with all required fields
        Given I have valid user authentication
        And I have fee amount 0
        And I have currency "USD"
        And I have biller details for utility payment
        And I have payer amount 7
        And I have payer details with encrypted PIN
        And I have payment subtype "merchant-pay"
        And I have channel "sasai-super-app"
        And I have device information
        When I send utility payment request with complete body
        Then response status code should be 200
        And response should contain payment confirmation
        And response should contain transaction ID

    @utility_payment @positive @merchant_payment @sasai
    Scenario: Create utility payment with notes field
        Given I have valid user authentication
        And I have utility payment request body
        And I have payment notes
        When I send utility payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response should contain payment confirmation

    @utility_payment @negative @merchant_payment @sasai
    Scenario: Create utility payment without authentication
        Given I have no authentication token
        And I have utility payment request body
        When I send utility payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 401

    @utility_payment @negative @merchant_payment @sasai
    Scenario: Create utility payment with app token instead of user token
        Given I have app token only
        And I have utility payment request body
        When I send utility payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 401 or 403

    @utility_payment @negative @merchant_payment @sasai
    Scenario: Create utility payment with expired user token
        Given I have expired user token
        And I have utility payment request body
        When I send utility payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 401

    @utility_payment @negative @merchant_payment @sasai
    Scenario: Create utility payment with invalid user token
        Given I have invalid user token
        And I have utility payment request body
        When I send utility payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 401

    @utility_payment @negative @merchant_payment @sasai
    Scenario: Create utility payment with missing biller details
        Given I have valid user authentication
        And I have utility payment request without biller details
        When I send utility payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 400

    @utility_payment @negative @merchant_payment @sasai
    Scenario: Create utility payment with missing payer details
        Given I have valid user authentication
        And I have utility payment request without payer details
        When I send utility payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 400

    @utility_payment @negative @merchant_payment @sasai
    Scenario: Create utility payment with invalid currency
        Given I have valid user authentication
        And I have utility payment request body
        And I have invalid currency "XXX"
        When I send utility payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 400

    @utility_payment @negative @merchant_payment @sasai
    Scenario: Create utility payment with missing encrypted PIN
        Given I have valid user authentication
        And I have utility payment request without encrypted PIN
        When I send utility payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 400

    @utility_payment @negative @merchant_payment @sasai
    Scenario: Create utility payment with invalid encrypted PIN
        Given I have valid user authentication
        And I have utility payment request body
        And I have invalid payment PIN "invalid_pin_12345"
        When I send utility payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 400 or 401

    @utility_payment @negative @merchant_payment @sasai
    Scenario: Create utility payment with missing payment method
        Given I have valid user authentication
        And I have utility payment request without payment method
        When I send utility payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 400

    @utility_payment @negative @merchant_payment @sasai
    Scenario: Create utility payment with invalid payment method
        Given I have valid user authentication
        And I have utility payment request body
        And I have invalid payment method "invalid-method"
        When I send utility payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 400

    @utility_payment @negative @merchant_payment @sasai
    Scenario: Create utility payment with missing amount
        Given I have valid user authentication
        And I have utility payment request without amount
        When I send utility payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 400

    @utility_payment @negative @merchant_payment @sasai
    Scenario: Create utility payment with zero amount
        Given I have valid user authentication
        And I have utility payment request body
        And I have payer amount 0
        When I send utility payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 400

    @utility_payment @negative @merchant_payment @sasai
    Scenario: Create utility payment with negative amount
        Given I have valid user authentication
        And I have utility payment request body
        And I have payer amount -10
        When I send utility payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 400

    @utility_payment @validation @merchant_payment @sasai
    Scenario: Verify utility payment response structure
        Given I have valid user authentication
        And I have utility payment request body
        When I send utility payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response body should be valid JSON
        And response should have payment structure

    @utility_payment @validation @merchant_payment @sasai
    Scenario: Verify utility payment response contains required fields
        Given I have valid user authentication
        And I have utility payment request body
        When I send utility payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And payment response should have required fields

    @utility_payment @validation @merchant_payment @sasai
    Scenario: Verify utility payment response contains transaction ID
        Given I have valid user authentication
        And I have utility payment request body
        When I send utility payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response should contain transaction ID

    @utility_payment @headers @validation @merchant_payment @sasai
    Scenario: Verify utility payment response headers
        Given I have valid user authentication
        And I have utility payment request body
        When I send utility payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response header "Content-Type" should be present
        And response header "Content-Type" should contain "application/json"

    @utility_payment @security @merchant_payment @sasai
    Scenario: Verify utility payment with missing Authorization header
        Given I have no Authorization header
        And I have utility payment request body
        When I send utility payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 401

    @utility_payment @security @merchant_payment @sasai
    Scenario: Verify utility payment with empty Bearer token
        Given I have empty Bearer token
        And I have utility payment request body
        When I send utility payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 401

    @utility_payment @security @merchant_payment @sasai
    Scenario: Verify utility payment with malformed Bearer token
        Given I have malformed Bearer token
        And I have utility payment request body
        When I send utility payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 401

    @utility_payment @error_handling @merchant_payment @sasai
    Scenario: Create utility payment with invalid HTTP method
        Given I have valid user authentication
        And I have utility payment request body
        When I send GET request to "/bff/v2/order/utility/payment"
        Then response status code should be 405

    @utility_payment @error_handling @merchant_payment @sasai
    Scenario: Create utility payment with wrong endpoint path
        Given I have valid user authentication
        And I have utility payment request body
        When I send POST request to "/bff/v2/order/utility/payments"
        Then response status code should be 404

    @utility_payment @error_handling @merchant_payment @sasai
    Scenario: Create utility payment with malformed JSON body
        Given I have valid user authentication
        And I have malformed JSON request body
        When I send utility payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 400

    @utility_payment @performance @merchant_payment @sasai
    Scenario: Verify utility payment response time
        Given I have valid user authentication
        And I have utility payment request body
        When I send utility payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response time should be less than 8000 ms

    @utility_payment @integration @merchant_payment @sasai
    Scenario: Complete flow - PIN Verify to Utility Payment
        Given I have valid PIN verification details
        When I send PIN verification request to "/bff/v4/auth/pin/verify"
        Then response status code should be 200
        And I store the user token from response
        Given I have utility payment request body
        When I send utility payment request with stored token to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response should contain payment confirmation

    @utility_payment @integration @merchant_payment @sasai
    Scenario: Complete merchant payment flow - Payment Options to Utility Payment
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v1/payment/options"
        Then response status code should be 200
        And response should contain payment options
        Given I have utility payment request body
        When I send utility payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response should contain payment confirmation
        And response should contain transaction ID
