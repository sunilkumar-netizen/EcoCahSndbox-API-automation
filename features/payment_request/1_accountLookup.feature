Feature: Payment Request Account Lookup
    As a user
    I want to lookup account details for payment requests
    So that I can verify recipient information before sending payment requests

    # NOTE: Payment Request Account Lookup API requires user token (accessToken) from PIN Verify API
    # Endpoint: POST /bff/v3/payment/account/lookup
    # Request Body: { "accountNumber": "+263771222221", "origin": "requestPay" }
    # Response: Returns account details including name, status, and other information
    # This API is used to validate and retrieve account information for payment request flow

    Background:
        Given API is available
        And I am authenticated with valid app token
        And I have valid user token from PIN verification

    @smoke @payment_request @account_lookup @sasai
    Scenario: Lookup valid account for payment request
        Given I have valid user authentication
        And I have payment request account lookup details:
            | field         | value          |
            | accountNumber | +263789124669  |
            | origin        | requestPay     |
        When I send payment request account lookup to "/bff/v3/payment/account/lookup"
        Then response status code should be 200
        And response body should be valid JSON
        And response should contain account details

    @payment_request @positive @account_lookup @sasai
    Scenario: Lookup account with valid mobile number format
        Given I have valid user authentication
        And I have payment request account lookup details:
            | field         | value          |
            | accountNumber | +263771222224  |
            | origin        | requestPay     |
        When I send payment request account lookup to "/bff/v3/payment/account/lookup"
        Then response status code should be 200
        And response body should be valid JSON
        And response should contain account details

    @payment_request @positive @account_lookup @sasai
    Scenario: Lookup account with alternative mobile number format
        Given I have valid user authentication
        And I have payment request account lookup details:
            | field         | value         |
            | accountNumber | 263789124669  |
            | origin        | requestPay    |
        When I send payment request account lookup to "/bff/v3/payment/account/lookup"
        Then response status code should be 200
        And response body should be valid JSON

    @payment_request @positive @account_lookup @sasai
    Scenario: Lookup account for different origin types
        Given I have valid user authentication
        And I have payment request account lookup details:
            | field         | value          |
            | accountNumber | +263789124669  |
            | origin        | requestPay     |
        When I send payment request account lookup to "/bff/v3/payment/account/lookup"
        Then response status code should be 200
        And response body should be valid JSON

    @payment_request @negative @account_lookup @validation @sasai
    Scenario: Lookup account with missing account number
        Given I have valid user authentication
        And I have payment request account lookup without account number
        When I send payment request account lookup to "/bff/v3/payment/account/lookup"
        Then response status code should be 400

    @payment_request @negative @account_lookup @validation @sasai
    Scenario: Lookup account with missing origin
        Given I have valid user authentication
        And I have payment request account lookup without origin
        When I send payment request account lookup to "/bff/v3/payment/account/lookup"
        Then response status code should be 400

    @payment_request @negative @account_lookup @validation @sasai
    Scenario: Lookup account with empty account number
        Given I have valid user authentication
        And I have payment request account lookup details:
            | field         | value      |
            | accountNumber |            |
            | origin        | requestPay |
        When I send payment request account lookup to "/bff/v3/payment/account/lookup"
        Then response status code should be 400

    @payment_request @negative @account_lookup @validation @sasai
    Scenario: Lookup account with invalid account number format
        Given I have valid user authentication
        And I have payment request account lookup details:
            | field         | value          |
            | accountNumber | invalid123     |
            | origin        | requestPay     |
        When I send payment request account lookup to "/bff/v3/payment/account/lookup"
        Then response status code should be 400

    @payment_request @negative @account_lookup @validation @sasai
    Scenario: Lookup account with invalid mobile number (too short)
        Given I have valid user authentication
        And I have payment request account lookup details:
            | field         | value      |
            | accountNumber | +26378     |
            | origin        | requestPay |
        When I send payment request account lookup to "/bff/v3/payment/account/lookup"
        Then response status code should be 400

    @payment_request @negative @account_lookup @validation @sasai
    Scenario: Lookup account with invalid mobile number (too long)
        Given I have valid user authentication
        And I have payment request account lookup details:
            | field         | value              |
            | accountNumber | +2637891246691234  |
            | origin        | requestPay         |
        When I send payment request account lookup to "/bff/v3/payment/account/lookup"
        Then response status code should be 400

    @payment_request @negative @account_lookup @validation @sasai
    Scenario: Lookup account with non-existent account number
        Given I have valid user authentication
        And I have payment request account lookup details:
            | field         | value          |
            | accountNumber | +263700000000  |
            | origin        | requestPay     |
        When I send payment request account lookup to "/bff/v3/payment/account/lookup"
        Then response status code should be 404

    @payment_request @negative @account_lookup @validation @sasai
    Scenario: Lookup account with invalid origin value
        Given I have valid user authentication
        And I have payment request account lookup details:
            | field         | value          |
            | accountNumber | +263789124669  |
            | origin        | invalidOrigin  |
        When I send payment request account lookup to "/bff/v3/payment/account/lookup"
        Then response status code should be 400

    @payment_request @negative @account_lookup @validation @sasai
    Scenario: Lookup account with special characters in account number
        Given I have valid user authentication
        And I have payment request account lookup details:
            | field         | value             |
            | accountNumber | +263789@#$%^&*()  |
            | origin        | requestPay        |
        When I send payment request account lookup to "/bff/v3/payment/account/lookup"
        Then response status code should be 400

    @payment_request @negative @account_lookup @validation @sasai
    Scenario: Lookup account with alphabetic characters in account number
        Given I have valid user authentication
        And I have payment request account lookup details:
            | field         | value          |
            | accountNumber | +263abcdefghi  |
            | origin        | requestPay     |
        When I send payment request account lookup to "/bff/v3/payment/account/lookup"
        Then response status code should be 400

    @payment_request @negative @account_lookup @auth @sasai
    Scenario: Lookup account without authentication
        Given I am not authenticated
        And I have payment request account lookup details:
            | field         | value          |
            | accountNumber | +263789124669  |
            | origin        | requestPay     |
        When I send payment request account lookup to "/bff/v3/payment/account/lookup"
        Then response status code should be 401

    @payment_request @negative @account_lookup @auth @sasai
    Scenario: Lookup account with invalid user token
        Given I have invalid user token
        And I have payment request account lookup details:
            | field         | value          |
            | accountNumber | +263789124669  |
            | origin        | requestPay     |
        When I send payment request account lookup to "/bff/v3/payment/account/lookup"
        Then response status code should be 401

    @payment_request @negative @account_lookup @auth @sasai
    Scenario: Lookup account with expired user token
        Given I have expired user token
        And I have payment request account lookup details:
            | field         | value          |
            | accountNumber | +263789124669  |
            | origin        | requestPay     |
        When I send payment request account lookup to "/bff/v3/payment/account/lookup"
        Then response status code should be 401

    @payment_request @integration @account_lookup @end_to_end @sasai
    Scenario: Complete account lookup flow for payment request
        Given I have valid user authentication
        # Step 1: User token should be valid
        Then user token should be valid
        # Step 2: Lookup account for payment request
        Given I have payment request account lookup details:
            | field         | value          |
            | accountNumber | +263789124669  |
            | origin        | requestPay     |
        When I send payment request account lookup to "/bff/v3/payment/account/lookup"
        Then response status code should be 200
        And response body should be valid JSON
        And response should contain account details
        # Step 3: Verify account details structure
        And response should contain field "accountNumber"
        And response should contain field "name"

    @payment_request @performance @account_lookup @sasai
    Scenario: Multiple consecutive account lookups
        Given I have valid user authentication
        # First lookup
        And I have payment request account lookup details:
            | field         | value          |
            | accountNumber | +263789124669  |
            | origin        | requestPay     |
        When I send payment request account lookup to "/bff/v3/payment/account/lookup"
        Then response status code should be 200
        # Second lookup with different number
        Given I have payment request account lookup details:
            | field         | value          |
            | accountNumber | +263771222221  |
            | origin        | requestPay     |
        When I send payment request account lookup to "/bff/v3/payment/account/lookup"
        Then response status code should be 200
        # Third lookup - same as first
        Given I have payment request account lookup details:
            | field         | value          |
            | accountNumber | +263789124669  |
            | origin        | requestPay     |
        When I send payment request account lookup to "/bff/v3/payment/account/lookup"
        Then response status code should be 200

    @payment_request @boundary @account_lookup @sasai
    Scenario: Lookup account with minimum valid mobile number length
        Given I have valid user authentication
        And I have payment request account lookup details:
            | field         | value         |
            | accountNumber | +26378912466  |
            | origin        | requestPay    |
        When I send payment request account lookup to "/bff/v3/payment/account/lookup"
        Then response status code should be 200 or 400

    @payment_request @boundary @account_lookup @sasai
    Scenario: Lookup account with maximum valid mobile number length
        Given I have valid user authentication
        And I have payment request account lookup details:
            | field         | value            |
            | accountNumber | +263789124669    |
            | origin        | requestPay       |
        When I send payment request account lookup to "/bff/v3/payment/account/lookup"
        Then response status code should be 200
