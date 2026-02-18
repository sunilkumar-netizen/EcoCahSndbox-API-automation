Feature: Wallet Profile Balance - Check Balance API
    As a user
    I want to check my wallet profile balance for different currencies
    So that I can view my available funds using the profile balance endpoint

    # NOTE: Profile Balance API requires user token (accessToken) from PIN Verify API
    # This API checks the balance using query parameters (simpler than wallet/balance endpoint)
    # Endpoint: GET /bff/v1/wallet/profile/balance?currency={currency}&providerCode={providerCode}
    # Headers: Authorization (Bearer user token), requestId, appChannel
    # Query Params: currency (USD/ZWG), providerCode (ecocash/ecocash-diaspora)

    Background:
        Given API is available
        And I am authenticated with valid app token
        And I have valid user token from PIN verification

    @smoke @profile_balance @wallet_balances @sasai
    Scenario: Check USD profile balance with ecocash provider
        Given I have valid user authentication
        And I have profile balance query parameters:
            | parameter    | value    |
            | currency     | USD      |
            | providerCode | ecocash  |
        When I send profile balance request to "/bff/v1/wallet/profile/balance"
        Then response status code should be 200
        And response should contain profile balance information
        And response body should be valid JSON

    @smoke @profile_balance @wallet_balances @sasai
    Scenario: Check ZWG profile balance with ecocash provider
        Given I have valid user authentication
        And I have profile balance query parameters:
            | parameter    | value   |
            | currency     | ZWG     |
            | providerCode | ecocash |
        When I send profile balance request to "/bff/v1/wallet/profile/balance"
        Then response status code should be 200
        And response should contain profile balance information
        And response body should be valid JSON

    @smoke @profile_balance @wallet_balances @sasai
    Scenario: Check USD profile balance with ecocash-diaspora provider
        Given I have valid user authentication
        And I have profile balance query parameters:
            | parameter    | value             |
            | currency     | USD               |
            | providerCode | ecocash-diaspora  |
        When I send profile balance request to "/bff/v1/wallet/profile/balance"
        Then response status code should be 200
        And response should contain profile balance information
        And response body should be valid JSON

    @regression @profile_balance @wallet_balances @sasai
    Scenario Outline: Check profile balance for multiple currency and provider combinations
        Given I have valid user authentication
        And I have profile balance query parameters:
            | parameter    | value        |
            | currency     | <currency>   |
            | providerCode | <provider>   |
        When I send profile balance request to "/bff/v1/wallet/profile/balance"
        Then response status code should be 200
        And response should contain profile balance information

        Examples:
            | currency | provider          |
            | USD      | ecocash           |
            | USD      | ecocash-diaspora  |
            | ZWG      | ecocash           |

    @negative @profile_balance @wallet_balances @sasai
    Scenario: Check profile balance without authentication
        Given I have profile balance query parameters:
            | parameter    | value   |
            | currency     | USD     |
            | providerCode | ecocash |
        When I send profile balance request without token to "/bff/v1/wallet/profile/balance"
        Then response status code should be 401

    @negative @profile_balance @wallet_balances @sasai
    Scenario: Check profile balance with invalid token
        Given I have invalid user token
        And I have profile balance query parameters:
            | parameter    | value   |
            | currency     | USD     |
            | providerCode | ecocash |
        When I send profile balance request to "/bff/v1/wallet/profile/balance"
        Then response status code should be 401

    @negative @profile_balance @wallet_balances @sasai
    Scenario: Check profile balance without currency parameter
        Given I have valid user authentication
        And I have profile balance query parameters:
            | parameter    | value   |
            | providerCode | ecocash |
        When I send profile balance request to "/bff/v1/wallet/profile/balance"
        Then response status code should be 400

    @negative @profile_balance @wallet_balances @sasai
    Scenario: Check profile balance without provider code parameter
        Given I have valid user authentication
        And I have profile balance query parameters:
            | parameter | value |
            | currency  | USD   |
        When I send profile balance request to "/bff/v1/wallet/profile/balance"
        Then response status code should be 400

    @negative @profile_balance @wallet_balances @sasai
    Scenario: Check profile balance with invalid currency
        Given I have valid user authentication
        And I have profile balance query parameters:
            | parameter    | value   |
            | currency     | XYZ     |
            | providerCode | ecocash |
        When I send profile balance request to "/bff/v1/wallet/profile/balance"
        Then response status code should be 400

    @negative @profile_balance @wallet_balances @sasai
    Scenario: Check profile balance with invalid provider code
        Given I have valid user authentication
        And I have profile balance query parameters:
            | parameter    | value        |
            | currency     | USD          |
            | providerCode | invalid-code |
        When I send profile balance request to "/bff/v1/wallet/profile/balance"
        Then response status code should be 400 or 404

    @validation @profile_balance @wallet_balances @sasai
    Scenario: Verify profile balance response contains all required fields
        Given I have valid user authentication
        And I have profile balance query parameters:
            | parameter    | value   |
            | currency     | USD     |
            | providerCode | ecocash |
        When I send profile balance request to "/bff/v1/wallet/profile/balance"
        Then response status code should be 200
        And response should contain field "balance" or "balanceAmount"

    @validation @profile_balance @wallet_balances @sasai
    Scenario: Verify profile balance amount is numeric
        Given I have valid user authentication
        And I have profile balance query parameters:
            | parameter    | value   |
            | currency     | USD     |
            | providerCode | ecocash |
        When I send profile balance request to "/bff/v1/wallet/profile/balance"
        Then response status code should be 200
        And profile balance amount should be numeric

    @performance @profile_balance @wallet_balances @sasai
    Scenario: Check profile balance response time
        Given I have valid user authentication
        And I have profile balance query parameters:
            | parameter    | value   |
            | currency     | USD     |
            | providerCode | ecocash |
        When I send profile balance request to "/bff/v1/wallet/profile/balance"
        Then response status code should be 200
        And response time should be less than 3000 milliseconds
