# P2P Order Details API - Dynamic Order ID Flow

## Overview
The Order Details API uses a **dynamic order ID** retrieved from the Payment Transfer API response. This ensures that you're always querying the most recent transaction.

## Complete P2P Payment Flow with Dynamic Order ID

```
┌─────────────────────────────────────────────────────────────────┐
│                    P2P PAYMENT WORKFLOW                          │
└─────────────────────────────────────────────────────────────────┘

1. Search Contact API (GET)
   ↓ Extract: contact details
   
2. Account Lookup API (POST)
   ↓ Extract: beneficiary account info
   
3. Payment Options API (GET)
   ↓ Extract: payment instruments
   
4. Payment Transfer API (POST)  ← Execute actual payment
   ↓ Response: { "orderId": "177036-4133-153222", ... }
   ↓ Store in: context.order_id (AUTOMATIC)
   
5. Order Details API (GET) ← Query with dynamic order ID
   ↓ URL: /bff/v2/order/details/{context.order_id}
   ↓ Response: Complete transaction details
```

## How Dynamic Order ID Works

### Step 1: Payment Transfer Executes
```gherkin
When I send payment transfer request to "/bff/v2/order/transfer/payment"
Then response status code should be 200 or 201
And response should have P2P order ID  # ← This step extracts & stores order ID
```

**What happens behind the scenes:**
```python
# In p2p_payment_transfer_steps.py
@then('response should have P2P order ID')
def step_response_has_order_id(context):
    response_data = context.response.json()
    
    # Extract order ID from response
    order_id = response_data.get('orderId') or response_data.get('id')
    
    # Store in context for next API call
    context.order_id = order_id  # ← STORED HERE
    
    logger.info(f"✓ Order ID found: {order_id}")
```

### Step 2: Order Details Uses Dynamic Order ID
```gherkin
When I send P2P order details request to "/bff/v2/order/details"
Then response status code should be 200
And order ID in details should match transfer order ID
```

**What happens behind the scenes:**
```python
# In p2p_order_details_steps.py
@when('I send P2P order details request to "{endpoint}"')
def step_send_order_details_request(context, endpoint):
    # Retrieve dynamic order ID from context
    order_id = getattr(context, 'order_id', None)  # ← RETRIEVED HERE
    
    # Build URL with dynamic order ID
    if order_id:
        full_endpoint = f"{endpoint}/{order_id}"
        # Result: /bff/v2/order/details/177036-4133-153222
    
    # Send GET request
    response = context.base_test.api_client.get(full_endpoint, headers=headers)
```

## Integration Test Example

```gherkin
@p2p_order_details @integration @order_details @p2p @sasai
Scenario: Complete P2P flow - Transfer then get order details
    Given I have valid user authentication
    
    # Step 1: Execute payment transfer
    And I have complete payment transfer payload
    When I send payment transfer request to "/bff/v2/order/transfer/payment"
    Then response status code should be 200 or 201
    And response should have P2P order ID          # ← Extracts: context.order_id = "177036-4133-153222"
    And order ID should not be empty
    
    # Step 2: Get order details using dynamic order ID from transfer
    When I send P2P order details request to "/bff/v2/order/details"  # ← Uses: context.order_id
    Then response status code should be 200
    And response should contain P2P order details data
    And order ID in details should match transfer order ID
```

## Benefits of Dynamic Order ID

✅ **Always Current**: Uses the actual order ID from the latest transaction
✅ **No Hardcoding**: No need to manually update order IDs in test data
✅ **Real Integration**: Tests the actual flow as users experience it
✅ **Automatic Validation**: Ensures order ID consistency between APIs
✅ **Production-Ready**: All tests use real order IDs from payment transfers

## API Request Example

### Payment Transfer Response (Step 4)
```json
{
  "orderId": "177036-4133-153222",
  "status": "success",
  "transactionId": "TXN123456",
  "amount": 2,
  "currency": "ZWG"
}
```

