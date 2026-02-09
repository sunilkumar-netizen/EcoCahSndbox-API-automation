Feature: P2P Payment Transfer API
    As a user
    I want to transfer money to another person
    So that I can send payments through the P2P payment system

    # NOTE: Payment Transfer API requires user token (accessToken) from PIN Verify API
    # Endpoint: POST /bff/v2/order/transfer/payment
    # Request Body: Complex JSON with beneficiary details, payer details, device info, etc.
    # Response: Returns transaction details including order ID, status, etc.
    # This API executes the actual money transfer after search, lookup, and payment options selection
    # This is the final step in the P2P payment flow

    Background:
        Given API is available
        And I am authenticated with valid app token
        And I have valid user token from PIN verification

    @smoke @p2p_transfer @payment_transfer @p2p @sasai
    Scenario: Execute P2P payment transfer with valid details
        Given I have valid user authentication
        And I have account number "+263789124669"
        When I send account lookup request to "/bff/v3/payment/account/lookup"
        Then response status code should be 200
        Given I have service type "ZWPersonPaymentOptions"
        When I send P2P payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        Given I have payment transfer details:
            | field                  | value                                    |
            | feeAmount              | 0.5                                      |
            | currency               | ZWG                                      |
            | payerAmount            | 3                                        |
            | payeeAmount            | 3                                        |
            | paymentMethod          | wallet                                   |
            | provider               | ecocash                                  |
            | beneficiaryName        | Ropafadzo Nyagwaya                       |
            | beneficiaryMobile      | +263789124669                            |
            | message                | P2P Test Transaction                     |
            | subType                | p2p-pay                                  |
            | channel                | sasai-super-app                          |
        When I send payment transfer request to "/bff/v2/order/transfer/payment"
        Then response status code should be 200 or 201
        And response body should be valid JSON
        And response should contain P2P transaction details
        And response should have P2P order ID
        And P2P transaction status should be valid

    @p2p_transfer @positive @payment_transfer @p2p @sasai
    Scenario: Transfer payment and verify response structure
        Given I have valid user authentication
        And I have complete payment transfer payload
        When I send payment transfer request to "/bff/v2/order/transfer/payment"
        Then response status code should be 200 or 201
        And response should have complete P2P transaction details
        And response should have P2P transaction ID
        And response should have P2P transaction timestamp

    @p2p_transfer @positive @payment_transfer @p2p @sasai
    Scenario: Transfer payment with minimum amount
        Given I have valid user authentication
        And I have payment transfer with amount 1 ZWG
        When I send payment transfer request to "/bff/v2/order/transfer/payment"
        Then response status code should be 200 or 201
        And response should contain P2P transaction details

    @p2p_transfer @positive @payment_transfer @p2p @sasai
    Scenario: Transfer payment with custom message
        Given I have valid user authentication
        And I have payment transfer with message "Birthday gift for friend"
        When I send payment transfer request to "/bff/v2/order/transfer/payment"
        Then response status code should be 200 or 201
        And response should contain P2P transaction details

    @p2p_transfer @integration @payment_transfer @p2p @sasai
    Scenario: Complete P2P flow - Search, Lookup, Options, Transfer
        Given I have valid user authentication
        # Step 1: Search for contact
        And I have search query "EcoCash User Five"
        And I have country code "ZW"
        And I have page number 1
        And I have page count 20
        When I send contact search request to "/search/v3/collection/search"
        Then response status code should be 200
        And I extract first contact from search results
        # Step 2: Lookup beneficiary account
        Given I have account number from extracted contact
        When I send account lookup request to "/bff/v3/payment/account/lookup"
        Then response status code should be 200
        And response should contain account details
        And I extract beneficiary name from response
        # Step 3: Get payment options
        Given I have service type "ZWPersonPaymentOptions"
        When I send P2P payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response should contain P2P payment options
        And I extract first P2P payment option
        # Step 4: Execute payment transfer
        Given I have payment transfer with extracted beneficiary details
        When I send payment transfer request to "/bff/v2/order/transfer/payment"
        Then response status code should be 200 or 201
        And response should contain P2P transaction details

    @p2p_transfer @negative @payment_transfer @p2p @sasai
    Scenario: Transfer payment without authentication
        Given I have no authentication token
        And I have complete payment transfer payload
        When I send payment transfer request to "/bff/v2/order/transfer/payment"
        Then response status code should be 401

    @p2p_transfer @negative @payment_transfer @p2p @sasai
    Scenario: Transfer payment with invalid user token
        Given I have invalid user token
        And I have complete payment transfer payload
        When I send payment transfer request to "/bff/v2/order/transfer/payment"
        Then response status code should be 401

    @p2p_transfer @negative @payment_transfer @p2p @sasai
    Scenario: Transfer payment with expired user token
        Given I have expired user token
        And I have complete payment transfer payload
        When I send payment transfer request to "/bff/v2/order/transfer/payment"
        Then response status code should be 401

    @p2p_transfer @negative @payment_transfer @p2p @sasai
    Scenario: Transfer payment without beneficiary details
        Given I have valid user authentication
        And I have payment transfer without beneficiary details
        When I send payment transfer request to "/bff/v2/order/transfer/payment"
        Then response status code should be 400

    @p2p_transfer @negative @payment_transfer @p2p @sasai
    Scenario: Transfer payment without payer details
        Given I have valid user authentication
        And I have payment transfer without payer details
        When I send payment transfer request to "/bff/v2/order/transfer/payment"
        Then response status code should be 400

    @p2p_transfer @negative @payment_transfer @p2p @sasai
    Scenario: Transfer payment with zero amount
        Given I have valid user authentication
        And I have payment transfer with amount 0 ZWG
        When I send payment transfer request to "/bff/v2/order/transfer/payment"
        Then response status code should be 400

    @p2p_transfer @negative @payment_transfer @p2p @sasai
    Scenario: Transfer payment with negative amount
        Given I have valid user authentication
        And I have payment transfer with amount -10 ZWG
        When I send payment transfer request to "/bff/v2/order/transfer/payment"
        Then response status code should be 400

    @p2p_transfer @negative @payment_transfer @p2p @sasai
    Scenario: Transfer payment with invalid currency
        Given I have valid user authentication
        And I have payment transfer with currency "INVALID"
        When I send payment transfer request to "/bff/v2/order/transfer/payment"
        Then response status code should be 400

    @p2p_transfer @negative @payment_transfer @p2p @sasai
    Scenario: Transfer payment with missing payment method
        Given I have valid user authentication
        And I have payment transfer without payment method
        When I send payment transfer request to "/bff/v2/order/transfer/payment"
        Then response status code should be 400

    @p2p_transfer @negative @payment_transfer @p2p @sasai
    Scenario: Transfer payment with invalid provider
        Given I have valid user authentication
        And I have payment transfer with provider "invalid-provider"
        When I send payment transfer request to "/bff/v2/order/transfer/payment"
        Then response status code should be 400

    @p2p_transfer @negative @payment_transfer @p2p @sasai
    Scenario: Transfer payment without device info
        Given I have valid user authentication
        And I have payment transfer without device info
        When I send payment transfer request to "/bff/v2/order/transfer/payment"
        Then response status code should be 400

    @p2p_transfer @negative @payment_transfer @p2p @sasai
    Scenario: Transfer payment with missing PIN
        Given I have valid user authentication
        And I have payment transfer without PIN
        When I send payment transfer request to "/bff/v2/order/transfer/payment"
        Then response status code should be 400 or 401

    @p2p_transfer @negative @payment_transfer @p2p @sasai
    Scenario: Transfer payment with invalid PIN format
        Given I have valid user authentication
        And I have payment transfer with invalid PIN
        When I send payment transfer request to "/bff/v2/order/transfer/payment"
        Then response status code should be 400 or 401

    @p2p_transfer @validation @payment_transfer @p2p @sasai
    Scenario: Verify payment transfer response contains order ID
        Given I have valid user authentication
        And I have complete payment transfer payload
        When I send payment transfer request to "/bff/v2/order/transfer/payment"
        Then response status code should be 200 or 201
        And response should have P2P order ID
        And order ID should not be empty

    @p2p_transfer @validation @payment_transfer @p2p @sasai
    Scenario: Verify payment transfer response has transaction status
        Given I have valid user authentication
        And I have complete payment transfer payload
        When I send payment transfer request to "/bff/v2/order/transfer/payment"
        Then response status code should be 200 or 201
        And response should have P2P transaction status
        And P2P transaction status should be valid

    @p2p_transfer @validation @payment_transfer @p2p @sasai
    Scenario: Verify payment transfer amounts match request
        Given I have valid user authentication
        And I have payment transfer with amount 5 ZWG
        When I send payment transfer request to "/bff/v2/order/transfer/payment"
        Then response status code should be 200 or 201
        And P2P response transaction amount should be 5 ZWG

    @p2p_transfer @validation @payment_transfer @p2p @sasai
    Scenario: Verify beneficiary details in response
        Given I have valid user authentication
        And I have complete payment transfer payload
        When I send payment transfer request to "/bff/v2/order/transfer/payment"
        Then response status code should be 200 or 201
        And response should contain P2P beneficiary information
        And P2P beneficiary name should match request

    @p2p_transfer @headers @validation @payment_transfer @p2p @sasai
    Scenario: Verify payment transfer response headers
        Given I have valid user authentication
        And I have complete payment transfer payload
        When I send payment transfer request to "/bff/v2/order/transfer/payment"
        Then response status code should be 200 or 201
        And response header "Content-Type" should be present
        And response header "Content-Type" should contain "application/json"

    @p2p_transfer @security @payment_transfer @p2p @sasai
    Scenario: Verify transfer with missing Authorization header
        Given I have no Authorization header
        And I have complete payment transfer payload
        When I send payment transfer request to "/bff/v2/order/transfer/payment"
        Then response status code should be 401

    @p2p_transfer @security @payment_transfer @p2p @sasai
    Scenario: Verify transfer with empty Bearer token
        Given I have empty Bearer token
        And I have complete payment transfer payload
        When I send payment transfer request to "/bff/v2/order/transfer/payment"
        Then response status code should be 401

    @p2p_transfer @security @payment_transfer @p2p @sasai
    Scenario: Verify transfer with malformed Bearer token
        Given I have malformed Bearer token
        And I have complete payment transfer payload
        When I send payment transfer request to "/bff/v2/order/transfer/payment"
        Then response status code should be 401

    @p2p_transfer @security @payment_transfer @p2p @sasai
    Scenario: Verify transfer with missing Content-Type header
        Given I have valid user authentication
        And I have no Content-Type header
        And I have complete payment transfer payload
        When I send payment transfer request to "/bff/v2/order/transfer/payment"
        Then response status code should be 400 or 415

    @p2p_transfer @error_handling @payment_transfer @p2p @sasai
    Scenario: Transfer with invalid HTTP method GET
        Given I have valid user authentication
        When I send GET request to "/bff/v2/order/transfer/payment"
        Then response status code should be 405

    @p2p_transfer @error_handling @payment_transfer @p2p @sasai
    Scenario: Transfer with invalid HTTP method PUT
        Given I have valid user authentication
        When I send PUT request to "/bff/v2/order/transfer/payment"
        Then response status code should be 405

    @p2p_transfer @error_handling @payment_transfer @p2p @sasai
    Scenario: Transfer with wrong endpoint path
        Given I have valid user authentication
        And I have complete payment transfer payload
        When I send payment transfer request to "/bff/v2/order/transfer/payments"
        Then response status code should be 404

    @p2p_transfer @error_handling @payment_transfer @p2p @sasai
    Scenario: Transfer with malformed JSON body
        Given I have valid user authentication
        And I have malformed JSON body
        When I send payment transfer request to "/bff/v2/order/transfer/payment"
        Then response status code should be 400

    @p2p_transfer @performance @payment_transfer @p2p @sasai
    Scenario: Verify payment transfer response time
        Given I have valid user authentication
        And I have complete payment transfer payload
        When I send payment transfer request to "/bff/v2/order/transfer/payment"
        Then response status code should be 200 or 201
        And response time should be less than 5000 ms

    @p2p_transfer @performance @payment_transfer @p2p @sasai
    Scenario: Verify payment transfer response time is acceptable
        Given I have valid user authentication
        And I have complete payment transfer payload
        When I send payment transfer request to "/bff/v2/order/transfer/payment"
        Then response status code should be 200 or 201
        And response time should be less than 8000 ms

    @p2p_transfer @idempotency @payment_transfer @p2p @sasai
    Scenario: Verify duplicate transaction prevention
        Given I have valid user authentication
        And I have complete payment transfer payload
        When I send payment transfer request to "/bff/v2/order/transfer/payment"
        Then response status code should be 200 or 201
        And I store first P2P transfer response
        When I send same payment transfer request again
        Then response status code should be 400 or 409
        And response should indicate duplicate P2P transaction

    @p2p_transfer @amounts @payment_transfer @p2p @sasai
    Scenario Outline: Transfer payment with different amounts
        Given I have valid user authentication
        And I have payment transfer with amount <amount> ZWG
        When I send payment transfer request to "/bff/v2/order/transfer/payment"
        Then response status code should be <statusCode>

        Examples:
            | amount | statusCode      |
            | 1      | 200 or 201      |
            | 10     | 200 or 201      |
            | 100    | 200 or 201      |
            | 1000   | 200 or 201      |

    @p2p_transfer @currencies @payment_transfer @p2p @sasai
    Scenario Outline: Transfer payment with different currencies
        Given I have valid user authentication
        And I have payment transfer with currency "<currency>"
        When I send payment transfer request to "/bff/v2/order/transfer/payment"
        Then response status code should be <statusCode>

        Examples:
            | currency | statusCode      |
            | ZWG      | 200 or 201      |
            | USD      | 400             |
            | ZAR      | 400             |

    @p2p_transfer @providers @payment_transfer @p2p @sasai
    Scenario Outline: Transfer payment with different providers
        Given I have valid user authentication
        And I have payment transfer with provider "<provider>"
        When I send payment transfer request to "/bff/v2/order/transfer/payment"
        Then response status code should be <statusCode>

        Examples:
            | provider | statusCode      |
            | ecocash  | 200 or 201      |
            | onemoney | 400             |
            | telecash | 400             |
