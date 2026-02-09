# Smoke Test Approaches for P2P Order Details API

## Overview

The P2P Order Details API now has **TWO smoke test scenarios** to handle different testing needs:

1. **Static Smoke Test** - Uses hardcoded order ID (fast, simple)
2. **Dynamic Smoke Test** - Uses order ID from payment transfer (realistic, always valid)

## 🎯 Two Smoke Test Approaches

### Approach 1: Static Order ID (Quick Testing)

```gherkin
@smoke @p2p_order_details @order_details @p2p @sasai @static
Scenario: Get order details with valid order ID (Static)
    Given I have valid user authentication
    And I have order ID "177036-4133-153222"  # ← Hardcoded order ID
    When I send P2P order details request to "/bff/v2/order/details"
    Then response status code should be 200
    And response body should be valid JSON
    And response should contain P2P order details data
```

**When to Use:**
- ✅ Quick smoke testing
- ✅ CI/CD pipeline (fast execution)
- ✅ When you have a known valid order ID
- ✅ Testing API availability and basic response structure

**Limitations:**
- ⚠️ Order ID might become stale/invalid over time
- ⚠️ Doesn't test the complete payment flow
- ⚠️ Requires manual update if order ID expires

**Running It:**
```bash
# Run static smoke test only
behave features/Pay_to_Person\(Domestic\)/5_orderDetails.feature --tags=@static

# Or by line number
behave features/Pay_to_Person\(Domestic\)/5_orderDetails.feature:26 --no-capture
```

---

### Approach 2: Dynamic Order ID (Realistic Testing)

```gherkin
@smoke @p2p_order_details @order_details @p2p @sasai @dynamic
Scenario: Get order details with dynamic order ID (Dynamic Smoke Test)
    Given I have valid user authentication
    # Execute payment transfer to get real order ID
    And I have complete payment transfer payload
    When I send payment transfer request to "/bff/v2/order/transfer/payment"
    Then response status code should be 200 or 201
    And response should have P2P order ID  # ← Extracts order ID dynamically
    # Now get order details with dynamic order ID
    When I send P2P order details request to "/bff/v2/order/details"
    Then response status code should be 200
    And response body should be valid JSON
    And response should contain P2P order details data
```

**When to Use:**
- ✅ Realistic end-to-end smoke testing
- ✅ When order IDs expire quickly
- ✅ Testing the complete payment → details flow
- ✅ Ensuring integration between APIs works

**Benefits:**
- ✅ Always uses valid, fresh order IDs
- ✅ Tests the actual user flow
- ✅ No maintenance needed for order IDs
- ✅ Catches integration issues early

**Limitations:**
- ⚠️ Takes longer (executes payment transfer first)
- ⚠️ Requires valid payment credentials
- ⚠️ Depends on payment transfer API availability

**Running It:**
```bash
# Run dynamic smoke test only
behave features/Pay_to_Person\(Domestic\)/5_orderDetails.feature --tags=@dynamic

# Or by line number
behave features/Pay_to_Person\(Domestic\)/5_orderDetails.feature:39 --no-capture
```

---

## 📊 Comparison Table

| Feature | Static Smoke Test | Dynamic Smoke Test |
|---------|------------------|-------------------|
| **Speed** | ⚡ Fast (~1-2s) | 🐢 Slower (~3-5s) |
| **Maintenance** | 🔧 Requires updating order IDs | ✅ No maintenance |
| **Reliability** | ⚠️ Can break if order ID expires | ✅ Always valid |
| **Realism** | 📝 Tests API only | ✅ Tests complete flow |
| **Dependencies** | 🎯 None (standalone) | 🔗 Requires Payment Transfer API |
| **Use Case** | Quick CI/CD checks | End-to-end validation |

---

## 🎯 How Dynamic Order ID Works in Smoke Test

### Step-by-Step Flow

```
┌───────────────────────────────────────────────────────────┐
│  DYNAMIC SMOKE TEST FLOW                                  │
└───────────────────────────────────────────────────────────┘

Step 1: Execute Payment Transfer
├─ POST /bff/v2/order/transfer/payment
├─ Response: { "orderId": "NEW-ORDER-123" }
└─ Store: context.order_id = "NEW-ORDER-123"  ← DYNAMIC!

Step 2: Get Order Details (Same Test)
├─ GET /bff/v2/order/details/{context.order_id}
├─ GET /bff/v2/order/details/NEW-ORDER-123
└─ Response: { "orderId": "NEW-ORDER-123", "status": "success" }

✓ Complete flow tested in ONE smoke test!
```

### Code Behind the Scenes

```python
# Step 1: Payment Transfer extracts order ID
@then('response should have P2P order ID')
def step_response_has_order_id(context):
    response_data = context.response.json()
    order_id = response_data.get('orderId')
    context.order_id = order_id  # ← Store for next step
    logger.info(f"✓ Extracted order ID: {order_id}")

# Step 2: Order Details uses the stored order ID
@when('I send P2P order details request to "{endpoint}"')
def step_send_order_details_request(context, endpoint):
    order_id = context.order_id  # ← Retrieve stored order ID
    full_endpoint = f"{endpoint}/{order_id}"
    # GET /bff/v2/order/details/NEW-ORDER-123
    response = context.base_test.api_client.get(full_endpoint)
```

