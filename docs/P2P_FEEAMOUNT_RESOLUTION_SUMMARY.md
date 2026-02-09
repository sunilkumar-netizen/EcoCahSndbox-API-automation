# P2P Flow - feeAmount Issue Resolution Summary

## 🎯 Current Status

**Date:** 2026-02-09  
**Status:** ❌ BLOCKED - Payment Transfer API rejects requests despite correct `feeAmount: 0`

### Test Results Summary

| API | Status | Notes |
|-----|--------|-------|
| 1. Search Contact | ✅ PASS | Works perfectly (6 contacts found) |
| 2. Account Lookup | ✅ PASS | Returns beneficiary details correctly |
| 3. Payment Options | ✅ PASS | Returns payment options successfully |
| 4. Payment Transfer | ❌ FAIL | Rejects with `"feeAmount" is required"` |
| 5. Order Details | ❌ FAIL | Blocked by Payment Transfer failure |

## 🔍 Investigation Results

### What We Tried

1. **feeAmount: 0** ❌ - API rejected
   ```json
   {"feeAmount": 0}  // Integer zero
   ```

2. **feeAmount: 0.5** ❌ - API rejected
   ```json
   {"feeAmount": 0.5}  // Float
   ```

3. **feeAmount: 1** ❌ - API rejected
   ```json
   {"feeAmount": 1}  // Integer one
   ```

### Current Configuration

**config/qa.yaml:**
```yaml
p2p_payment_transfer:
  fee_amount: 0  # As confirmed working in Postman
  currency: "ZWG"
  payer_amount: 2
  payee_amount: 2
```

**steps/p2p_payment_transfer_steps.py:**
```python
fee_amount = config.get('p2p_payment_transfer.fee_amount', 0)  # Loads 0
payload = {
    "feeAmount": fee_amount,  # Sends: "feeAmount": 0
    ...
}
```

### Actual Payload Sent

```json
{
  "feeAmount": 0,  ← FIELD IS PRESENT!
  "currency": "ZWG",
  "payerAmount": 2,
  "beneficiaryDetails": {
    "payeeAmount": 2,
    "paymentMethod": "wallet",
    "instrumentId": "9f894ed8-9116-496b-8599-526cc114b566",
    "beneficiaryInstrumentToken": "c6b5de1b-63e4-46c4-a899-67f4427d5f5f",
    "name": "Ropafadzo Nyagwaya",
    "provider": "ecocash",
    "customerId": "f044ff8d-abe6-47aa-8837-ec329e8a0edc"
  },
  "payerDetails": {
    "instrumentToken": "9d753911-b338-4005-8776-4b0a0feae8dd",
    "paymentMethod": "wallet",
    "provider": "ecocash",
    "pin": "ZXodNbU...",  ← LIKELY EXPIRED/INVALID!
    "publicKeyAlias": "payment-links"
  },
  "deviceInfo": { ... },
  "notes": { ... },
  "subType": "p2p-pay",
  "channel": "sasai-super-app"
}
```

### API Response

```json
{
  "errorCode": "http.bad.request",
  "errors": [{
    "message": "\"feeAmount\" is required",
    "code": "feeAmount"
  }]
}
```

## 💡 Critical Discovery

**User confirmed:** `feeAmount: 0` works in Postman! ✅

This means:
- ✅ `feeAmount: 0` is the CORRECT value
- ❌ The issue is NOT with feeAmount itself
- ❌ The issue is with OTHER fields in the payload

## 🔴 Root Cause Analysis

### Theory: Misleading Error Message

The API error `"feeAmount" is required"` is **likely misleading**. The actual problem is probably:

1. **Expired Encrypted PIN** 🔴
   - Hardcoded PIN: `"ZXodNbU..."`
   - PINs are session-specific and expire quickly
   - Invalid PIN → API fails validation → Returns generic "feeAmount required" error

2. **Invalid Instrument Tokens** 🔴
   - Payer token: `"9d753911-b338-4005-8776-4b0a0feae8dd"`
   - Beneficiary token: `"c6b5de1b-63e4-46c4-a899-67f4427d5f5f"`
   - These are user/session-specific and dynamic
   - Invalid tokens → API fails validation → Returns generic error

3. **Invalid Customer IDs** 🔴
   - Customer ID: `"f044ff8d-abe6-47aa-8837-ec329e8a0edc"`
   - Must match the authenticated user
   - Wrong customer ID → API fails validation → Generic error

### Why This Happens

Many APIs return **generic validation errors** when they encounter authentication/authorization failures for security reasons. Instead of revealing "Invalid PIN" or "Expired token", they return "Required field missing" to prevent information leakage.

