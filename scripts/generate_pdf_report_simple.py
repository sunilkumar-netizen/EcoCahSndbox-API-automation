#!/usr/bin/env python3
"""
Generate Professional PDF Report from Allure Test Results
Uses ReportLab for PDF generation - simple and reliable
"""

import json
import os
from datetime import datetime
from pathlib import Path
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.platypus import Image as RLImage
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

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

def create_pdf_report(scenarios, total_duration, filename):
    """Create PDF report using ReportLab"""
    
    # Create PDF document
    doc = SimpleDocTemplate(filename, pagesize=A4,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.HexColor('#007bff'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=16,
        textColor=colors.HexColor('#666666'),
        spaceAfter=12,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=18,
        textColor=colors.HexColor('#007bff'),
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold'
    )
    
    # Calculate statistics
    passed = sum(1 for s in scenarios if s['status'] == 'passed')
    failed = sum(1 for s in scenarios if s['status'] == 'failed')
    total = len(scenarios)
    pass_rate = (passed / total * 100) if total > 0 else 0
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Title
    elements.append(Paragraph("🚀 Sasai Payment Gateway", title_style))
    elements.append(Paragraph("API Test Execution Report", title_style))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Generated on {timestamp}", subtitle_style))
    elements.append(Spacer(1, 30))
    
    # Executive Summary
    elements.append(Paragraph("📊 Executive Summary", heading_style))
    elements.append(Paragraph("Automated API testing for Sasai Payment Gateway App Token authentication endpoints.", 
                             styles['Normal']))
    elements.append(Spacer(1, 20))
    
    # Pass Rate - Large and prominent
    pass_rate_color = colors.green if pass_rate >= 75 else colors.orange if pass_rate >= 50 else colors.red
    pass_rate_style = ParagraphStyle(
        'PassRate',
        parent=styles['Normal'],
        fontSize=48,
        textColor=pass_rate_color,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    elements.append(Paragraph(f"{pass_rate:.1f}% Pass Rate", pass_rate_style))
    elements.append(Spacer(1, 30))
    
    # Statistics Table
    stats_data = [
        ['Metric', 'Value'],
        ['Total Tests', str(total)],
        ['Passed', str(passed)],
        ['Failed', str(failed)],
        ['Total Duration', f'{total_duration:.2f}s'],
        ['Average Duration', f'{total_duration/total:.2f}s' if total > 0 else 'N/A']
    ]
    
    stats_table = Table(stats_data, colWidths=[3*inch, 2*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#007bff')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
    ]))
    
    elements.append(stats_table)
    elements.append(Spacer(1, 30))
    
    # Test Environment
    elements.append(Paragraph("🔧 Test Environment", heading_style))
    
    env_data = [
        ['Environment:', 'QA Sandbox'],
        ['Base URL:', 'https://sandbox.sasaipaymentgateway.com'],
        ['Framework:', 'Python + Behave (BDD)'],
        ['Test Type:', 'API Integration Testing'],
        ['Execution Date:', timestamp]
    ]
    
    env_table = Table(env_data, colWidths=[2*inch, 4*inch])
    env_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    
    elements.append(env_table)
    elements.append(Spacer(1, 30))
    
    # Test Cases
    elements.append(Paragraph("📝 Test Cases Executed", heading_style))
    elements.append(Spacer(1, 12))
    
    # Test cases table
    test_data = [['#', 'Test Case', 'Status', 'Duration', 'Steps']]
    
    for i, scenario in enumerate(scenarios, 1):
        status_symbol = '✅' if scenario['status'] == 'passed' else '❌'
        test_data.append([
            str(i),
            scenario['name'][:60],  # Truncate long names
            f"{status_symbol} {scenario['status'].upper()}",
            f"{scenario['duration']:.3f}s",
            str(scenario['steps'])
        ])
    
    test_table = Table(test_data, colWidths=[0.4*inch, 3.5*inch, 1.2*inch, 0.8*inch, 0.6*inch])
    
    # Create table style
    table_style = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#007bff')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]
    
    # Add row colors based on status
    for i, scenario in enumerate(scenarios, 1):
        if scenario['status'] == 'passed':
            table_style.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor('#d4edda')))
        else:
            table_style.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor('#f8d7da')))
    
    test_table.setStyle(TableStyle(table_style))
    elements.append(test_table)
    
    # Footer
    elements.append(Spacer(1, 50))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    elements.append(Paragraph("_" * 80, footer_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("<b>EcoCash API Automation Framework</b>", footer_style))
    elements.append(Paragraph("Confidential - For Internal Use Only", footer_style))
    elements.append(Paragraph("Report generated automatically by Allure + ReportLab", footer_style))
    
    # Build PDF
    doc.build(elements)

def main():
    """Main function to generate PDF report"""
    print("🚀 Generating PDF Report from Allure Results...")
    print("=" * 70)
    
    # Load test results
    print("📊 Loading test results...")
    scenarios, total_duration = load_allure_results()
    print(f"✅ Loaded {len(scenarios)} test scenarios")
    
    # Create PDF output directory
    pdf_dir = Path("reports/pdf")
    pdf_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate PDF filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_filename = f"Sasai_API_Test_Report_{timestamp}.pdf"
    pdf_path = pdf_dir / pdf_filename
    
    # Generate PDF
    print("📄 Generating PDF report...")
    create_pdf_report(scenarios, total_duration, str(pdf_path))
    
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
    
    return str(pdf_path)

if __name__ == "__main__":
    main()
