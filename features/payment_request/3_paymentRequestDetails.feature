Feature: Payment Request Details API
    As a user
    I want to retrieve payment request details by order ID
    So that I can view the status and information of my payment requests

    # NOTE: Payment Request Details API requires user token (accessToken) from PIN Verify API
    # Endpoint: GET /bff/v2/order/details/{orderId}
    # Path Parameter: orderId - The order ID from payment request creation response (e.g., "177089-5320-994120")
    # Authentication: User token in Authorization header as Bearer token
    # Response: Returns complete payment request details including status, amounts, customer info, etc.
    # This API is used to retrieve details of a previously created payment request

    Background:
        Given API is available
        And I am authenticated with valid app token
        And I have valid user token from PIN verification

    @smoke @payment_request @get_details @positive @sasai
    Scenario: Get payment request details with valid order ID
        Given I have valid user authentication
        # First create a payment request to get orderId and customerId
        And I have payment request details:
            | field       | value                                  |
            | feeAmount   | 0.0                                    |
            | currency    | ZWG                                    |
            | payerAmount | 5                                      |
            | payeeAmount | 5                                      |
            | channel     | sasai-super-app                        |
            | customerId  | ef1ebf57-8e9b-4c6c-be89-de72dfd7376c   |
            | message     | Payment request for details lookup     |
        When I send payment request to "/bff/v3/order/payment/request"
        Then response status code should be 200
        And response should contain payment request details
        And I extract "orderId" from payment request response
        And I extract "customerId" from payment request response
        # Now get the payment request details
        When I send GET request to payment request details endpoint
        Then response status code should be 200
        And response body should be valid JSON
        And response should contain payment request order details
        And response should contain "orderId"
        And response should contain "status"
        And response should contain "payerAmount"
        And response should contain "currency"

    @payment_request @get_details @positive @verify_fields @sasai
    Scenario: Verify all fields in payment request details response
        Given I have valid user authentication
        # Create payment request
        And I have payment request details:
            | field       | value                                  |
            | feeAmount   | 0.0                                    |
            | currency    | ZWG                                    |
            | payerAmount | 10                                     |
            | payeeAmount | 10                                     |
            | channel     | sasai-super-app                        |
            | customerId  | ef1ebf57-8e9b-4c6c-be89-de72dfd7376c   |
            | message     | Detailed field verification            |
        When I send payment request to "/bff/v3/order/payment/request"
        Then response status code should be 200
        And I extract "orderId" from payment request response
        # Get details
        When I send GET request to payment request details endpoint
        Then response status code should be 200
        And response should contain "customerId"
        And response should contain "requestPayId"
        And response should contain "payerInfo"
        And response should contain "expiryAt"

    @payment_request @get_details @positive @amount_verification @sasai
    Scenario: Verify amount in payment request details matches creation
        Given I have valid user authentication
        And I have payment request details:
            | field       | value                                  |
            | feeAmount   | 0.0                                    |
            | currency    | ZWG                                    |
            | payerAmount | 15                                     |
            | payeeAmount | 15                                     |
            | channel     | sasai-super-app                        |
            | customerId  | ef1ebf57-8e9b-4c6c-be89-de72dfd7376c   |
            | message     | Amount verification test               |
        When I send payment request to "/bff/v3/order/payment/request"
        Then response status code should be 200
        And I extract "orderId" from payment request response
        When I send GET request to payment request details endpoint
        Then response status code should be 200
        And response field "amount" should be "15"
        And response field "currency" should be "ZWG"

    @payment_request @get_details @positive @status_check @sasai
    Scenario: Verify payment request status is 'created'
        Given I have valid user authentication
        And I have payment request details:
            | field       | value                                  |
            | feeAmount   | 0.0                                    |
            | currency    | ZWG                                    |
            | payerAmount | 7                                      |
            | payeeAmount | 7                                      |
            | channel     | sasai-super-app                        |
            | customerId  | ef1ebf57-8e9b-4c6c-be89-de72dfd7376c   |
            | message     | Status verification test               |
        When I send payment request to "/bff/v3/order/payment/request"
        Then response status code should be 200
        And I extract "orderId" from payment request response
        When I send GET request to payment request details endpoint
        Then response status code should be 200
        And response field "status" should be "created"

    @payment_request @get_details @negative @invalid_orderid @sasai
    Scenario: Get payment request details with invalid order ID
        Given I have valid user authentication
        And I set invalid order ID "INVALID-ORDER-ID-123"
        When I send GET request to payment request details endpoint
        Then response status code should be 404
        And response body should be valid JSON

    @payment_request @get_details @negative @nonexistent_orderid @sasai
    Scenario: Get payment request details with non-existent order ID
        Given I have valid user authentication
        And I set order ID "999999-9999-999999"
        When I send GET request to payment request details endpoint
        Then response status code should be 404
        And response body should be valid JSON

    @payment_request @get_details @negative @malformed_orderid @sasai
    Scenario: Get payment request details with malformed order ID format
        Given I have valid user authentication
        And I set invalid order ID "12345"
        When I send GET request to payment request details endpoint
        Then response status code should be 404
        And response body should be valid JSON

    @payment_request @get_details @negative @auth @sasai
    Scenario: Get payment request details without authentication
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

    @payment_request @get_details @negative @auth @sasai
    Scenario: Get payment request details with invalid token
        Given I have invalid user authentication
        And I set order ID "177089-5320-994120"
        When I send GET request to payment request details endpoint
        Then response status code should be 401
        And response body should be valid JSON

    @payment_request @get_details @negative @auth @sasai
    Scenario: Get payment request details with expired token
        Given I have expired user authentication
        And I set order ID "177089-5320-994120"
        When I send GET request to payment request details endpoint
        Then response status code should be 401
        And response body should be valid JSON

    @payment_request @get_details @integration @complete_flow @sasai
    Scenario: Complete flow - Create payment request and get details multiple times
        Given I have valid user authentication
        # Create first payment request to get dynamic IDs
        And I have payment request details:
            | field       | value                                  |
            | feeAmount   | 0.0                                    |
            | currency    | ZWG                                    |
            | payerAmount | 20                                     |
            | payeeAmount | 20                                     |
            | channel     | sasai-super-app                        |
            | customerId  | ef1ebf57-8e9b-4c6c-be89-de72dfd7376c   |
            | message     | Complete flow test                     |
        When I send payment request to "/bff/v3/order/payment/request"
        Then response status code should be 200
        And I extract "orderId" from payment request response
        And I extract "customerId" from payment request response
        # Get details first time
        When I send GET request to payment request details endpoint
        Then response status code should be 200
        And response should contain payment request order details
        # Get details second time (verify idempotency)
        When I send GET request to payment request details endpoint
        Then response status code should be 200
        And response should contain payment request order details

    @payment_request @get_details @integration @with_account_lookup @sasai
    Scenario: Complete flow with account lookup, create request, and get details
        Given I have valid user authentication
        # Account lookup
        And I have payment request account lookup details:
            | field         | value          |
            | accountNumber | +263789124669  |
            | origin        | requestPay     |
        When I send payment request account lookup to "/bff/v3/payment/account/lookup"
        Then response status code should be 200
        # Create payment request
        And I have payment request details:
            | field       | value                                  |
            | feeAmount   | 0.0                                    |
            | currency    | ZWG                                    |
            | payerAmount | 8                                      |
            | payeeAmount | 8                                      |
            | channel     | sasai-super-app                        |
            | customerId  | ef1ebf57-8e9b-4c6c-be89-de72dfd7376c   |
            | message     | Full integration test                  |
        When I send payment request to "/bff/v3/order/payment/request"
        Then response status code should be 200
        And I extract "orderId" from payment request response
        # Get payment request details
        When I send GET request to payment request details endpoint
        Then response status code should be 200
        And response should contain payment request order details
        And response should contain "payerInfo"

    @payment_request @get_details @performance @sasai
    Scenario: Get payment request details with response time validation
        Given I have valid user authentication
        And I have payment request details:
            | field       | value                                  |
            | feeAmount   | 0.0                                    |
            | currency    | ZWG                                    |
            | payerAmount | 4                                      |
            | payeeAmount | 4                                      |
            | channel     | sasai-super-app                        |
            | customerId  | ef1ebf57-8e9b-4c6c-be89-de72dfd7376c   |
            | message     | Performance test                       |
        When I send payment request to "/bff/v3/order/payment/request"
        Then response status code should be 200
        And I extract "orderId" from payment request response
        When I send GET request to payment request details endpoint
        Then response status code should be 200
        And response time should be less than 3000 ms

    @payment_request @get_details @boundary @recent_order @sasai
    Scenario: Get details of recently created payment request
        Given I have valid user authentication
        And I have payment request details:
            | field       | value                                  |
            | feeAmount   | 0.0                                    |
            | currency    | ZWG                                    |
            | payerAmount | 1                                      |
            | payeeAmount | 1                                      |
            | channel     | sasai-super-app                        |
            | customerId  | ef1ebf57-8e9b-4c6c-be89-de72dfd7376c   |
            | message     | Recent order test                      |
        When I send payment request to "/bff/v3/order/payment/request"
        Then response status code should be 200
        And I extract "orderId" from payment request response
        # Immediately get details
        When I send GET request to payment request details endpoint
        Then response status code should be 200
        And response should contain payment request order details

    @payment_request @get_details @boundary @usd_currency @sasai
    Scenario: Get details of USD payment request
        Given I have valid user authentication
        And I have payment request details:
            | field       | value                                  |
            | feeAmount   | 0.0                                    |
            | currency    | USD                                    |
            | payerAmount | 2                                      |
            | payeeAmount | 2                                      |
            | channel     | sasai-super-app                        |
            | customerId  | ef1ebf57-8e9b-4c6c-be89-de72dfd7376c   |
            | message     | USD currency test                      |
        When I send payment request to "/bff/v3/order/payment/request"
        Then response status code should be 200
        And I extract "orderId" from payment request response
        When I send GET request to payment request details endpoint
        Then response status code should be 200
        And response field "currency" should be "USD"

    @payment_request @get_details @integration @dynamic_customer @sasai
    Scenario: Verify dynamic customerId extraction and order details retrieval
        Given I have valid user authentication
        # Create first payment request and extract customerId
        And I have payment request details:
            | field       | value                                  |
            | feeAmount   | 0.0                                    |
            | currency    | ZWG                                    |
            | payerAmount | 5                                      |
            | payeeAmount | 5                                      |
            | channel     | sasai-super-app                        |
            | customerId  | ef1ebf57-8e9b-4c6c-be89-de72dfd7376c   |
            | message     | First request for dynamic test         |
        When I send payment request to "/bff/v3/order/payment/request"
        Then response status code should be 200
        And I extract "orderId" from payment request response
        And I extract "customerId" from payment request response
        # Verify we can get details of first order
        When I send GET request to payment request details endpoint
        Then response status code should be 200
        And response should contain payment request order details
        # Note: Extracted customerId (stored in context) can be used in subsequent API calls
        # This demonstrates the dynamic extraction feature works correctly