## 📋 Comparison Needed

To resolve this, we need to compare the **working Postman request** with the **failing automated test request**:

### Required Information from Postman

1. **Complete JSON Payload** (exact copy)
   ```json
   {
     "feeAmount": 0,  ← Confirm this value
     "currency": "?",
     "beneficiaryDetails": {
       "instrumentId": "?",  ← Is this different?
       "beneficiaryInstrumentToken": "?",  ← Is this different?
       "customerId": "?"  ← Is this different?
     },
     "payerDetails": {
       "instrumentToken": "?",  ← Is this different?
       "pin": "?"  ← Is this different? (CRITICAL!)
     }
     // ... rest of payload
   }
   ```

2. **All Headers**
   ```
   Content-Type: application/json
   Authorization: Bearer <token>  ← Which token? User token?
   X-Request-ID: ?
   ... any other headers?
   ```

3. **Token Information**
   - Where did you get the Bearer token in Postman?
   - Is it the user token from PIN verification?
   - How recent is it? (tokens expire!)

4. **Dynamic Values**
   - Are instrument IDs/tokens fresh from Account Lookup API?
   - Is encrypted PIN fresh from current session?
   - Are customer IDs from current authenticated user?

## ✅ Next Steps

### Immediate Actions

1. **Get Working Postman Request**
   - Export the working Postman request as JSON
   - Share the complete payload (mask sensitive data if needed)
   - Note which values are hardcoded vs dynamic

2. **Compare Payloads**
   - Line-by-line comparison
   - Identify differences in:
     - Field names (camelCase vs snake_case?)
     - Field values (especially tokens, IDs, PINs)
     - Field order (probably not important but worth checking)
     - Field types (string vs number?)

3. **Update Test Data**
   - Replace hardcoded values with fresh values from Postman
   - Or better: make values dynamic from previous API calls

### Long-term Solution

**Create Complete Dynamic Flow:**

```gherkin
@smoke @p2p @complete_flow
Scenario: Complete P2P Payment Flow (Fully Dynamic)
    # Step 1: Authentication
    Given I am authenticated with valid app token
    And I have valid user token from PIN verification
    
    # Step 2: Search for beneficiary
    And I have search query "+263789124669"
    When I send contact search request
    Then I extract first contact
    
    # Step 3: Account Lookup
    When I send account lookup for extracted contact
    Then I extract beneficiary details:
        - instrumentId
        - beneficiaryInstrumentToken
        - customerId
        - beneficiaryName
    
    # Step 4: Payment Options
    When I send payment options request
    Then I extract payment provider details:
        - providerCode
        - paymentMethod
    
    # Step 5: Get Fresh Encrypted PIN
    When I encrypt PIN with current session key
    Then I have fresh encrypted PIN
    
    # Step 6: Build Dynamic Payload
    When I build payment transfer payload with:
        - feeAmount: 0 (from config)
        - Extracted beneficiary details
        - Fresh encrypted PIN
        - Current user's instrument token
        - Current session device info
    
    # Step 7: Execute Payment Transfer
    When I send payment transfer request
    Then response status code should be 200 or 201
    And I extract order ID
    
    # Step 8: Get Order Details
    When I send order details request with extracted order ID
    Then response status code should be 200
    And order details match transfer details
```

## 📊 Test Coverage Status

```
✅ Working APIs (60%):
├─ Search Contact       ✅ 41 scenarios (100% passing in smoke test)
├─ Account Lookup       ✅ 37 scenarios (100% passing in smoke test)
└─ Payment Options      ✅ 32 scenarios (100% passing in smoke test)

❌ Blocked APIs (40%):
├─ Payment Transfer     ❌ 44 scenarios (blocked by validation)
└─ Order Details        ❌ 37 scenarios (dependent on Payment Transfer)

Total: 191 scenarios, ~1,636 lines of BDD
```

## 🎯 Success Criteria

Payment Transfer will be considered **fixed** when:
1. ✅ Payload contains `feeAmount: 0`
2. ✅ API accepts the request (status 200/201)
3. ✅ Response contains order ID
4. ✅ Order Details API can retrieve the transaction

## 📝 Notes

- All earlier steps (Search, Lookup, Payment Options) work perfectly
- The test infrastructure is solid and comprehensive
- The issue is specifically with Payment Transfer validation
- User confirmed `feeAmount: 0` works in Postman
- Need to identify what's different between Postman and automated tests

---

**Action Required:** Please share the working Postman request details so we can identify the difference!
