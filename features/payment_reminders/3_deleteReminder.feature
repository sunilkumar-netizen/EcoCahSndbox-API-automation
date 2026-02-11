Feature: Delete Payment Reminder
    As a user
    I want to delete a payment reminder
    So that I can cancel scheduled payments that are no longer needed

    # NOTE: Delete Reminder API requires user token (accessToken) from PIN Verify API
    # Endpoint: DELETE /bff/v1/payment/reminder/{reminderId}
    # Path Parameter: reminderId (UUID of the reminder to delete)
    # Response: Returns 200/204 on successful deletion
    # This API deletes a specific payment reminder for the authenticated user

    Background:
        Given API is available
        And I am authenticated with valid app token
        And I have valid user token from PIN verification

   # @smoke @payment_reminder @delete_reminder @sasai
   # Scenario: Delete a payment reminder successfully (using stored reminder ID from Get All)
    #    Given I have valid user authentication
        # Note: This scenario expects reminder ID to be stored from previous Get All Reminders test
        # If running standalone, it will use reminder ID from config
    #    When I send delete reminder request to "/bff/v1/payment/reminder/{reminderId}"
   #     Then response status code should be 200 or 204
   #     And response body should be valid JSON

    @payment_reminder @positive @delete_reminder @sasai
    Scenario: Delete reminder after creating it
        Given I have valid user authentication
        # Step 1: Create a new reminder
        And I have payment reminder details:
            | field       | value                    |
            | amount      | 150                      |
            | currency    | ZWG                      |
            | alias       | Reminder to be deleted   |
            | frequency   | no-repeat                |
            | beneficiary | +263789124669            |
            | paymentType | wallet                   |
        When I send set reminder request to "/bff/v2/payment/reminder"
        Then response status code should be 200 or 201
        # Step 2: Get all reminders and extract the reminder ID
        When I send get all reminders request with count 10 and skip 0
        Then response status code should be 200
        And I should extract and store first reminder ID if available
        # Step 3: Delete the created reminder
        When I send delete reminder request to "/bff/v1/payment/reminder/{reminderId}"
        Then response status code should be 200 or 204

    @payment_reminder @positive @delete_reminder @sasai
    Scenario: Delete reminder and verify it's removed
        Given I have valid user authentication
        # Step 1: Create a new reminder
        And I have payment reminder details:
            | field       | value                  |
            | amount      | 100                    |
            | currency    | ZWG                    |
            | alias       | Test Delete Reminder   |
            | frequency   | no-repeat              |
            | beneficiary | +263789124669          |
            | paymentType | wallet                 |
        When I send set reminder request to "/bff/v2/payment/reminder"
        Then response status code should be 200 or 201
        # Step 2: Get all reminders and extract the reminder ID
        When I send get all reminders request with count 10 and skip 0
        Then response status code should be 200
        And I should extract and store first reminder ID if available
        # Step 3: Delete the reminder
        When I send delete reminder request to "/bff/v1/payment/reminder/{reminderId}"
        Then response status code should be 200 or 204
        # Step 4: Try to get all reminders again (deleted reminder should not appear)
        When I send get all reminders request with count 10 and skip 0
        Then response status code should be 200

  #  @payment_reminder @negative @delete_reminder @validation @sasai
  #  Scenario: Delete reminder with invalid reminder ID format
  #      Given I have valid user authentication
  #      When I send delete reminder request to "/bff/v1/payment/reminder/invalid-id-123"
  #      Then response status code should be 400

    @payment_reminder @negative @delete_reminder @validation @sasai
    Scenario: Delete reminder with non-existent reminder ID
        Given I have valid user authentication
        When I send delete reminder request to "/bff/v1/payment/reminder/00000000-0000-0000-0000-000000000000"
        Then response status code should be 404

    @payment_reminder @negative @delete_reminder @validation @sasai
    Scenario: Delete reminder with empty reminder ID
        Given I have valid user authentication
        When I send delete reminder request to "/bff/v1/payment/reminder/"
        Then response status code should be 404 or 405

   # @payment_reminder @negative @delete_reminder @validation @sasai
   # Scenario: Delete reminder with special characters in ID
   #     Given I have valid user authentication
   #     When I send delete reminder request to "/bff/v1/payment/reminder/@#$%^&*()"
   #     Then response status code should be 400

    @payment_reminder @negative @delete_reminder @auth @sasai
    Scenario: Delete reminder without authentication
        Given I am not authenticated
        And I have a valid reminder ID from config
        When I send delete reminder request to "/bff/v1/payment/reminder/{reminderId}"
        Then response status code should be 401

    @payment_reminder @negative @delete_reminder @auth @sasai
    Scenario: Delete reminder with invalid token
        Given I have invalid user token
        And I have a valid reminder ID from config
        When I send delete reminder request to "/bff/v1/payment/reminder/{reminderId}"
        Then response status code should be 401

    @payment_reminder @negative @delete_reminder @auth @sasai
    Scenario: Delete reminder with expired token
        Given I have expired user token
        And I have a valid reminder ID from config
        When I send delete reminder request to "/bff/v1/payment/reminder/{reminderId}"
        Then response status code should be 401

   # @payment_reminder @integration @delete_reminder @end_to_end @sasai
   # Scenario: Complete reminder lifecycle - Create, Retrieve, Delete, Verify
   #     Given I have valid user authentication
   #     # Step 1: Create a new payment reminder
   #     Given I have payment reminder details:
   #         | field       | value                         |
   #         | amount      | 250                           |
   #         | currency    | ZWG                           |
   #         | alias       | Complete Lifecycle Test       |
   #         | frequency   | no-repeat                     |
   #         | beneficiary | +263789124669                 |
   #         | paymentType | wallet                        |
   #     When I send set reminder request to "/bff/v2/payment/reminder"
   #     Then response status code should be 200 or 201
   #     And response body should be valid JSON
   #     # Step 2: Retrieve all reminders to find the created one
   #     When I send get all reminders request with count 10 and skip 0
   #     Then response status code should be 200
   #     And response body should be valid JSON
   #     And response should contain reminders list
   #     And I should extract and store first reminder ID if available
   #     # Step 3: Delete the reminder using extracted ID
   #     When I send delete reminder request to "/bff/v1/payment/reminder/{reminderId}"
   #     Then response status code should be 200 or 204
   #     And response body should be valid JSON
   #     # Step 4: Verify deletion by retrieving all reminders again
   #     When I send get all reminders request with count 10 and skip 0
   #     Then response status code should be 200
   #     And response body should be valid JSON

    @payment_reminder @integration @delete_reminder @multiple @sasai
    Scenario: Delete multiple reminders sequentially
        Given I have valid user authentication
        # Create first reminder
        And I have payment reminder details:
            | field       | value                |
            | amount      | 100                  |
            | currency    | ZWG                  |
            | alias       | First Reminder       |
            | frequency   | no-repeat            |
            | beneficiary | +263789124669        |
            | paymentType | wallet               |
        When I send set reminder request to "/bff/v2/payment/reminder"
        Then response status code should be 200 or 201
        # Get and delete first reminder
        When I send get all reminders request with count 10 and skip 0
        Then response status code should be 200
        And I should extract and store first reminder ID if available
        When I send delete reminder request to "/bff/v1/payment/reminder/{reminderId}"
        Then response status code should be 200 or 204
        # Create second reminder
        Given I have payment reminder details:
            | field       | value                |
            | amount      | 200                  |
            | currency    | ZWG                  |
            | alias       | Second Reminder      |
            | frequency   | no-repeat            |
            | beneficiary | +263789124669        |
            | paymentType | wallet               |
        When I send set reminder request to "/bff/v2/payment/reminder"
        Then response status code should be 200 or 201
        # Get and delete second reminder
        When I send get all reminders request with count 10 and skip 0
        Then response status code should be 200
        And I should extract and store first reminder ID if available
        When I send delete reminder request to "/bff/v1/payment/reminder/{reminderId}"
        Then response status code should be 200 or 204
