Feature: Pay to Merchant- Order Details
    As a user
    I want to retrieve order details from Sasai Payment Gateway API
    So that I can view payment details that were completed in the merchant flow

    # NOTE: Order Details API requires user token (accessToken) from PIN Verify API
    # This is part of the "Merchant Payment" flow (after Utility Payment)
    # Endpoint: GET /bff/v2/order/details/{orderReference}

    Background:
        Given API is available
        And I am authenticated with valid app token
        And I have valid user token from PIN verification

    @smoke @order_details @merchant_payment @sasai
    Scenario: Get order details with valid order reference
        Given I have valid user authentication
        And I have order reference "176888-6726-665218"
        When I send order details request to "/bff/v2/order/details/176888-6726-665218"
        Then response status code should be 200
        And response time should be less than 5000 ms
        And response should contain order details

    @order_details @positive @merchant_payment @sasai
    Scenario: Get order details for completed payment
        Given I have valid user authentication
        And I have order reference "176888-6726-665218"
        When I send GET request to order details endpoint
        Then response status code should be 200
        And response should contain order details
        And response should contain order status

    @order_details @positive @merchant_payment @sasai
    Scenario: Get order details with request ID header
        Given I have valid user authentication
        And I have order reference "176888-6726-665218"
        And I have request ID "bdefac7b-bbc0-48b4-9ef0-84e6b9b34a6f"
        When I send order details request with headers
        Then response status code should be 200
        And response should contain order details

    @order_details @negative @merchant_payment @sasai
    Scenario: Get order details without authentication
        Given I have no authentication token
        And I have order reference "176888-6726-665218"
        When I send order details request to "/bff/v2/order/details/176888-6726-665218"
        Then response status code should be 401

    @order_details @negative @merchant_payment @sasai
    Scenario: Get order details with app token instead of user token
        Given I have app token only
        And I have order reference "176888-6726-665218"
        When I send order details request to "/bff/v2/order/details/176888-6726-665218"
        Then response status code should be 401 or 403

    @order_details @negative @merchant_payment @sasai
    Scenario: Get order details with expired user token
        Given I have expired user token
        And I have order reference "176888-6726-665218"
        When I send order details request to "/bff/v2/order/details/176888-6726-665218"
        Then response status code should be 401

    @order_details @negative @merchant_payment @sasai
    Scenario: Get order details with invalid user token
        Given I have invalid user token
        And I have order reference "176888-6726-665218"
        When I send order details request to "/bff/v2/order/details/176888-6726-665218"
        Then response status code should be 401

    @order_details @negative @merchant_payment @sasai
    Scenario: Get order details with missing order reference
        Given I have valid user authentication
        When I send order details request to "/bff/v2/order/details/"
        Then response status code should be 404

    @order_details @negative @merchant_payment @sasai
    Scenario: Get order details with invalid order reference format
        Given I have valid user authentication
        And I have order reference "invalid-format"
        When I send order details request with invalid reference
        Then response status code should be 400 or 404

    @order_details @negative @merchant_payment @sasai
    Scenario: Get order details with non-existent order reference
        Given I have valid user authentication
        And I have order reference "999999-9999-999999"
        When I send order details request to "/bff/v2/order/details/999999-9999-999999"
        Then response status code should be 404

    @order_details @negative @merchant_payment @sasai
    Scenario: Get order details with empty order reference
        Given I have valid user authentication
        And I have empty order reference
        When I send order details request to "/bff/v2/order/details/"
        Then response status code should be 404

    @order_details @negative @merchant_payment @sasai
    Scenario: Get order details with special characters in reference
        Given I have valid user authentication
        And I have order reference "test@#$%^&*()"
        When I send order details request with special characters
        Then response status code should be 400 or 404

    @order_details @validation @merchant_payment @sasai
    Scenario: Verify order details response structure
        Given I have valid user authentication
        And I have order reference "176888-6726-665218"
        When I send order details request to "/bff/v2/order/details/176888-6726-665218"
        Then response status code should be 200
        And response body should be valid JSON
        And response should have order structure

    @order_details @validation @merchant_payment @sasai
    Scenario: Verify order details response contains required fields
        Given I have valid user authentication
        And I have order reference "176888-6726-665218"
        When I send order details request to "/bff/v2/order/details/176888-6726-665218"
        Then response status code should be 200
        And order response should have required fields

    @order_details @validation @merchant_payment @sasai
    Scenario: Verify order details contains payment information
        Given I have valid user authentication
        And I have order reference "176888-6726-665218"
        When I send order details request to "/bff/v2/order/details/176888-6726-665218"
        Then response status code should be 200
        And response should contain payment information

    @order_details @validation @merchant_payment @sasai
    Scenario: Verify order details contains transaction timestamp
        Given I have valid user authentication
        And I have order reference "176888-6726-665218"
        When I send order details request to "/bff/v2/order/details/176888-6726-665218"
        Then response status code should be 200
        And response should contain timestamp

    @order_details @headers @validation @merchant_payment @sasai
    Scenario: Verify order details response headers
        Given I have valid user authentication
        And I have order reference "176888-6726-665218"
        When I send order details request to "/bff/v2/order/details/176888-6726-665218"
        Then response status code should be 200
        And response header "Content-Type" should be present
        And response header "Content-Type" should contain "application/json"

    @order_details @headers @validation @merchant_payment @sasai
    Scenario: Verify order details accepts request ID header
        Given I have valid user authentication
        And I have order reference "176888-6726-665218"
        And I have request ID "test-request-id-123"
        When I send order details request with headers
        Then response status code should be 200
        And response should contain order details

    @order_details @security @merchant_payment @sasai
    Scenario: Verify order details with missing Authorization header
        Given I have no Authorization header
        And I have order reference "176888-6726-665218"
        When I send order details request to "/bff/v2/order/details/176888-6726-665218"
        Then response status code should be 401

    @order_details @security @merchant_payment @sasai
    Scenario: Verify order details with empty Bearer token
        Given I have empty Bearer token
        And I have order reference "176888-6726-665218"
        When I send order details request to "/bff/v2/order/details/176888-6726-665218"
        Then response status code should be 401

    @order_details @security @merchant_payment @sasai
    Scenario: Verify order details with malformed Bearer token
        Given I have malformed Bearer token
        And I have order reference "176888-6726-665218"
        When I send order details request to "/bff/v2/order/details/176888-6726-665218"
        Then response status code should be 401

    @order_details @security @merchant_payment @sasai
    Scenario: Verify order details for another user's order
        Given I have valid user authentication
        And I have order reference from different user
        When I send order details request to different user order
        Then response status code should be 403 or 404

    @order_details @error_handling @merchant_payment @sasai
    Scenario: Get order details with invalid HTTP method
        Given I have valid user authentication
        And I have order reference "176888-6726-665218"
        When I send POST request to "/bff/v2/order/details/176888-6726-665218"
        Then response status code should be 405

    @order_details @error_handling @merchant_payment @sasai
    Scenario: Get order details with wrong endpoint path
        Given I have valid user authentication
        And I have order reference "176888-6726-665218"
        When I send GET request to "/bff/v2/order/detail/176888-6726-665218"
        Then response status code should be 404

    @order_details @performance @merchant_payment @sasai
    Scenario: Verify order details response time
        Given I have valid user authentication
        And I have order reference "176888-6726-665218"
        When I send order details request to "/bff/v2/order/details/176888-6726-665218"
        Then response status code should be 200
        And response time should be less than 3000 ms

    @order_details @integration @merchant_payment @sasai
    Scenario: Complete flow - PIN Verify to Order Details
        Given I have valid PIN verification details
        When I send PIN verification request to "/bff/v4/auth/pin/verify"
        Then response status code should be 200
        And I store the user token from response
        Given I have order reference "176888-6726-665218"
        When I send order details request with stored token to "/bff/v2/order/details/176888-6726-665218"
        Then response status code should be 200
        And response should contain order details

    @order_details @integration @merchant_payment @sasai
    Scenario: Complete merchant payment flow - Utility Payment to Order Details
        Given I have valid user authentication
        And I have utility payment request body
        When I send utility payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And I extract order reference from payment response
        When I send order details request with extracted reference
        Then response status code should be 200
        And response should contain order details
        And order status should match payment status
