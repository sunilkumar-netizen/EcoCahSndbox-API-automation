# 🚀 Church Payment API - Quick Reference

## 📍 API Endpoint
```
POST /bff/v2/order/utility/payment
```

## 🔑 Authentication
**User Token Required** (from PIN Verify API)

---

## 📊 Quick Stats
- **Feature File**: `features/pay_to_church/17_churchPayment.feature`
- **Step File**: `steps/church_payment_steps.py`
- **Scenarios**: 67
- **Tags**: `@church_payment`, `@pay_to_church`, `@sasai`

---

## 🎯 Most Common Test Commands

```bash
# Run all church payment tests
behave -t @church_payment

# Run smoke test
behave -t @smoke -t @church_payment

# Run positive tests
behave -t @positive -t @church_payment

# Run negative tests
behave -t @negative -t @church_payment

# Run integration tests
behave -t @integration -t @church_payment

# Run with HTML report
behave -t @church_payment --format html --outfile reports/church_payment.html

# Dry run (verify steps)
behave --dry-run features/pay_to_church/17_churchPayment.feature
```

---

## 📋 Request Body Template

```json
{
    "feeAmount": 0,
    "currency": "USD",
    "billerDetails": {
        "operatorId": "SZWOCH0001",
        "categoryId": "SZWC10018",
        "amount": 1.0,
        "currency": "USD",
        "Q1": "156611",
        "Q2": "Offering"
    },
    "payerAmount": 1.0,
    "payerDetails": {
        "instrumentToken": "from-payment-options",
        "paymentMethod": "wallet",
        "provider": "ecocash",
        "pin": "encrypted-pin",
        "publicKeyAlias": "payment-links"
    },
    "subType": "pay-to-church",
    "channel": "sasai-super-app",
    "deviceInfo": {...},
    "notes": {
        "operatorName": "church-name",
        "code": "church-code",
        "transferPurpose": "purpose"
    }
}
```

---

## 🔗 Complete Flow

```gherkin
# Step 1: Search church
GET /bff/v1/catalog/search-school-church-merchant?type=CHURCH

# Step 2: Lookup church
GET /bff/v1/catalog/merchant-lookup?merCode={code}

# Step 3: Get payment options
GET /bff/v2/payment/options?serviceType=sasai-app-payment

# Step 4: Make payment
POST /bff/v2/order/utility/payment
```

---

## 🧪 Key Step Definitions

### Setup Payment
```gherkin
Given I have church payment details
Given I have church payment details with purpose "Offering"
Given I have church payment details with amount 10.0
Given I have church payment details with currency "USD"
```

### Send Request
```gherkin
When I send church payment request to "/bff/v2/order/utility/payment"
```

### Validate Response
```gherkin
Then response should contain payment confirmation
Then response should have transaction ID
Then transaction ID should be valid format
```

---

## 💰 Common Amounts
- Minimum: 0.01
- Small: 1.0, 5.0
- Medium: 10.0, 50.0
- Large: 100.0

---

## 💱 Supported Currencies
- ✅ USD
- ✅ ZWL
- ❌ EUR (invalid)
- ❌ GBP (invalid)

---

## 🎯 Payment Purposes
- Offering
- Tithe
- Building Fund
- Mission Support
- Special Collection

---

## 📌 Required Fields

| Field | Type | Example |
|-------|------|---------|
| `currency` | string | "USD" |
| `billerDetails.operatorId` | string | "SZWOCH0001" |
| `billerDetails.categoryId` | string | "SZWC10018" |
| `billerDetails.amount` | number | 1.0 |
| `billerDetails.Q1` | string | "156611" (church code) |
| `billerDetails.Q2` | string | "Offering" (purpose) |
| `payerAmount` | number | 1.0 |
| `payerDetails.instrumentToken` | string | From payment options |
| `payerDetails.pin` | string | Encrypted PIN |
| `subType` | string | "pay-to-church" |
| `channel` | string | "sasai-super-app" |

---

## ⚠️ Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | No/invalid token | Get user token from PIN Verify |
| 400 Missing token | No instrument token | Call payment options first |
| 400 Invalid PIN | Wrong/unencrypted PIN | Use correct encryption |
| 400 Invalid amount | Zero/negative | Use positive amount |
| 404 Not Found | Invalid operator ID | Use valid church operator |
| 402 Payment Required | Insufficient balance | Check wallet balance |

