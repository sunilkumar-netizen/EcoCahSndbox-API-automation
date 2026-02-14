Feature: Login- OTP Verify
    As a merchant
    I want to verify OTP from Sasai Payment Gateway API
    So that I can complete user authentication for secure transactions

    Background:
        Given API is available
        And I am authenticated with valid app token

    @otp_verify @positive @sasai
    Scenario: Verify OTP with valid parameters
        Given I have valid OTP verification details
        When I send OTP verification request to "/bff/v1/auth/otp/verify"
        Then response status code should be 200
        And response time should be less than 5000 ms
        And response should contain OTP verification status

    @otp_verify @positive @sasai
    Scenario: Verify OTP with correct OTP code
        Given I have OTP reference ID from previous request
        And I have valid OTP code "123456"
        And I have user reference ID
        When I send OTP verification request to "/bff/v1/auth/otp/verify"
        Then response status code should be 200
        And OTP verification should be successful

    @otp_verify @negative @sasai
    Scenario: Verify OTP without authentication
        Given I have valid OTP verification details
        When I send POST request to "/bff/v1/auth/otp/verify"
        Then response status code should be 401

    @otp_verify @negative @sasai
    Scenario: Verify OTP with invalid OTP code
        Given I have OTP reference ID from previous request
        And I have invalid OTP code "000000"
        And I have user reference ID
        When I send OTP verification request to "/bff/v1/auth/otp/verify"
        Then response status code should be 400

    @otp_verify @negative @sasai
    Scenario: Verify OTP with expired OTP reference
        Given I have expired OTP reference ID
        And I have valid OTP code "123456"
        And I have user reference ID
        When I send OTP verification request to "/bff/v1/auth/otp/verify"
        Then response status code should be 400

    @otp_verify @negative @sasai
    Scenario: Verify OTP with missing OTP reference ID
        Given I have OTP verification without reference ID
        When I send OTP verification request to "/bff/v1/auth/otp/verify"
        Then response status code should be 400

    @otp_verify @negative @sasai
    Scenario: Verify OTP with missing OTP code
        Given I have OTP reference ID from previous request
        And I have user reference ID
        And I have OTP verification without OTP code
        When I send OTP verification request to "/bff/v1/auth/otp/verify"
        Then response status code should be 400

    @otp_verify @negative @sasai
    Scenario: Verify OTP with invalid user reference ID
        Given I have OTP reference ID from previous request
        And I have valid OTP code "123456"
        And I have invalid user reference ID
        When I send OTP verification request to "/bff/v1/auth/otp/verify"
        Then response status code should be 400

    @otp_verify @validation @sasai
    Scenario: Verify OTP response structure
        Given I have valid OTP verification details
        When I send OTP verification request to "/bff/v1/auth/otp/verify"
        Then response status code should be 200
        And response body should be valid JSON
        And response should contain verification status

    @otp_verify @headers @validation @sasai
    Scenario: Verify OTP verification response headers
        Given I have valid OTP verification details
        When I send OTP verification request to "/bff/v1/auth/otp/verify"
        Then response status code should be 200
        And response header "Content-Type" should be present
        And response header "Content-Type" should contain "application/json"

    @otp_verify @headers @validation @sasai
    Scenario: Verify OTP verification has required headers
        Given I have valid OTP verification details
        When I send OTP verification request to "/bff/v1/auth/otp/verify"
        Then response status code should be 200
        And response header "Content-Type" should not be empty
        And response header "Date" should be present

    @otp_verify @headers @security @sasai
    Scenario: Verify OTP verification security headers
        Given I have valid OTP verification details
        When I send OTP verification request to "/bff/v1/auth/otp/verify"
        Then response status code should be 200
        And response header "Content-Type" should contain "json"

    @otp_verify @security @sasai
    Scenario: Verify OTP with expired authentication token
        Given I have expired authentication token
        And I have valid OTP verification details
        When I send OTP verification request to "/bff/v1/auth/otp/verify"
        Then response status code should be 401

    @otp_verify @security @sasai
    Scenario: Verify OTP with invalid Bearer token
        Given I have invalid authentication token
        And I have valid OTP verification details
        When I send OTP verification request to "/bff/v1/auth/otp/verify"
        Then response status code should be 401

    @otp_verify @negative @sasai
    Scenario: Verify OTP with malformed request body
        Given I have malformed OTP verification data
        When I send OTP verification request to "/bff/v1/auth/otp/verify"
        Then response status code should be 400
