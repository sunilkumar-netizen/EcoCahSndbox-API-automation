# Church Payment Options Feature - Complete Documentation

## Overview
The Church Payment Options API is used to retrieve available payment methods for church donations/payments. This is Step 3 in the "Pay to Church" flow, occurring after church lookup by code.

---

## API Details

### Endpoint
```
GET /bff/v2/payment/options
```

### Query Parameters
- **serviceType** (required): Type of service for payment
  - Value: `sasai-app-payment`

### Authentication
- **User Token Required**: Yes (Bearer token from PIN Verify API)
- **App Token**: Not sufficient (must be user token)

### Required Headers
```
Authorization: Bearer {userToken}
os: RM6877
deviceType: android
currentVersion: 2.2.1
Accept-Encoding: gzip
Connection: keep-alive
requestId: {uuid}
appChannel: sasai-super-app
simNumber: {uuid}
deviceId: {uuid}
model: {deviceModel}
network: {networkType}
latitude: {latitude}
longitude: {longitude}
osVersion: {osVersion}
appVersion: {appVersion}
package: com.sasai.sasaipay
```

### Example Request
```bash
curl 'https://sandbox.sasaipaymentgateway.com/bff/v2/payment/options?serviceType=sasai-app-payment' \
  --header 'Authorization: Bearer {userToken}' \
  --header 'deviceType: android' \
  --header 'osVersion: 15' \
  --header 'appVersion: 2.2.1' \
  --header 'latitude: 28.508632' \
  --header 'longitude: 77.092242' \
  --header 'requestId: 43843e90-d1c8-11f0-a41e-95f35da604e5'
```

### Response Structure
```json
{
  "items": [
    {
      "code": "wallet",
      "name": "Wallet Payment",
      "instruments": [
        {
          "instrumentToken": "token123",
          "balance": 1000.00,
          "currency": "ZWL",
          "isDefault": true
        }
      ],
      "providers": [
        {
          "code": "provider1",
          "name": "Provider Name",
          "healthCheck": "ACTIVE",
          "balanceEnquiryEnabled": true
        }
      ]
    }
  ],
  "paymentMenu": {...}
}
```

---

## Test Coverage Summary

### Total Scenarios: **53**

### By Category:

#### ✅ **Positive Tests (9 scenarios)**
- Valid authentication with service type
- Correct response structure validation
- All required headers present
- Location headers included
- Device information verification

#### ❌ **Negative Tests (11 scenarios)**
- No authentication
- Invalid user token
- Expired user token
- App token instead of user token
- Missing service type
- Empty service type
- Invalid service type

#### 🔍 **Validation Tests (5 scenarios)**
- Required fields in response
- Response structure validation
- Response headers validation
- Request ID header
- Device headers verification

#### 🔒 **Security Tests (3 scenarios)**
- Missing Authorization header
- Empty Bearer token
- Malformed Bearer token

#### ⚠️ **Error Handling (4 scenarios)**
- Invalid HTTP methods (POST, PUT, DELETE)
- Wrong endpoint path

#### ⚡ **Performance Tests (2 scenarios)**
- Response time < 3000ms
- Response time < 5000ms

#### 🔗 **Integration Tests (3 scenarios)**
- Church Lookup → Payment Options
- PIN Verify → Payment Options
- Church Search → Lookup → Payment Options

#### 📊 **Data Validation (3 scenarios)**
- Wallet payment option present
- Payment instruments not empty
- Cached response validation

#### 🔄 **Concurrency Tests (2 scenarios)**
- Multiple requests with same token
- Rapid requests consistency

#### 🧪 **Service Type Tests (1 scenario outline)**
- Different service types validation

#### 📍 **Location Tests (1 scenario outline)**
- Different geographical locations

#### 📤 **Data Extraction Tests (2 scenarios)**
- Extract available payment methods
- Wallet balance information

#### ⚡ **Stress Tests (1 scenario)**
- 5 rapid requests consistency check

#### 📋 **Headers Tests (2 scenarios)**
- Without device headers
- With minimal headers