---

## 🚀 Running Different Smoke Test Combinations

### Run Both Smoke Tests
```bash
# Run all smoke tests (static + dynamic)
behave features/Pay_to_Person\(Domestic\)/5_orderDetails.feature --tags=@smoke
```

### Run Only Static Smoke Test
```bash
# Fast execution for CI/CD
behave features/Pay_to_Person\(Domestic\)/5_orderDetails.feature --tags=@static
```

### Run Only Dynamic Smoke Test
```bash
# Realistic end-to-end validation
behave features/Pay_to_Person\(Domestic\)/5_orderDetails.feature --tags=@dynamic
```

### Run All P2P Order Details Tests
```bash
# Full suite (38 scenarios)
behave features/Pay_to_Person\(Domestic\)/5_orderDetails.feature
```

---

## 💡 Best Practices

### For CI/CD Pipelines

**Strategy 1: Fast First, Thorough Later**
```yaml
# Fast smoke test in pre-commit
- name: Quick Smoke Test
  run: behave --tags=@static

# Thorough smoke test in nightly builds
- name: Full Smoke Test
  run: behave --tags=@smoke
```

**Strategy 2: Parallel Execution**
```bash
# Run both in parallel for speed + coverage
behave --tags=@static & behave --tags=@dynamic &
wait
```

### For Manual Testing

**Quick Check:**
```bash
# Use static when you just want to verify API is up
behave --tags=@static
```

**Thorough Validation:**
```bash
# Use dynamic when you want to test the complete flow
behave --tags=@dynamic
```

---

## 🔍 Troubleshooting

### Static Smoke Test Fails: 404 Not Found

**Problem:** Order ID "177036-4133-153222" no longer exists

**Solution 1:** Update the order ID in the feature file
```gherkin
And I have order ID "NEW-VALID-ORDER-ID"  # ← Update here
```

**Solution 2:** Use dynamic smoke test instead
```bash
behave --tags=@dynamic  # Always uses fresh order ID
```

### Dynamic Smoke Test Fails: Payment Transfer Error

**Problem:** Payment transfer returns 400/401

**Solution:** Check authentication and payload
```gherkin
# Ensure valid user token
And I have valid user token from PIN verification

# Ensure valid payment payload
And I have complete payment transfer payload
```

---

## 📈 Test Execution Times

### Static Smoke Test
```
Scenario: Get order details with valid order ID (Static)
  Runtime: ~1.2 seconds
  API Calls: 1 (Order Details only)
  Status: ✓ PASSED
```

### Dynamic Smoke Test
```
Scenario: Get order details with dynamic order ID (Dynamic Smoke Test)
  Runtime: ~3.5 seconds
  API Calls: 2 (Payment Transfer + Order Details)
  Status: ✓ PASSED
```

**Recommendation:**
- Use **static** for quick CI/CD checks (1-2s)
- Use **dynamic** for thorough validation (3-5s)
- Use **both** for comprehensive smoke testing

---

## 📋 Summary

### Static Smoke Test (@static)
```
✅ Fast execution (~1-2s)
✅ Simple, no dependencies
✅ Good for CI/CD
⚠️ Requires order ID maintenance
⚠️ Can become stale
```

**Best for:** Quick availability checks, fast CI/CD pipelines

### Dynamic Smoke Test (@dynamic)
```
✅ Always valid order IDs
✅ Tests complete flow
✅ No maintenance needed
✅ Realistic testing
⚠️ Slower execution (~3-5s)
⚠️ Depends on payment transfer
```

**Best for:** End-to-end validation, thorough smoke testing

### Integration Test (@integration)
```
✅ Complete workflow validation
✅ Validates order ID consistency
✅ Tests all API interactions
⚠️ Longest execution time
```

**Best for:** Full integration testing, release validation

---

## 🎯 Recommended Usage

**Daily CI/CD:**
```bash
behave --tags=@static  # Quick check
```

**Pre-Release:**
```bash
behave --tags=@dynamic  # Thorough check
```

**Full Regression:**
```bash
behave --tags=@smoke  # Both static + dynamic
```

**Integration Testing:**
```bash
behave --tags=@integration  # Complete flow
```

---

## 🔗 Related Files

- **Feature File:** `features/Pay_to_Person(Domestic)/5_orderDetails.feature`
- **Step Definitions:** `steps/p2p_order_details_steps.py`
- **Payment Transfer Steps:** `steps/p2p_payment_transfer_steps.py`
- **Documentation:** `docs/P2P_ORDER_DETAILS_DYNAMIC_FLOW.md`

Now you have **maximum flexibility** with THREE testing approaches:
1. **@static** - Fast static order ID
2. **@dynamic** - Dynamic smoke test
3. **@integration** - Full workflow validation

Choose the right approach for your testing needs! 🎉
