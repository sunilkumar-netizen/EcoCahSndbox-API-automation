Feature: Send to Many - Payment Options API
    As a user
    I want to get payment options for send to many transactions
    So that I can initiate bulk payment transfers

    # NOTE: Payment Options API requires user token (accessToken) from PIN Verify API
    # This API retrieves available payment options for ZWSendManyTransactions service type
    # Endpoint: GET /bff/v2/payment/options?serviceType=ZWSendManyTransactions
    # Headers: Authorization (Bearer user token), requestId
    # Query Params: serviceType (ZWSendManyTransactions)

    Background:
        Given API is available
        And I am authenticated with valid app token
        And I have valid user token from PIN verification

    @smoke @send_to_many_payment_options @send_to_many @sasai
    Scenario: Get payment options for send to many transactions
        Given I have valid user authentication
        And I have send to many payment options query parameters:
            | parameter   | value                   |
            | serviceType | ZWSendManyTransactions  |
        When I send send to many payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response should contain send to many payment options
        And response body should be valid JSON
