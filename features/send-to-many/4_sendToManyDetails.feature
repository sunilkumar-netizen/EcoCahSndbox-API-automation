Feature: Send to Many - Get Transaction Details API
    As a user
    I want to retrieve details of a send-to-many transaction
    So that I can track the status and information of my bulk payment

    # NOTE: Send to Many Details API requires user token (accessToken) from PIN Verify API
    # This API retrieves transaction details for a specific send-to-many payment
    # Endpoint: GET /bff/v1/wallet/payments/send-to-many/{sendManyId}
    # Headers: Authorization (Bearer user token)
    # Path Parameter: sendManyId (UUID from send to many payment response)
    # Response: Transaction details including status, recipients, amounts, timestamps

    Background:
        Given API is available
        And I am authenticated with valid app token
        And I have valid user token from PIN verification

    @smoke @send_to_many_details @send_to_many @sasai
    Scenario: Get send to many transaction details successfully
        Given I have valid user authentication
        And I have send to many payment request body with 2 recipients
        When I send send to many payment request to "/bff/v1/wallet/payments/send-to-many"
        Then response status code should be 200 or 201
        And response should contain send to many payment confirmation
        When I retrieve the send many ID from payment response
        And I send get send to many details request to "/bff/v1/wallet/payments/send-to-many"
        Then response status code should be 200
        And response should contain send to many transaction details
        And send to many transaction status should be created
        And response body should be valid JSON

   @smoke @regression @send_to_many_details @send_to_many @sasai
    Scenario: Get send to many details after creating transaction
        Given I have valid user authentication
        And I have send to many payment request body with 2 recipients
        When I send send to many payment request to "/bff/v1/wallet/payments/send-to-many"
        Then response status code should be 200 or 201
        And response should contain send to many payment confirmation
        When I retrieve the send many ID from payment response
        And I send get send to many details request to "/bff/v1/wallet/payments/send-to-many"
        Then response status code should be 200
        And response should contain send to many transaction details
        And send to many transaction status should be created

    @regression @send_to_many_details @send_to_many @sasai
    Scenario: Verify send to many details contains all transaction information
        Given I have valid user authentication
        And I have send to many payment request body with 2 recipients
        When I send send to many payment request to "/bff/v1/wallet/payments/send-to-many"
        Then response status code should be 200 or 201
        When I retrieve the send many ID from payment response
        And I send get send to many details request to "/bff/v1/wallet/payments/send-to-many"
        Then response status code should be 200
        And send to many details should contain transaction ID
        And send to many details should contain recipient information
        And send to many details should contain amount details
        And send to many transaction status should be created

    @negative @send_to_many_details @send_to_many @sasai
    Scenario: Get send to many details without authentication
        Given I have valid user authentication
        And I have send to many payment request body with 2 recipients
        When I send send to many payment request to "/bff/v1/wallet/payments/send-to-many"
        Then response status code should be 200 or 201
        When I retrieve the send many ID from payment response
        And I send get send to many details request without token to "/bff/v1/wallet/payments/send-to-many"
        Then response status code should be 401

    @negative @send_to_many_details @send_to_many @sasai
    Scenario: Get send to many details with invalid token
        Given I have invalid user token
        And I have send to many payment request body with 2 recipients
        When I send send to many payment request to "/bff/v1/wallet/payments/send-to-many"
        Then response status code should be 200 or 201
        When I retrieve the send many ID from payment response
        And I send get send to many details request to "/bff/v1/wallet/payments/send-to-many"
        Then response status code should be 401

    @negative @send_to_many_details @send_to_many @sasai
    Scenario: Get send to many details with non-existent transaction ID
        Given I have valid user authentication
        And I have an invalid send to many transaction ID
        When I send get send to many details request to "/bff/v1/wallet/payments/send-to-many"
        Then response status code should be 404

    @negative @send_to_many_details @send_to_many @sasai
    Scenario: Get send to many details with malformed transaction ID
        Given I have valid user authentication
        And I have a malformed send to many transaction ID
        When I send get send to many details request to "/bff/v1/wallet/payments/send-to-many"
        Then response status code should be 404

    @validation @send_to_many_details @send_to_many @sasai
    Scenario: Verify send to many details response structure
        Given I have valid user authentication
        And I have send to many payment request body with 2 recipients
        When I send send to many payment request to "/bff/v1/wallet/payments/send-to-many"
        Then response status code should be 200 or 201
        When I retrieve the send many ID from payment response
        And I send get send to many details request to "/bff/v1/wallet/payments/send-to-many"
        Then response status code should be 200
        And response should be a valid send to many details object
        And send to many transaction should have valid status

    @performance @send_to_many_details @send_to_many @sasai
    Scenario: Send to many details response time validation
        Given I have valid user authentication
        And I have send to many payment request body with 2 recipients
        When I send send to many payment request to "/bff/v1/wallet/payments/send-to-many"
        Then response status code should be 200 or 201
        When I retrieve the send many ID from payment response
        And I send get send to many details request to "/bff/v1/wallet/payments/send-to-many"
        Then response status code should be 200
        And response time should be less than 3000 milliseconds

    @security @send_to_many_details @send_to_many @sasai
    Scenario: Verify user can only access their own send to many transactions
        Given I have valid user authentication
        And I have a send to many transaction ID from another user
        When I send get send to many details request to "/bff/v1/wallet/payments/send-to-many"
        Then response status code should be 403 or 404
