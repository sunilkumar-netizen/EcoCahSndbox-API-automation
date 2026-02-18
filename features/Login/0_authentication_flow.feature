Feature: Login- Authentication Flow Validation
    As a test suite
    I want to validate that global authentication completed successfully
    So that all smoke tests can use the cached tokens

    # This feature validates that the global authentication optimization is working
    # It checks that tokens were obtained and cached during before_all hook

    @smoke @auth_validation @sasai
    Scenario: Validate global authentication completed successfully
        Given API is available
        Then I should have cached app token from global authentication
        And I should have cached user token from global authentication
        And cached tokens should be valid and not expired

    @smoke @auth_validation @sasai
    Scenario: Validate cached app token is usable
        Given I have cached app token from global authentication
        When I use the cached app token for API request
        Then the cached app token should be accepted by the API

    @smoke @auth_validation @sasai
    Scenario: Validate cached user token is usable
        Given I have cached user token from global authentication
        When I use the cached user token for API request
        Then the cached user token should be accepted by the API
