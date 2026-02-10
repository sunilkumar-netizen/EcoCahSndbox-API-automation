#!/usr/bin/env python3
"""
Email Test Report Generator and Sender
Generates email-friendly Markdown report and sends via SMTP
"""

import os
import sys
import smtplib
import yaml
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from datetime import datetime
import xml.etree.ElementTree as ET


class EmailReportGenerator:
    def __init__(self, config_file='config/email_config.yaml'):
        self.project_root = Path(__file__).parent.parent
        self.config = self.load_config(config_file)
        self.results = None
        
    def load_config(self, config_file):
        """Load email configuration"""
        config_path = self.project_root / config_file
        if not config_path.exists():
            print(f"❌ Email config not found: {config_path}")
            sys.exit(1)
            
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def parse_junit_results(self, junit_dir):
        """Parse JUnit XML files to extract test results"""
        results = {
            'total': 0,
            'passed': 0,
            'failed': 0,
            'skipped': 0,
            'duration': 0,
            'features': [],
            'failed_tests': [],
            'categories': {}
        }
        
        junit_path = Path(junit_dir)
        if not junit_path.exists():
            return results
        
        for xml_file in junit_path.glob('TESTS-*.xml'):
            try:
                tree = ET.parse(xml_file)
                root = tree.getroot()
                
                # Check if root is testsuite or contains testsuites
                testsuites = root.findall('.//testsuite') if root.tag != 'testsuite' else [root]
                
                for testsuite in testsuites:
                    feature_name = testsuite.get('name', 'Unknown Feature')
                    
                    # Clean up feature name - remove file path prefix
                    # Format: "Pay_to_Person(Domestic).4_paymentTransfer.P2P Payment Transfer API"
                    # We want: "P2P Payment Transfer API"
                    if '.' in feature_name:
                        # Split by dots and take the last part (actual feature name)
                        feature_name = feature_name.split('.')[-1].strip()
                    
                    tests = int(testsuite.get('tests', 0))
                    failures = int(testsuite.get('failures', 0))
                    errors = int(testsuite.get('errors', 0))
                    skipped = int(testsuite.get('skipped', 0))
                    time = float(testsuite.get('time', 0))
                    
                    passed = tests - failures - errors - skipped
                    
                    results['total'] += tests
                    results['passed'] += passed
                    results['failed'] += failures + errors
                    results['skipped'] += skipped
                    results['duration'] += time
                    
                    # Categorize feature
                    category = self.categorize_feature(feature_name)
                    if category not in results['categories']:
                        results['categories'][category] = {
                            'total': 0, 'passed': 0, 'failed': 0, 'skipped': 0
                        }
                    results['categories'][category]['total'] += tests
                    results['categories'][category]['passed'] += passed
                    results['categories'][category]['failed'] += failures + errors
                    results['categories'][category]['skipped'] += skipped
                    
                    # Store feature details
                    status = '✅ PASSED' if failures + errors == 0 else '❌ FAILED'
                    results['features'].append({
                        'name': feature_name,
                        'total': tests,
                        'passed': passed,
                        'failed': failures + errors,
                        'skipped': skipped,
                        'duration': time,
                        'status': status,
                        'category': category
                    })
                    
                    # Get failed test details
                    for testcase in testsuite.findall('.//testcase'):
                        failure = testcase.find('failure')
                        error = testcase.find('error')
                        if failure is not None or error is not None:
                            # Extract scenario name from testcase name
                            test_name = testcase.get('name', 'Unknown Test')
                            
                            # Clean up scenario name - remove line numbers and extra info
                            scenario_name = test_name
                            if '--' in scenario_name:
                                # Format: "Scenario: Name -- @line_number"
                                scenario_name = scenario_name.split('--')[0].strip()
                            
                            # Extract just the scenario description if it starts with "Scenario:"
                            if scenario_name.startswith('Scenario:'):
                                scenario_name = scenario_name.replace('Scenario:', '').strip()
                            
                            error_elem = failure if failure is not None else error
                            error_msg = error_elem.get('message', 'Unknown error') if error_elem is not None else 'Unknown error'
                            
                            results['failed_tests'].append({
                                'feature': feature_name,  # Full feature name from testsuite
                                'scenario': scenario_name,  # Cleaned scenario name
                                'error': error_msg[:200] + '...' if len(error_msg) > 200 else error_msg
                            })
            except Exception as e:
                print(f"⚠️ Error parsing {xml_file}: {e}")
        
        return results
    
    def categorize_feature(self, feature_name):
        """Categorize feature by name"""
        feature_lower = feature_name.lower()
        if any(x in feature_lower for x in ['login', 'otp', 'pin', 'token', 'auth']):
            return '🔐 Authentication & Login'
        elif any(x in feature_lower for x in ['p2p', 'person', 'transfer']):
            return '👥 P2P Payments'
        elif 'school' in feature_lower:
            return '🎓 School Payments'
        elif 'church' in feature_lower:
            return '⛪ Church Payments'
        elif any(x in feature_lower for x in ['merchant', 'utility']):
            return '🏪 Merchant Payments'
        elif 'offline' in feature_lower:
            return '📴 Offline Biller'
        else:
            return '📦 Other'
    
    def format_duration(self, seconds):
        """Format duration"""
        if seconds < 60:
            return f"{seconds:.2f}s"
        elif seconds < 3600:
            return f"{int(seconds // 60)}m {seconds % 60:.2f}s"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}h {minutes}m"
    
    def generate_html_report(self, env, tags):
        """Generate HTML formatted email report"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        results = self.results
        
        # Calculate pass rate
        pass_rate = (results['passed'] / results['total'] * 100) if results['total'] > 0 else 0
        
        # Determine overall status
        if results['failed'] == 0:
            status_color = "#28a745"  # Green
            status_text = "✅ ALL TESTS PASSED"
            status_bg = "#d4edda"
        else:
            status_color = "#dc3545"  # Red
            status_text = f"❌ {results['failed']} TEST(S) FAILED"
            status_bg = "#f8d7da"
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 900px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                .container {{
                    background-color: white;
                    border-radius: 8px;
                    padding: 30px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    border-radius: 8px;
                    margin-bottom: 30px;
                    text-align: center;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 28px;
                }}
                .header p {{
                    margin: 10px 0 0 0;
                    opacity: 0.9;
                }}
                .status-banner {{
                    background-color: {status_bg};
                    border-left: 4px solid {status_color};
                    padding: 20px;
                    margin: 20px 0;
                    border-radius: 4px;
                }}
                .status-banner h2 {{
                    margin: 0;
                    color: {status_color};
                    font-size: 24px;
                }}
                .metrics {{
                    margin: 30px 0;
                    width: 100%;
                }}
                .metrics-table {{
                    width: 100%;
                    border-collapse: separate;
                    border-spacing: 15px;
                }}
                .metric-card {{
                    background: white;
                    padding: 25px 15px;
                    border-radius: 12px;
                    text-align: center;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    border: 2px solid #e9ecef;
                    vertical-align: middle;
                }}
                .metric-card .value {{
                    font-size: 42px;
                    font-weight: bold;
                    margin: 15px 0 10px 0;
                    line-height: 1;
                    display: block;
                }}
                .metric-card .label {{
                    font-size: 13px;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                    font-weight: 600;
                    margin-bottom: 5px;
                    display: block;
                }}
                .metric-card.total {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border-color: #667eea;
                }}
                .metric-card.total .value,
                .metric-card.total .label {{
                    color: white;
                }}
                .metric-card.passed {{
                    background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                    border-color: #11998e;
                }}
                .metric-card.passed .value,
                .metric-card.passed .label {{ 
                    color: white;
                }}
                
                .metric-card.failed {{
                    background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
                    border-color: #eb3349;
                }}
                .metric-card.failed .value,
                .metric-card.failed .label {{ 
                    color: white;
                }}
                
                .metric-card.skipped {{
                    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                    border-color: #f093fb;
                }}
                .metric-card.skipped .value,
                .metric-card.skipped .label {{ 
                    color: white;
                }}
                
                .metric-card.passrate {{
                    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                    border-color: #4facfe;
                }}
                .metric-card.passrate .value,
                .metric-card.passrate .label {{ 
                    color: white;
                }}
                
                .metric-card.duration {{
                    background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
                    border-color: #fa709a;
                }}
                .metric-card.duration .value {{ 
                    font-size: 28px;
                    color: white;
                }}
                .metric-card.duration .label {{ 
                    color: white;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                    background: white;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }}
                th {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 12px;
                    text-align: left;
                    font-weight: 600;
                }}
                td {{
                    padding: 12px;
                    border-bottom: 1px solid #e9ecef;
                }}
                tr:hover {{
                    background-color: #f8f9fa;
                }}
                .section-title {{
                    font-size: 20px;
                    color: #667eea;
                    margin: 30px 0 15px 0;
                    padding-bottom: 10px;
                    border-bottom: 2px solid #667eea;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 40px;
                    padding-top: 20px;
                    border-top: 1px solid #dee2e6;
                    color: #6c757d;
                    font-size: 14px;
                }}
                .badge {{
                    display: inline-block;
                    padding: 4px 8px;
                    border-radius: 4px;
                    font-size: 12px;
                    font-weight: bold;
                }}
                .badge-success {{ background-color: #d4edda; color: #155724; }}
                .badge-danger {{ background-color: #f8d7da; color: #721c24; }}
                .info-box {{
                    background-color: #e7f3ff;
                    border-left: 4px solid #2196F3;
                    padding: 15px;
                    margin: 20px 0;
                    border-radius: 4px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📊 OneApp API Automation Execution Report</h1>
                    <p>Generated: {timestamp}</p>
                    <p>Environment: <strong>{env.upper()}</strong> | Tags: <strong>{tags if tags else 'All Tests'}</strong></p>
                </div>
                
                <div class="status-banner">
                    <h2>{status_text}</h2>
                </div>
                
                <div class="metrics">
                    <table class="metrics-table" cellpadding="0" cellspacing="0">
                        <tr>
                            <td class="metric-card total">
                                <span class="label">Total Tests</span>
                                <span class="value">{results['total']}</span>
                            </td>
                            <td class="metric-card passed">
                                <span class="label">✅ Passed</span>
                                <span class="value">{results['passed']}</span>
                            </td>
                            <td class="metric-card failed">
                                <span class="label">❌ Failed</span>
                                <span class="value">{results['failed']}</span>
                            </td>
                        </tr>
                        <tr>
                            <td class="metric-card skipped">
                                <span class="label">⏭️ Skipped</span>
                                <span class="value">{results['skipped']}</span>
                            </td>
                            <td class="metric-card passrate">
                                <span class="label">Pass Rate</span>
                                <span class="value">{pass_rate:.1f}%</span>
                            </td>
                            <td class="metric-card duration">
                                <span class="label">Duration</span>
                                <span class="value">{self.format_duration(results['duration'])}</span>
                            </td>
                        </tr>
                    </table>
                </div>
                
                <h2 class="section-title">📊 Test Coverage by Category</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Category</th>
                            <th>Total</th>
                            <th>Passed</th>
                            <th>Failed</th>
                            <th>Pass Rate</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        for category, stats in sorted(results['categories'].items()):
            cat_pass_rate = (stats['passed'] / stats['total'] * 100) if stats['total'] > 0 else 0
            status_badge = '<span class="badge badge-success">✅ PASSED</span>' if stats['failed'] == 0 else '<span class="badge badge-danger">❌ FAILED</span>'
            html += f"""
                        <tr>
                            <td>{category} {status_badge}</td>
                            <td>{stats['total']}</td>
                            <td style="color: #28a745; font-weight: bold;">{stats['passed']}</td>
                            <td style="color: #dc3545; font-weight: bold;">{stats['failed']}</td>
                            <td><strong>{cat_pass_rate:.1f}%</strong></td>
                        </tr>
            """
        
        html += """
                    </tbody>
                </table>
        """
        
        # Failed tests section
        if results['failed_tests']:
            html += """
                <h2 class="section-title">❌ Failed Tests Details</h2>
                <table>
                    <thead>
                        <tr>
                            <th style="width: 35%;">Feature</th>
                            <th style="width: 40%;">Test Scenario</th>
                            <th style="width: 25%;">Error Message</th>
                        </tr>
                    </thead>
                    <tbody>
            """
            
            for failed in results['failed_tests']:
                # Format feature name with proper styling
                feature_display = failed['feature']
                
                # Format scenario name with emoji if present
                scenario_display = failed['scenario']
                
                # Truncate error message for readability but show more
                error_display = failed['error']
                
                html += f"""
                        <tr>
                            <td style="font-weight: 600; color: #495057;">{feature_display}</td>
                            <td style="color: #6c757d;">{scenario_display}</td>
                            <td style="color: #dc3545; font-size: 11px; font-family: 'Courier New', monospace;">{error_display}</td>
                        </tr>
                """
            
            html += """
                    </tbody>
                </table>
            """
        
        # Report links
        html += f"""
                <div class="info-box">
                    <h3 style="margin-top: 0;">📁 Detailed Reports Available</h3>
                    <ul>
                        <li><strong>Allure Report:</strong> reports/allure-report/index.html</li>
                        <li><strong>HTML Report:</strong> reports/html-report/report.html</li>
                        <li><strong>Log Files:</strong> logs/</li>
                    </ul>
                </div>
                
                <div class="footer">
                    <p>This report was automatically generated by EcoCash API Automation Framework</p>
                    <p>© {datetime.now().year} Kellton Tech | EcoCash API Testing</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def send_email(self, env, tags):
        """Send email report"""
        email_config = self.config['email']
        
        # Check if email is enabled
        if not email_config.get('enabled', True):
            print("📧 Email reporting is disabled in configuration")
            return False
        
        # Check triggers
        triggers = email_config.get('triggers', {})
        if not triggers.get('send_always', True):
            if self.results['failed'] > 0 and not triggers.get('send_on_failure', True):
                print("📧 Skipping email (send_on_failure=false)")
                return False
            if self.results['failed'] == 0 and not triggers.get('send_on_success', False):
                print("📧 Skipping email (send_on_success=false and all tests passed)")
                return False
        
        # Get SMTP settings
        smtp_config = email_config['smtp']
        sender_config = email_config['sender']
        recipients_config = email_config['recipients']
        content_config = email_config.get('content', {})
        
        # Get password from environment or config
        password = os.getenv('SMTP_PASSWORD') or sender_config.get('password', '')
        if not password:
            print("❌ SMTP password not configured. Set SMTP_PASSWORD environment variable.")
            print("   For Gmail, use App Password: https://support.google.com/accounts/answer/185833")
            return False
        
        # Get username (for Mailjet/other SMTP services that use API keys)
        username = sender_config.get('username') or sender_config.get('email')
        
        # Create message
        msg = MIMEMultipart('alternative')
        
        # Subject with timestamp replacement
        subject_prefix = content_config.get('subject_prefix', '[EcoCash API Tests]')
        # Replace {timestamp} placeholder with current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        subject_prefix = subject_prefix.replace('{timestamp}', timestamp)
        
        status = "✅ PASSED" if self.results['failed'] == 0 else f"❌ FAILED ({self.results['failed']} failures)"
        msg['Subject'] = f"{subject_prefix} {status} - {env.upper()} Environment"
        msg['From'] = f"{sender_config.get('name', 'EcoCash Automation')} <{sender_config['email']}>"
        
        # Recipients
        to_addresses = recipients_config.get('to', [])
        cc_addresses = recipients_config.get('cc', [])
        bcc_addresses = recipients_config.get('bcc', [])
        
        msg['To'] = ', '.join(to_addresses)
        if cc_addresses:
            msg['CC'] = ', '.join(cc_addresses)
        
        # Generate HTML content
        html_content = self.generate_html_report(env, tags)
        
        # Attach HTML
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        # Send email with retry
        retry_count = email_config.get('settings', {}).get('retry_count', 3)
        timeout = email_config.get('settings', {}).get('timeout', 30)
        
        for attempt in range(retry_count):
            try:
                print(f"📧 Sending email report (attempt {attempt + 1}/{retry_count})...")
                
                # Connect to SMTP server
                if smtp_config.get('use_ssl', False):
                    server = smtplib.SMTP_SSL(smtp_config['server'], smtp_config['port'], timeout=timeout)
                else:
                    server = smtplib.SMTP(smtp_config['server'], smtp_config['port'], timeout=timeout)
                    if smtp_config.get('use_tls', True):
                        server.starttls()
                
                # Login
                server.login(username, password)
                
                # Send email
                all_recipients = to_addresses + cc_addresses + bcc_addresses
                server.sendmail(sender_config['email'], all_recipients, msg.as_string())
                server.quit()
                
                print(f"✅ Email sent successfully to: {', '.join(to_addresses)}")
                if cc_addresses:
                    print(f"   CC: {', '.join(cc_addresses)}")
                return True
                
            except Exception as e:
                print(f"❌ Failed to send email (attempt {attempt + 1}): {str(e)}")
                if attempt == retry_count - 1:
                    return False
        
        return False


def main():
    """Main function"""
    # Get environment and tags from command line or environment variables
    env = sys.argv[1] if len(sys.argv) > 1 else os.getenv('TEST_ENV', 'qa')
    tags = sys.argv[2] if len(sys.argv) > 2 else os.getenv('TEST_TAGS', '')
    
    print("="*80)
    print("📧 Email Test Report Generator")
    print("="*80)
    
    # Initialize generator
    generator = EmailReportGenerator()
    
    # Parse test results
    junit_dir = generator.project_root / 'reports' / 'junit'
    print(f"📊 Parsing test results from: {junit_dir}")
    
    generator.results = generator.parse_junit_results(junit_dir)
    
    if generator.results['total'] == 0:
        print("⚠️ No test results found. Skipping email report.")
        return 1
    
    print(f"✅ Found {generator.results['total']} tests")
    print(f"   Passed: {generator.results['passed']}")
    print(f"   Failed: {generator.results['failed']}")
    print(f"   Skipped: {generator.results['skipped']}")
    print()
    
    # Send email
    success = generator.send_email(env, tags)
    
    print("="*80)
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
