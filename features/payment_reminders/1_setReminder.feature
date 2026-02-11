Feature: Set Payment Reminder -Person
    As a user
    I want to set payment reminders for person-to-person payments
    So that I can schedule and automate future payments

    # NOTE: Set Reminder API requires user token (accessToken) from PIN Verify API
    # Endpoint: POST /bff/v2/payment/reminder
    # Request Body: Contains customerId, amount, currency, alias, trigger (frequency, startAt), and notes
    # Response: Returns reminder details including reminder ID, status, etc.
    # This API creates a payment reminder that can be non-recurring or recurring

    Background:
        Given API is available
        And I am authenticated with valid app token
        And I have valid user token from PIN verification

    @smoke @payment_reminder @set_reminder @sasai
    Scenario: Set non-recurring payment reminder with valid details
        Given I have valid user authentication
        And I have payment reminder details:
            | field           | value                      |
            | amount          | 127                        |
            | currency        | ZWG                        |
            | alias           | NonRec Person Reminder     |
            | frequency       | no-repeat                  |
            | beneficiary     | +263789124669              |
            | paymentType     | wallet                     |
        When I send set reminder request to "/bff/v2/payment/reminder"
        Then response status code should be 200 or 201
        And response body should be valid JSON

    @payment_reminder @positive @set_reminder @sasai
    Scenario: Set payment reminder with minimum amount
        Given I have valid user authentication
        And I have payment reminder with amount 1 ZWG
        When I send set reminder request to "/bff/v2/payment/reminder"
        Then response status code should be 200 or 201

    @payment_reminder @positive @set_reminder @sasai
    Scenario: Set payment reminder with custom alias
        Given I have valid user authentication
        And I have payment reminder with alias "Monthly Rent Payment"
        When I send set reminder request to "/bff/v2/payment/reminder"
        Then response status code should be 200 or 201

    @payment_reminder @positive @set_reminder @sasai
    Scenario: Set payment reminder with different currency (USD)
        Given I have valid user authentication
        And I have payment reminder with currency "USD"
        When I send set reminder request to "/bff/v2/payment/reminder"
        Then response status code should be 200 or 201

    @payment_reminder @negative @set_reminder @validation @sasai
    Scenario: Set payment reminder with missing amount
        Given I have valid user authentication
        And I have payment reminder without amount
        When I send set reminder request to "/bff/v2/payment/reminder"
        Then response status code should be 400

#    @payment_reminder @negative @set_reminder @validation @sasai
#    Scenario: Set payment reminder with invalid amount (zero)
#        Given I have valid user authentication
#        And I have payment reminder with amount 0
#        When I send set reminder request to "/bff/v2/payment/reminder"
#        Then response status code should be 400

  #  @payment_reminder @negative @set_reminder @validation @sasai
  #  Scenario: Set payment reminder with negative amount
  #      Given I have valid user authentication
  #      And I have payment reminder with amount -100
  #      When I send set reminder request to "/bff/v2/payment/reminder"
  #      Then response status code should be 400

    @payment_reminder @negative @set_reminder @validation @sasai
    Scenario: Set payment reminder with missing currency
        Given I have valid user authentication
        And I have payment reminder without currency
        When I send set reminder request to "/bff/v2/payment/reminder"
        Then response status code should be 400

    @payment_reminder @negative @set_reminder @validation @sasai
    Scenario: Set payment reminder with invalid currency
        Given I have valid user authentication
        And I have payment reminder with currency "INVALID"
        When I send set reminder request to "/bff/v2/payment/reminder"
        Then response status code should be 400

    @payment_reminder @negative @set_reminder @validation @sasai
    Scenario: Set payment reminder with missing frequency
        Given I have valid user authentication
        And I have payment reminder without frequency
        When I send set reminder request to "/bff/v2/payment/reminder"
        Then response status code should be 400

    @payment_reminder @negative @set_reminder @validation @sasai
    Scenario: Set payment reminder with invalid frequency
        Given I have valid user authentication
        And I have payment reminder with frequency "invalid-frequency"
        When I send set reminder request to "/bff/v2/payment/reminder"
        Then response status code should be 400

   # @payment_reminder @negative @set_reminder @validation @sasai
   # Scenario: Set payment reminder with missing beneficiary
   #     Given I have valid user authentication
   #     And I have payment reminder without beneficiary
   #     When I send set reminder request to "/bff/v2/payment/reminder"
   #     Then response status code should be 400

   # @payment_reminder @negative @set_reminder @validation @sasai
   # Scenario: Set payment reminder with invalid beneficiary phone
   #     Given I have valid user authentication
   #     And I have payment reminder with beneficiary "invalid-phone"
   #     When I send set reminder request to "/bff/v2/payment/reminder"
   #     Then response status code should be 400

    @payment_reminder @negative @set_reminder @auth @sasai
    Scenario: Set payment reminder without authentication
        Given I am not authenticated
        And I have complete payment reminder payload with non-recurring frequency
        When I send set reminder request to "/bff/v2/payment/reminder"
        Then response status code should be 401

    @payment_reminder @negative @set_reminder @auth @sasai
    Scenario: Set payment reminder with invalid token
        Given I have invalid user token
        And I have complete payment reminder payload with non-recurring frequency
        When I send set reminder request to "/bff/v2/payment/reminder"
        Then response status code should be 401

    @payment_reminder @integration @set_reminder @end_to_end @sasai
    Scenario: Complete flow - Login and Set Payment Reminder
        Given I have valid user authentication
        # Step 1: Verify user is authenticated
        Then user token should be valid
        # Step 2: Set payment reminder
        Given I have payment reminder details:
            | field           | value                      |
            | amount          | 150                        |
            | currency        | ZWG                        |
            | alias           | Integration Test Reminder  |
            | frequency       | no-repeat                  |
            | beneficiary     | +263789124669              |
            | paymentType     | wallet                     |
        When I send set reminder request to "/bff/v2/payment/reminder"
        Then response status code should be 200 or 201
        And response body should be valid JSON
