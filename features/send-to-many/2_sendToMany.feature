Feature: Send to Many - Send to Many Payment API
    As a user
    I want to send payments to multiple recipients at once
    So that I can transfer funds efficiently to multiple people

    # NOTE: Send to Many API requires user token (accessToken) from PIN Verify API
    # This API processes bulk payment transfers to multiple recipients
    # Endpoint: POST /bff/v1/wallet/payments/send-to-many
    # Headers: Authorization (Bearer user token), Content-Type
    # Body: currency, description, instrumentToken, provider, pin, notes, recipientDetails[]
    # Each recipient requires: amount, name, mobileNumber, customerId

    Background:
        Given API is available
        And I am authenticated with valid app token
        And I have valid user token from PIN verification

    @smoke @send_to_many_payment @send_to_many @sasai
    Scenario: Send payment to multiple recipients successfully
        Given I have valid user authentication
        And I have send to many payment request body with 2 recipients
        When I send send to many payment request to "/bff/v1/wallet/payments/send-to-many"
        Then response status code should be 200 or 201
        And response should contain send to many payment confirmation
        And response body should be valid JSON

    @regression @send_to_many_payment @send_to_many @sasai
    Scenario: Send payment to multiple recipients with ZWG currency
        Given I have valid user authentication
        And I have send to many payment request with currency "ZWG"
        And I have send to many recipients list:
            | amount | name              | mobileNumber   | customerId                           |
            | 4      | EcoCash User Two  | +263789124558  | 2f3a5e5a-9387-4669-8674-58df6c28b5ac |
            | 4      | Ecocash User Two  | +263789124669  | f044ff8d-abe6-47aa-8837-ec329e8a0edc |
        When I send send to many payment request to "/bff/v1/wallet/payments/send-to-many"
        Then response status code should be 200 or 201

    @regression @send_to_many_payment @send_to_many @sasai
    Scenario: Send payment to multiple recipients with USD currency
        Given I have valid user authentication
        And I have send to many payment request with currency "USD"
        And I have send to many recipients list:
            | amount | name              | mobileNumber   | customerId                           |
            | 1      | Test User One     | +263789124558  | 2f3a5e5a-9387-4669-8674-58df6c28b5ac |
            | 1      | Test User Two     | +263789124669  | f044ff8d-abe6-47aa-8837-ec329e8a0edc |
        When I send send to many payment request to "/bff/v1/wallet/payments/send-to-many"
        Then response status code should be 200 or 201

    @negative @send_to_many_payment @send_to_many @sasai
    Scenario: Send to many payment without authentication
        Given I have send to many payment request body with 2 recipients
        When I send send to many payment request without token to "/bff/v1/wallet/payments/send-to-many"
        Then response status code should be 401

    @negative @send_to_many_payment @send_to_many @sasai
    Scenario: Send to many payment with invalid token
        Given I have invalid user token
        And I have send to many payment request body with 2 recipients
        When I send send to many payment request to "/bff/v1/wallet/payments/send-to-many"
        Then response status code should be 401

    @negative @send_to_many_payment @send_to_many @sasai
    Scenario: Send to many payment without currency
        Given I have valid user authentication
        And I have send to many payment request without currency field
        When I send send to many payment request to "/bff/v1/wallet/payments/send-to-many"
        Then response status code should be 400

    @negative @send_to_many_payment @send_to_many @sasai
    Scenario: Send to many payment without recipients
        Given I have valid user authentication
        And I have send to many payment request without recipients
        When I send send to many payment request to "/bff/v1/wallet/payments/send-to-many"
        Then response status code should be 400

    @negative @send_to_many_payment @send_to_many @sasai
    Scenario: Send to many payment with invalid currency
        Given I have valid user authentication
        And I have send to many payment request with currency "XYZ"
        And I have send to many recipients list:
            | amount | name         | mobileNumber   | customerId                           |
            | 1      | Test User    | +263789124558  | 2f3a5e5a-9387-4669-8674-58df6c28b5ac |
        When I send send to many payment request to "/bff/v1/wallet/payments/send-to-many"
        Then response status code should be 400

    @negative @send_to_many_payment @send_to_many @sasai
    Scenario: Send to many payment with invalid instrument token
        Given I have valid user authentication
        And I have send to many payment request with invalid instrument token
        When I send send to many payment request to "/bff/v1/wallet/payments/send-to-many"
        Then response status code should be 400 or 404

    @negative @send_to_many_payment @send_to_many @sasai
    Scenario: Send to many payment with missing recipient details
        Given I have valid user authentication
        And I have send to many payment request with incomplete recipient data
        When I send send to many payment request to "/bff/v1/wallet/payments/send-to-many"
        Then response status code should be 400

    @validation @send_to_many_payment @send_to_many @sasai
    Scenario: Verify send to many payment response contains transaction details
        Given I have valid user authentication
        And I have send to many payment request body with 2 recipients
        When I send send to many payment request to "/bff/v1/wallet/payments/send-to-many"
        Then response status code should be 200 or 201
        And response should contain field "transactionId" or "orderId" or "paymentId"

    @validation @send_to_many_payment @send_to_many @sasai
    Scenario: Verify send to many payment processes all recipients
        Given I have valid user authentication
        And I have send to many payment request body with 2 recipients
        When I send send to many payment request to "/bff/v1/wallet/payments/send-to-many"
        Then response status code should be 200 or 201
        And send to many payment should process all recipients successfully

    @performance @send_to_many_payment @send_to_many @sasai
    Scenario: Send to many payment response time validation
        Given I have valid user authentication
        And I have send to many payment request body with 2 recipients
        When I send send to many payment request to "/bff/v1/wallet/payments/send-to-many"
        Then response status code should be 200 or 201
        And response time should be less than 5000 milliseconds

    @security @send_to_many_payment @send_to_many @sasai
    Scenario: Send to many payment requires encrypted PIN
        Given I have valid user authentication
        And I have send to many payment request with unencrypted pin
        When I send send to many payment request to "/bff/v1/wallet/payments/send-to-many"
        Then response status code should be 400 or 401