---

## Complete Step Definitions

### Church-Specific Steps (church_payment_options_steps.py)

#### WHEN Steps:
```gherkin
When I send church payment options request to "{endpoint}"
When I send church payment options request with stored token to "{endpoint}"
When I send {count:d} church payment options requests to "{endpoint}"
```

#### THEN Steps:
```gherkin
Then payment instruments should not be empty
Then wallet option should have balance information
Then I extract available payment methods from response
Then extracted payment methods should not be empty
```

### Reused Steps from Other Files:

#### From school_payment_options_steps.py:
- `I have device information headers`
- `I have all required device headers`
- `I have device type "{device_type}"`
- `I have OS version "{os_version}"`
- `I have app version "{app_version}"`
- `I have latitude "{latitude}"`
- `I have longitude "{longitude}"`
- `response should have payment instruments`
- `response should contain wallet payment option`
- And many more...

#### From payment_options_steps.py:
- `I have service type "{service_type}"`
- `I have no service type`
- `response should have payment options`
- `response should have payment options structure`

#### From merchant_lookup_steps.py:
- `I have request ID "{request_id}"`

#### From login_devices_steps.py:
- `I have no authentication token`
- `I have invalid user token`
- `I have expired user token`
- `I have app token only`
- `I have valid user authentication`

#### From common_steps.py:
- `response status code should be {status_code:d}`
- `response body should be valid JSON`
- `response time should be less than {max_time:d} ms`
- And HTTP method steps...

---

## Running the Tests

### Run All Church Payment Options Tests
```bash
behave -t @church_payment_options
```

### Run Smoke Tests Only
```bash
behave -t @smoke -t @church_payment_options
```

### Run Specific Scenario
```bash
behave features/pay_to_church/16_churchPaymentOptions.feature:20
```

### Run by Category
```bash
# Security tests
behave -t @security -t @church_payment_options

# Integration tests  
behave -t @integration -t @church_payment_options

# Performance tests
behave -t @performance -t @church_payment_options

# Positive tests only
behave -t @positive -t @church_payment_options

# Negative tests only
behave -t @negative -t @church_payment_options
```

### Run with HTML Report
```bash
behave -t @church_payment_options --format html --outfile reports/church_payment_options.html
```

### Run with Allure Report
```bash
behave -t @church_payment_options -f allure_behave.formatter:AllureFormatter -o allure-results/
allure serve allure-results/
```

---

## Integration with Pay to Church Flow

### Complete Church Payment Flow:

1. **Church Search** (Feature 14)
   - Search for churches by name
   - Get list of churches with merchant codes

2. **Church Lookup by Code** (Feature 15)
   - Look up specific church by merchant code
   - Verify church details

3. **Church Payment Options** (Feature 16 - THIS API)
   - Get available payment methods
   - Check wallet balance
   - Select payment instrument

4. **Church Payment** (Feature 17 - NEXT)
   - Make actual payment to church
   - Confirm transaction

### Flow Example:
```gherkin
Scenario: Complete Church Payment Flow
    # Step 1: Search
    Given I have search type "CHURCH"
    When I send church search request
    Then I extract first merchant code
    
    # Step 2: Lookup
    When I send merchant lookup by code request with extracted code
    Then response should contain merchant details
    
    # Step 3: Get Payment Options (THIS API)
    Given I have service type "sasai-app-payment"
    When I send church payment options request
    Then response should have payment options
    And I extract available payment methods
    
    # Step 4: Make Payment (NEXT FEATURE)
    When I send church payment request with selected instrument
    Then payment should be successful
```

---

## Key Response Fields

