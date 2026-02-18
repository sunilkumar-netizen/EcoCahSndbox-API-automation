Feature: Wallet Balances - USD, ZWG & Diaspora
    As a user
    I want to check my wallet balance for different currencies
    So that I can view my available funds in my EcoCash wallet

    # NOTE: Wallet Balance API requires user token (accessToken) from PIN Verify API
    # This API checks the balance for a specific wallet and currency
    # Endpoint: POST /bff/v1/wallet/balance
    # Headers: Authorization (Bearer user token), Content-Type (application/json)
    # Body: country, currency, providerName, providerCode, pin (encrypted), instrumentToken

    Background:
        Given API is available
        And I am authenticated with valid app token
        And I have valid user token from PIN verification

    @smoke @wallet_balance @wallet_balances @sasai
    Scenario: Check ZWG wallet balance with valid credentials
        Given I have valid user authentication
        And I have wallet balance request payload:
            | field        | value    |
            | country      | ZW       |
            | currency     | ZWG      |
            | providerName | ecocash  |
            | providerCode | ecocash  |
        When I send wallet balance request to "/bff/v1/wallet/balance"
        Then response status code should be 200
        And response should contain wallet balance information
        And response body should be valid JSON

    @smoke @wallet_balance @wallet_balances @sasai
    Scenario: Check USD wallet balance with valid credentials
        Given I have valid user authentication
        And I have wallet balance request payload:
            | field        | value    |
            | country      | ZW       |
            | currency     | USD      |
            | providerName | ecocash  |
            | providerCode | ecocash  |
        When I send wallet balance request to "/bff/v1/wallet/balance"
        Then response status code should be 200
        And response should contain wallet balance information
        And response should contain currency "USD"

    @smoke @wallet_balance @wallet_balances @sasai
    Scenario: Check USD wallet balance with ecocash-diaspora provider
        Given I have valid user authentication
        And I have wallet balance request payload:
            | field        | value             |
            | country      | ZW                |
            | currency     | USD               |
            | providerName | ecocash-diaspora  |
            | providerCode | ecocash-diaspora  |
        When I send wallet balance request to "/bff/v1/wallet/balance"
        Then response status code should be 200
        And response should contain wallet balance information
        And response should contain currency "USD"

    @regression @wallet_balance @wallet_balances @sasai
    Scenario Outline: Check wallet balance for different currencies
        Given I have valid user authentication
        And I have wallet balance request payload with currency "<currency>"
        When I send wallet balance request to "/bff/v1/wallet/balance"
        Then response status code should be 200
        And response should contain wallet balance information
        And response should contain currency "<currency>"

        Examples:
            | currency |
            | ZWG      |
            | USD      |

    @negative @wallet_balance @wallet_balances @sasai
    Scenario: Check wallet balance without authentication
        Given I have wallet balance request payload with currency "ZWG"
        When I send wallet balance request without token to "/bff/v1/wallet/balance"
        Then response status code should be 401

    @negative @wallet_balance @wallet_balances @sasai
    Scenario: Check wallet balance with invalid token
        Given I have invalid user token
        And I have wallet balance request payload with currency "ZWG"
        When I send wallet balance request to "/bff/v1/wallet/balance"
        Then response status code should be 401

    @negative @wallet_balance @wallet_balances @sasai
    Scenario: Check wallet balance with missing required fields
        Given I have valid user authentication
        And I have incomplete wallet balance request payload
        When I send wallet balance request to "/bff/v1/wallet/balance"
        Then response status code should be 400

    @negative @wallet_balance @wallet_balances @sasai
    Scenario: Check wallet balance with invalid currency
        Given I have valid user authentication
        And I have wallet balance request payload with invalid currency "XYZ"
        When I send wallet balance request to "/bff/v1/wallet/balance"
        Then response status code should be 400

    @negative @wallet_balance @wallet_balances @sasai
    Scenario: Check wallet balance with invalid instrument token
        Given I have valid user authentication
        And I have wallet balance request payload with invalid instrument token
        When I send wallet balance request to "/bff/v1/wallet/balance"
        Then response status code should be 400 or 404

    @validation @wallet_balance @wallet_balances @sasai
    Scenario: Verify wallet balance response contains all required fields
        Given I have valid user authentication
        And I have wallet balance request payload with currency "ZWG"
        When I send wallet balance request to "/bff/v1/wallet/balance"
        Then response status code should be 200
        And response should contain field "balance"
        And response should contain field "currency"
        And response should contain field "providerName"

    @validation @wallet_balance @wallet_balances @sasai
    Scenario: Verify wallet balance amount is numeric
        Given I have valid user authentication
        And I have wallet balance request payload with currency "ZWG"
        When I send wallet balance request to "/bff/v1/wallet/balance"
        Then response status code should be 200
        And wallet balance amount should be numeric

    @security @wallet_balance @wallet_balances @sasai
    Scenario: Verify PIN is encrypted in request
        Given I have valid user authentication
        And I have wallet balance request payload with currency "ZWG"
        When I send wallet balance request to "/bff/v1/wallet/balance"
        Then request should contain encrypted PIN

    @performance @wallet_balance @wallet_balances @sasai
    Scenario: Check wallet balance response time
        Given I have valid user authentication
        And I have wallet balance request payload with currency "ZWG"
        When I send wallet balance request to "/bff/v1/wallet/balance"
        Then response status code should be 200
        And response time should be less than 3000 milliseconds
