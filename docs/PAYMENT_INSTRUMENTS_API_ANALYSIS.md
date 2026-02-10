# Payment Instruments API Analysis
**Date**: February 10, 2026  
**Status**: 🔍 Investigation - encryptedPin Not Found in Response

## Executive Summary
Payment Instruments API was successfully integrated and returns 200, but **does NOT include `encryptedPin` in the response**. This means we still can't get a fresh encrypted PIN, and the payment transfer continues to fail with the same error.

## API Details

### Endpoint
```
GET /bff/v1/payment/instruments/{instrumentId}
```

### Response Structure (Actual)
```json
{
  "instrumentId": "c3722703-eefa-4e28-8b7f-40141575cfbf",
  "instrumentToken": "e78bc558-65f4-48e6-94d1-f1b1fcd5d970",  ✅ Fresh token retrieved
  "type": "wallet",
  "country": "ZW",
  "isDefault": true,
  "walletDetails": {
    "maskedAccountNumber": "XXXXX2221",
    "providerName": "EcoCash",
    "providerCode": "ecocash",
    "fullName": "Ropafadzo Nyagwaya",
    "nickName": "EcoCash",
    "accountType": "wallet",
    "accountNumber": "771222221"
  },
  "currency": [...]
}
```

### What's Missing
- ❌ **No `encryptedPin` field in response**
- The API only returns instrument metadata and a fresh instrument token
- Cannot get fresh encrypted PIN from this endpoint

## Implementation Status

### ✅ Successfully Implemented
1. Payment Instruments API step definition
2. Fresh instrument token extraction (`e78bc558-65f4-48e6-94d1-f1b1fcd5d970`)
3. Using fresh token in payment transfer payload
4. Proper header configuration (15+ headers)

### ❌ Still Missing
1. Fresh encrypted PIN - API doesn't provide it
2. Payment Transfer still returns 400 error
3. Root cause unresolved

## Test Results

### Latest Test Execution
```
✅ Payment Instruments API: 200 OK (211ms)
✅ Fresh instrumentToken extracted
❌ encryptedPin NOT in response
⚠️  Still using PIN from config
❌ Payment Transfer: 400 Bad Request
   Error: "feeAmount" is required (misleading)
```

### Payload Used
```json
{
  "payerDetails": {
    "instrumentToken": "e78bc558-65f4-48e6-94d1-f1b1fcd5d970",  ✅ FRESH from API
    "pin": "ZXodNbUKicCm/E01R6xI6NLUxqxP4g+mZAbQik8VYCeJYDGL9n...",  ⚠️  OLD from config
    ...
  },
  "feeAmount": 0.5,  ✅ Correct type (float)
  ...
}
```

## Questions for User

### Critical Questions
1. **Does the payment instruments API in Postman return an `encryptedPin` field?**
   - If YES: What's the exact field name?
   - If NO: Where do you get the fresh encrypted PIN in Postman?

2. **Is there a separate API endpoint to encrypt the PIN?**
   - Some systems have `/encrypt-pin` or similar endpoints
   - Need endpoint details if it exists

3. **Could the issue be something other than the PIN?**
   - Fresh instrument token is now being used
   - feeAmount is correct (0.5 as float)
   - All dynamic tokens are working
   - Maybe the config PIN is actually valid and the error is elsewhere?

## Possible Solutions

### Option 1: Different API Endpoint
If there's a PIN encryption endpoint, we should call that to get fresh encrypted PIN.

### Option 2: PIN from PIN Verification Response
Maybe we should store and reuse the encrypted PIN from the initial PIN verification API response instead of loading from config.

### Option 3: The PIN Might Be Valid
Perhaps the error is not actually about the PIN, but something else entirely (e.g., customer ID mismatch, instrument validation, etc.).

### Option 4: Request Body Format Issue
Maybe the payload structure or some field validation is failing server-side, and the API returns a generic error for security reasons.

## Next Steps

**Waiting for User Input:**
1. Check Postman collection for payment instruments API response
2. Identify where fresh encrypted PIN comes from
3. Confirm if there's a PIN encryption endpoint
4. Share any additional API calls made before payment transfer in Postman

## Debug Logs Summary

```
🔍 Fetching Payment Instrument Details
🔑 Instrument ID: c3722703-eefa-4e28-8b7f-40141575cfbf
📊 Status Code: 200
⏱️  Response Time: 211.08 ms
✅ Payment Instrument Details Retrieved
🎯 Fresh Instrument Token extracted: e78bc558-65f4-48e6-94d1-f1b1fc...
```

```
🔍 DEBUG MODE: Building Payment Transfer Payload
🔐 Encrypted PIN (first 50 chars): ZXodNbUKicCm/E01R6xI6NLUxqxP4g+mZAbQik8VYCeJYDGL9n...
🔐 PIN Source: CONFIG (p2p_payment_transfer) ⚠️  <-- Still from config!
🎯 Using FRESH payer token from Payment Instruments API: e78bc558-65f4-48e6-9... ✅
```

```
📊 Status Code: 400
❌ ERROR Response: {"errorCode":"http.bad.request","errors":[{"message":"\"feeAmount\" is required","code":"feeAmount"}]}
```

## Conclusion
Payment Instruments API integration is working correctly and providing fresh tokens, but it does NOT solve the encrypted PIN problem because the API doesn't return a PIN. We need to either:
1. Find the correct endpoint to get/encrypt the PIN
2. Use the PIN from a different source (PIN verification response?)
3. Investigate if the issue is actually something other than the PIN

**Status**: 🔴 Blocked - Awaiting user guidance on where to get fresh encrypted PIN
