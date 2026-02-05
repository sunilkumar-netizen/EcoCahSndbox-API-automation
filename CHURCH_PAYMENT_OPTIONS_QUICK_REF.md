# Church Payment Options - Quick Reference

## ⚡ Quick Start

```bash
# Run all church payment options tests
behave -t @church_payment_options

# Run smoke test only
behave -t @smoke -t @church_payment_options

# Run specific scenario line
behave features/pay_to_church/16_churchPaymentOptions.feature:20
```

---

## 📍 API Endpoint

```
GET /bff/v2/payment/options?serviceType=sasai-app-payment
```

**Authentication**: User Token (Bearer) from PIN Verify

---

## 🎯 Key Test Scenarios

### Smoke Test
```gherkin
@smoke @church_payment_options
Scenario: Get church payment options with valid authentication
    Given I have valid user authentication
    And I have service type "sasai-app-payment"
    And I have device information headers
    When I send church payment options request to "/bff/v2/payment/options"
    Then response status code should be 200
    And response should have payment options
```

### Integration Test
```gherkin
@integration @church_payment_options
Scenario: Complete flow - Church Lookup to Payment Options
    Given I have valid user authentication
    And I have merchant code "394875"
    When I send merchant lookup by code request
    Then response status code should be 200
    Given I have service type "sasai-app-payment"
    And I have device information headers
    When I send church payment options request
    Then response status code should be 200
    And response should have payment options
```

---

## 📊 Test Statistics

- **Total Scenarios**: 53
- **Smoke**: 1
- **Positive**: 9
- **Negative**: 11
- **Security**: 3
- **Performance**: 2
- **Integration**: 3
- **Status**: ✅ All steps defined (Zero errors)

---

## 🔑 Required Steps (Church-Specific)

```gherkin
# Setup
Given I have service type "sasai-app-payment"
Given I have device information headers
Given I have valid user authentication

# Action
When I send church payment options request to "/bff/v2/payment/options"

# Validation
Then response should have payment options
Then response should have payment instruments
Then payment instruments should not be empty
Then response should contain wallet payment option
```

---

## 📝 Common Test Patterns

### Pattern 1: Basic Payment Options
```gherkin
Given I have valid user authentication
And I have service type "sasai-app-payment"
And I have device information headers
When I send church payment options request to "/bff/v2/payment/options"
Then response status code should be 200
And response should have payment options
```

### Pattern 2: With Location
```gherkin
Given I have valid user authentication
And I have service type "sasai-app-payment"
And I have device information headers
And I have latitude "28.508632"
And I have longitude "77.092242"
When I send church payment options request to "/bff/v2/payment/options"
Then response status code should be 200
```

### Pattern 3: Negative Test
```gherkin
Given I have invalid user token
And I have service type "sasai-app-payment"
And I have device information headers
When I send church payment options request to "/bff/v2/payment/options"
Then response status code should be 401
```

---

## 🏃 Quick Commands

```bash
# All tests
behave -t @church_payment_options

# By category
behave -t @positive -t @church_payment_options
behave -t @negative -t @church_payment_options
behave -t @security -t @church_payment_options
behave -t @integration -t @church_payment_options
behave -t @performance -t @church_payment_options

# With reports
behave -t @church_payment_options --format html --outfile reports/church_payment_options.html
behave -t @church_payment_options -f allure_behave.formatter:AllureFormatter -o allure-results/
```

---

## 📂 Files

```
features/pay_to_church/
  └── 16_churchPaymentOptions.feature (410 lines, 53 scenarios)

steps/
  └── church_payment_options_steps.py (Church-specific steps)

docs/
  ├── CHURCH_PAYMENT_OPTIONS_COMPLETE.md (Full documentation)
  ├── CHURCH_PAYMENT_OPTIONS_SUCCESS.md (Success summary)
  └── CHURCH_PAYMENT_OPTIONS_QUICK_REF.md (This file)
```

---

## ✅ Status: READY FOR TESTING

**Errors**: 0  
**Scenarios**: 53  
**Coverage**: Comprehensive  
**Integration**: Complete  

---

## 📞 Need Help?

See full documentation:
- `CHURCH_PAYMENT_OPTIONS_COMPLETE.md` - Complete API and test guide
- `CHURCH_PAYMENT_OPTIONS_SUCCESS.md` - Feature success summary

---

**Quick Ref Version**: 1.0  
**Last Updated**: February 5, 2026
