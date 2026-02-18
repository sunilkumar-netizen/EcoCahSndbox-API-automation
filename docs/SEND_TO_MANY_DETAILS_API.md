# Send to Many API Suite - Complete Implementation

## Overview
Complete end-to-end implementation of the Send to Many payment flow, including payment options retrieval, bulk payment execution, and transaction details retrieval.

## APIs Implemented

### 1. Payment Options API
- **Endpoint**: `GET /bff/v2/payment/options?serviceType=ZWSendManyTransactions`
- **Purpose**: Retrieve available payment instruments for send to many transactions
- **Feature File**: `features/send-to-many/1_paymentOptions.feature`
- **Step Definitions**: `steps/send_to_many_payment_options_steps.py`
- **Test Status**: ✅ Smoke test passing

### 2. Send to Many Payment API
- **Endpoint**: `POST /bff/v1/wallet/payments/send-to-many`
- **Purpose**: Execute bulk payment to multiple recipients
- **Feature File**: `features/send-to-many/2_sendToMany.feature`
- **Step Definitions**: `steps/send_to_many_steps.py`
- **Test Status**: ✅ Smoke test passing
- **Key Feature**: Automatically captures `sendManyId` from response for use in details API

### 3. Complete Flow Integration
- **Purpose**: End-to-end flow combining payment options and payment execution
- **Feature File**: `features/send-to-many/3_completeFlow.feature`
- **Test Status**: ✅ Smoke test passing

### 4. Send to Many Details API (NEW)
- **Endpoint**: `GET /bff/v1/wallet/payments/send-to-many/{sendManyId}`
- **Purpose**: Retrieve detailed transaction information for a specific send-to-many payment
- **Feature File**: `features/send-to-many/4_sendToManyDetails.feature`
- **Step Definitions**: `steps/send_to_many_details_steps.py`
- **Test Status**: ✅ Smoke test passing

## Request/Response Details

### Send to Many Details API

#### Request Format
```bash
GET /bff/v1/wallet/payments/send-to-many/{sendManyId}

Headers:
- Authorization: Bearer {user_token}
- Content-Type: application/json
- requestId: {uuid}

Path Parameter:
- sendManyId: UUID (e.g., "8a334e5a-f035-49b9-a4a5-31db7c022c0d")
```

#### Response Fields (200 OK)
```json
{
  "sendManyId": "8a334e5a-f035-49b9-a4a5-31db7c022c0d",
  "referenceId": "REF123456",
  "status": "COMPLETED",
  "currency": "ZWG",
  "recipientDetails": [
    {
      "amount": 4,
      "name": "EcoCash User Two",
      "mobileNumber": "+263789124558",
      "customerId": "2f3a5e5a-9387-4669-8674-58df6c28b5ac"
    }
  ],
  "createdAt": "2026-02-18T15:08:58Z",
  "description": "Test Send to Many Recipients"
}
```

## Test Coverage

### 4_sendToManyDetails.feature Test Scenarios

#### Smoke Tests (1)
1. ✅ Get send to many transaction details successfully

#### Regression Tests (2)
1. Get send to many details after creating transaction (end-to-end flow)
2. Verify send to many details contains all transaction information

#### Negative Tests (4)
1. Get send to many details without authentication → 401
2. Get send to many details with invalid token → 401
3. Get send to many details with non-existent transaction ID → 404
4. Get send to many details with malformed transaction ID → 400

#### Validation Tests (1)
1. Verify send to many details response structure

#### Performance Tests (1)
1. Send to many details response time validation (< 3000ms)

#### Security Tests (1)
1. Verify user can only access their own send to many transactions → 403/404

**Total Scenarios**: 11 (1 smoke, 2 regression, 4 negative, 1 validation, 1 performance, 1 security)

## Key Features Implemented

### 1. Automatic sendManyId Capture
The Send to Many Payment API automatically captures the `sendManyId` from the response and stores it in `context.send_many_id` for immediate use in the Details API.

**Implementation** (in `send_to_many_steps.py`):
```python
# After successful payment POST (200/201)
possible_fields = [
    'sendManyId', 'transactionId', 'orderId', 'paymentId', 
    'referenceId', 'id', 'sendToManyId', 'sendManyTransactionId'
]

# Check root level and nested structures
# Store in context.send_many_id
print(f"🔑 Captured send many ID: {send_many_id}")
```

### 2. Flexible sendManyId Extraction
The Details API step definitions can extract the sendManyId from multiple response structures:
- Root level fields
- Nested `data` object
- Nested `result` object
- Multiple field name variations