---

## 🏷️ Available Tags

**Primary Tags:**
- `@church_payment` - All church payment tests
- `@pay_to_church` - Church payment flow
- `@sasai` - Sasai app tests

**Category Tags:**
- `@smoke` - Critical path (1)
- `@positive` - Happy path (7)
- `@negative` - Error cases (21)
- `@validation` - Data validation (5)
- `@security` - Security tests (3)
- `@integration` - Flow tests (4)
- `@performance` - Speed tests (2)
- `@amount_validation` - Amount tests (7)
- `@currency_validation` - Currency tests (4)
- `@purpose_validation` - Purpose tests (5)

---

## 📊 Test Coverage

| Category | Count | %Coverage |
|----------|-------|-----------|
| Positive | 7 | 10.4% |
| Negative | 21 | 31.3% |
| Security | 3 | 4.5% |
| Integration | 4 | 6.0% |
| Validation | 5 | 7.5% |
| Amount Tests | 7 | 10.4% |
| Currency Tests | 4 | 6.0% |
| Purpose Tests | 5 | 7.5% |
| Other | 11 | 16.4% |
| **TOTAL** | **67** | **100%** |

---

## 🔧 Debug Commands

```bash
# Check if steps are defined
behave --dry-run features/pay_to_church/17_churchPayment.feature

# Run specific scenario
behave features/pay_to_church/17_churchPayment.feature:18

# Run with verbose output
behave -t @church_payment --verbose

# Run and stop on first failure
behave -t @church_payment --stop
```

---

## 📁 File Locations

```
features/pay_to_church/
  └── 17_churchPayment.feature (540 lines, 67 scenarios)

steps/
  └── church_payment_steps.py (500+ lines, 35+ steps)

docs/
  ├── CHURCH_PAYMENT_COMPLETE.md (Complete guide)
  ├── CHURCH_PAYMENT_SUCCESS.md (Success summary)
  └── CHURCH_PAYMENT_QUICK_REF.md (This file)
```

---

## 🎯 Integration Example

```gherkin
Scenario: Complete church payment flow
    # Get user token
    Given I have valid user credentials
    When I verify PIN
    Then I store user token
    
    # Search church
    When I search for church "Faith"
    Then I extract church code
    
    # Get payment options
    When I get payment options
    Then I extract instrument token
    
    # Make payment
    Given I have church payment details with extracted info
    When I send church payment request
    Then response should contain payment confirmation
    And response should have transaction ID
```

---

## 📞 Quick Help

**Need to add a new scenario?**
1. Add scenario to `17_churchPayment.feature`
2. Use existing steps from `church_payment_steps.py`
3. Add new steps if needed
4. Tag appropriately
5. Test with dry-run

**Need to modify payment details?**
- Look at `church_payment_steps.py`
- Find step definition for payment setup
- Modify the payload as needed

**Need to add new validation?**
- Add `Then` step to feature file
- Implement step in `church_payment_steps.py`
- Use assertions from `core/assertions.py`

---

## ✅ Pre-Flight Checklist

Before running tests:
- [ ] User token available (from PIN Verify)
- [ ] Church code available (from Search/Lookup)
- [ ] Instrument token available (from Payment Options)
- [ ] Device info configured
- [ ] Environment set (QA)
- [ ] Network connectivity

---

## 🎉 Status

**Feature**: ✅ COMPLETE  
**Steps**: ✅ IMPLEMENTED  
**Docs**: ✅ READY  
**Tests**: ✅ RUNNABLE  

---

## 📚 Related Docs

- `CHURCH_PAYMENT_COMPLETE.md` - Full documentation
- `CHURCH_PAYMENT_SUCCESS.md` - Success summary
- `CHURCH_PAYMENT_OPTIONS_COMPLETE.md` - Payment options guide
- `API_INVENTORY.md` - All APIs

---

**Last Updated**: February 5, 2026  
**Status**: ✅ Production Ready  
**Version**: 1.0  

---

**🚀 Quick Reference Guide - Ready to Use!**
