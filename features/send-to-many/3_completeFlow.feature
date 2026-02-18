Feature: Send to Many - Complete Flow with Payment Options
    As a user
    I want to get payment options and then send payments to multiple recipients
    So that I can complete the full send to many transaction flow

    # This feature demonstrates the complete flow:
    # 1. Call Payment Options API to get instrumentToken
    # 2. Use the instrumentToken in Send to Many Payment API

    Background:
        Given API is available
        And I am authenticated with valid app token
        And I have valid user token from PIN verification

    @smoke @send_to_many_complete_flow @send_to_many @sasai
    Scenario: Complete send to many flow - Get payment options then send payment
        Given I have valid user authentication
        # Step 1: Get payment options to retrieve instrumentToken
        And I have send to many payment options query parameters:
            | parameter   | value                   |
            | serviceType | ZWSendManyTransactions  |
        When I send send to many payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response should contain send to many payment options
        # Step 2: Use the instrumentToken in send to many payment
        Given I have send to many payment request body with 2 recipients
        When I send send to many payment request to "/bff/v1/wallet/payments/send-to-many"
        Then response status code should be 200 or 201
        And response should contain send to many payment confirmation
        And response body should be valid JSON

    @regression @send_to_many_complete_flow @send_to_many @sasai
    Scenario: Complete send to many flow with ZWG currency
        Given I have valid user authentication
        # Step 1: Get payment options
        And I have send to many payment options query parameters:
            | parameter   | value                   |
            | serviceType | ZWSendManyTransactions  |
        When I send send to many payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        # Step 2: Send payment to multiple recipients
        Given I have send to many payment request with currency "ZWG"
        And I have send to many recipients list:
            | amount | name              | mobileNumber   | customerId                           |
            | 4      | EcoCash User Two  | +263789124558  | 2f3a5e5a-9387-4669-8674-58df6c28b5ac |
            | 4      | Ecocash User Two  | +263789124669  | f044ff8d-abe6-47aa-8837-ec329e8a0edc |
        When I send send to many payment request to "/bff/v1/wallet/payments/send-to-many"
        Then response status code should be 200 or 201
        And response should contain send to many payment confirmation