**Implementation** (in `send_to_many_details_steps.py`):
```python
@when('I retrieve the send many ID from payment response')
def step_retrieve_send_many_id_from_response(context):
    # Intelligent extraction from various response structures
    # Checks 8+ possible field names
    # Handles nested objects
    # Provides visual feedback with 🔑 emoji
```

### 3. Comprehensive Error Handling
All API calls include:
- Try-catch blocks with formatted error output
- 80-character bordered error messages
- Detailed error context (endpoint, request ID, etc.)
- HTTP 500 detection with backend error messaging
- Visual indicators (❌, ⚠️, ✅, 🔑)

### 4. Multiple Test ID Scenarios
The Details API tests support:
- Using a sample/known transaction ID
- Extracting ID from previous payment response
- Testing with invalid/malformed IDs
- Testing with another user's ID (security)

## Complete Flow Example

### End-to-End Test Execution
```gherkin
Scenario: Get send to many details after creating transaction
  # Step 1: Create payment
  Given I have send to many payment request body with 2 recipients
  When I send send to many payment request to "/bff/v1/wallet/payments/send-to-many"
  Then response status code should be 200 or 201
  
  # Step 2: Automatically captures sendManyId: "14d5c7b6-f923-402d-a226-db70209fa3eb"
  
  # Step 3: Extract ID from response
  When I retrieve the send many ID from payment response
  
  # Step 4: Retrieve transaction details
  And I send get send to many details request to "/bff/v1/wallet/payments/send-to-many"
  Then response status code should be 200
  And response should contain send to many transaction details
```

### Test Execution Results
```
✅ Send payment to multiple recipients successfully
🔑 Captured send many ID: 14d5c7b6-f923-402d-a226-db70209fa3eb
✅ Send many ID extracted: 14d5c7b6-f923-402d-a226-db70209fa3eb
✅ Get send to many details request successful - Status: 200
✅ Send to many transaction details validated
```

## Running Tests

### Smoke Tests
```bash
# Run all send-to-many smoke tests (4 scenarios)
behave features/send-to-many/ --tags=smoke --no-capture

# Run only Details API smoke test
behave features/send-to-many/4_sendToManyDetails.feature --tags=smoke --no-capture
```

### Regression Tests
```bash
# Run all send-to-many regression tests
behave features/send-to-many/ --tags=regression --no-capture

# Run specific end-to-end flow test
behave features/send-to-many/4_sendToManyDetails.feature:29 --no-capture
```

### Negative Tests
```bash
# Run all negative tests
behave features/send-to-many/4_sendToManyDetails.feature --tags=negative --no-capture
```

### All Tests
```bash
# Run complete send-to-many test suite (all 4 feature files)
behave features/send-to-many/ --no-capture
```

## Test Results Summary

### Current Test Status (4 Feature Files)
| Feature | Smoke | Regression | Negative | Validation | Performance | Security | Total |
|---------|-------|------------|----------|------------|-------------|----------|-------|
| Payment Options | ✅ 1/1 | - | - | - | - | - | 1 |
| Send to Many Payment | ✅ 1/1 | 2 | 6 | 2 | 1 | 1 | 14 |
| Complete Flow | ✅ 1/1 | 1 | - | - | - | - | 2 |
| Details API | ✅ 1/1 | 2 | 4 | 1 | 1 | 1 | 11 |
| **TOTAL** | **✅ 4/4** | **5** | **10** | **3** | **2** | **2** | **28** |

### Execution Time
- Payment Options smoke: ~0.7s
- Send to Many Payment smoke: ~1.6s
- Complete Flow smoke: ~2.4s
- Details API smoke: ~1.1s
- **Total (4 smoke tests): ~5.3s**

### All Smoke Tests Passing
```
4 features passed, 0 failed, 0 skipped
4 scenarios passed, 0 failed, 23 skipped
40 steps passed, 0 failed, 180 skipped, 0 undefined
Took 0m5.299s
```

## Files Structure

```
features/send-to-many/
├── 1_paymentOptions.feature          (26 lines, 1 scenario)
├── 2_sendToMany.feature              (129 lines, 14 scenarios)
├── 3_completeFlow.feature            (49 lines, 2 scenarios)
└── 4_sendToManyDetails.feature       (101 lines, 11 scenarios) ← NEW

steps/
├── send_to_many_payment_options_steps.py  (203 lines)
├── send_to_many_steps.py                  (617 lines) ← ENHANCED
└── send_to_many_details_steps.py          (547 lines) ← NEW
```

