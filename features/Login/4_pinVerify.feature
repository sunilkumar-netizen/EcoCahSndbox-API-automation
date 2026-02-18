Feature: Login- PIN Verify
    As a merchant
    I want to verify PIN from Sasai Payment Gateway API
    So that I can authenticate users securely for transactions

    # NOTE: PIN Verify API returns authentication tokens (accessToken, refreshToken, username)
    # Similar to App Token API, it's an authentication endpoint that verifies PIN

    Background:
        Given API is available
        And I am authenticated with valid app token

    @pin_verify @positive @sasai
    Scenario: Verify PIN with valid parameters
        Given I have valid PIN verification details
        When I send PIN verification request to "/bff/v4/auth/pin/verify"
        Then response status code should be 200
        And response time should be less than 5000 ms
        And response should contain PIN verification status

    @pin_verify @positive @sasai
    Scenario: Verify PIN with correct encrypted PIN
        Given I have encrypted PIN
        And I have user reference ID for PIN
        When I send PIN verification request to "/bff/v4/auth/pin/verify"
        Then response status code should be 200
        And PIN verification should be successful

    @pin_verify @positive @sasai
    Scenario: Verify PIN with query parameters
        Given I have valid PIN verification details
        And I have tenant ID "sasai"
        And I have azp "sasai-pay-client"
        When I send PIN verification request with query params to "/bff/v4/auth/pin/verify"
        Then response status code should be 200
        And response should contain PIN verification status

    @pin_verify @negative @sasai
    Scenario: Verify PIN without authentication
        Given I have valid PIN verification details
        When I send POST request to "/bff/v4/auth/pin/verify"
        Then response status code should be 400

    @pin_verify @negative @sasai
    Scenario: Verify PIN with invalid encrypted PIN
        Given I have invalid encrypted PIN
        And I have user reference ID for PIN
        When I send PIN verification request to "/bff/v4/auth/pin/verify"
        Then response status code should be 400

    @pin_verify @negative @sasai
    Scenario: Verify PIN with missing PIN field
        Given I have PIN verification without PIN
        When I send PIN verification request to "/bff/v4/auth/pin/verify"
        Then response status code should be 400

    @pin_verify @negative @sasai
    Scenario: Verify PIN with missing user reference ID
        Given I have encrypted PIN
        And I have PIN verification without user reference ID
        When I send PIN verification request to "/bff/v4/auth/pin/verify"
        Then response status code should be 400

    @pin_verify @negative @sasai
    Scenario: Verify PIN with invalid user reference ID
        Given I have encrypted PIN
        And I have invalid user reference ID for PIN
        When I send PIN verification request to "/bff/v4/auth/pin/verify"
        Then response status code should be 400

    @pin_verify @negative @sasai
    Scenario: Verify PIN with empty PIN
        Given I have empty PIN
        And I have user reference ID for PIN
        When I send PIN verification request to "/bff/v4/auth/pin/verify"
        Then response status code should be 400

    @pin_verify @negative @sasai
    Scenario: Verify PIN with invalid tenant ID
        Given I have valid PIN verification details
        And I have invalid tenant ID "invalid-tenant"
        When I send PIN verification request with query params to "/bff/v4/auth/pin/verify"
        Then response status code should be 400

    @pin_verify @negative @sasai
    Scenario: Verify PIN with missing model header
        Given I have valid PIN verification details
        When I send PIN verification request without model header to "/bff/v4/auth/pin/verify"
        Then response status code should be 400

    @pin_verify @validation @sasai
    Scenario: Verify PIN response structure
        Given I have valid PIN verification details
        When I send PIN verification request to "/bff/v4/auth/pin/verify"
        Then response status code should be 200
        And response body should be valid JSON
        And response should contain verification status

    @pin_verify @headers @validation @sasai
    Scenario: Verify PIN verification response headers
        Given I have valid PIN verification details
        When I send PIN verification request to "/bff/v4/auth/pin/verify"
        Then response status code should be 200
        And response header "Content-Type" should be present
        And response header "Content-Type" should contain "application/json"

    @pin_verify @headers @validation @sasai
    Scenario: Verify PIN verification has required headers
        Given I have valid PIN verification details
        When I send PIN verification request to "/bff/v4/auth/pin/verify"
        Then response status code should be 200
        And response header "Content-Type" should not be empty
        And response header "Date" should be present

    @pin_verify @headers @security @sasai
    Scenario: Verify PIN verification security headers
        Given I have valid PIN verification details
        When I send PIN verification request to "/bff/v4/auth/pin/verify"
        Then response status code should be 200
        And response header "Content-Type" should contain "json"

    @pin_verify @security @sasai
    Scenario: Verify PIN with expired authentication token
        Given I have expired authentication token
        And I have valid PIN verification details
        When I send PIN verification request to "/bff/v4/auth/pin/verify"
        Then response status code should be 401

    @pin_verify @security @sasai
    Scenario: Verify PIN with invalid Bearer token
        Given I have invalid authentication token
        And I have valid PIN verification details
        When I send PIN verification request to "/bff/v4/auth/pin/verify"
        Then response status code should be 401

    @pin_verify @negative @sasai
    Scenario: Verify PIN with malformed request body
        Given I have malformed PIN verification data
        When I send PIN verification request to "/bff/v4/auth/pin/verify"
        Then response status code should be 400

    @pin_verify @security @sasai
    Scenario: Verify PIN with wrong device model
        Given I have valid PIN verification details
        And I have invalid device model "HackerDevice"
        When I send PIN verification request to "/bff/v4/auth/pin/verify"
        Then response status code should be 400 or 403
