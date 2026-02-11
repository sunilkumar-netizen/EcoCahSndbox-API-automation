Feature: Payment Reminders - Complete Smoke Test Flow
    As a user
    I want to test the complete payment reminder lifecycle
    So that I can verify Set, Get All, and Delete operations work together

    # NOTE: This is an integrated smoke test that exercises all 3 payment reminder APIs
    # in sequence: Set → Get All (extract ID) → Delete
    # This ensures the reminder ID flows correctly between operations

    Background:
        Given API is available
        And I am authenticated with valid app token
        And I have valid user token from PIN verification

    @smoke @payment_reminder @complete_flow @sasai
    Scenario: Complete payment reminder lifecycle - Set, Get All, Delete
        Given I have valid user authentication
        
        # Step 1: Set a new payment reminder
        And I have payment reminder details:
            | field       | value                         |
            | amount      | 127                           |
            | currency    | ZWG                           |
            | alias       | Smoke Test Complete Flow      |
            | frequency   | no-repeat                     |
            | beneficiary | +263789124669                 |
            | paymentType | wallet                        |
        When I send set reminder request to "/bff/v2/payment/reminder"
        Then response status code should be 200 or 201
        And response body should be valid JSON
        
        # Step 2: Get all reminders and extract the created reminder ID
        When I send get all reminders request to "/bff/v1/payment/reminder" with parameters:
            | parameter | value  |
            | count     | 10     |
            | skip      | 0      |
            | status    | active |
        Then response status code should be 200
        And response body should be valid JSON
        And response should contain reminders list
        And I should extract and store first reminder ID if available
        
        # Step 3: Delete the reminder using extracted ID
        When I send delete reminder request to "/bff/v1/payment/reminder/{reminderId}"
        Then response status code should be 200 or 204
        And response body should be valid JSON
