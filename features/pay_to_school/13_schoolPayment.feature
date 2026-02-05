Feature: School Payment
    As a user
    I want to make payments to schools
    So that I can pay school fees and related charges

    # NOTE: School Payment API requires user token (accessToken) from PIN Verify API
    # This is part of the "Pay to School" flow
    # Endpoint: POST /bff/v2/order/utility/payment
    # Request Body: Payment details including biller info, payer details, and device info
    # Sub Type: pay-to-school

    Background:
        Given API is available
        And I am authenticated with valid app token
        And I have valid user token from PIN verification

    @smoke @school_payment @pay_to_school @sasai
    Scenario: Process school payment with valid details
        Given I have valid user authentication
        And I have instrument token from payment options
        And I have school payment details
        And I have biller details with school code "054329"
        And I have payment amount 2.0
        When I send school payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response should contain payment confirmation
        And response should have transaction reference

    @school_payment @positive @pay_to_school @sasai
    Scenario: Process school payment returns correct structure
        Given I have valid user authentication
        And I have instrument token from payment options
        And I have school payment details
        And I have biller details with school code "054329"
        And I have payment amount 2.0
        When I send school payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response body should be valid JSON
        And response should have payment structure

    @school_payment @positive @pay_to_school @sasai
    Scenario: Process school payment with student reference
        Given I have valid user authentication
        And I have instrument token from payment options
        And I have school payment details
        And I have biller details with school code "054329"
        And I have student reference "John Doe"
        And I have payment amount 5.0
        When I send school payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response should contain payment confirmation

    @school_payment @positive @pay_to_school @sasai
    Scenario: Process school payment with different amount
        Given I have valid user authentication
        And I have instrument token from payment options
        And I have school payment details
        And I have biller details with school code "054329"
        And I have payment amount 10.0
        When I send school payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response should contain payment confirmation

    @school_payment @positive @pay_to_school @sasai
    Scenario: Process school payment with device information
        Given I have valid user authentication
        And I have instrument token from payment options
        And I have school payment details with device info
        And I have biller details with school code "054329"
        And I have payment amount 2.0
        When I send school payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response should contain payment confirmation

    @school_payment @negative @pay_to_school @sasai
    Scenario: Process school payment without authentication
        Given I have no authentication token
        And I have school payment details
        When I send school payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 401

    @school_payment @negative @pay_to_school @sasai
    Scenario: Process school payment with invalid user token
        Given I have invalid user token
        And I have school payment details
        When I send school payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 401

    @school_payment @negative @pay_to_school @sasai
    Scenario: Process school payment with expired user token
        Given I have expired user token
        And I have school payment details
        When I send school payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 401

    @school_payment @negative @pay_to_school @sasai
    Scenario: Process school payment with app token instead of user token
        Given I have app token only
        And I have school payment details
        When I send school payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 401 or 403

    @school_payment @negative @pay_to_school @sasai
    Scenario: Process school payment without instrument token
        Given I have valid user authentication
        And I have school payment details without instrument token
        When I send school payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 400

    @school_payment @negative @pay_to_school @sasai
    Scenario: Process school payment with invalid instrument token
        Given I have valid user authentication
        And I have invalid instrument token
        And I have school payment details
        When I send school payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 400 or 404

    @school_payment @negative @pay_to_school @sasai
    Scenario: Process school payment without payment amount
        Given I have valid user authentication
        And I have instrument token from payment options
        And I have school payment details without amount
        When I send school payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 400

    @school_payment @negative @pay_to_school @sasai
    Scenario: Process school payment with zero amount
        Given I have valid user authentication
        And I have instrument token from payment options
        And I have school payment details
        And I have payment amount 0
        When I send school payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 400

    @school_payment @negative @pay_to_school @sasai
    Scenario: Process school payment with negative amount
        Given I have valid user authentication
        And I have instrument token from payment options
        And I have school payment details
        And I have payment amount -5.0
        When I send school payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 400

    @school_payment @negative @pay_to_school @sasai
    Scenario: Process school payment without biller details
        Given I have valid user authentication
        And I have instrument token from payment options
        And I have school payment details without biller
        When I send school payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 400

    @school_payment @negative @pay_to_school @sasai
    Scenario: Process school payment with invalid school code
        Given I have valid user authentication
        And I have instrument token from payment options
        And I have school payment details
        And I have biller details with school code "9999999"
        And I have payment amount 2.0
        When I send school payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 400 or 404

    @school_payment @negative @pay_to_school @sasai
    Scenario: Process school payment without currency
        Given I have valid user authentication
        And I have instrument token from payment options
        And I have school payment details without currency
        When I send school payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 400

    @school_payment @negative @pay_to_school @sasai
    Scenario: Process school payment with invalid currency
        Given I have valid user authentication
        And I have instrument token from payment options
        And I have school payment details with currency "INVALID"
        When I send school payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 400

    @school_payment @validation @pay_to_school @sasai
    Scenario: Verify school payment response contains required fields
        Given I have valid user authentication
        And I have instrument token from payment options
        And I have school payment details
        And I have biller details with school code "054329"
        And I have payment amount 2.0
        When I send school payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And payment response should have status
        And payment response should have transaction ID
        And payment response should have reference number

    @school_payment @validation @pay_to_school @sasai
    Scenario: Verify school payment response structure
        Given I have valid user authentication
        And I have instrument token from payment options
        And I have school payment details
        And I have biller details with school code "054329"
        And I have payment amount 2.0
        When I send school payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response body should be valid JSON
        And response should have payment structure

    @school_payment @headers @validation @pay_to_school @sasai
    Scenario: Verify school payment response headers
        Given I have valid user authentication
        And I have instrument token from payment options
        And I have school payment details
        And I have biller details with school code "054329"
        And I have payment amount 2.0
        When I send school payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response header "Content-Type" should be present
        And response header "Content-Type" should contain "application/json"

    @school_payment @security @pay_to_school @sasai
    Scenario: Verify school payment with missing Authorization header
        Given I have no Authorization header
        And I have school payment details
        When I send school payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 401

    @school_payment @security @pay_to_school @sasai
    Scenario: Verify school payment with empty Bearer token
        Given I have empty Bearer token
        And I have school payment details
        When I send school payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 401

    @school_payment @security @pay_to_school @sasai
    Scenario: Verify school payment with malformed Bearer token
        Given I have malformed Bearer token
        And I have school payment details
        When I send school payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 401

    @school_payment @error_handling @pay_to_school @sasai
    Scenario: School payment with invalid HTTP method GET
        Given I have valid user authentication
        When I send GET request to "/bff/v2/order/utility/payment"
        Then response status code should be 405

    @school_payment @error_handling @pay_to_school @sasai
    Scenario: School payment with invalid HTTP method PUT
        Given I have valid user authentication
        When I send PUT request to "/bff/v2/order/utility/payment"
        Then response status code should be 405

    @school_payment @error_handling @pay_to_school @sasai
    Scenario: School payment with invalid HTTP method DELETE
        Given I have valid user authentication
        When I send DELETE request to "/bff/v2/order/utility/payment"
        Then response status code should be 405

    @school_payment @error_handling @pay_to_school @sasai
    Scenario: School payment with wrong endpoint path
        Given I have valid user authentication
        And I have school payment details
        When I send POST request to "/bff/v2/order/utility/payments"
        Then response status code should be 404

    @school_payment @performance @pay_to_school @sasai
    Scenario: Verify school payment response time
        Given I have valid user authentication
        And I have instrument token from payment options
        And I have school payment details
        And I have biller details with school code "054329"
        And I have payment amount 2.0
        When I send school payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response time should be less than 5000 ms

    @school_payment @performance @pay_to_school @sasai
    Scenario: Verify school payment response time is acceptable
        Given I have valid user authentication
        And I have instrument token from payment options
        And I have school payment details
        And I have biller details with school code "054329"
        And I have payment amount 2.0
        When I send school payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response time should be less than 10000 ms

    @school_payment @integration @pay_to_school @sasai
    Scenario: Complete flow - PIN Verify to School Payment
        Given I have valid PIN verification details
        When I send PIN verification request to "/bff/v4/auth/pin/verify"
        Then response status code should be 200
        And I store the user token from response
        Given I have service type "sasai-app-payment"
        When I send school payment options request with stored token to "/bff/v2/payment/options"
        Then response status code should be 200
        And I extract instrument token from response
        Given I have school payment details with extracted token
        And I have biller details with school code "054329"
        And I have payment amount 2.0
        When I send school payment request with stored token to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response should contain payment confirmation

    @school_payment @integration @pay_to_school @sasai
    Scenario: Complete flow - Search School, Get Options, Make Payment
        Given I have valid user authentication
        And I have search type "SCHOOL"
        And I have page number 0
        And I have page size 10
        And I have name query "school"
        When I send school search request to "/bff/v1/catalog/search-school-church-merchant"
        Then response status code should be 200
        And response should contain search results
        And I extract first merchant code from search results
        Given I have service type "sasai-app-payment"
        When I send school payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And I extract instrument token from response
        Given I have school payment details with extracted token and code
        And I have payment amount 2.0
        When I send school payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response should contain payment confirmation

    @school_payment @data_validation @pay_to_school @sasai
    Scenario: Verify payment confirmation status
        Given I have valid user authentication
        And I have instrument token from payment options
        And I have school payment details
        And I have biller details with school code "054329"
        And I have payment amount 2.0
        When I send school payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And payment status should be success or pending

    @school_payment @data_validation @pay_to_school @sasai
    Scenario: Verify payment amount in response
        Given I have valid user authentication
        And I have instrument token from payment options
        And I have school payment details
        And I have biller details with school code "054329"
        And I have payment amount 2.0
        When I send school payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And payment response should contain amount 2.0

    @school_payment @data_validation @pay_to_school @sasai
    Scenario: Verify school details in payment response
        Given I have valid user authentication
        And I have instrument token from payment options
        And I have school payment details
        And I have biller details with school code "054329"
        And I have school name "PRINCE EDWARD HIGH SCHOOL"
        And I have payment amount 2.0
        When I send school payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response should contain school details

    @school_payment @device_info @pay_to_school @sasai
    Scenario: School payment with complete device information
        Given I have valid user authentication
        And I have instrument token from payment options
        And I have complete device information
        And I have school payment details
        And I have biller details with school code "054329"
        And I have payment amount 2.0
        When I send school payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response should contain payment confirmation

    @school_payment @notes @pay_to_school @sasai
    Scenario: School payment with custom notes
        Given I have valid user authentication
        And I have instrument token from payment options
        And I have school payment details
        And I have biller details with school code "054329"
        And I have payment notes with student info
        And I have payment amount 2.0
        When I send school payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response should contain payment confirmation

    @school_payment @currency @pay_to_school @sasai
    Scenario Outline: School payment with different currencies
        Given I have valid user authentication
        And I have instrument token from payment options
        And I have school payment details with currency "<currency>"
        And I have biller details with school code "054329"
        And I have payment amount 2.0
        When I send school payment request to "/bff/v2/order/utility/payment"
        Then response status code should be <statusCode>

        Examples:
            | currency | statusCode |
            | USD      | 200        |
            | ZWG      | 200        |

    @school_payment @amounts @pay_to_school @sasai
    Scenario Outline: School payment with different amounts
        Given I have valid user authentication
        And I have instrument token from payment options
        And I have school payment details
        And I have biller details with school code "054329"
        And I have payment amount <amount>
        When I send school payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response should contain payment confirmation

        Examples:
            | amount |
            | 1.0    |
            | 2.0    |
            | 5.0    |
            | 10.0   |
            | 20.0   |
            | 50.0   |

    @school_payment @operators @pay_to_school @sasai
    Scenario: School payment with operator and category IDs
        Given I have valid user authentication
        And I have instrument token from payment options
        And I have school payment details
        And I have operator ID "SZWOSL0001"
        And I have category ID "SZWC10017"
        And I have biller details with school code "054329"
        And I have payment amount 2.0
        When I send school payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response should contain payment confirmation

    @school_payment @pin_encryption @pay_to_school @sasai
    Scenario: School payment with encrypted PIN
        Given I have valid user authentication
        And I have instrument token from payment options
        And I have school payment details with encrypted PIN
        And I have biller details with school code "054329"
        And I have payment amount 2.0
        When I send school payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response should contain payment confirmation

    @school_payment @provider @pay_to_school @sasai
    Scenario: School payment with EcoCash provider
        Given I have valid user authentication
        And I have instrument token from payment options
        And I have school payment details with provider "ecocash"
        And I have biller details with school code "054329"
        And I have payment amount 2.0
        When I send school payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response should contain payment confirmation

    @school_payment @channel @pay_to_school @sasai
    Scenario: School payment with Sasai super app channel
        Given I have valid user authentication
        And I have instrument token from payment options
        And I have school payment details with channel "sasai-super-app"
        And I have biller details with school code "054329"
        And I have payment amount 2.0
        When I send school payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response should contain payment confirmation

    @school_payment @subtype @pay_to_school @sasai
    Scenario: School payment with pay-to-school subtype
        Given I have valid user authentication
        And I have instrument token from payment options
        And I have school payment details with subtype "pay-to-school"
        And I have biller details with school code "054329"
        And I have payment amount 2.0
        When I send school payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response should contain payment confirmation

    @school_payment @idempotency @pay_to_school @sasai
    Scenario: School payment idempotency check
        Given I have valid user authentication
        And I have instrument token from payment options
        And I have school payment details with unique request ID
        And I have biller details with school code "054329"
        And I have payment amount 2.0
        When I send school payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And I store the transaction reference
        When I send the same school payment request again
        Then response status code should be 200 or 409

    @school_payment @receipt @pay_to_school @sasai
    Scenario: School payment generates receipt data
        Given I have valid user authentication
        And I have instrument token from payment options
        And I have school payment details
        And I have biller details with school code "054329"
        And I have payment amount 2.0
        When I send school payment request to "/bff/v2/order/utility/payment"
        Then response status code should be 200
        And response should have receipt information
