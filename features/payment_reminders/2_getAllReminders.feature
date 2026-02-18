Feature: Get All Payment Reminders
    As a user
    I want to retrieve all my payment reminders
    So that I can view and manage my scheduled payments

    # NOTE: Get All Reminders API requires user token (accessToken) from PIN Verify API
    # Endpoint: GET /bff/v1/payment/reminder
    # Query Parameters: count (pagination size), skip (offset), status (filter by status)
    # Response: Returns list of reminders with details including reminderId, amount, status, etc.
    # This API retrieves all payment reminders for the authenticated user

    Background:
        Given API is available
        And I am authenticated with valid app token
        And I have valid user token from PIN verification

    @smoke @payment_reminder @get_reminders @sasai
    Scenario: Get all active payment reminders
        Given I have valid user authentication
        When I send get all reminders request to "/bff/v1/payment/reminder" with parameters:
            | parameter | value  |
            | count     | 10     |
            | skip      | 0      |
            | status    | active |
        Then response status code should be 200
        And response body should be valid JSON
        And response should contain reminders list
        And I should extract and store first reminder ID if available

    @payment_reminder @positive @get_reminders @sasai
    Scenario: Get all reminders without status filter
        Given I have valid user authentication
        When I send get all reminders request to "/bff/v1/payment/reminder" with parameters:
            | parameter | value |
            | count     | 10    |
            | skip      | 0     |
        Then response status code should be 200
        And response body should be valid JSON

    @payment_reminder @positive @get_reminders @sasai
    Scenario: Get reminders with pagination (first page)
        Given I have valid user authentication
        When I send get all reminders request with count 5 and skip 0
        Then response status code should be 200
        And response body should be valid JSON

    @payment_reminder @positive @get_reminders @sasai
    Scenario: Get reminders with pagination (second page)
        Given I have valid user authentication
        When I send get all reminders request with count 5 and skip 5
        Then response status code should be 200
        And response body should be valid JSON

    @payment_reminder @positive @get_reminders @sasai
    Scenario: Get reminders with large count
        Given I have valid user authentication
        When I send get all reminders request with count 50 and skip 0
        Then response status code should be 200
        And response body should be valid JSON

    @payment_reminder @positive @get_reminders @sasai
    Scenario: Get reminders and extract reminder ID
        Given I have valid user authentication
        When I send get all reminders request with count 10 and skip 0
        Then response status code should be 200
        And response body should be valid JSON
        And I should extract and store first reminder ID if available

   # @payment_reminder @positive @get_reminders @status_filter @sasai
   # Scenario Outline: Get reminders filtered by status
   #     Given I have valid user authentication
   #     When I send get all reminders request to "/bff/v1/payment/reminder" with parameters:
   #         | parameter | value    |
   #         | count     | 10       |
   #         | skip      | 0        |
   #         | status    | <status> |
   #     Then response status code should be 200
   #     And response body should be valid JSON
   #     And response should contain reminders list
#
   #     Examples:
   #         | status   |
   #         | active   |
   #         | in-active |

   # @payment_reminder @negative @get_reminders @validation @sasai
   # Scenario: Get reminders with invalid count (zero)
   #     Given I have valid user authentication
   #     When I send get all reminders request with count 0 and skip 0
   #     Then response status code should be 400

   # @payment_reminder @negative @get_reminders @validation @sasai
   # Scenario: Get reminders with negative count
   #     Given I have valid user authentication
   #     When I send get all reminders request with count -10 and skip 0
   #     Then response status code should be 400

  #  @payment_reminder @negative @get_reminders @validation @sasai
  #  Scenario: Get reminders with negative skip
  #      Given I have valid user authentication
  #      When I send get all reminders request with count 10 and skip -5
  #      Then response status code should be 400

    @payment_reminder @negative @get_reminders @validation @sasai
    Scenario: Get reminders with invalid status
        Given I have valid user authentication
        When I send get all reminders request to "/bff/v1/payment/reminder" with parameters:
            | parameter | value          |
            | count     | 10             |
            | skip      | 0              |
            | status    | invalid-status |
        Then response status code should be 400

    @payment_reminder @negative @get_reminders @auth @sasai
    Scenario: Get reminders without authentication
        Given I am not authenticated
        When I send get all reminders request with count 10 and skip 0
        Then response status code should be 401

    @payment_reminder @negative @get_reminders @auth @sasai
    Scenario: Get reminders with invalid token
        Given I have invalid user token
        When I send get all reminders request with count 10 and skip 0
        Then response status code should be 401

   # @payment_reminder @integration @get_reminders @end_to_end @sasai
   # Scenario: Complete flow - Set reminder and retrieve all reminders
   #     Given I have valid user authentication
   #     # Step 1: Verify user is authenticated
   #     Then user token should be valid
   #     # Step 2: Set a new payment reminder
   #     Given I have payment reminder details:
   #         | field       | value                         |
   #         | amount      | 200                           |
   #         | currency    | ZWG                           |
   #         | alias       | Test Reminder for Retrieval   |
   #         | frequency   | no-repeat                     |
   #         | beneficiary | +263789124669                 |
   #         | paymentType | wallet                        |
   #     When I send set reminder request to "/bff/v2/payment/reminder"
   #     Then response status code should be 200 or 201
   #     # Step 3: Retrieve all reminders to verify creation
   #     When I send get all reminders request with count 10 and skip 0
   #     Then response status code should be 200
   #     And response body should be valid JSON
   #     And response should contain reminders list
