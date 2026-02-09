Feature: Complete P2P Payment Flow with Dynamic Tokens
    As a user
    I want to execute the complete P2P payment flow
    So that I can transfer money with automatically extracted fresh tokens

    # This feature demonstrates the FULLY DYNAMIC P2P payment flow:
    # 1. Account Lookup → Extracts beneficiary instrument token automatically
    # 2. Payment Options → Extracts payer instrument token automatically  
    # 3. Payment Transfer → Uses fresh tokens from steps 1 & 2
    # 4. Order Details → Uses dynamic order ID from step 3
    # 
    # NO HARDCODED TOKENS - All tokens are fresh from current session!
    # This approach ensures tests are reliable and maintainable.

    Background:
        Given API is available
        And I am authenticated with valid app token
        And I have valid user token from PIN verification

    @integration @p2p_complete_flow @dynamic_tokens @sasai
    Scenario: Complete P2P flow with automatic token extraction
        Given I have valid user authentication
        And I have account number "+263789124669"
        When I send account lookup request to "/bff/v3/payment/account/lookup"
        Then response status code should be 200
        And response should contain account details
        And response should have beneficiary name
        Given I have service type "ZWPersonPaymentOptions"
        When I send P2P payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response should contain P2P payment options
        And P2P payment options should not be empty
        Given I have complete payment transfer payload
        When I send payment transfer request to "/bff/v2/order/transfer/payment"
        Then response status code should be 200 or 201
        And response body should be valid JSON
        And response should have P2P order ID
        When I send P2P order details request to "/bff/v2/order/details"
        Then response status code should be 200
        And response body should be valid JSON
        And response should contain P2P order details data
        And P2P order details should have order ID
        And P2P order details should have status
        And P2P order details should have amount

    @smoke @integration @p2p_flow @quick_test @sasai
    Scenario: Quick P2P transfer with dynamic tokens
        Given I have valid user authentication
        
        # Get beneficiary details
        And I have account number "+263789124669"
        When I send account lookup request to "/bff/v3/payment/account/lookup"
        Then response status code should be 200
        
        # Get payment options
        And I have service type "ZWPersonPaymentOptions"
        When I send P2P payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        
        # Execute transfer with fresh tokens
        And I have complete payment transfer payload
        When I send payment transfer request to "/bff/v2/order/transfer/payment"
        Then response status code should be 200 or 201
        And response should have P2P order ID

    @integration @p2p_flow @with_verification @sasai
    Scenario: P2P flow with detailed verification
        Given I have valid user authentication
        
        # Step 1: Account Lookup with verification
        And I have account number "+263789124669"
        When I send account lookup request to "/bff/v3/payment/account/lookup"
        Then response status code should be 200
        And response should contain account details
        And response should have beneficiary name
        And response should have account status
        
        # Step 2: Payment Options with verification
        And I have service type "ZWPersonPaymentOptions"
        And I have request ID "bdefac7b-bbc0-48b4-9ef0-84e6b9b34a6f"
        When I send P2P payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response should contain P2P payment options
        And P2P payment options should not be empty
        
        # Step 3: Payment Transfer with verification
        And I have complete payment transfer payload
        When I send payment transfer request to "/bff/v2/order/transfer/payment"
        Then response status code should be 200 or 201
        And response body should be valid JSON
        And response should contain P2P transaction details
        And response should have P2P order ID
        And P2P transaction status should be valid
        
        # Step 4: Order Details with verification
        When I send P2P order details request to "/bff/v2/order/details"
        Then response status code should be 200
        And response body should be valid JSON
        And response should contain P2P order details data
        And P2P order details should have order ID
        And P2P order details should have status
        And P2P order details should have amount
        And P2P order details should have complete information

    @integration @p2p_search_to_transfer @full_flow @sasai
    Scenario: Complete P2P flow from search to transfer
        Given I have valid user authentication
        
        # Step 0: Search for contact (optional but realistic)
        And I have search query "EcoCash User Five"
        And I have country code "ZW"
        And I have page number 1
        And I have page count 20
        When I send contact search request to "/search/v3/collection/search"
        Then response status code should be 200
        And response should contain search results
        
        # Step 1: Account Lookup
        And I have account number "+263789124669"
        When I send account lookup request to "/bff/v3/payment/account/lookup"
        Then response status code should be 200
        And response should contain account details
        
        # Step 2: Payment Options
        And I have service type "ZWPersonPaymentOptions"
        When I send P2P payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        And response should contain P2P payment options
        
        # Step 3: Payment Transfer
        And I have complete payment transfer payload
        When I send payment transfer request to "/bff/v2/order/transfer/payment"
        Then response status code should be 200 or 201
        And response should have P2P order ID
        
        # Step 4: Order Details
        When I send P2P order details request to "/bff/v2/order/details"
        Then response status code should be 200
        And P2P order details should have order ID

    @integration @negative @p2p_flow @error_handling @sasai
    Scenario: P2P flow without account lookup (missing beneficiary token)
        Given I have valid user authentication
        
        # Skip account lookup - no beneficiary token extracted
        # Get payment options only
        And I have service type "ZWPersonPaymentOptions"
        When I send P2P payment options request to "/bff/v2/payment/options"
        Then response status code should be 200
        
        # Try to execute transfer - should fail with config token
        And I have complete payment transfer payload
        When I send payment transfer request to "/bff/v2/order/transfer/payment"
        # Will use fallback config token which may be expired
        # This demonstrates why dynamic tokens are important!
