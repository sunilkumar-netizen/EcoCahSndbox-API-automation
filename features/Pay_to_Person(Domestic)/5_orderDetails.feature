Feature: P2P Order Details
    As a user
    I want to retrieve order details for my P2P payment transactions
    So that I can view transaction history and verify payment status

    # NOTE: Order Details API requires user token (accessToken) from PIN Verify API
    # Endpoint: GET /bff/v2/order/details/{orderId}
    # Path Parameter: orderId - The transaction order ID (e.g., "177036-4133-153222")
    # Headers: Authorization (Bearer token)
    # Response: Returns complete transaction details including status, amounts, beneficiary info, timestamps, etc.
    # This API is used after payment transfer to check transaction status and retrieve receipt details
    #
    # DYNAMIC ORDER ID FLOW:
    # The orderId parameter is dynamically retrieved from the Payment Transfer API response
    # When you execute a payment transfer, the response contains an orderId field
    # This orderId is automatically stored in context.order_id
    # The Order Details API then uses context.order_id to fetch the transaction details
    # See the integration scenario (line 62) for an example of this dynamic flow

    Background:
        Given API is available
        And I am authenticated with valid app token
        And I have valid user token from PIN verification

    @smoke @p2p_order_details @order_details @p2p @sasai @dynamic
    Scenario: Get order details with dynamic order ID from payment transfer
        Given I have valid user authentication
        And I have account number "+263789124669"
        When I send account lookup request to "/bff/v3/payment/account/lookup"
        Then response status code should be 200
        Given I have service type "ZWPersonPaymentOptions"
        When I send P2P payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        Given I have complete payment transfer payload
        When I send payment transfer request to "/bff/v2/order/transfer/payment"
        Then response status code should be 200 or 201
        And response should have P2P order ID
        When I send P2P order details request to "/bff/v2/order/details"
        Then response status code should be 200
        And response body should be valid JSON
        And response should contain P2P order details data
        And P2P order details should have order ID
        And P2P order details should have status
        And P2P order details should have amount

    @p2p_order_details @positive @order_details @p2p @sasai
    Scenario: Get order details and verify complete response structure
        Given I have valid user authentication
        And I have order ID "177036-4133-153222"
        When I send P2P order details request to "/bff/v2/order/details"
        Then response status code should be 200
        And P2P order details should have complete information
        And P2P order details should have beneficiary details
        And P2P order details should have payer details
        And P2P order details should have timestamps

    @p2p_order_details @positive @order_details @p2p @sasai
    Scenario: Get order details and extract transaction info
        Given I have valid user authentication
        And I have order ID "177036-4133-153222"
        When I send P2P order details request to "/bff/v2/order/details"
        Then response status code should be 200
        And I extract transaction status from order details
        And I extract transaction amount from order details
        And extracted order details should be valid

    @p2p_order_details @positive @order_details @p2p @sasai
    Scenario: Get order details for successful transaction
        Given I have valid user authentication
        And I have successful order ID "177036-4133-153222"
        When I send P2P order details request to "/bff/v2/order/details"
        Then response status code should be 200
        And order status should be successful
        And order should have completion timestamp

    @p2p_order_details @integration @order_details @p2p @sasai
    Scenario: Complete P2P flow - Transfer then get order details
        Given I have valid user authentication
        # Step 1: Execute payment transfer
        And I have complete payment transfer payload
        When I send payment transfer request to "/bff/v2/order/transfer/payment"
        Then response status code should be 200 or 201
        And response should have P2P order ID
        And order ID should not be empty
        # Step 2: Get order details using dynamic order ID from transfer
        When I send P2P order details request to "/bff/v2/order/details"
        Then response status code should be 200
        And response should contain P2P order details data
        And order ID in details should match transfer order ID

    @p2p_order_details @negative @order_details @p2p @sasai
    Scenario: Get order details without authentication
        Given I have no authentication token
        And I have order ID "177036-4133-153222"
        When I send P2P order details request to "/bff/v2/order/details"
        Then response status code should be 401

    @p2p_order_details @negative @order_details @p2p @sasai
    Scenario: Get order details with invalid user token
        Given I have invalid user token
        And I have order ID "177036-4133-153222"
        When I send P2P order details request to "/bff/v2/order/details"
        Then response status code should be 401

    @p2p_order_details @negative @order_details @p2p @sasai
    Scenario: Get order details with expired user token
        Given I have expired user token
        And I have order ID "177036-4133-153222"
        When I send P2P order details request to "/bff/v2/order/details"
        Then response status code should be 401

    @p2p_order_details @negative @order_details @p2p @sasai
    Scenario: Get order details without order ID
        Given I have valid user authentication
        And I have no order ID
        When I send P2P order details request to "/bff/v2/order/details"
        Then response status code should be 404

    @p2p_order_details @negative @order_details @p2p @sasai
    Scenario: Get order details with empty order ID
        Given I have valid user authentication
        And I have no order ID
        When I send P2P order details request to "/bff/v2/order/details"
        Then response status code should be 404

    @p2p_order_details @negative @order_details @p2p @sasai
    Scenario: Get order details with invalid order ID format
        Given I have valid user authentication
        And I have order ID "invalid-order-123"
        When I send P2P order details request to "/bff/v2/order/details"
        Then response status code should be 404

    @p2p_order_details @negative @order_details @p2p @sasai
    Scenario: Get order details with non-existent order ID
        Given I have valid user authentication
        And I have order ID "999999-9999-999999"
        When I send P2P order details request to "/bff/v2/order/details"
        Then response status code should be 404

    @p2p_order_details @negative @order_details @p2p @sasai
    Scenario: Get order details with special characters in order ID
        Given I have valid user authentication
        And I have order ID "177036@#$%^&"
        When I send P2P order details request to "/bff/v2/order/details"
        Then response status code should be 400 or 404

    @p2p_order_details @negative @order_details @p2p @sasai
    Scenario: Get order details for another user's order
        Given I have valid user authentication
        And I have another user order ID "000000-0000-000000"
        When I send P2P order details request to "/bff/v2/order/details"
        Then response status code should be 403 or 404

    @p2p_order_details @validation @order_details @p2p @sasai
    Scenario: Verify order details contains required fields
        Given I have valid user authentication
        And I have order ID "177036-4133-153222"
        When I send P2P order details request to "/bff/v2/order/details"
        Then response status code should be 200
        And order details should have order ID field
        And order details should have status field
        And order details should have amount field
        And order details should have currency field

    @p2p_order_details @validation @order_details @p2p @sasai
    Scenario: Verify order details has transaction timestamps
        Given I have valid user authentication
        And I have order ID "177036-4133-153222"
        When I send P2P order details request to "/bff/v2/order/details"
        Then response status code should be 200
        And order details should have creation timestamp
        And order details should have update timestamp
        And timestamps should be in valid format

    @p2p_order_details @validation @order_details @p2p @sasai
    Scenario: Verify order details has beneficiary information
        Given I have valid user authentication
        And I have order ID "177036-4133-153222"
        When I send P2P order details request to "/bff/v2/order/details"
        Then response status code should be 200
        And order details should have beneficiary name
        And order details should have beneficiary account
        And beneficiary information should be valid

    @p2p_order_details @validation @order_details @p2p @sasai
    Scenario: Verify order details has payer information
        Given I have valid user authentication
        And I have order ID "177036-4133-153222"
        When I send P2P order details request to "/bff/v2/order/details"
        Then response status code should be 200
        And order details should have payer information
        And payer information should be valid

    @p2p_order_details @headers @validation @order_details @p2p @sasai
    Scenario: Verify order details response headers
        Given I have valid user authentication
        And I have order ID "177036-4133-153222"
        When I send P2P order details request to "/bff/v2/order/details"
        Then response status code should be 200
        And response header "Content-Type" should be present
        And response header "Content-Type" should contain "application/json"

    @p2p_order_details @security @order_details @p2p @sasai
    Scenario: Verify order details with missing Authorization header
        Given I have no Authorization header
        And I have order ID "177036-4133-153222"
        When I send P2P order details request to "/bff/v2/order/details"
        Then response status code should be 401

    @p2p_order_details @security @order_details @p2p @sasai
    Scenario: Verify order details with empty Bearer token
        Given I have empty Bearer token
        And I have order ID "177036-4133-153222"
        When I send P2P order details request to "/bff/v2/order/details"
        Then response status code should be 401

    @p2p_order_details @security @order_details @p2p @sasai
    Scenario: Verify order details with malformed Bearer token
        Given I have malformed Bearer token
        And I have order ID "177036-4133-153222"
        When I send P2P order details request to "/bff/v2/order/details"
        Then response status code should be 401

    @p2p_order_details @error_handling @order_details @p2p @sasai
    Scenario: Order details with invalid HTTP method POST
        Given I have valid user authentication
        And I have order ID "177036-4133-153222"
        When I send POST request to "/bff/v2/order/details/177036-4133-153222"
        Then response status code should be 405

    @p2p_order_details @error_handling @order_details @p2p @sasai
    Scenario: Order details with invalid HTTP method PUT
        Given I have valid user authentication
        And I have order ID "177036-4133-153222"
        When I send PUT request to "/bff/v2/order/details/177036-4133-153222"
        Then response status code should be 405

    @p2p_order_details @error_handling @order_details @p2p @sasai
    Scenario: Order details with wrong endpoint path
        Given I have valid user authentication
        And I have order ID "177036-4133-153222"
        When I send P2P order details request to "/bff/v2/order/detail"
        Then response status code should be 404

    @p2p_order_details @performance @order_details @p2p @sasai
    Scenario: Verify order details response time
        Given I have valid user authentication
        And I have order ID "177036-4133-153222"
        When I send P2P order details request to "/bff/v2/order/details"
        Then response status code should be 200
        And response time should be less than 2000 ms

    @p2p_order_details @performance @order_details @p2p @sasai
    Scenario: Verify order details response time is acceptable
        Given I have valid user authentication
        And I have order ID "177036-4133-153222"
        When I send P2P order details request to "/bff/v2/order/details"
        Then response status code should be 200
        And response time should be less than 3000 ms

    @p2p_order_details @data_validation @order_details @p2p @sasai
    Scenario: Verify same order details retrieved multiple times
        Given I have valid user authentication
        And I have order ID "177036-4133-153222"
        When I send P2P order details request to "/bff/v2/order/details"
        Then response status code should be 200
        And I store first order details response
        When I send P2P order details request to "/bff/v2/order/details"
        Then response status code should be 200
        And second order details should match first

    @p2p_order_details @status_verification @order_details @p2p @sasai
    Scenario: Verify order details for pending transaction
        Given I have valid user authentication
        And I have pending order ID "177036-4133-153223"
        When I send P2P order details request to "/bff/v2/order/details"
        Then response status code should be 200
        And order status should be pending or processing

    @p2p_order_details @status_verification @order_details @p2p @sasai
    Scenario: Verify order details for failed transaction
        Given I have valid user authentication
        And I have failed order ID "177036-4133-153224"
        When I send P2P order details request to "/bff/v2/order/details"
        Then response status code should be 200
        And order status should be failed or rejected
        And order should have failure reason

    @p2p_order_details @order_ids @order_details @p2p @sasai
    Scenario Outline: Get order details with different order ID formats
        Given I have valid user authentication
        And I have order ID "<orderId>"
        When I send P2P order details request to "/bff/v2/order/details"
        Then response status code should be <statusCode>

        Examples:
            | orderId               | statusCode |
            | 177036-4133-153222    | 200        |
            | 177036-4133-153223    | 200 or 404 |
            | 123456-7890-123456    | 200 or 404 |
            | 000000-0000-000000    | 404        |

    @p2p_order_details @transaction_types @order_details @p2p @sasai
    Scenario Outline: Get order details for different transaction types
        Given I have valid user authentication
        And I have <transactionType> order ID "<orderId>"
        When I send P2P order details request to "/bff/v2/order/details"
        Then response status code should be <statusCode>

        Examples:
            | transactionType | orderId            | statusCode |
            | successful      | 177036-4133-153222 | 200        |
            | pending         | 177036-4133-153223 | 200        |
            | failed          | 177036-4133-153224 | 200        |
