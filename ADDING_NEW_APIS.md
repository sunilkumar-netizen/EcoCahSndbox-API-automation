# 📝 Guide: Adding New APIs to the Framework

This guide will help you add new API endpoints to the automation framework quickly and efficiently.

---

## 🚀 Quick Start Checklist

Before adding new APIs:
- [ ] Understand the API endpoint (URL, method, parameters)
- [ ] Get sample request/response from API documentation
- [ ] Have test credentials/authentication details
- [ ] Know expected status codes and error scenarios

---

## 📋 Step-by-Step Process

### Step 1: Create Feature File

Create a new `.feature` file in the `features/` directory:

```bash
touch features/payments.feature
```

**Template:**
```gherkin
Feature: Payment API Testing
  As a merchant
  I want to process payments via Sasai Payment Gateway
  So that customers can complete transactions

  Background:
    Given API is available

  @smoke @payments @sasai
  Scenario: Create a new payment
    Given I have valid payment credentials
    And I have payment details with amount "100.00"
    When I send POST request to "/api/v1/payments"
    Then response status code should be 200
    And response body should contain "paymentId"
    And response body should contain "status"
    And response field "status" should be "pending"
    And response time should be less than 5000 ms

  @payments @negative @sasai
  Scenario: Create payment with invalid amount
    Given I have valid payment credentials
    And I have payment details with amount "-10.00"
    When I send POST request to "/api/v1/payments"
    Then response status code should be 400

  @payments @validation @sasai
  Scenario: Verify payment response structure
    Given I have valid payment credentials
    And I have valid payment details
    When I send POST request to "/api/v1/payments"
    Then response status code should be 200
    And response body should contain "paymentId"
    And response body should contain "merchantId"
    And response body should contain "amount"
    And response body should contain "currency"
    And response field "paymentId" should not be empty
```

---

### Step 2: Create Step Definitions

Create a new step definition file in the `steps/` directory:

```bash
touch steps/payments_steps.py
```

**Template:**
```python
"""
Payment API Step Definitions
Implements step definitions for payment-related API scenarios.
"""

from behave import given, when, then


@given('I have valid payment credentials')
def step_have_payment_credentials(context):
    """Prepare payment authentication credentials."""
    # Get token from previous authentication or use stored token
    config = context.base_test.config
    context.headers = {
        'Authorization': f'Bearer {getattr(context, "accessToken", "")}',
        'Content-Type': 'application/json'
    }
    context.base_test.logger.info("Payment credentials prepared")


@given('I have payment details with amount "{amount}"')
def step_have_payment_details_with_amount(context, amount):
    """Prepare payment request data with specific amount."""
    config = context.base_test.config
    context.request_data = {
        'amount': float(amount),
        'currency': 'USD',
        'merchantId': config.get('merchant.id', 'test-merchant'),
        'description': 'Test payment transaction'
    }
    context.base_test.logger.info(f"Payment details prepared with amount: {amount}")


@given('I have valid payment details')
def step_have_valid_payment_details(context):
    """Prepare valid payment request data."""
    config = context.base_test.config
    context.request_data = {
        'amount': 100.00,
        'currency': 'USD',
        'merchantId': config.get('merchant.id', 'test-merchant'),
        'customerId': 'cust-12345',
        'description': 'Test payment transaction',
        'metadata': {
            'orderId': 'ORD-001',
            'source': 'web'
        }
    }
    context.base_test.logger.info("Valid payment details prepared")


@given('I have payment details with invalid merchant')
def step_have_invalid_merchant_payment(context):
    """Prepare payment request with invalid merchant ID."""
    context.request_data = {
        'amount': 100.00,
        'currency': 'USD',
        'merchantId': 'invalid-merchant-id',
        'description': 'Test payment'
    }
    context.base_test.logger.info("Payment details with invalid merchant prepared")


@when('I send payment request to "{endpoint}"')
def step_send_payment_request(context, endpoint):
    """Send payment request with authentication."""
    api_client = context.base_test.api_client
    headers = getattr(context, 'headers', {})
    request_data = getattr(context, 'request_data', {})
    
    context.response = api_client.post(
        endpoint=endpoint,
        json_data=request_data,
        headers=headers
    )
    context.base_test.logger.info(f"Payment request sent to {endpoint}")


@then('payment status should be "{expected_status}"')
def step_verify_payment_status(context, expected_status):
    """Verify payment status in response."""
    response_data = context.response.json()
    actual_status = response_data.get('status')
    
    assert actual_status == expected_status, \
        f"Expected payment status '{expected_status}', but got '{actual_status}'"
    
    context.base_test.logger.info(f"✅ Payment status is '{actual_status}'")


@then('I store the payment ID')
def step_store_payment_id(context):
    """Store payment ID from response for later use."""
    response_data = context.response.json()
    payment_id = response_data.get('paymentId')
    
    context.payment_id = payment_id
    context.base_test.logger.info(f"Stored payment ID: {payment_id}")
```

---

### Step 3: Update Configuration (if needed)

Add any new configuration parameters to `config/qa.yaml`:

```yaml
# Payment API Configuration
merchant:
  id: test-merchant-12345
  api_key: your-api-key-here

payment:
  default_currency: USD
  max_amount: 10000.00
  min_amount: 1.00
```

---

### Step 4: Run Tests

