#!/bin/bash
# Generate PDF Report from Allure HTML Report
# This script converts the Allure HTML report to PDF for stakeholders

echo "🚀 Generating PDF Report from Allure HTML Report..."
echo "=========================================="

# Check if wkhtmltopdf is installed
if ! command -v wkhtmltopdf &> /dev/null; then
    echo "❌ wkhtmltopdf is not installed"
    echo "📦 Installing wkhtmltopdf..."
    
    # Check OS and install accordingly
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            echo "Installing via Homebrew..."
            brew install --cask wkhtmltopdf
        else
            echo "❌ Homebrew not found. Please install wkhtmltopdf manually from:"
            echo "   https://wkhtmltopdf.org/downloads.html"
            exit 1
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        sudo apt-get update && sudo apt-get install -y wkhtmltopdf
    else
        echo "❌ Unsupported OS. Please install wkhtmltopdf manually from:"
        echo "   https://wkhtmltopdf.org/downloads.html"
        exit 1
    fi
fi

# Paths
ALLURE_REPORT_DIR="reports/allure-report"
PDF_OUTPUT_DIR="reports/pdf"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
PDF_FILENAME="Sasai_API_Test_Report_${TIMESTAMP}.pdf"

# Create PDF output directory
mkdir -p "$PDF_OUTPUT_DIR"

# Check if Allure report exists
if [ ! -f "$ALLURE_REPORT_DIR/index.html" ]; then
    echo "❌ Allure report not found at $ALLURE_REPORT_DIR/index.html"
    echo "Please generate Allure report first using:"
    echo "   allure generate reports/allure-results --clean -o reports/allure-report"
    exit 1
fi

echo "📄 Converting HTML report to PDF..."
echo "   Source: $ALLURE_REPORT_DIR/index.html"
echo "   Output: $PDF_OUTPUT_DIR/$PDF_FILENAME"

# Convert HTML to PDF with proper settings
wkhtmltopdf \
    --enable-local-file-access \
    --page-size A4 \
    --orientation Portrait \
    --margin-top 10mm \
    --margin-bottom 10mm \
    --margin-left 10mm \
    --margin-right 10mm \
    --enable-javascript \
    --javascript-delay 2000 \
    --no-stop-slow-scripts \
    --debug-javascript \
    "$ALLURE_REPORT_DIR/index.html" \
    "$PDF_OUTPUT_DIR/$PDF_FILENAME"

if [ $? -eq 0 ]; then
    echo "✅ PDF Report generated successfully!"
    echo "📍 Location: $PDF_OUTPUT_DIR/$PDF_FILENAME"
    echo ""
    echo "📊 Report Details:"
    ls -lh "$PDF_OUTPUT_DIR/$PDF_FILENAME"
    echo ""
    echo "🎉 You can now share this PDF report with stakeholders!"
    
    # Open PDF automatically (macOS)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo ""
        read -p "Open PDF now? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            open "$PDF_OUTPUT_DIR/$PDF_FILENAME"
        fi
    fi
else
    echo "❌ Failed to generate PDF report"
    exit 1
fi
