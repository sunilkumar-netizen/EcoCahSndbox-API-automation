Feature: Login Devices
    As a user
    I want to retrieve my login devices from Sasai Payment Gateway API
    So that I can view all devices where I'm logged in

    # NOTE: Login Devices API requires user token (accessToken) from PIN Verify API
    # This is a user-level endpoint that returns list of devices where user is logged in

    Background:
        Given API is available
        And I am authenticated with valid app token
        And I have valid user token from PIN verification

    @smoke @login_devices @sasai
    Scenario: Get login devices with valid user token
        Given I have valid user authentication
        When I send login devices request to "/bff/v1/user/login-devices"
        Then response status code should be 200
        And response time should be less than 5000 ms
        And response should contain login devices list

    @login_devices @positive @sasai
    Scenario: Get login devices returns array
        Given I have valid user authentication
        When I send login devices request to "/bff/v1/user/login-devices"
        Then response status code should be 200
        And response body should be valid JSON
        And response should be a list

    @login_devices @positive @sasai
    Scenario: Get login devices with valid Bearer token
        Given I have valid user authentication
        When I send login devices request to "/bff/v1/user/login-devices"
        Then response status code should be 200
        And response should contain login devices list

    @login_devices @negative @sasai
    Scenario: Get login devices without authentication
        Given I have no authentication token
        When I send login devices request to "/bff/v1/user/login-devices"
        Then response status code should be 401

    @login_devices @negative @sasai
    Scenario: Get login devices with app token instead of user token
        Given I have app token only
        When I send login devices request to "/bff/v1/user/login-devices"
        Then response status code should be 401 or 403

    @login_devices @negative @sasai
    Scenario: Get login devices with expired user token
        Given I have expired user token
        When I send login devices request to "/bff/v1/user/login-devices"
        Then response status code should be 401

    @login_devices @negative @sasai
    Scenario: Get login devices with invalid user token
        Given I have invalid user token
        When I send login devices request to "/bff/v1/user/login-devices"
        Then response status code should be 401

    @login_devices @negative @sasai
    Scenario: Get login devices with malformed Bearer token
        Given I have malformed Bearer token
        When I send login devices request to "/bff/v1/user/login-devices"
        Then response status code should be 401

    @login_devices @validation @sasai
    Scenario: Verify login devices response structure
        Given I have valid user authentication
        When I send login devices request to "/bff/v1/user/login-devices"
        Then response status code should be 200
        And response body should be valid JSON
        And response should be a list

    @login_devices @validation @sasai
    Scenario: Verify login devices response contains device information
        Given I have valid user authentication
        When I send login devices request to "/bff/v1/user/login-devices"
        Then response status code should be 200
        And each device should have required fields

    @login_devices @headers @validation @sasai
    Scenario: Verify login devices response headers
        Given I have valid user authentication
        When I send login devices request to "/bff/v1/user/login-devices"
        Then response status code should be 200
        And response header "Content-Type" should be present
        And response header "Content-Type" should contain "application/json"

    @login_devices @headers @validation @sasai
    Scenario: Verify login devices has required headers
        Given I have valid user authentication
        When I send login devices request to "/bff/v1/user/login-devices"
        Then response status code should be 200
        And response header "Content-Type" should not be empty
        And response header "Date" should be present

    @login_devices @headers @security @sasai
    Scenario: Verify login devices security headers
        Given I have valid user authentication
        When I send login devices request to "/bff/v1/user/login-devices"
        Then response status code should be 200
        And response header "Content-Type" should contain "json"

    @login_devices @security @sasai
    Scenario: Get login devices with missing Authorization header
        Given I have no Authorization header
        When I send login devices request to "/bff/v1/user/login-devices"
        Then response status code should be 401

    @login_devices @security @sasai
    Scenario: Get login devices with empty Bearer token
        Given I have empty Bearer token
        When I send login devices request to "/bff/v1/user/login-devices"
        Then response status code should be 401

    @login_devices @security @sasai
    Scenario: Get login devices without Bearer prefix
        Given I have token without Bearer prefix
        When I send login devices request to "/bff/v1/user/login-devices"
        Then response status code should be 401

    @login_devices @error_handling @sasai
    Scenario: Get login devices with invalid HTTP method
        Given I have valid user authentication
        When I send POST request to "/bff/v1/user/login-devices"
        Then response status code should be 404

    @login_devices @error_handling @sasai
    Scenario: Get login devices with wrong endpoint
        Given I have valid user authentication
        When I send GET request to "/bff/v1/user/login-device"
        Then response status code should be 404

    @login_devices @performance @sasai
    Scenario: Verify login devices response time
        Given I have valid user authentication
        When I send login devices request to "/bff/v1/user/login-devices"
        Then response status code should be 200
        And response time should be less than 3000 ms

    @login_devices @integration @sasai
    Scenario: Complete flow - PIN Verify to Login Devices
        Given I have valid PIN verification details
        When I send PIN verification request to "/bff/v4/auth/pin/verify"
        Then response status code should be 200
        And I store the user token from response
        When I send login devices request with stored token to "/bff/v1/user/login-devices"
        Then response status code should be 200
        And response should contain login devices list