```bash
# Run new payment tests
behave -D env=qa features/payments.feature --tags=@payments \
  -f allure_behave.formatter:AllureFormatter \
  -o reports/allure-results

# Run specific scenario
behave -D env=qa features/payments.feature:10

# Run with specific tag
behave -D env=qa --tags=@smoke
```

---

## 🎯 Common API Patterns

### GET Request (Retrieve Data)
```gherkin
Scenario: Get payment details
  Given I have valid authentication token
  And I have a payment ID "PAY-12345"
  When I send GET request to "/api/v1/payments/{paymentId}"
  Then response status code should be 200
  And response body should contain "paymentId"
```

**Step Definition:**
```python
@given('I have a payment ID "{payment_id}"')
def step_have_payment_id(context, payment_id):
    context.payment_id = payment_id
    context.base_test.logger.info(f"Payment ID set: {payment_id}")

@when('I send GET request to "/api/v1/payments/{paymentId}"')
def step_get_payment_details(context):
    api_client = context.base_test.api_client
    endpoint = f"/api/v1/payments/{context.payment_id}"
    context.response = api_client.get(endpoint=endpoint)
```

### PUT Request (Update Data)
```gherkin
Scenario: Update payment status
  Given I have valid authentication token
  And I have a payment ID "PAY-12345"
  And I have updated payment status "completed"
  When I send PUT request to "/api/v1/payments/{paymentId}"
  Then response status code should be 200
```

**Step Definition:**
```python
@given('I have updated payment status "{status}"')
def step_have_updated_status(context, status):
    context.request_data = {'status': status}

@when('I send PUT request to "/api/v1/payments/{paymentId}"')
def step_update_payment(context):
    api_client = context.base_test.api_client
    endpoint = f"/api/v1/payments/{context.payment_id}"
    context.response = api_client.put(
        endpoint=endpoint,
        json_data=context.request_data
    )
```

### DELETE Request (Remove Data)
```gherkin
Scenario: Cancel a payment
  Given I have valid authentication token
  And I have a payment ID "PAY-12345"
  When I send DELETE request to "/api/v1/payments/{paymentId}"
  Then response status code should be 204
```

**Step Definition:**
```python
@when('I send DELETE request to "/api/v1/payments/{paymentId}"')
def step_delete_payment(context):
    api_client = context.base_test.api_client
    endpoint = f"/api/v1/payments/{context.payment_id}"
    context.response = api_client.delete(endpoint=endpoint)
```

---

## 🔐 Authentication Patterns

### Bearer Token Authentication
```python
@given('I have valid authentication token')
def step_have_auth_token(context):
    # Use token from previous authentication
    token = getattr(context, 'accessToken', '')
    context.headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
```

### API Key Authentication
```python
@given('I have valid API key')
def step_have_api_key(context):
    config = context.base_test.config
    context.headers = {
        'X-API-Key': config.get('api.key'),
        'Content-Type': 'application/json'
    }
```

### Basic Authentication
```python
@given('I have basic authentication credentials')
def step_have_basic_auth(context):
    import base64
    config = context.base_test.config
    username = config.get('auth.username')
    password = config.get('auth.password')
    credentials = f"{username}:{password}"
    encoded = base64.b64encode(credentials.encode()).decode()
    context.headers = {
        'Authorization': f'Basic {encoded}',
        'Content-Type': 'application/json'
    }
```

---

## 📊 Test Organization

### Use Tags Effectively
```gherkin
@smoke          # Critical tests that must pass
@regression     # Full test suite
@positive       # Happy path scenarios
@negative       # Error handling scenarios
@validation     # Data validation tests
@performance    # Response time tests
@security       # Authentication/authorization tests
```

### Run Tests by Tags
```bash
# Smoke tests only
behave --tags=@smoke

# All payment tests
behave --tags=@payments

# Negative tests for payments
behave --tags=@payments,@negative

# Exclude slow tests
behave --tags=~@slow
```

---

## ✅ Validation Checklist

After adding new API tests:

- [ ] Tests run successfully
- [ ] All scenarios pass
- [ ] Proper error handling for negative scenarios
- [ ] Response time validations added
- [ ] Authentication is secure (no hardcoded credentials)
- [ ] Documentation updated (README.md)
- [ ] Allure reports generated
- [ ] PDF report generated
- [ ] Code follows PEP 8 style guide
- [ ] Step definitions are reusable

---

## 🐛 Troubleshooting

### Test Fails with "Step not found"
**Solution:** Make sure step definition matches exactly (including quotes and parameters)

### Authentication Fails
**Solution:** Check if token is stored correctly from previous authentication step

### Response is Empty
**Solution:** Add `And I print the response` step to debug actual response

### Timeout Errors
**Solution:** Increase timeout in `config/qa.yaml` or check API performance

---

## 📚 Additional Resources

- **Common Steps:** `steps/common_steps.py` - Reusable HTTP and assertion steps
- **API Client:** `core/api_client.py` - HTTP methods and retry logic
- **Assertions:** `core/assertions.py` - 20+ validation methods
- **Config:** `config/qa.yaml` - Environment configuration

---

## 🎉 Example: Complete API Test Suite

See `features/appToken.feature` and `steps/appToken_steps.py` for a complete working example with:
- ✅ Positive scenarios
- ✅ Negative scenarios
- ✅ Validation tests
- ✅ Authentication flow
- ✅ Error handling
- ✅ Response time checks

---

**Happy Testing! 🚀**