### Payment Options Structure:
```python
{
    "items": [                    # List of payment options
        {
            "code": str,          # Payment method code (e.g., "wallet")
            "name": str,          # Display name
            "instruments": [      # Available instruments
                {
                    "instrumentToken": str,      # Token for payment
                    "balance": float,            # Available balance
                    "currency": str,             # Currency code
                    "isDefault": bool,           # Default instrument
                    "maskedNumber": str          # Masked account
                }
            ],
            "providers": [        # Payment providers
                {
                    "code": str,                 # Provider code
                    "name": str,                 # Provider name
                    "healthCheck": str,          # Status
                    "balanceEnquiryEnabled": bool
                }
            ]
        }
    ],
    "paymentMenu": {...}          # Additional menu options
}
```

---

## Common Issues and Solutions

### Issue 1: 401 Unauthorized
**Cause**: Missing or invalid user token  
**Solution**: Ensure PIN Verify was successful and token is stored

### Issue 2: 400 Bad Request
**Cause**: Missing serviceType parameter  
**Solution**: Always include `serviceType=sasai-app-payment` in query

### Issue 3: Empty Payment Options
**Cause**: No payment instruments configured for user  
**Solution**: Check user account has active payment methods

### Issue 4: Missing Device Headers
**Cause**: Required headers not sent  
**Solution**: Use `I have device information headers` step

---

## Success Criteria

✅ **All 53 scenarios passing**  
✅ **Zero undefined steps**  
✅ **Response time < 5000ms**  
✅ **All payment instruments retrieved**  
✅ **Wallet balance information available**  

---

## Next Steps

1. ✅ **COMPLETED**: Church Search API (Feature 14)
2. ✅ **COMPLETED**: Church Lookup by Code API (Feature 15)
3. ✅ **COMPLETED**: Church Payment Options API (Feature 16)
4. ⏳ **NEXT**: Church Payment API (Feature 17)
   - Make actual payments to churches
   - Handle transaction confirmations
   - Verify payment success

---

## Tags Reference

All scenarios are tagged with:
- `@church_payment_options` - Primary feature tag
- `@pay_to_church` - Flow tag
- `@sasai` - Application tag

Additional tags by scenario type:
- `@smoke` - Critical tests (1)
- `@positive` - Happy path tests (9)
- `@negative` - Error cases (11)
- `@validation` - Data validation (5)
- `@security` - Security tests (3)
- `@error_handling` - Error scenarios (4)
- `@performance` - Speed tests (2)
- `@integration` - Flow tests (3)
- `@headers` - Header tests (2)
- `@device_headers` - Device info tests (3)
- `@data_validation` - Data checks (3)
- `@cache` - Caching tests (1)
- `@concurrent` - Multiple requests (2)
- `@service_types` - Service type tests (1)
- `@location` - Location tests (1)
- `@extract_data` - Data extraction (2)
- `@wallet_validation` - Wallet checks (1)
- `@stress` - Load tests (1)
- `@headers_missing` - Missing headers (1)
- `@headers_optional` - Optional headers (1)

---

## Benefits of This Feature

1. ✅ **Comprehensive Testing**: 53 scenarios covering all edge cases
2. ✅ **Reusable Steps**: Leverages existing step definitions
3. ✅ **Clear Documentation**: Well-documented API and test structure
4. ✅ **Integration Ready**: Fits into complete church payment flow
5. ✅ **Performance Validated**: Response time checks included
6. ✅ **Security Tested**: Authentication and authorization validation
7. ✅ **Error Handling**: All error scenarios covered

---

## File Structure

```
features/pay_to_church/
  └── 16_churchPaymentOptions.feature (410 lines, 53 scenarios)

steps/
  └── church_payment_options_steps.py (Church-specific steps)
  
docs/
  └── CHURCH_PAYMENT_OPTIONS_COMPLETE.md (This file)
```

---

## Maintenance Notes

- **Reuse Existing Steps**: Most steps are reused from payment_options and school_payment_options
- **No Duplicates**: Duplicates removed to avoid Behave errors
- **Church-Specific**: Only church-specific naming and logging added
- **Same API**: Uses same endpoint as school payment options
- **Consistent**: Follows same pattern as other payment features

---

**Feature Status**: ✅ COMPLETE - Ready for Testing  
**Last Updated**: February 5, 2026  
**Author**: API Automation Team
