# 📧 Email Reporting Feature - Quick Start Guide

## ✅ What Was Added

### 1. Configuration File
**File:** `config/email_config.yaml`
- SMTP settings (Gmail configured by default)
- Sender: sunil.kumar8@kellton.com
- Recipients: sunil.kumar8@kellton.com
- Email triggers and conditions
- Environment-specific recipient lists

### 2. Email Report Script
**File:** `scripts/send_email_report.py`
- Parses JUnit test results
- Generates beautiful HTML email reports
- Sends emails via SMTP
- Automatic retry on failure
- Detailed test metrics and failure information

### 3. Test Runner Integration
**File:** `run_tests.sh` (Updated)
- Automatically sends email after test execution
- Integrated with existing test workflow

### 4. Setup Script
**File:** `scripts/setup_email.sh`
- Quick setup wizard
- Tests SMTP connection
- Validates configuration

### 5. Documentation
**File:** `docs/EMAIL_REPORTING.md`
- Complete setup instructions
- Troubleshooting guide
- Configuration options
- CI/CD integration examples

## 🚀 Quick Setup (5 Minutes)

### Step 1: Generate Gmail App Password

1. Go to Google Account: https://myaccount.google.com/security
2. Enable 2-Step Verification (if not already enabled)
3. Go to App Passwords: https://myaccount.google.com/apppasswords
4. Select "Mail" and "Other (Custom name)"
5. Name it: "EcoCash API Automation"
6. Copy the 16-character password

### Step 2: Set Environment Variable

```bash
# Set for current session
export SMTP_PASSWORD="your-16-character-app-password"

# Make it permanent
echo 'export SMTP_PASSWORD="your-16-character-app-password"' >> ~/.zshrc
source ~/.zshrc
```

### Step 3: Verify Setup

```bash
# Run the setup script
./scripts/setup_email.sh
```

This will:
- ✅ Check configuration
- ✅ Test SMTP connection
- ✅ Verify email settings

### Step 4: Test Email Sending

```bash
# Run smoke tests - email will be sent automatically
./run_tests.sh -e qa -t @smoke
```

## 📧 Email Report Contents

Your email will include:

### Header Section
- ✅ Test status (PASSED/FAILED)
- 📊 Environment and tags
- ⏱️ Execution timestamp

### Executive Summary (Metrics Cards)
- Total tests executed
- ✅ Passed tests
- ❌ Failed tests
- ⏭️ Skipped tests
- 📈 Pass rate percentage
- ⏱️ Total execution time

### Test Coverage by Category
Beautiful table showing:
- 🔐 Authentication & Login
- 👥 P2P Payments
- 🎓 School Payments
- ⛪ Church Payments
- 🏪 Merchant Payments
- 📴 Offline Biller

### Failed Tests Details (if any)
- Feature name
- Test scenario
- Error message

### Report Links
- Allure report location
- HTML report location
- Log files location

## 🎯 Configuration Options

### Enable/Disable Email
Edit `config/email_config.yaml`:
```yaml
email:
  enabled: true  # Set to false to disable
```

### Change Recipients
```yaml
recipients:
  to:
    - "sunil.kumar8@kellton.com"
    - "another@email.com"
  cc:
    - "manager@kellton.com"
```

### Email Triggers
```yaml
triggers:
  send_always: true        # Send after every run
  send_on_failure: true    # Send when tests fail
  send_on_success: false   # Send only on success
```

## 🔧 Troubleshooting

### Email Not Sending?

**1. Check SMTP Password**
```bash
echo $SMTP_PASSWORD  # Should show your app password
```

**2. Run Setup Script**
```bash
./scripts/setup_email.sh
```

**3. Test SMTP Connection**
```bash
python3 << 'EOF'
import smtplib
server = smtplib.SMTP('smtp.gmail.com', 587, timeout=10)
server.starttls()
server.login('sunil.kumar8@kellton.com', 'your-app-password')
server.quit()
print("✅ Connection successful!")
EOF
```

### Common Issues

| Issue | Solution |
|-------|----------|
| "Authentication failed" | Generate new App Password |
| "Connection refused" | Check firewall, use port 587 |
| "No test results" | Run tests first to generate reports |
| "Password not set" | Set SMTP_PASSWORD environment variable |

## 📝 Manual Email Sending

Send email report from existing test results:

```bash
python3 scripts/send_email_report.py qa "@smoke"
```

## 🔐 Security Notes

- ✅ Never commit SMTP_PASSWORD to git
- ✅ Use App Passwords (not account password)
- ✅ Rotate passwords regularly
- ✅ Keep email_config.yaml secure

## 📞 Support

For questions or issues:
- **Email:** sunil.kumar8@kellton.com
- **Documentation:** docs/EMAIL_REPORTING.md

## ✨ Sample Email Preview

Your email will look like this:

```
┌─────────────────────────────────────────────────┐
│  📊 EcoCash API Automation Test Report         │
│  Generated: 2026-02-09 14:30:00                 │
│  Environment: QA | Tags: @smoke                 │
└─────────────────────────────────────────────────┘

        ✅ ALL TESTS PASSED

┌──────────────┬──────────┐
│ Total Tests  │    25    │
│ ✅ Passed    │    23    │
│ ❌ Failed    │     2    │
│ ⏭️ Skipped   │     0    │
│ Pass Rate    │  92.0%   │
│ Duration     │  2m 40s  │
└──────────────┴──────────┘

📊 Test Coverage by Category
================================
| Category              | Total | Passed | Failed |
|----------------------|-------|--------|--------|
| 🔐 Authentication    |   5   |   5    |   0    |
| 🎓 School Payments   |   5   |   5    |   0    |
| 🏪 Merchant Payments |   4   |   4    |   0    |
| ⛪ Church Payments    |   5   |   5    |   0    |
| 👥 P2P Payments      |   6   |   4    |   2    |

📁 Detailed Reports Available
- Allure Report: reports/allure-report/index.html
- HTML Report: reports/html-report/report.html
- Log Files: logs/
```

---

**Ready to use!** Just set your SMTP_PASSWORD and run tests! 🚀
