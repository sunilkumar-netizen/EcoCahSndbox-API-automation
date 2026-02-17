Feature: Wallet Balances - Payment Options
    As a user
    I want to retrieve available payment options for checking wallet balances
    So that I can view all payment methods available for balance inquiries

    # NOTE: Payment Options API requires user token (accessToken) from PIN Verify API
    # This API returns all available payment options including wallets, cards, and bank accounts
    # Endpoint: GET /bff/v1/payment/options
    # Query Parameters: serviceType (e.g., ZWAllPaymentOptions)
    # Headers: Authorization (Bearer user token), requestId (UUID)

    Background:
        Given API is available
        And I am authenticated with valid app token
        And I have valid user token from PIN verification

    @smoke @payment_options @wallet_balances @sasai
    Scenario: Get payment options with valid authentication
        Given I have valid user authentication
        And I have service type "ZWAllPaymentOptions"
        And I have valid request ID
        When I send wallet balance payment options request to "/bff/v1/payment/options"
        Then response status code should be 200
        And response should contain payment options list
        And response body should be valid JSON
