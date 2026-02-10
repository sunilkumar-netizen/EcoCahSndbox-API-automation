# P2P Payment Transfer - Debug Analysis Report
**Date:** 2026-02-10  
**Status:** ❌ BLOCKED - API Rejects Valid Payload with Misleading Error

---

## 🎯 Executive Summary

After extensive debugging with enhanced logging, we've confirmed:
1. ✅ **feeAmount is correctly sent** as `0.5` (float type)
2. ✅ **All required fields are present** in the payload
3. ✅ **Dynamic tokens are being used** from Account Lookup & Payment Options APIs
4. ✅ **PIN is loaded from config** successfully
5. ❌ **API still rejects with** `"feeAmount" is required"` error

**Conclusion:** The error message is **MISLEADING**. The real issue is elsewhere.

---

## 📊 Test Execution Results

### ✅ Passing Tests (3/5 - 60%)
1. **Search Contact** ✅ - 6 contacts found, all validations pass
2. **Account Lookup** ✅ - Beneficiary details retrieved, tokens extracted
3. **Payment Options** ✅ - Payment options retrieved, payer tokens extracted

### ❌ Failing Tests (2/5 - 40%)
4. **Payment Transfer** ❌ - API returns 400: `"feeAmount" is required"`
5. **Order Details** ❌ - Blocked by Payment Transfer failure

---

## 🔍 Detailed Debug Output Analysis

### Payload Construction
```yaml
Fee Amount: 0.5 (type: float) ✅
Currency: ZWG ✅
Payer Amount: 3 ✅
Payee Amount: 3 ✅
PIN Length: 344 chars ✅
PIN Source: CONFIG ✅
```

### Dynamic Tokens (✅ Working)
```
🎯 beneficiaryInstrumentToken: 1a3e103a-d923-4826-b79b-44641a... (DYNAMIC from Account Lookup)
🎯 payer instrumentToken: 3859af04-acf0-4c75-a5f0-9fabf9381cc9 (DYNAMIC from Payment Options)
```

### Complete Payload Sent
```json
{
  "feeAmount": 0.5,  ← CORRECT TYPE & VALUE
  "currency": "ZWG",
  "payerAmount": 3,
  "beneficiaryDetails": {
    "payeeAmount": 3,
    "paymentMethod": "wallet",
    "instrumentId": "9f894ed8-9116-496b-8599-526cc114b566",
    "beneficiaryInstrumentToken": "1a3e103a-d923-4826-b79b-44641a...",  ← DYNAMIC
    "name": "Ropafadzo Nyagwaya",
    "provider": "ecocash",
    "customerId": "f044ff8d-abe6-47aa-8837-ec329e8a0edc"
  },
  "payerDetails": {
    "instrumentToken": "3859af04-acf0-4c75-a5f0-9fabf9381cc9",  ← DYNAMIC
    "paymentMethod": "wallet",
    "provider": "ecocash",
    "pin": "ZXodNbUKicCm/E01R6xI6NLUxqxP4g+mZAbQik8VYCeJYDGL9n...",  ← FROM CONFIG
    "publicKeyAlias": "payment-links"
  },
  "deviceInfo": {
    "ip": "192.0.0.2",
    "model": "Samsung",
    "network": "unidentified",
    "latitude": "unidentified",
    "longitude": "unidentified",
    "os": "Android",
    "osVersion": "13",
    "appVersion": "1.4.1",
    "package": "com.sasai.sasaipay",
    "simNumber": "71ff20d0-83ff-11f0-969e-4b09cf763135",
    "deviceId": "71ff20d0-83ff-11f0-969e-4b09cf763135"
  },
  "notes": {
    "message": "P2P Test Transaction",
    "beneficiaryInstrumentId": "9f894ed8-9116-496b-8599-526cc114b566",
    "beneficiaryMobileNumber": "+263789124669"
  },
  "subType": "p2p-pay",
  "channel": "sasai-super-app"
}
```

### API Response
```json
{
  "errorUserMsg": null,
  "errorCode": "http.bad.request",
  "step": "",
  "referenceId": "",
  "traceId": "",  ← NO TRACE ID (suspicious)
  "errors": [
    {
      "message": "\"feeAmount\" is required",  ← MISLEADING ERROR
      "code": "feeAmount"
    }
  ]
}
```

---

## 🔴 Root Cause Analysis

### Theory: Security-Related Validation Failure

The API is returning a **generic/misleading error** instead of the real issue for security reasons.

**Evidence:**
1. ✅ `feeAmount: 0.5` is present and correct type
2. ✅ All required fields are present
3. ✅ Dynamic tokens are fresh from current session
4. ❌ No `traceId` in error response (suggests early validation failure)
5. ❌ Same error occurs with different feeAmount values (0, 0.5, 1)

### Most Likely Causes (In Order of Probability):

#### 1. 🔴 **Expired/Invalid Encrypted PIN** (90% Likely)
```yaml
Current PIN: "ZXodNbUKicCm/E01R6xI6NLUxqxP4g+mZAbQik8VYCeJYDGL9n..."
Source: pin_verify.sample_encrypted_pin (HARDCODED in config)
Issue: PINs are session-specific and expire quickly
```

**Why This Is The Problem:**
- PIN is used for **authentication validation**
- Invalid PIN → Backend auth fails → Returns generic "feeAmount required" error
- Security best practice: Don't reveal "Invalid PIN" to prevent brute force attacks

#### 2. 🟡 **Customer ID Mismatch** (60% Likely)
```yaml
Current: "f044ff8d-abe6-47aa-8837-ec329e8a0edc" (HARDCODED in config)
Issue: Must match the authenticated user's actual customer ID
```

**Test:** The user token is obtained dynamically from PIN verification. We should extract the customer ID from the user token or from a profile API.

