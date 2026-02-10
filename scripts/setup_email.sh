#!/bin/bash

###############################################################################
# Email Feature Setup Script
# Quick setup for email reporting functionality
###############################################################################

echo "╔═══════════════════════════════════════════════════╗"
echo "║                                                   ║"
echo "║   📧 Email Reporting Setup                        ║"
echo "║                                                   ║"
echo "╚═══════════════════════════════════════════════════╝"
echo ""

# Check if config exists
if [ ! -f "config/email_config.yaml" ]; then
    echo "❌ Email config not found: config/email_config.yaml"
    exit 1
fi

echo "✅ Email configuration found"
echo ""

# Check SMTP password
if [ -z "$SMTP_PASSWORD" ]; then
    echo "⚠️  SMTP_PASSWORD environment variable is not set"
    echo ""
    echo "📝 To set up Gmail App Password:"
    echo "   1. Enable 2-Factor Authentication in your Google Account"
    echo "   2. Go to: https://myaccount.google.com/apppasswords"
    echo "   3. Generate an App Password for 'Mail'"
    echo "   4. Set the password as environment variable:"
    echo ""
    echo "      export SMTP_PASSWORD='your-app-password-here'"
    echo ""
    echo "   5. Make it permanent by adding to ~/.zshrc:"
    echo ""
    echo "      echo 'export SMTP_PASSWORD=\"your-app-password\"' >> ~/.zshrc"
    echo "      source ~/.zshrc"
    echo ""
    read -p "Enter SMTP App Password (or press Enter to skip): " password
    
    if [ ! -z "$password" ]; then
        export SMTP_PASSWORD="$password"
        echo ""
        echo "✅ SMTP_PASSWORD set for this session"
        echo ""
        echo "💡 To make it permanent, run:"
        echo "   echo 'export SMTP_PASSWORD=\"$password\"' >> ~/.zshrc"
        echo "   source ~/.zshrc"
    fi
else
    echo "✅ SMTP_PASSWORD is set"
fi

echo ""
echo "📧 Current Email Configuration:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Parse and display config
python3 << 'PYTHON_SCRIPT'
import yaml

try:
    with open('config/email_config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    email_config = config.get('email', {})
    
    print(f"Status: {'✅ Enabled' if email_config.get('enabled') else '❌ Disabled'}")
    print(f"SMTP Server: {email_config.get('smtp', {}).get('server')}")
    print(f"SMTP Port: {email_config.get('smtp', {}).get('port')}")
    print(f"Sender: {email_config.get('sender', {}).get('email')}")
    print(f"Recipients (TO): {', '.join(email_config.get('recipients', {}).get('to', []))}")
    
    cc_list = email_config.get('recipients', {}).get('cc', [])
    if cc_list:
        print(f"Recipients (CC): {', '.join(cc_list)}")
    
    triggers = email_config.get('triggers', {})
    print(f"\nTriggers:")
    print(f"  - Send Always: {triggers.get('send_always')}")
    print(f"  - Send on Failure: {triggers.get('send_on_failure')}")
    print(f"  - Send on Success: {triggers.get('send_on_success')}")
    
except Exception as e:
    print(f"❌ Error reading config: {e}")
PYTHON_SCRIPT

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Test SMTP connection
if [ ! -z "$SMTP_PASSWORD" ]; then
    echo "🔍 Testing SMTP connection..."
    python3 << 'PYTHON_SCRIPT'
import smtplib
import yaml
import sys

try:
    with open('config/email_config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    smtp_config = config['email']['smtp']
    sender = config['email']['sender']['email']
    password = os.environ.get('SMTP_PASSWORD')
    
    if not password:
        print("❌ SMTP_PASSWORD not set")
        sys.exit(1)
    
    server = smtplib.SMTP(smtp_config['server'], smtp_config['port'], timeout=10)
    if smtp_config.get('use_tls'):
        server.starttls()
    server.login(sender, password)
    server.quit()
    
    print("✅ SMTP connection successful!")
    
except Exception as e:
    print(f"❌ SMTP connection failed: {str(e)}")
    print("\n💡 Common issues:")
    print("   - Wrong App Password")
    print("   - 2FA not enabled")
    print("   - Firewall blocking SMTP port")
    sys.exit(1)
PYTHON_SCRIPT
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Email reporting is ready!"
        echo ""
        echo "📝 Next steps:"
        echo "   1. Run tests: ./run_tests.sh -e qa -t @smoke"
        echo "   2. Email report will be sent automatically"
        echo "   3. Check your inbox: sunil.kumar8@kellton.com"
    fi
else
    echo "⚠️  SMTP_PASSWORD not configured. Email sending will be skipped."
fi

echo ""
echo "📚 For more information, see: docs/EMAIL_REPORTING.md"
echo ""
