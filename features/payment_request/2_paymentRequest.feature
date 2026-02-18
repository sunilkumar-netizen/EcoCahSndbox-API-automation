Feature: Payment Request API
    As a user
    I want to create payment requests
    So that I can request money from other users

    # NOTE: Payment Request API requires user token (accessToken) from PIN Verify API
    # Endpoint: POST /bff/v3/order/payment/request
    # Request Body: {
    #   "feeAmount": 0.0,
    #   "currency": "ZWG",
    #   "payerAmount": 3,
    #   "channel": "sasai-super-app",
    #   "beneficiaryDetails": { "payeeAmount": 3 },
    #   "payerDetails": { "customerId": "customer-uuid" },
    #   "notes": { "message": "Payment request message" }
    # }
    # Response: Returns payment request details including order reference, status, and request information
    # This API is used to create a payment request from a beneficiary to request money from a payer

    Background:
        Given API is available
        And I am authenticated with valid app token
        And I have valid user token from PIN verification

    @smoke @payment_request @create_request @positive @sasai
    Scenario: Create valid payment request with all required fields
        Given I have valid user authentication
        And I have payment request details:
            | field       | value                                  |
            | feeAmount   | 0.0                                    |
            | currency    | ZWG                                    |
            | payerAmount | 3                                      |
            | payeeAmount | 3                                      |
            | channel     | sasai-super-app                        |
            | customerId  | ef1ebf57-8e9b-4c6c-be89-de72dfd7376c   |
            | message     | Test Payment Request                    |
        When I send payment request to "/bff/v3/order/payment/request"
        Then response status code should be 200
        And response body should be valid JSON
        And response should contain payment request details
        And response should contain "orderId"
        And response should contain "status"

    @payment_request @create_request @positive @sasai
    Scenario: Create payment request with custom message
        Given I have valid user authentication
        And I have payment request details:
            | field       | value                                  |
            | feeAmount   | 0.0                                    |
            | currency    | ZWG                                    |
            | payerAmount | 5                                      |
            | payeeAmount | 5                                      |
            | channel     | sasai-super-app                        |
            | customerId  | ef1ebf57-8e9b-4c6c-be89-de72dfd7376c   |
            | message     | Lunch payment request                   |
        When I send payment request to "/bff/v3/order/payment/request"
        Then response status code should be 200
        And response body should be valid JSON
        And response should contain payment request details

    @payment_request @create_request @positive @sasai
    Scenario: Create payment request with USD currency
        Given I have valid user authentication
        And I have payment request details:
            | field       | value                                  |
            | feeAmount   | 0.0                                    |
            | currency    | USD                                    |
            | payerAmount | 2                                      |
            | payeeAmount | 2                                      |
            | channel     | sasai-super-app                        |
            | customerId  | ef1ebf57-8e9b-4c6c-be89-de72dfd7376c   |
            | message     | USD Payment Request                     |
        When I send payment request to "/bff/v3/order/payment/request"
        Then response status code should be 200
        And response body should be valid JSON
        And response should contain payment request details

    @payment_request @create_request @positive @amount_variation @sasai
    Scenario: Create payment request with different amount
        Given I have valid user authentication
        And I have payment request details:
            | field       | value                                  |
            | feeAmount   | 0.0                                    |
            | currency    | ZWG                                    |
            | payerAmount | 10                                     |
            | payeeAmount | 10                                     |
            | channel     | sasai-super-app                        |
            | customerId  | ef1ebf57-8e9b-4c6c-be89-de72dfd7376c   |
            | message     | Higher amount request                   |
        When I send payment request to "/bff/v3/order/payment/request"
        Then response status code should be 200
        And response body should be valid JSON
        And response should contain payment request details

    @payment_request @create_request @negative @validation @sasai
    Scenario: Create payment request without feeAmount
        Given I have valid user authentication
        And I have payment request without feeAmount:
            | field       | value                                  |
            | currency    | ZWG                                    |
            | payerAmount | 3                                      |
            | payeeAmount | 3                                      |
            | channel     | sasai-super-app                        |
            | customerId  | ef1ebf57-8e9b-4c6c-be89-de72dfd7376c   |
            | message     | Test Payment Request                    |
        When I send payment request to "/bff/v3/order/payment/request"
        Then response status code should be 400
        And response body should be valid JSON

    @payment_request @create_request @negative @validation @sasai
    Scenario: Create payment request without currency
        Given I have valid user authentication
        And I have payment request without currency:
            | field       | value                                  |
            | feeAmount   | 0.0                                    |
            | payerAmount | 3                                      |
            | payeeAmount | 3                                      |
            | channel     | sasai-super-app                        |
            | customerId  | ef1ebf57-8e9b-4c6c-be89-de72dfd7376c   |
            | message     | Test Payment Request                    |
        When I send payment request to "/bff/v3/order/payment/request"
        Then response status code should be 400
        And response body should be valid JSON

    @payment_request @create_request @negative @validation @sasai
    Scenario: Create payment request without payerAmount
        Given I have valid user authentication
        And I have payment request without payerAmount:
            | field       | value                                  |
            | feeAmount   | 0.0                                    |
            | currency    | ZWG                                    |
            | payeeAmount | 3                                      |
            | channel     | sasai-super-app                        |
            | customerId  | ef1ebf57-8e9b-4c6c-be89-de72dfd7376c   |
            | message     | Test Payment Request                    |
        When I send payment request to "/bff/v3/order/payment/request"
        Then response status code should be 400
        And response body should be valid JSON

    @payment_request @create_request @negative @validation @sasai
    Scenario: Create payment request without channel
        Given I have valid user authentication
        And I have payment request without channel:
            | field       | value                                  |
            | feeAmount   | 0.0                                    |
            | currency    | ZWG                                    |
            | payerAmount | 3                                      |
            | payeeAmount | 3                                      |
            | customerId  | ef1ebf57-8e9b-4c6c-be89-de72dfd7376c   |
            | message     | Test Payment Request                    |
        When I send payment request to "/bff/v3/order/payment/request"
        Then response status code should be 400
        And response body should be valid JSON

    @payment_request @create_request @negative @validation @sasai
    Scenario: Create payment request without customerId
        Given I have valid user authentication
        And I have payment request without customerId:
            | field       | value                     |
            | feeAmount   | 0.0                       |
            | currency    | ZWG                       |
            | payerAmount | 3                         |
            | payeeAmount | 3                         |
            | channel     | sasai-super-app           |
            | message     | Test Payment Request      |
        When I send payment request to "/bff/v3/order/payment/request"
        Then response status code should be 400
        And response body should be valid JSON

    @payment_request @create_request @negative @validation @sasai
    Scenario: Create payment request with invalid currency
        Given I have valid user authentication
        And I have payment request details:
            | field       | value                                  |
            | feeAmount   | 0.0                                    |
            | currency    | INVALID                                |
            | payerAmount | 3                                      |
            | payeeAmount | 3                                      |
            | channel     | sasai-super-app                        |
            | customerId  | ef1ebf57-8e9b-4c6c-be89-de72dfd7376c   |
            | message     | Test Payment Request                    |
        When I send payment request to "/bff/v3/order/payment/request"
        Then response status code should be 400
        And response body should be valid JSON

    @payment_request @create_request @negative @validation @sasai
    Scenario: Create payment request with zero amount
        Given I have valid user authentication
        And I have payment request details:
            | field       | value                                  |
            | feeAmount   | 0.0                                    |
            | currency    | ZWG                                    |
            | payerAmount | 0                                      |
            | payeeAmount | 0                                      |
            | channel     | sasai-super-app                        |
            | customerId  | ef1ebf57-8e9b-4c6c-be89-de72dfd7376c   |
            | message     | Test Payment Request                    |
        When I send payment request to "/bff/v3/order/payment/request"
        Then response status code should be 400
        And response body should be valid JSON

    @payment_request @create_request @negative @validation @sasai
    Scenario: Create payment request with negative amount
        Given I have valid user authentication
        And I have payment request details:
            | field       | value                                  |
            | feeAmount   | 0.0                                    |
            | currency    | ZWG                                    |
            | payerAmount | -5                                     |
            | payeeAmount | -5                                     |
            | channel     | sasai-super-app                        |
            | customerId  | ef1ebf57-8e9b-4c6c-be89-de72dfd7376c   |
            | message     | Test Payment Request                    |
        When I send payment request to "/bff/v3/order/payment/request"
        Then response status code should be 400
        And response body should be valid JSON

    @payment_request @create_request @negative @validation @sasai
    Scenario: Create payment request with invalid customerId format
        Given I have valid user authentication
        And I have payment request details:
            | field       | value                     |
            | feeAmount   | 0.0                       |
            | currency    | ZWG                       |
            | payerAmount | 3                         |
            | payeeAmount | 3                         |
            | channel     | sasai-super-app           |
            | customerId  | invalid-customer-id       |
            | message     | Test Payment Request      |
        When I send payment request to "/bff/v3/order/payment/request"
        Then response status code should be 400
        And response body should be valid JSON

    @payment_request @create_request @negative @auth @sasai
    Scenario: Create payment request without authentication
        Given I have payment request details:
            | field       | value                                  |
            | feeAmount   | 0.0                                    |
            | currency    | ZWG                                    |
            | payerAmount | 3                                      |
            | payeeAmount | 3                                      |
            | channel     | sasai-super-app                        |
            | customerId  | ef1ebf57-8e9b-4c6c-be89-de72dfd7376c   |
            | message     | Test Payment Request                    |
        When I send payment request to "/bff/v3/order/payment/request"
        Then response status code should be 401
        And response body should be valid JSON

    @payment_request @create_request @negative @auth @sasai
    Scenario: Create payment request with invalid token
        Given I have invalid user authentication
        And I have payment request details:
            | field       | value                                  |
            | feeAmount   | 0.0                                    |
            | currency    | ZWG                                    |
            | payerAmount | 3                                      |
            | payeeAmount | 3                                      |
            | channel     | sasai-super-app                        |
            | customerId  | ef1ebf57-8e9b-4c6c-be89-de72dfd7376c   |
            | message     | Test Payment Request                    |
        When I send payment request to "/bff/v3/order/payment/request"
        Then response status code should be 401
        And response body should be valid JSON

    @payment_request @create_request @negative @auth @sasai
    Scenario: Create payment request with expired token
        Given I have expired user authentication
        And I have payment request details:
            | field       | value                                  |
            | feeAmount   | 0.0                                    |
            | currency    | ZWG                                    |
            | payerAmount | 3                                      |
            | payeeAmount | 3                                      |
            | channel     | sasai-super-app                        |
            | customerId  | ef1ebf57-8e9b-4c6c-be89-de72dfd7376c   |
            | message     | Test Payment Request                    |
        When I send payment request to "/bff/v3/order/payment/request"
        Then response status code should be 401
        And response body should be valid JSON

    @payment_request @create_request @integration @full_flow @sasai
    Scenario: Complete payment request flow with account lookup
        Given I have valid user authentication
        # First lookup the account
        And I have payment request account lookup details:
            | field         | value          |
            | accountNumber | +263789124669  |
            | origin        | requestPay     |
        When I send payment request account lookup to "/bff/v3/payment/account/lookup"
        Then response status code should be 200
        And response should contain account details
        # Then create payment request
        Given I have payment request details:
            | field       | value                                  |
            | feeAmount   | 0.0                                    |
            | currency    | ZWG                                    |
            | payerAmount | 3                                      |
            | payeeAmount | 3                                      |
            | channel     | sasai-super-app                        |
            | customerId  | ef1ebf57-8e9b-4c6c-be89-de72dfd7376c   |
            | message     | Complete flow payment request           |
        When I send payment request to "/bff/v3/order/payment/request"
        Then response status code should be 200
        And response should contain payment request details

    @payment_request @create_request @performance @sasai
    Scenario: Create multiple payment requests consecutively
        Given I have valid user authentication
        And I have payment request details:
            | field       | value                                  |
            | feeAmount   | 0.0                                    |
            | currency    | ZWG                                    |
            | payerAmount | 1                                      |
            | payeeAmount | 1                                      |
            | channel     | sasai-super-app                        |
            | customerId  | ef1ebf57-8e9b-4c6c-be89-de72dfd7376c   |
            | message     | Request 1                               |
        When I send payment request to "/bff/v3/order/payment/request"
        Then response status code should be 200
        And response should contain payment request details
        When I update payment request message to "Request 2"
        And I send payment request to "/bff/v3/order/payment/request"
        Then response status code should be 200
        And response should contain payment request details

    @payment_request @create_request @boundary @sasai
    Scenario: Create payment request with minimum amount
        Given I have valid user authentication
        And I have payment request details:
            | field       | value                                  |
            | feeAmount   | 0.0                                    |
            | currency    | ZWG                                    |
            | payerAmount | 0.01                                   |
            | payeeAmount | 0.01                                   |
            | channel     | sasai-super-app                        |
            | customerId  | ef1ebf57-8e9b-4c6c-be89-de72dfd7376c   |
            | message     | Minimum amount request                  |
        When I send payment request to "/bff/v3/order/payment/request"
        Then response status code should be 200
        And response should contain payment request details

    @payment_request @create_request @boundary @sasai
    Scenario: Create payment request with maximum amount
        Given I have valid user authentication
        And I have payment request details:
            | field       | value                                  |
            | feeAmount   | 0.0                                    |
            | currency    | ZWG                                    |
            | payerAmount | 100000                                 |
            | payeeAmount | 100000                                 |
            | channel     | sasai-super-app                        |
            | customerId  | ef1ebf57-8e9b-4c6c-be89-de72dfd7376c   |
            | message     | Maximum amount request                  |
        When I send payment request to "/bff/v3/order/payment/request"
        Then response status code should be 200
        And response should contain payment request details

    @payment_request @create_request @boundary @message_length @sasai
    Scenario: Create payment request with long message
        Given I have valid user authentication
        And I have payment request details:
            | field       | value                                                                                        |
            | feeAmount   | 0.0                                                                                          |
            | currency    | ZWG                                                                                          |
            | payerAmount | 3                                                                                            |
            | payeeAmount | 3                                                                                            |
            | channel     | sasai-super-app                                                                              |
            | customerId  | ef1ebf57-8e9b-4c6c-be89-de72dfd7376c                                                         |
            | message     | This is a very long payment request message to test the maximum character limit allowed      |
        When I send payment request to "/bff/v3/order/payment/request"
        Then response status code should be 200
        And response should contain payment request details

    @payment_request @create_request @boundary @empty_message @sasai
    Scenario: Create payment request with empty message
        Given I have valid user authentication
        And I have payment request details:
            | field       | value                                  |
            | feeAmount   | 0.0                                    |
            | currency    | ZWG                                    |
            | payerAmount | 3                                      |
            | payeeAmount | 3                                      |
            | channel     | sasai-super-app                        |
            | customerId  | ef1ebf57-8e9b-4c6c-be89-de72dfd7376c   |
            | message     |                                        |
        When I send payment request to "/bff/v3/order/payment/request"
        Then response status code should be 200
        And response should contain payment request details
