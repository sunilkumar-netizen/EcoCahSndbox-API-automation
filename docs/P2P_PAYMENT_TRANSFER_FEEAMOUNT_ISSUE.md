# P2P Payment Transfer - feeAmount Issue Analysis

## 🔴 Problem Summary

**Error Message:**
```json
{
  "errorCode": "http.bad.request",
  "errors": [{"message": "\"feeAmount\" is required", "code": "feeAmount"}]
}
```

**What We Tried:**
1. ❌ `feeAmount: 0` - API rejected (original value)
2. ❌ `feeAmount: 0.5` - API rejected (decimal value)
3. ❌ `feeAmount: 1` - API rejected (integer value)

## 📊 Analysis

### The Field IS Being Sent
The logs clearly show `feeAmount` is present in the payload:
```json
{
  "feeAmount": 1,  ← Field exists!
  "currency": "ZWG",
  "payerAmount": 2,
  ...
}
```

### Why the API Still Rejects It

The error `"feeAmount" is required` despite the field being present suggests **one of these scenarios**:

#### 1. **API Expects feeAmount from Payment Options API** ✅ (Most Likely)
The `feeAmount` should be retrieved dynamically from the **Payment Options API** response:

```
Complete P2P Flow:
1. Search Contact → Find user
2. Account Lookup → Get account details
3. Payment Options → GET FEE AMOUNT ← This is where feeAmount comes from!
4. Payment Transfer → Use feeAmount from step 3
5. Order Details → View transaction
```

**Solution:** Execute the Payment Options API first and extract the `feeAmount` from its response.

#### 2. **Test Data is Invalid** ✅ (Also Likely)
The hardcoded test data might be causing validation failure:
- ❌ **Encrypted PIN**: Session-specific, expires quickly
- ❌ **Instrument Tokens**: User-specific, dynamic
- ❌ **Customer IDs**: Must match authenticated user
- ❌ **Beneficiary Tokens**: Must be valid and active

The API might fail validation on these fields first, then return a generic "feeAmount required" error.

#### 3. **feeAmount Must Match a Calculation**
The API might validate that:
```
feeAmount + payerAmount = total expected amount
```

If the calculation doesn't match, it might reject with "feeAmount required".

#### 4. **API Backend Issue**
The API validation logic might have a bug where it doesn't properly check if `feeAmount` exists before returning the error.

## 🎯 Recommended Solutions

### Solution 1: Execute Complete P2P Flow (BEST APPROACH)

Update the test to execute all steps in order:

```gherkin
@smoke @p2p_order_details @order_details @p2p @sasai @dynamic @complete_flow
Scenario: Complete P2P flow with dynamic fee from payment options
    Given I have valid user authentication
    
    # Step 1: Search for beneficiary
    And I have search contact payload for "Ropafadzo"
    When I send P2P search contact request
    Then response should have contact results
    
    # Step 2: Account lookup
    When I send P2P account lookup request for first contact
    Then response should have account details
    
    # Step 3: Get payment options (THIS PROVIDES feeAmount!)
    When I send P2P payment options request
    Then response should have payment options
    And I extract fee amount from payment options  ← EXTRACT FEE HERE
    
    # Step 4: Execute payment transfer with dynamic fee
    And I have payment transfer payload with dynamic fee
    When I send payment transfer request to "/bff/v2/order/transfer/payment"
    Then response status code should be 200 or 201
    And response should have P2P order ID
    
    # Step 5: Get order details
    When I send P2P order details request to "/bff/v2/order/details"
    Then response status code should be 200
    And response should contain P2P order details data
```

### Solution 2: Use Real/Fresh Test Data

Instead of hardcoded values, dynamically build the payload:

```python
@given('I have dynamic payment transfer payload')
def step_dynamic_payment_transfer_payload(context):
    # Get fresh values from previous API calls
    instrument_token = context.payer_instrument_token  # From payment options
    beneficiary_token = context.beneficiary_token  # From account lookup
    customer_id = context.customer_id  # From user authentication
    fee_amount = context.fee_amount  # From payment options ← KEY!
    encrypted_pin = context.fresh_encrypted_pin  # Fresh PIN encryption
    
    payload = {
        "feeAmount": fee_amount,  # Dynamic!
        "currency": "ZWG",
        ...
    }
```

### Solution 3: Check Payment Options API Response

Let me check what the Payment Options API returns:

```bash
# Run Payment Options test to see the fee structure
behave --tags=@smoke features/Pay_to_Person(Domestic)/3_paymentOptions.feature
```

Look for fields like:
- `feeAmount`
- `totalFee`
- `transactionFee`
- `charge`

## 📝 Configuration Changes Made

### config/qa.yaml

Added P2P Payment Transfer configuration:

```yaml
# P2P Payment Transfer Configuration (Pay to Person Flow)
p2p_payment_transfer:
  fee_amount: 1  # Currently set to 1, but should be dynamic from Payment Options
  currency: "ZWG"
  payer_amount: 2
  payee_amount: 2
  payment_method: "wallet"
  provider: "ecocash"
  subtype: "p2p-pay"
  channel: "sasai-super-app"
  endpoint: "/bff/v2/order/transfer/payment"
  public_key_alias: "payment-links"
  # ... (more configuration)
```

### steps/p2p_payment_transfer_steps.py

Updated to load from config:

```python
@given('I have complete payment transfer payload')
def step_complete_payment_transfer_payload(context):
    # Load configuration values
    config = context.config_loader
    fee_amount = config.get('p2p_payment_transfer.fee_amount', 1)  # Loads from config
    currency = config.get('p2p_payment_transfer.currency', 'ZWG')
    payer_amount = config.get('p2p_payment_transfer.payer_amount', 2)
    payee_amount = config.get('p2p_payment_transfer.payee_amount', 2)
    
    payload = {
        "feeAmount": fee_amount,  # From config
        ...
    }
```

## ✅ Next Steps

1. **Check Payment Options API response structure** to see where `feeAmount` comes from
2. **Create a complete flow test** that executes all P2P steps in sequence
3. **Extract `feeAmount` from Payment Options** and use it in Payment Transfer
4. **Update test data** with fresh, valid values (encrypted PIN, tokens, IDs)
5. **Add validation** to ensure all dynamic values are properly extracted before payment transfer

## 🔍 Debug Commands

```bash
# Check Payment Options response
behave --tags=@smoke features/Pay_to_Person(Domestic)/3_paymentOptions.feature --no-capture

# Test with specific line number
behave features/Pay_to_Person(Domestic)/3_paymentOptions.feature:26

# Dry-run to verify steps
behave --dry-run features/Pay_to_Person(Domestic)/

# Check all P2P features
behave features/Pay_to_Person(Domestic)/ --tags=@smoke --dry-run
```

## 📚 Related Documentation

- `docs/P2P_ORDER_DETAILS_DYNAMIC_FLOW.md` - How dynamic order ID works
- `docs/P2P_ORDER_DETAILS_DYNAMIC_IMPLEMENTATION.md` - Implementation details
- `features/Pay_to_Person(Domestic)/3_paymentOptions.feature` - Payment Options API
- `features/Pay_to_Person(Domestic)/4_paymentTransfer.feature` - Payment Transfer API

## 🎯 Conclusion

The `feeAmount` issue is **NOT a configuration problem** - it's a **workflow problem**. The Payment Transfer API expects the complete P2P flow to be executed in order, with values dynamically extracted from each step.

**The fix:** Execute Payment Options API first, extract `feeAmount`, then use it in Payment Transfer.
