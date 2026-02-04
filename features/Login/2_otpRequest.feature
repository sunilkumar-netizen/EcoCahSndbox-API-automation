Feature: Login- OTP Request
    As a merchant
    I want to request OTP from Sasai Payment Gateway API
    So that I can verify user identity for secure transactions

    Background:
        Given API is available
        And I am authenticated with valid app token

    @smoke @otp @sasai
    Scenario: Request OTP with valid parameters
        Given I have valid OTP request details
        When I send authenticated POST request to "/bff/v2/auth/otp/request"
        Then response status code should be 200
        And response time should be less than 5000 ms

    @otp @positive @sasai
    Scenario: Request OTP with SMS mode
        Given I have OTP request with sender ID "771222221"
        And I have country code "+263"
        And I have OTP purpose "0"
        And I have OTP mode "0"
        When I send authenticated POST request to "/bff/v2/auth/otp/request"
        Then response status code should be 200

    @otp @negative @sasai
    Scenario: Request OTP without authentication
        Given I have valid OTP request details
        When I send POST request to "/bff/v2/auth/otp/request"
        Then response status code should be 401

    @otp @negative @sasai
    Scenario: Request OTP with invalid sender ID
        Given I have OTP request with sender ID "invalid"
        And I have country code "+263"
        And I have OTP purpose "0"
        And I have OTP mode "0"
        When I send authenticated POST request to "/bff/v2/auth/otp/request"
        Then response status code should be 400

    @otp @negative @sasai
    Scenario: Request OTP with missing sender ID
        Given I have OTP request without sender ID
        When I send authenticated POST request to "/bff/v2/auth/otp/request"
        Then response status code should be 400

    @otp @negative @sasai
    Scenario: Request OTP with invalid country code
        Given I have OTP request with sender ID "771222221"
        And I have country code "invalid"
        And I have OTP purpose "0"
        And I have OTP mode "0"
        When I send authenticated POST request to "/bff/v2/auth/otp/request"
        Then response status code should be 400

    @otp @validation @sasai
    Scenario: Verify OTP request response structure
        Given I have valid OTP request details
        When I send authenticated POST request to "/bff/v2/auth/otp/request"
        Then response status code should be 200
        And response body should contain "otpReferenceId"
        And response body should contain "userReferenceId"

    @otp @headers @validation @sasai
    Scenario: Verify OTP request response headers
        Given I have valid OTP request details
        When I send authenticated POST request to "/bff/v2/auth/otp/request"
        Then response status code should be 200
        And response header "Content-Type" should be present
        And response header "Content-Type" should contain "application/json"

    @otp @headers @validation @sasai
    Scenario: Verify OTP request has required headers
        Given I have valid OTP request details
        When I send authenticated POST request to "/bff/v2/auth/otp/request"
        Then response status code should be 200
        And response header "Content-Type" should not be empty
        And response header "Date" should be present

    @otp @headers @security @sasai
    Scenario: Verify OTP request security headers
        Given I have valid OTP request details
        When I send authenticated POST request to "/bff/v2/auth/otp/request"
        Then response status code should be 200
        And response header "Content-Type" should contain "json"

    @otp @security @sasai
    Scenario: Request OTP with expired token
        Given I have expired authentication token
        And I have valid OTP request details
        When I send authenticated POST request to "/bff/v2/auth/otp/request"
        Then response status code should be 401