### Order Details Request (Step 5)
```http
GET /bff/v2/order/details/177036-4133-153222
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Order Details Response (Step 5)
```json
{
  "orderId": "177036-4133-153222",
  "status": "completed",
  "amount": 2,
  "currency": "ZWG",
  "beneficiary": {
    "name": "Ropafadzo Nyagwaya",
    "mobileNumber": "+263789124669"
  },
  "createdAt": "2026-02-06T10:30:00Z",
  "completedAt": "2026-02-06T10:30:02Z"
}
```

## Context Flow Diagram

```
┌──────────────────────────────────────────────────────────┐
│                    CONTEXT OBJECT                         │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  After Payment Transfer:                                 │
│  ┌─────────────────────────────────────────────┐        │
│  │ context.order_id = "177036-4133-153222"     │        │
│  │ context.response = <payment transfer resp>  │        │
│  │ context.user_token = "Bearer eyJ..."         │        │
│  └─────────────────────────────────────────────┘        │
│                      ↓                                    │
│  Order Details Request automatically uses:               │
│  GET /bff/v2/order/details/{context.order_id}           │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

## Running the Dynamic Flow Test

```bash
# Run the smoke test with dynamic order ID
behave features/Pay_to_Person\(Domestic\)/5_orderDetails.feature:26 --no-capture

# Or run with tag
behave --tags=@smoke features/Pay_to_Person\(Domestic\)/5_orderDetails.feature --no-capture

# Run the integration test with dynamic order ID
behave features/Pay_to_Person\(Domestic\)/5_orderDetails.feature:77 --no-capture

# Or run with tag
behave --tags=@integration features/Pay_to_Person\(Domestic\)/5_orderDetails.feature --no-capture
```

## Expected Test Output

```
Scenario: Get order details with dynamic order ID (Smoke Test)
  Given I have valid user authentication ... passed
  And I have complete payment transfer payload ... passed
  When I send payment transfer request to "/bff/v2/order/transfer/payment" ... passed
  Then response status code should be 200 or 201 ... passed
  And response should have P2P order ID ... passed
    ✓ Order ID found: 177036-4133-153222
  When I send P2P order details request to "/bff/v2/order/details" ... passed
    Sending GET request to: https://sandbox.../bff/v2/order/details/177036-4133-153222
  Then response status code should be 200 ... passed
  And response body should be valid JSON ... passed
  And response should contain P2P order details data ... passed
  And P2P order details should have order ID ... passed
  And P2P order details should have status ... passed
  And P2P order details should have amount ... passed

1 scenario passed, 0 failed, 0 skipped
```

## Static vs Dynamic Order ID

### ❌ Static Order ID (Removed)
```gherkin
Given I have order ID "177036-4133-153222"  # ← Hardcoded - can become stale
```
- **Problem**: Order IDs become invalid over time
- **Issue**: Not realistic for integration testing
- **Status**: Removed in favor of dynamic approach

### ✅ Dynamic Order ID (Current Implementation)
```gherkin
When I send payment transfer request to "/bff/v2/order/transfer/payment"
Then response should have P2P order ID  # ← Extracts from response
When I send P2P order details request to "/bff/v2/order/details"  # ← Uses extracted ID
```
- **Use case**: Real-world integration testing
- **Benefit**: Always uses valid, current order IDs

## Troubleshooting

### Error: "Transfer order ID not found in context"
**Cause**: Payment Transfer step didn't execute or failed to extract order ID

**Solution**: Ensure the Payment Transfer API executes successfully first:
```gherkin
When I send payment transfer request to "/bff/v2/order/transfer/payment"
Then response status code should be 200 or 201
And response should have P2P order ID  # ← This must pass
```

### Error: "Order ID mismatch"
**Cause**: Different order IDs in transfer response vs details response

**Solution**: Check response data extraction logic - both APIs might use different field names
- Transfer: `orderId`, `id`, `transactionId`
- Details: Same fields but verify API documentation

## Summary

The P2P Order Details API implementation uses a **smart dynamic order ID system** that:

1. ✅ Automatically extracts order ID from Payment Transfer response
2. ✅ Stores it in `context.order_id` for subsequent API calls
3. ✅ Uses the dynamic order ID in Order Details API request
4. ✅ Validates that both APIs return the same order ID
5. ✅ Provides both static (smoke tests) and dynamic (integration tests) approaches

This approach ensures **realistic, end-to-end testing** of the complete P2P payment workflow! 🎉
