#!/usr/bin/env python3
"""
Generate PDF Report from Test Results
Converts Allure test results into a professional PDF report for stakeholders
"""

import json
import os
from datetime import datetime
from pathlib import Path
from weasyprint import HTML, CSS

def load_allure_results():
    """Load and parse Allure test results"""
    results_dir = Path("reports/allure-results")
    
    scenarios = []
    total_duration = 0
    
    # Read all result JSON files
    for file in results_dir.glob("*-result.json"):
        with open(file, 'r') as f:
            data = json.load(f)
            
            status = data.get('status', 'unknown')
            name = data.get('name', 'Unknown')
            duration = data.get('time', {}).get('duration', 0) / 1000  # Convert to seconds
            
            scenarios.append({
                'name': name,
                'status': status,
                'duration': duration,
                'steps': len(data.get('steps', []))
            })
            
            total_duration += duration
    
    return scenarios, total_duration

def generate_html_report(scenarios, total_duration):
    """Generate HTML content for the report"""
    
    passed = sum(1 for s in scenarios if s['status'] == 'passed')
    failed = sum(1 for s in scenarios if s['status'] == 'failed')
    total = len(scenarios)
    pass_rate = (passed / total * 100) if total > 0 else 0
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Sasai API Test Report</title>
        <style>
            @page {{
                size: A4;
                margin: 2cm;
            }}
            
            body {{
                font-family: 'Helvetica', 'Arial', sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
            }}
            
            .header {{
                text-align: center;
                border-bottom: 3px solid #007bff;
                padding-bottom: 20px;
                margin-bottom: 30px;
            }}
            
            .header h1 {{
                color: #007bff;
                margin: 0;
                font-size: 32px;
            }}
            
            .header .subtitle {{
                color: #666;
                font-size: 16px;
                margin-top: 10px;
            }}
            
            .summary-box {{
                background: #f8f9fa;
                border-left: 5px solid #007bff;
                padding: 20px;
                margin: 30px 0;
                border-radius: 5px;
            }}
            
            .summary-box h2 {{
                margin-top: 0;
                color: #007bff;
            }}
            
            .stats-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                margin: 20px 0;
            }}
            
            .stat-card {{
                background: white;
                padding: 20px;
                border-radius: 8px;
                border: 1px solid #dee2e6;
                text-align: center;
            }}
            
            .stat-card .number {{
                font-size: 36px;
                font-weight: bold;
                margin: 10px 0;
            }}
            
            .stat-card .label {{
                color: #666;
                font-size: 14px;
                text-transform: uppercase;
            }}
            
            .stat-card.passed {{
                border-left: 5px solid #28a745;
            }}
            
            .stat-card.failed {{
                border-left: 5px solid #dc3545;
            }}
            
            .stat-card.total {{
                border-left: 5px solid #007bff;
            }}
            
            .stat-card.duration {{
                border-left: 5px solid #ffc107;
            }}
            
            .pass-rate {{
                font-size: 48px;
                font-weight: bold;
                color: {"#28a745" if pass_rate >= 75 else "#ffc107" if pass_rate >= 50 else "#dc3545"};
                text-align: center;
                margin: 30px 0;
            }}
            
            .test-cases {{
                margin: 30px 0;
            }}
            
            .test-cases h2 {{
                color: #007bff;
                border-bottom: 2px solid #007bff;
                padding-bottom: 10px;
            }}
            
            .test-case {{
                background: white;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                padding: 15px;
                margin: 15px 0;
                page-break-inside: avoid;
            }}
            
            .test-case.passed {{
                border-left: 5px solid #28a745;
            }}
            
            .test-case.failed {{
                border-left: 5px solid #dc3545;
            }}
            
            .test-case .name {{
                font-weight: bold;
                font-size: 16px;
                margin-bottom: 10px;
            }}
            
            .test-case .status {{
                display: inline-block;
                padding: 5px 15px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: bold;
                text-transform: uppercase;
            }}
            
            .test-case .status.passed {{
                background: #d4edda;
                color: #155724;
            }}
            
            .test-case .status.failed {{
                background: #f8d7da;
                color: #721c24;
            }}
            
            .test-case .meta {{
                color: #666;
                font-size: 14px;
                margin-top: 10px;
            }}
            
            .footer {{
                margin-top: 50px;
                padding-top: 20px;
                border-top: 2px solid #dee2e6;
                text-align: center;
                color: #666;
                font-size: 12px;
            }}
            
            .environment {{
                background: #e9ecef;
                padding: 15px;
                border-radius: 5px;
                margin: 20px 0;
            }}
            
            .environment h3 {{
                margin-top: 0;
                color: #495057;
            }}
            
            .environment table {{
                width: 100%;
                border-collapse: collapse;
            }}
            
            .environment td {{
                padding: 8px;
                border-bottom: 1px solid #dee2e6;
            }}
            
            .environment td:first-child {{
                font-weight: bold;
                width: 40%;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🚀 Sasai Payment Gateway</h1>
            <h2>API Test Execution Report</h2>
            <div class="subtitle">Generated on {timestamp}</div>
        </div>
        
        <div class="summary-box">
            <h2>📊 Executive Summary</h2>
            <p>Automated API testing for Sasai Payment Gateway App Token authentication endpoints.</p>
            
            <div class="pass-rate">
                {pass_rate:.1f}% Pass Rate
            </div>
            
            <div class="stats-grid">
                <div class="stat-card total">
                    <div class="label">Total Tests</div>
                    <div class="number">{total}</div>
                </div>
                <div class="stat-card passed">
                    <div class="label">Passed</div>
                    <div class="number" style="color: #28a745;">{passed}</div>
                </div>
                <div class="stat-card failed">
                    <div class="label">Failed</div>
                    <div class="number" style="color: #dc3545;">{failed}</div>
                </div>
                <div class="stat-card duration">
                    <div class="label">Total Duration</div>
                    <div class="number" style="color: #ffc107;">{total_duration:.2f}s</div>
                </div>
            </div>
        </div>
        
        <div class="environment">
            <h3>🔧 Test Environment</h3>
            <table>
                <tr>
                    <td>Environment:</td>
                    <td>QA Sandbox</td>
                </tr>
                <tr>
                    <td>Base URL:</td>
                    <td>https://sandbox.sasaipaymentgateway.com</td>
                </tr>
                <tr>
                    <td>Framework:</td>
                    <td>Python + Behave (BDD)</td>
                </tr>
                <tr>
                    <td>Test Type:</td>
                    <td>API Integration Testing</td>
                </tr>
                <tr>
                    <td>Execution Date:</td>
                    <td>{timestamp}</td>
                </tr>
            </table>
        </div>
        
        <div class="test-cases">
            <h2>📝 Test Cases Executed</h2>
    """
    
    # Add test cases
    for i, scenario in enumerate(scenarios, 1):
        status_class = scenario['status']
        status_text = scenario['status'].upper()
        
        html_content += f"""
            <div class="test-case {status_class}">
                <div class="name">
                    {i}. {scenario['name']}
                </div>
                <span class="status {status_class}">{status_text}</span>
                <div class="meta">
                    ⏱️ Duration: {scenario['duration']:.3f}s | 
                    📋 Steps: {scenario['steps']}
                </div>
            </div>
        """
    
    # Add footer
    html_content += """
        </div>
        
        <div class="footer">
            <p><strong>EcoCash API Automation Framework</strong></p>
            <p>Confidential - For Internal Use Only</p>
            <p>Report generated automatically by Allure + WeasyPrint</p>
        </div>
    </body>
    </html>
    """
    
    return html_content

def main():
    """Main function to generate PDF report"""
    print("🚀 Generating PDF Report from Allure Results...")
    print("=" * 70)
    
    # Load test results
    print("📊 Loading test results...")
    scenarios, total_duration = load_allure_results()
    print(f"✅ Loaded {len(scenarios)} test scenarios")
    
    # Generate HTML
    print("📝 Generating HTML content...")
    html_content = generate_html_report(scenarios, total_duration)
    
    # Create PDF output directory
    pdf_dir = Path("reports/pdf")
    pdf_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate PDF filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_filename = f"Sasai_API_Test_Report_{timestamp}.pdf"
    pdf_path = pdf_dir / pdf_filename
    
    # Convert HTML to PDF
    print("📄 Converting to PDF...")
    HTML(string=html_content).write_pdf(pdf_path)
    
    print("=" * 70)
    print("✅ PDF Report Generated Successfully!")
    print(f"📍 Location: {pdf_path}")
    print(f"📊 File Size: {pdf_path.stat().st_size / 1024:.2f} KB")
    print("=" * 70)
    print("\n🎉 You can now share this PDF with stakeholders!")
    
    # Open PDF automatically (macOS)
    import subprocess
    try:
        subprocess.run(["open", str(pdf_path)])
        print("📖 PDF opened in default viewer")
    except Exception:
        pass

if __name__ == "__main__":
    main()
