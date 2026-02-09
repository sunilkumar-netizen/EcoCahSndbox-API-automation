# Quick Reference: Dynamic Order ID in Smoke Tests

## 🎯 Problem Solved

**Question:** "How do you handle dynamic order ID in smoke test?"

**Answer:** We now have **TWO smoke test approaches**:

---

## Option 1: Static Smoke Test (Fast) ⚡

```gherkin
@smoke @static
Scenario: Get order details with valid order ID (Static)
    Given I have valid user authentication
    And I have order ID "177036-4133-153222"  # ← Hardcoded
    When I send P2P order details request to "/bff/v2/order/details"
    Then response status code should be 200
```

**Run it:**
```bash
behave --tags=@static features/Pay_to_Person\(Domestic\)/5_orderDetails.feature
```

**Pros:** Fast (~1s), simple, good for CI/CD
**Cons:** Order ID might expire, needs manual updates

---

## Option 2: Dynamic Smoke Test (Realistic) ✅

```gherkin
@smoke @dynamic
Scenario: Get order details with dynamic order ID (Dynamic Smoke Test)
    Given I have valid user authentication
    # Get fresh order ID from payment transfer
    And I have complete payment transfer payload
    When I send payment transfer request to "/bff/v2/order/transfer/payment"
    Then response should have P2P order ID  # ← Extracts & stores order ID
    # Use dynamic order ID
    When I send P2P order details request to "/bff/v2/order/details"
    Then response status code should be 200
```

**Run it:**
```bash
behave --tags=@dynamic features/Pay_to_Person\(Domestic\)/5_orderDetails.feature
```

**Pros:** Always valid, no maintenance, tests complete flow
**Cons:** Slower (~3-5s), depends on payment transfer API

---

## How Dynamic Order ID Works

```
Payment Transfer API
     ↓
Response: { "orderId": "ABC-123" }
     ↓
context.order_id = "ABC-123"  ← Stored automatically
     ↓
Order Details API uses context.order_id
     ↓
GET /bff/v2/order/details/ABC-123  ← Dynamic!
```

---

## Quick Commands

```bash
# Run static smoke test (fast)
behave --tags=@static

# Run dynamic smoke test (realistic)
behave --tags=@dynamic

# Run both smoke tests
behave --tags=@smoke

# Run specific line
behave features/Pay_to_Person\(Domestic\)/5_orderDetails.feature:39
```

---

## When to Use Each

| Scenario | Use This |
|----------|----------|
| Quick CI/CD check | @static |
| Pre-release validation | @dynamic |
| Order ID keeps expiring | @dynamic |
| Testing API availability only | @static |
| Testing complete flow | @dynamic |
| Speed is critical | @static |
| Realism is critical | @dynamic |

---

## Test Suite Summary

```
P2P Order Details API - 38 Scenarios
├─ 2 Smoke Tests
│  ├─ Static Smoke Test (@static) - Line 26
│  └─ Dynamic Smoke Test (@dynamic) - Line 39
├─ 3 Positive Tests
├─ 1 Integration Test (@integration)
├─ 9 Negative Tests
├─ 4 Validation Tests
├─ 1 Headers Test
├─ 3 Security Tests
├─ 3 Error Handling Tests
├─ 2 Performance Tests
├─ 1 Data Validation Test
├─ 2 Status Verification Tests
├─ 2 Scenario Outlines (7 examples total)
```

**Total Steps:** 317 steps (all properly defined ✅)

---

## Key Benefit

🎉 **You can now choose the right testing approach for your needs!**

- Need **speed**? Use `@static`
- Need **reliability**? Use `@dynamic`
- Need **both**? Use `@smoke`

No more stale order IDs breaking your smoke tests! 🚀