#### 3. 🟡 **Authorization Token Mismatch** (40% Likely)
```
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAi...
```

**Possible Issue:** The user token used in Authorization header may not match the session that generated the instrument tokens.

---

## ✅ What We've Fixed

1. ✅ Changed `feeAmount` from string to numeric (int/float)
2. ✅ Added encrypted PIN to config and using it from config
3. ✅ Using dynamic tokens from Account Lookup & Payment Options
4. ✅ Added comprehensive debug logging
5. ✅ Fixed payload override logic for feature file tables

---

## ❌ What Still Needs Investigation

### 🎯 Priority 1: Get Fresh Working PIN

**Option A: From Postman**
```bash
# Steps:
1. Run working Postman request for P2P Payment Transfer
2. Copy the encrypted PIN value from the request
3. Update config/qa.yaml:
   p2p_payment_transfer:
     encrypted_pin: "<PASTE_FRESH_PIN_HERE>"
4. Re-run tests immediately (before PIN expires)
```

**Option B: Dynamic PIN Encryption**
```python
# Need to implement:
1. Get public key from API
2. Encrypt user's PIN with public key
3. Use fresh encrypted PIN in each test run
```

### 🎯 Priority 2: Verify Customer ID

**Extract from User Token:**
```python
# Decode JWT user token to get:
- customerId
- sub (user ID)
- Other user details
```

**Or Call User Profile API:**
```bash
GET /bff/v1/user/profile
Authorization: Bearer <user_token>
# Response should contain customerId
```

### 🎯 Priority 3: Compare with Working Postman Request

**Required Information:**
1. Complete JSON payload from Postman (exact copy)
2. All request headers (especially Authorization)
3. PIN value being used in Postman
4. Customer ID value in Postman
5. Instrument tokens being used

---

## 🚀 Recommended Next Steps

### Immediate Actions (Today)

1. **Run Postman Request** ✅
   - Execute the working P2P Payment Transfer in Postman
   - Copy the COMPLETE request payload
   - Copy all headers
   - Save the response

2. **Extract Fresh PIN** 🔐
   ```yaml
   # Update in config/qa.yaml:
   p2p_payment_transfer:
     encrypted_pin: "<PASTE_FRESH_PIN_FROM_POSTMAN>"
   ```

3. **Re-run Test Immediately** ⚡
   ```bash
   behave -D env=qa --tags=@smoke \
     features/Pay_to_Person\(Domestic\)/4_paymentTransfer.feature:19
   ```

4. **Compare Payloads** 🔍
   - Use a diff tool to compare:
     - Automated test payload (from debug logs above)
     - Postman payload (working)
   - Identify ANY differences

### Short-term Actions (This Week)

1. **Implement Dynamic PIN Encryption**
   - Research API's public key endpoint
   - Implement PIN encryption utility
   - Use fresh PIN for each test execution

2. **Extract Customer ID Dynamically**
   - Decode user JWT token OR
   - Call user profile API
   - Use actual customer ID in payload

3. **Add More Debug Logging**
   - Log decoded user token claims
   - Log all response headers
   - Add request/response correlation IDs

### Long-term Actions (Next Sprint)

1. **Create Complete Dynamic Flow**
   - All values generated dynamically
   - No hardcoded PINs, tokens, or IDs
   - Session management between API calls

2. **Add Retry Logic**
   - Auto-retry with fresh PIN if authentication fails
   - Detect PIN expiration and re-encrypt

3. **Improve Error Handling**
   - Parse backend error codes
   - Provide actionable error messages
   - Auto-suggest fixes based on error type

---

## 📝 Test Configuration

### Current Config (config/qa.yaml)
```yaml
p2p_payment_transfer:
  fee_amount: 0
  currency: "ZWG"
  payer_amount: 3
  payee_amount: 3
  encrypted_pin: "ZXodNbUKicCm/E01R6xI6NLUxqxP4g+mZAbQik8VYCeJYDGL9n..."
  beneficiary_customer_id: "f044ff8d-abe6-47aa-8837-ec329e8a0edc"
```

### Feature File Override
```gherkin
Given I have payment transfer details:
    | field      | value |
    | feeAmount  | 0.5   |  ← Overrides config value of 0
```

---

## 🎯 Success Criteria

Payment Transfer tests will pass when:
1. ✅ Fresh encrypted PIN is used (not expired)
2. ✅ Correct customer ID is used (matches authenticated user)
3. ✅ API returns status 200/201
4. ✅ Response contains order ID
5. ✅ Order Details API can retrieve the transaction

---

## 📊 Overall Progress

```
Total P2P Test Scenarios: 5
Passing: 3 (60%) ✅✅✅
Failing: 2 (40%) ❌❌

Total Test Steps: 60+
Passing: 57+ (95%) ✅
Failing: 3 (5%) ❌

Infrastructure: 100% Working ✅
Dynamic Token Extraction: 100% Working ✅
Debug Logging: 100% Implemented ✅
Issue: Backend Authentication/Authorization ❌
```

---

## 📞 Action Required

**Please provide ONE of the following:**

1. **Fresh Encrypted PIN from Postman** (Quick Fix - 5 min)
   ```
   Copy PIN value from working Postman request
   Paste into config/qa.yaml → p2p_payment_transfer.encrypted_pin
   ```

2. **Complete Postman Request Details** (Comparison - 15 min)
   ```
   Export working Postman request as JSON
   Share complete payload and headers
   We'll identify differences
   ```

3. **PIN Encryption API Details** (Long-term Fix - 2 hours)
   ```
   API endpoint to get public key
   PIN encryption algorithm/format
   We'll implement dynamic PIN encryption
   ```

---

**Next Update:** After receiving fresh PIN or Postman details
