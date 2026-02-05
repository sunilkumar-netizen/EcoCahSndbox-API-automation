Feature: Church Payment
    As a user
    I want to make payments to churches
    So that I can donate or contribute to church activities

    # NOTE: Church Payment API requires user token (accessToken) from PIN Verify API
    # This is the final step in the "Pay to Church" flow - Step 4 after payment options
    # Endpoint: POST /bff/v2/order/utility/payment
    # Request Body: Contains payment details, biller details, payer details, device info
    # subType: "pay-to-church"

    Background:
        Given API is available
        And I am authenticated with valid app token
        And I have valid user token from PIN verification

    @smoke @church_payment @pay_to_church @sasai
    Scenario: Make church payment with valid details
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        And I have device information headers
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And I extract instrument token from response
        Given I have church payment details
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response should contain payment confirmation
        And response should have transaction ID

    @church_payment @positive @pay_to_church @sasai
    Scenario: Make church offering payment
        Given I have valid user authentication
        And I have church payment details with purpose "Offering"
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response should contain payment confirmation

    @church_payment @positive @pay_to_church @sasai
    Scenario: Make church tithe payment
        Given I have valid user authentication
        And I have church payment details with purpose "Tithe"
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response should contain payment confirmation

    @church_payment @positive @pay_to_church @sasai
    Scenario: Make church building fund payment
        Given I have valid user authentication
        And I have church payment details with purpose "Building Fund"
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response should contain payment confirmation

    @church_payment @positive @pay_to_church @sasai
    Scenario: Church payment with minimum amount
        Given I have valid user authentication
        And I have church payment details with amount 1.0
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200

    @church_payment @positive @pay_to_church @sasai
    Scenario: Church payment with different amounts
        Given I have valid user authentication
        And I have church payment details with amount 10.0
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200

    @church_payment @positive @pay_to_church @sasai
    Scenario: Church payment with USD currency
        Given I have valid user authentication
        And I have church payment details with currency "USD"
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200

    @church_payment @positive @pay_to_church @sasai
    Scenario: Church payment with ZWL currency
        Given I have valid user authentication
        And I have church payment details with currency "ZWL"
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200

    @church_payment @negative @pay_to_church @sasai
    Scenario: Church payment without authentication
        Given I have no authentication token
        And I have church payment details
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 401

    @church_payment @negative @pay_to_church @sasai
    Scenario: Church payment with invalid user token
        Given I have invalid user token
        And I have church payment details
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 401

    @church_payment @negative @pay_to_church @sasai
    Scenario: Church payment with expired user token
        Given I have expired user token
        And I have church payment details
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 401

    @church_payment @negative @pay_to_church @sasai
    Scenario: Church payment with app token instead of user token
        Given I have app token only
        And I have church payment details
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 401 or 403

    @church_payment @negative @pay_to_church @sasai
    Scenario: Church payment without payment details
        Given I have valid user authentication
        And I have no payment details
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 400

    @church_payment @negative @pay_to_church @sasai
    Scenario: Church payment with missing instrument token
        Given I have valid user authentication
        And I have church payment details without instrument token
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 400

    @church_payment @negative @pay_to_church @sasai
    Scenario: Church payment with invalid instrument token
        Given I have valid user authentication
        And I have church payment details with invalid instrument token
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 400

    @church_payment @negative @pay_to_church @sasai
    Scenario: Church payment with missing PIN
        Given I have valid user authentication
        And I have church payment details without PIN
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 400

    @church_payment @negative @pay_to_church @sasai
    Scenario: Church payment with incorrect PIN
        Given I have valid user authentication
        And I have church payment details with incorrect PIN
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 400 or 401

    @church_payment @negative @pay_to_church @sasai
    Scenario: Church payment with zero amount
        Given I have valid user authentication
        And I have church payment details with amount 0
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 400

    @church_payment @negative @pay_to_church @sasai
    Scenario: Church payment with negative amount
        Given I have valid user authentication
        And I have church payment details with amount -10.0
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 400

    @church_payment @negative @pay_to_church @sasai
    Scenario: Church payment with missing operator ID
        Given I have valid user authentication
        And I have church payment details without operator ID
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 400

    @church_payment @negative @pay_to_church @sasai
    Scenario: Church payment with invalid operator ID
        Given I have valid user authentication
        And I have church payment details with operator ID "INVALID123"
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 400 or 404

    @church_payment @negative @pay_to_church @sasai
    Scenario: Church payment with missing category ID
        Given I have valid user authentication
        And I have church payment details without category ID
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 400

    @church_payment @negative @pay_to_church @sasai
    Scenario: Church payment with invalid category ID
        Given I have valid user authentication
        And I have church payment details with category ID "INVALID"
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 400 or 404

    @church_payment @negative @pay_to_church @sasai
    Scenario: Church payment with missing church code
        Given I have valid user authentication
        And I have church payment details without church code
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 400

    @church_payment @negative @pay_to_church @sasai
    Scenario: Church payment with invalid currency
        Given I have valid user authentication
        And I have church payment details with currency "INVALID"
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 400

    @church_payment @negative @pay_to_church @sasai
    Scenario: Church payment with missing payment method
        Given I have valid user authentication
        And I have church payment details without payment method
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 400

    @church_payment @negative @pay_to_church @sasai
    Scenario: Church payment with insufficient balance
        Given I have valid user authentication
        And I have church payment details with amount 999999.0
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 400 or 402

    @church_payment @validation @pay_to_church @sasai
    Scenario: Verify church payment response structure
        Given I have valid user authentication
        And I have church payment details
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response body should be valid JSON
        And response should have payment structure

    @church_payment @validation @pay_to_church @sasai
    Scenario: Verify church payment response contains required fields
        Given I have valid user authentication
        And I have church payment details
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And payment response should have required fields

    @church_payment @validation @pay_to_church @sasai
    Scenario: Verify transaction ID format
        Given I have valid user authentication
        And I have church payment details
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response should have transaction ID
        And transaction ID should be valid format

    @church_payment @headers @validation @pay_to_church @sasai
    Scenario: Verify church payment response headers
        Given I have valid user authentication
        And I have church payment details
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response header "Content-Type" should be present
        And response header "Content-Type" should contain "application/json"

    @church_payment @headers @validation @pay_to_church @sasai
    Scenario: Church payment with request ID header
        Given I have valid user authentication
        And I have church payment details
        And I have request ID "2e74fcf0-d426-11f0-9f80-97a3c8562f7e"
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200

    @church_payment @security @pay_to_church @sasai
    Scenario: Verify church payment with missing Authorization header
        Given I have no Authorization header
        And I have church payment details
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 401

    @church_payment @security @pay_to_church @sasai
    Scenario: Verify church payment with empty Bearer token
        Given I have empty Bearer token
        And I have church payment details
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 401

    @church_payment @security @pay_to_church @sasai
    Scenario: Verify church payment with malformed Bearer token
        Given I have malformed Bearer token
        And I have church payment details
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 401

    @church_payment @error_handling @pay_to_church @sasai
    Scenario: Church payment with invalid HTTP method GET
        Given I have valid user authentication
        And I have church payment details
        When I send GET request to "/bff/v2/order/utility/payment"
        Then response status code should be 405

    @church_payment @error_handling @pay_to_church @sasai
    Scenario: Church payment with invalid HTTP method PUT
        Given I have valid user authentication
        And I have church payment details
        When I send PUT request to "/bff/v2/order/utility/payment"
        Then response status code should be 405

    @church_payment @error_handling @pay_to_church @sasai
    Scenario: Church payment with invalid HTTP method DELETE
        Given I have valid user authentication
        And I have church payment details
        When I send DELETE request to "/bff/v2/order/utility/payment"
        Then response status code should be 405

    @church_payment @error_handling @pay_to_church @sasai
    Scenario: Church payment with wrong endpoint path
        Given I have valid user authentication
        And I have church payment details
        And I have device information headers
        When I send POST request to "/bff/v2/order/payment"
        Then response status code should be 404

    @church_payment @performance @pay_to_church @sasai
    Scenario: Verify church payment response time
        Given I have valid user authentication
        And I have church payment details
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response time should be less than 5000 ms

    @church_payment @performance @pay_to_church @sasai
    Scenario: Verify church payment response time is acceptable
        Given I have valid user authentication
        And I have church payment details
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response time should be less than 10000 ms

    @church_payment @integration @pay_to_church @sasai
    Scenario: Complete flow - Payment Options to Church Payment
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        And I have device information headers
        When I send church payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And I extract instrument token from response
        Given I have church payment details with extracted instrument token
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response should contain payment confirmation

    @church_payment @integration @pay_to_church @sasai
    Scenario: Complete flow - Church Lookup to Payment
        Given I have valid user authentication
        And I have merchant code "156611"
        When I send merchant lookup by code request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And I extract merchant name from response
        And I extract merchant code from response
        Given I have church payment details with extracted merchant info
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200

    @church_payment @integration @pay_to_church @sasai
    Scenario: Complete flow - PIN Verify to Church Payment
        Given I have valid PIN verification details
        When I send PIN verification request to "/bff/v4/auth/pin/verify"
        Then response status code should be 200
        And I store the user token from response
        Given I have church payment details
        And I have device information headers
        When I send church payment request with stored token to "/bff/v2/order/utility/payment"
        Then response status code should be 200

    @church_payment @integration @pay_to_church @sasai
    Scenario: Complete end-to-end church payment flow
        Given I have valid user authentication
        # Step 1: Search for church
        And I have search type "CHURCH"
        And I have page number 0
        And I have page size 10
        And I have name query "FAITH MINISTRIES"
        When I send church search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 200
        And I extract first merchant code from search results
        # Step 2: Lookup church details
        When I send merchant lookup by code request with extracted code to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And I extract merchant name from response
        # Step 3: Get payment options
        Given I have service type "sasai-app-payment"
        And I have device information headers
        When I send church payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And I extract instrument token from response
        # Step 4: Make payment
        Given I have church payment details with extracted info
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response should contain payment confirmation

    @church_payment @data_validation @pay_to_church @sasai
    Scenario: Verify payment confirmation details
        Given I have valid user authentication
        And I have church payment details
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And payment confirmation should have transaction details
        And payment confirmation should have amount

    @church_payment @data_validation @pay_to_church @sasai
    Scenario: Verify payment response contains church details
        Given I have valid user authentication
        And I have church payment details
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response should contain church name
        And response should contain church code

    @church_payment @idempotency @pay_to_church @sasai
    Scenario: Duplicate payment with same request ID should be prevented
        Given I have valid user authentication
        And I have church payment details
        And I have request ID "duplicate-test-12345"
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 400 or 409

    @church_payment @amount_validation @pay_to_church @sasai
    Scenario Outline: Church payment with different amounts
        Given I have valid user authentication
        And I have church payment details with amount <amount>
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be <statusCode>

        Examples:
            | amount   | statusCode |
            | 1.0      | 200        |
            | 5.0      | 200        |
            | 10.0     | 200        |
            | 50.0     | 200        |
            | 100.0    | 200        |
            | 0.5      | 200 or 400 |
            | 0.01     | 200 or 400 |

    @church_payment @currency_validation @pay_to_church @sasai
    Scenario Outline: Church payment with different currencies
        Given I have valid user authentication
        And I have church payment details with currency "<currency>"
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be <statusCode>

        Examples:
            | currency | statusCode |
            | USD      | 200        |
            | ZWL      | 200        |
            | EUR      | 400        |
            | GBP      | 400        |

    @church_payment @purpose_validation @pay_to_church @sasai
    Scenario Outline: Church payment with different purposes
        Given I have valid user authentication
        And I have church payment details with purpose "<purpose>"
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200

        Examples:
            | purpose            |
            | Offering           |
            | Tithe              |
            | Building Fund      |
            | Mission Support    |
            | Special Collection |

    @church_payment @device_info @pay_to_church @sasai
    Scenario: Church payment with complete device information
        Given I have valid user authentication
        And I have church payment details
        And I have all required device headers
        And I have complete device information in payload
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200

    @church_payment @extract_data @pay_to_church @sasai
    Scenario: Extract payment confirmation details
        Given I have valid user authentication
        And I have church payment details
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And I extract transaction ID from payment response
        And I extract payment status from payment response
        And extracted payment details should not be empty

    @church_payment @payment_method @pay_to_church @sasai
    Scenario: Church payment with wallet payment method
        Given I have valid user authentication
        And I have church payment details with payment method "wallet"
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200

    @church_payment @provider_validation @pay_to_church @sasai
    Scenario: Church payment with ecocash provider
        Given I have valid user authentication
        And I have church payment details with provider "ecocash"
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200

    @church_payment @subtype_validation @pay_to_church @sasai
    Scenario: Verify pay-to-church subtype is required
        Given I have valid user authentication
        And I have church payment details with subtype "pay-to-church"
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200

    @church_payment @channel_validation @pay_to_church @sasai
    Scenario: Church payment with sasai-super-app channel
        Given I have valid user authentication
        And I have church payment details with channel "sasai-super-app"
        And I have device information headers
        When I send church payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