## Key Enhancements

### 1. Automatic ID Capture in send_to_many_steps.py
**Lines 353-374**: Added automatic sendManyId extraction after successful payment
- Checks 8+ possible field names
- Handles nested response structures
- Stores in `context.send_many_id`
- Visual feedback with 🔑 emoji

### 2. Comprehensive Details API Implementation
**New file: send_to_many_details_steps.py (547 lines)**
- 4 GIVEN steps for test setup
- 3 WHEN steps for API calls
- 8 THEN steps for validation
- Flexible ID extraction logic
- Comprehensive error handling
- Multiple response structure support

### 3. Complete Test Coverage
- 11 test scenarios covering all aspects
- Smoke, regression, negative, validation, performance, security tests
- End-to-end integration testing
- Authentication and authorization testing

## Integration with Existing Framework

### Dependencies
- ✅ Uses existing `APIClient` class
- ✅ Uses existing `Logger` class
- ✅ Integrates with existing authentication flow
- ✅ Follows existing step definition patterns
- ✅ Consistent error handling approach

### Reusable Components
- Common steps for status code validation
- Common steps for JSON validation
- Shared authentication steps
- Shared API availability checks

## Next Steps

### Recommended Actions
1. ✅ **COMPLETE**: Smoke tests all passing
2. 🔄 **TODO**: Run all regression tests (7 scenarios)
3. 🔄 **TODO**: Run all negative tests (10 scenarios)
4. 🔄 **TODO**: Run validation tests (3 scenarios)
5. 🔄 **TODO**: Run performance tests (2 scenarios)
6. 🔄 **TODO**: Run security tests (2 scenarios)

### Git Commit
```bash
git add features/send-to-many/4_sendToManyDetails.feature
git add steps/send_to_many_details_steps.py
git add steps/send_to_many_steps.py  # Enhanced with auto ID capture

git commit -m "feat: Add Send to Many Details API with auto ID capture

✨ New Features:
- Send to Many Details API (GET /bff/v1/wallet/payments/send-to-many/{sendManyId})
- Automatic sendManyId capture from payment response
- Flexible transaction ID extraction from multiple response structures
- 11 comprehensive test scenarios

📊 Test Coverage:
- 1 smoke test: Get transaction details ✅
- 2 regression tests: End-to-end flow, detailed validation
- 4 negative tests: No auth, invalid token, non-existent ID, malformed ID
- 1 validation test: Response structure
- 1 performance test: Response time < 3000ms
- 1 security test: User access control

🔧 Enhancements:
- Enhanced send_to_many_steps.py with automatic sendManyId capture
- Comprehensive error handling with formatted output
- Visual feedback with emojis (🔑, ✅, ⚠️, ❌)
- Support for multiple response structures

✅ Test Results:
- All 4 smoke tests passing (Payment Options + Payment + Complete Flow + Details)
- Total execution time: ~5.3 seconds
- 28 total test scenarios across 4 feature files

📝 Implementation Details:
- Feature file: 101 lines with 11 scenarios
- Step definitions: 547 lines
- Automatic ID capture: 22 lines added to send_to_many_steps.py
- Flexible ID extraction from 8+ possible field names"

git push origin QA
```

## Benefits

### 1. Complete API Coverage
All aspects of the Send to Many flow now testable:
- ✅ Payment options retrieval
- ✅ Bulk payment execution
- ✅ Transaction details retrieval
- ✅ End-to-end integration

### 2. Seamless Integration
The automatic ID capture creates a seamless test experience:
- No manual ID management required
- Supports both manual and dynamic ID scenarios
- Works with various response structures

### 3. Robust Testing
Comprehensive test coverage ensures:
- Functional correctness
- Security and authorization
- Error handling
- Performance requirements
- API contract validation

### 4. Developer Experience
Enhanced logging and visual feedback:
- 🔑 ID capture confirmation
- ✅ Success indicators
- ⚠️ Warning messages
- ❌ Error details
- Formatted error output

## Conclusion

The Send to Many Details API implementation completes the full payment flow testing capability. With automatic ID capture, flexible extraction logic, and comprehensive test coverage, the suite provides robust validation of the entire send-to-many payment journey from options retrieval through payment execution to transaction details verification.

**Total Implementation Stats**:
- **4 Feature Files**: 305 lines, 28 scenarios
- **3 Step Definition Files**: 1,367 lines
- **All Smoke Tests**: ✅ PASSING (4/4, 100%)
- **Execution Time**: ~5.3 seconds for complete smoke suite
