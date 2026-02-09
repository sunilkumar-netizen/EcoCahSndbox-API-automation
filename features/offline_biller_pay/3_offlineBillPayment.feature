Feature: Offline Bill Payment
    As a user
    I want to make offline bill payments
    So that I can pay utility bills using my wallet

    # NOTE: Offline Bill Payment API requires user token (accessToken) from PIN Verify API
    # Endpoint: POST /bff/v2/order/utility/payment
    # Request Body: Contains biller details, payer details with instrument token, amount, currency
    # Response: Returns payment confirmation with transaction ID and status
    # This API uses instrument token from payment options API and PIN encryption

    Background:
        Given API is available
        And I am authenticated with valid app token
        And I have valid user token from PIN verification

    @smoke @offline_bill_payment @offline_biller_pay @sasai
    Scenario: Make offline bill payment with valid details
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And I extract instrument token from response
        Given I have offline bill payment details
            | field           | value                |
            | merchantCode    | 8002                 |
            | accountNumber   | 1472365288           |
            | amount          | 3.0                  |
            | currency        | USD                  |
            | operatorId      | SZWOBO0001           |
            | categoryId      | SZWC10019            |
        When I send offline bill payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response body should be valid JSON
        And response should contain payment confirmation
        And response should have transaction ID
        And I should see final payment status in response
        And payment status should be success

    @offline_bill_payment @positive @offline_biller_pay @sasai
    Scenario: Verify offline bill payment response structure
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And I extract instrument token from response
        Given I have offline bill payment details
            | field           | value                |
            | merchantCode    | 8002                 |
            | accountNumber   | 1472365288           |
            | amount          | 3.0                  |
            | currency        | USD                  |
        When I send offline bill payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response should have payment status
        And response should have payment reference
        And I extract payment status from response
        And payment status should be success

    @offline_bill_payment @positive @offline_biller_pay @sasai
    Scenario: Complete flow - Lookup biller then make payment
        Given I have valid user authentication
        And I have merchant code "8002"
        When I send offline biller lookup request to "/bff/v1/catalog/merchant-lookup"
        Then response status code should be 200
        And response should contain biller details
        And I extract merchant code from response
        Given I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And I extract instrument token from response
        Given I have offline bill payment details with extracted data
            | field           | value                |
            | accountNumber   | 1472365288           |
            | amount          | 5.0                  |
            | currency        | USD                  |
        When I send offline bill payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response should contain payment confirmation
        And I should see final payment status in response
        And payment status should be success

    @offline_bill_payment @positive @offline_biller_pay @sasai
    Scenario: Make bill payment with different amounts
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And I extract instrument token from response
        Given I have offline bill payment details
            | field           | value                |
            | merchantCode    | 8002                 |
            | accountNumber   | 1472365288           |
            | amount          | 10.0                 |
            | currency        | USD                  |
        When I send offline bill payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And payment amount should match requested amount
        And I extract payment status from response
        And payment status should be success

    @offline_bill_payment @negative @offline_biller_pay @sasai
    Scenario: Make bill payment without authentication
        Given I have no authentication token
        And I have offline bill payment details
            | field           | value                |
            | merchantCode    | 8002                 |
            | accountNumber   | 1472365288           |
            | amount          | 3.0                  |
            | currency        | USD                  |
        When I send offline bill payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 401

    @offline_bill_payment @negative @offline_biller_pay @sasai
    Scenario: Make bill payment with invalid user token
        Given I have invalid user token
        And I have offline bill payment details
            | field           | value                |
            | merchantCode    | 8002                 |
            | accountNumber   | 1472365288           |
            | amount          | 3.0                  |
            | currency        | USD                  |
        When I send offline bill payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 401

    @offline_bill_payment @negative @offline_biller_pay @sasai
    Scenario: Make bill payment with expired user token
        Given I have expired user token
        And I have offline bill payment details
            | field           | value                |
            | merchantCode    | 8002                 |
            | accountNumber   | 1472365288           |
            | amount          | 3.0                  |
            | currency        | USD                  |
        When I send offline bill payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 401

    @offline_bill_payment @negative @offline_biller_pay @sasai
    Scenario: Make bill payment with invalid instrument token
        Given I have valid user authentication
        And I have offline bill payment details with invalid instrument token
            | field           | value                |
            | merchantCode    | 8002                 |
            | accountNumber   | 1472365288           |
            | amount          | 3.0                  |
            | currency        | USD                  |
        When I send offline bill payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 400 or 404

    @offline_bill_payment @negative @offline_biller_pay @sasai
    Scenario: Make bill payment with missing instrument token
        Given I have valid user authentication
        And I have offline bill payment details without instrument token
            | field           | value                |
            | merchantCode    | 8002                 |
            | accountNumber   | 1472365288           |
            | amount          | 3.0                  |
            | currency        | USD                  |
        When I send offline bill payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 400

    @offline_bill_payment @negative @offline_biller_pay @sasai
    Scenario: Make bill payment with missing biller details
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And I extract instrument token from response
        Given I have offline bill payment details without biller details
        When I send offline bill payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 400

    @offline_bill_payment @negative @offline_biller_pay @sasai
    Scenario: Make bill payment with invalid merchant code
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And I extract instrument token from response
        Given I have offline bill payment details
            | field           | value                |
            | merchantCode    | INVALID999           |
            | accountNumber   | 1472365288           |
            | amount          | 3.0                  |
            | currency        | USD                  |
        When I send offline bill payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 400 or 404

    @offline_bill_payment @negative @offline_biller_pay @sasai
    Scenario: Make bill payment with invalid account number
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And I extract instrument token from response
        Given I have offline bill payment details
            | field           | value                |
            | merchantCode    | 8002                 |
            | accountNumber   | INVALID123           |
            | amount          | 3.0                  |
            | currency        | USD                  |
        When I send offline bill payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 400 or 404

    @offline_bill_payment @negative @offline_biller_pay @sasai
    Scenario: Make bill payment with zero amount
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And I extract instrument token from response
        Given I have offline bill payment details
            | field           | value                |
            | merchantCode    | 8002                 |
            | accountNumber   | 1472365288           |
            | amount          | 0.0                  |
            | currency        | USD                  |
        When I send offline bill payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 400

    @offline_bill_payment @negative @offline_biller_pay @sasai
    Scenario: Make bill payment with negative amount
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And I extract instrument token from response
        Given I have offline bill payment details
            | field           | value                |
            | merchantCode    | 8002                 |
            | accountNumber   | 1472365288           |
            | amount          | -5.0                 |
            | currency        | USD                  |
        When I send offline bill payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 400

    @offline_bill_payment @negative @offline_biller_pay @sasai
    Scenario: Make bill payment with missing amount
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And I extract instrument token from response
        Given I have offline bill payment details without amount
            | field           | value                |
            | merchantCode    | 8002                 |
            | accountNumber   | 1472365288           |
            | currency        | USD                  |
        When I send offline bill payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 400

    @offline_bill_payment @negative @offline_biller_pay @sasai
    Scenario: Make bill payment with invalid currency
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And I extract instrument token from response
        Given I have offline bill payment details
            | field           | value                |
            | merchantCode    | 8002                 |
            | accountNumber   | 1472365288           |
            | amount          | 3.0                  |
            | currency        | INVALID              |
        When I send offline bill payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 400

    @offline_bill_payment @validation @offline_biller_pay @sasai
    Scenario: Verify bill payment response contains required fields
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And I extract instrument token from response
        Given I have offline bill payment details
            | field           | value                |
            | merchantCode    | 8002                 |
            | accountNumber   | 1472365288           |
            | amount          | 3.0                  |
            | currency        | USD                  |
        When I send offline bill payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response should have required payment fields
        And response should have transaction details

    @offline_bill_payment @validation @offline_biller_pay @sasai
    Scenario: Verify payment status in response
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And I extract instrument token from response
        Given I have offline bill payment details
            | field           | value                |
            | merchantCode    | 8002                 |
            | accountNumber   | 1472365288           |
            | amount          | 3.0                  |
            | currency        | USD                  |
        When I send offline bill payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And payment status should be valid

    @offline_bill_payment @headers @validation @offline_biller_pay @sasai
    Scenario: Verify bill payment response headers
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And I extract instrument token from response
        Given I have offline bill payment details
            | field           | value                |
            | merchantCode    | 8002                 |
            | accountNumber   | 1472365288           |
            | amount          | 3.0                  |
            | currency        | USD                  |
        When I send offline bill payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response header "Content-Type" should be present
        And response header "Content-Type" should contain "application/json"

    @offline_bill_payment @security @offline_biller_pay @sasai
    Scenario: Verify bill payment with missing Authorization header
        Given I have no Authorization header
        And I have offline bill payment details
            | field           | value                |
            | merchantCode    | 8002                 |
            | accountNumber   | 1472365288           |
            | amount          | 3.0                  |
            | currency        | USD                  |
        When I send offline bill payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 401

    @offline_bill_payment @security @offline_biller_pay @sasai
    Scenario: Verify bill payment with empty Bearer token
        Given I have empty Bearer token
        And I have offline bill payment details
            | field           | value                |
            | merchantCode    | 8002                 |
            | accountNumber   | 1472365288           |
            | amount          | 3.0                  |
            | currency        | USD                  |
        When I send offline bill payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 401

    @offline_bill_payment @security @offline_biller_pay @sasai
    Scenario: Verify bill payment with malformed Bearer token
        Given I have malformed Bearer token
        And I have offline bill payment details
            | field           | value                |
            | merchantCode    | 8002                 |
            | accountNumber   | 1472365288           |
            | amount          | 3.0                  |
            | currency        | USD                  |
        When I send offline bill payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 401

    @offline_bill_payment @error_handling @offline_biller_pay @sasai
    Scenario: Bill payment with invalid HTTP method GET
        Given I have valid user authentication
        When I send GET request to "/bff/v2/order/utility/payment"
        Then response status code should be 405

    @offline_bill_payment @error_handling @offline_biller_pay @sasai
    Scenario: Bill payment with invalid HTTP method PUT
        Given I have valid user authentication
        When I send PUT request to "/bff/v2/order/utility/payment"
        Then response status code should be 405

    @offline_bill_payment @error_handling @offline_biller_pay @sasai
    Scenario: Bill payment with wrong endpoint path
        Given I have valid user authentication
        And I have offline bill payment details
            | field           | value                |
            | merchantCode    | 8002                 |
            | accountNumber   | 1472365288           |
            | amount          | 3.0                  |
            | currency        | USD                  |
        When I send offline bill payment request to "/bff/v2/order/utility/payments"
        Then response status code should be 404

    @offline_bill_payment @performance @offline_biller_pay @sasai
    Scenario: Verify bill payment response time
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And I extract instrument token from response
        Given I have offline bill payment details
            | field           | value                |
            | merchantCode    | 8002                 |
            | accountNumber   | 1472365288           |
            | amount          | 3.0                  |
            | currency        | USD                  |
        When I send offline bill payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response time should be less than 5000 ms

    @offline_bill_payment @performance @offline_biller_pay @sasai
    Scenario: Verify bill payment response time is acceptable
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And I extract instrument token from response
        Given I have offline bill payment details
            | field           | value                |
            | merchantCode    | 8002                 |
            | accountNumber   | 1472365288           |
            | amount          | 3.0                  |
            | currency        | USD                  |
        When I send offline bill payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response time should be less than 10000 ms

    @offline_bill_payment @data_validation @offline_biller_pay @sasai
    Scenario: Verify transaction ID format
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And I extract instrument token from response
        Given I have offline bill payment details
            | field           | value                |
            | merchantCode    | 8002                 |
            | accountNumber   | 1472365288           |
            | amount          | 3.0                  |
            | currency        | USD                  |
        When I send offline bill payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And transaction ID format should be valid

    @offline_bill_payment @data_validation @offline_biller_pay @sasai
    Scenario: Verify payment reference is unique
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And I extract instrument token from response
        Given I have offline bill payment details
            | field           | value                |
            | merchantCode    | 8002                 |
            | accountNumber   | 1472365288           |
            | amount          | 3.0                  |
            | currency        | USD                  |
        When I send offline bill payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And I extract payment reference from response
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And I extract instrument token from response
        Given I have offline bill payment details
            | field           | value                |
            | merchantCode    | 8002                 |
            | accountNumber   | 1472365288           |
            | amount          | 3.0                  |
            | currency        | USD                  |
        When I send offline bill payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And I extract second payment reference from response
        And second payment reference should be different from first

    @offline_bill_payment @currency @offline_biller_pay @sasai
    Scenario Outline: Make bill payment with different currencies
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And I extract instrument token from response
        Given I have offline bill payment details
            | field           | value                |
            | merchantCode    | 8002                 |
            | accountNumber   | 1472365288           |
            | amount          | <amount>             |
            | currency        | <currency>           |
        When I send offline bill payment request to "/bff/v2/order/utility/payment"
        Then response status code should be <statusCode>

        Examples:
            | currency | amount | statusCode |
            | USD      | 3.0    | 200        |
            | ZWG      | 3.0    | 200 or 400 |

    @offline_bill_payment @amounts @offline_biller_pay @sasai
    Scenario Outline: Make bill payment with different amounts
        Given I have valid user authentication
        And I have service type "sasai-app-payment"
        When I send payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And I extract instrument token from response
        Given I have offline bill payment details
            | field           | value                |
            | merchantCode    | 8002                 |
            | accountNumber   | 1472365288           |
            | amount          | <amount>             |
            | currency        | USD                  |
        When I send offline bill payment request to "/bff/v2/order/utility/payment"
        Then response status code should be <statusCode>

        Examples:
            | amount  | statusCode |
            | 1.0     | 200        |
            | 5.0     | 200        |
            | 10.0    | 200        |
            | 50.0    | 200        |
            | 100.0   | 200        |
