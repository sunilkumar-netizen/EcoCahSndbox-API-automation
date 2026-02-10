# 📧 Email Reporting Feature

## Overview
Automatically send test execution reports via email after test completion. Reports are sent in HTML format with detailed test results, metrics, and failure information.

## Configuration

### Email Settings
Edit `config/email_config.yaml` to configure email settings:

```yaml
email:
  enabled: true  # Enable/disable email reports
  
  smtp:
    server: "smtp.gmail.com"  # SMTP server
    port: 587                  # SMTP port
    use_tls: true             # Use TLS encryption
  
  sender:
    email: "sunil.kumar8@kellton.com"
    name: "EcoCash API Automation"
  
  recipients:
    to:
      - "sunil.kumar8@kellton.com"
    cc: []  # Optional CC recipients
    bcc: [] # Optional BCC recipients
```

## Setup Instructions

### 1. For Gmail Users (Recommended)

#### Step 1: Enable 2-Factor Authentication
1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable 2-Step Verification if not already enabled

#### Step 2: Generate App Password
1. Go to [App Passwords](https://myaccount.google.com/apppasswords)
2. Select "Mail" and "Other (Custom name)"
3. Name it "EcoCash API Automation"
4. Copy the generated 16-character password

#### Step 3: Set Environment Variable
```bash
# On macOS/Linux
export SMTP_PASSWORD="your-app-password-here"

# To make it permanent, add to ~/.zshrc or ~/.bashrc:
echo 'export SMTP_PASSWORD="your-app-password-here"' >> ~/.zshrc
source ~/.zshrc
```

### 2. For Other Email Providers

#### Microsoft Outlook/Office 365
```yaml
smtp:
  server: "smtp-mail.outlook.com"
  port: 587
  use_tls: true
```

#### Yahoo Mail
```yaml
smtp:
  server: "smtp.mail.yahoo.com"
  port: 587
  use_tls: true
```

#### Custom SMTP Server
```yaml
smtp:
  server: "smtp.your-company.com"
  port: 587
  use_tls: true
```

## Usage

### Automatic Email Sending
Email reports are sent automatically after test execution:

```bash
# Run tests - email will be sent automatically
./run_tests.sh -e qa -t @smoke
```

### Manual Email Sending
Send email report manually from existing test results:

```bash
python3 scripts/send_email_report.py qa "@smoke"
```

### Disable Email Temporarily
```bash
# Method 1: Disable in config
# Edit config/email_config.yaml and set enabled: false

# Method 2: Unset environment variable
unset SMTP_PASSWORD
```

## Email Trigger Conditions

Configure when emails should be sent in `email_config.yaml`:

```yaml
triggers:
  send_always: true        # Send after every test run
  send_on_failure: true    # Send when tests fail
  send_on_success: false   # Send only when all tests pass
```

### Examples:
- **Send all reports**: `send_always: true`
- **Send only failures**: `send_always: false, send_on_failure: true, send_on_success: false`
- **Send only success**: `send_always: false, send_on_failure: false, send_on_success: true`

## Email Content

The email report includes:

### 📊 Executive Summary
- Total tests executed
- Pass/Fail/Skip counts
- Overall pass rate
- Execution duration

### 📈 Test Coverage by Category
- Authentication & Login
- P2P Payments
- School Payments
- Church Payments
- Merchant Payments
- Offline Biller

### ❌ Failed Tests Details
- Feature name
- Test scenario
- Error messages

### 📁 Report Links
- Allure report location
- HTML report location
- Log files location

## Environment-Specific Recipients

Configure different recipients per environment:

```yaml
environments:
  qa:
    recipients:
      to:
        - "qa-team@kellton.com"
        
  uat:
    recipients:
      to:
        - "uat-team@kellton.com"
        - "manager@kellton.com"
        
  prod:
    recipients:
      to:
        - "prod-team@kellton.com"
        - "senior-manager@kellton.com"
      cc:
        - "cto@kellton.com"
```

## Troubleshooting

### Email Not Sending

**1. Check SMTP Password**
```bash
echo $SMTP_PASSWORD  # Should show your app password
```

**2. Check Email Configuration**
```bash
cat config/email_config.yaml
```

**3. Test SMTP Connection**
```bash
python3 -c "import smtplib; s=smtplib.SMTP('smtp.gmail.com', 587); s.starttls(); print('✅ Connection successful')"
```

**4. Check Error Logs**
```bash
# Look for email-related errors in logs
grep -i "email" logs/*.log
```

### Common Issues

#### "Authentication failed"
- **Solution**: Generate a new App Password from Google Account settings
- **Gmail**: Use App Password, not regular password
- **2FA**: Must be enabled for Gmail App Passwords

#### "Connection refused"
- **Solution**: Check SMTP server and port in config
- **Firewall**: Ensure port 587 (TLS) or 465 (SSL) is not blocked

#### "Sender address rejected"
- **Solution**: Verify sender email matches the Gmail account used for authentication

#### "No test results found"
- **Solution**: Ensure tests have run successfully and JUnit reports exist in `reports/junit/`

## Advanced Configuration

### Retry Settings
```yaml
settings:
  retry_count: 3  # Number of retry attempts
  timeout: 30     # SMTP timeout in seconds
```

### Content Settings
```yaml
content:
  subject_prefix: "[EcoCash API Tests]"
  include_summary: true
  include_failed_tests: true
```

## Security Best Practices

1. **Never commit passwords** to version control
2. **Use environment variables** for sensitive data
3. **Use App Passwords** instead of account passwords (for Gmail)
4. **Restrict access** to email configuration files
5. **Rotate passwords** regularly

## Testing Email Feature

### Test with Dry Run
```bash
# Set test mode in config
TEST_EMAIL=true python3 scripts/send_email_report.py qa "@smoke"
```

### Verify Email Content Locally
The HTML report can be previewed by opening it in a browser before sending:
```bash
open reports/allure-report/index.html
```

## CI/CD Integration

### Jenkins
```groovy
environment {
    SMTP_PASSWORD = credentials('smtp-password-id')
}
post {
    always {
        sh './run_tests.sh -e qa -t @smoke'
    }
}
```

### GitHub Actions
```yaml
env:
  SMTP_PASSWORD: ${{ secrets.SMTP_PASSWORD }}
steps:
  - name: Run tests and send email
    run: ./run_tests.sh -e qa -t @smoke
```

## Support

For issues or questions:
1. Check this documentation
2. Review email configuration: `config/email_config.yaml`
3. Check application logs: `logs/`
4. Contact: sunil.kumar8@kellton.com

---

**Last Updated**: February 9, 2026  
**Version**: 1.0.0
