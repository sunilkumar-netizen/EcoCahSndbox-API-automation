#!/bin/bash
# Complete Test Execution and Report Generation Script
# This script runs tests, generates Allure HTML report, and creates PDF report

echo "🚀 EcoCash API Automation - Complete Test Suite"
echo "================================================"
echo ""

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Run tests with Allure formatter
echo ""
echo "🧪 Running test suite..."
echo "Environment: QA (Sandbox)"
echo "Base URL: https://sandbox.sasaipaymentgateway.com"
echo ""

behave -D env=qa \
    features/appToken.feature \
    --tags=sasai \
    -f allure_behave.formatter:AllureFormatter \
    -o reports/allure-results \
    --no-capture

TEST_EXIT_CODE=$?

echo ""
echo "================================================"
echo "📊 Test Execution Summary"
echo "================================================"

if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "✅ All tests passed!"
else
    echo "⚠️ Some tests failed (Exit code: $TEST_EXIT_CODE)"
fi

echo ""
echo "📈 Generating Allure HTML Report..."
allure generate reports/allure-results --clean -o reports/allure-report

if [ $? -eq 0 ]; then
    echo "✅ Allure HTML report generated successfully!"
    echo "📍 Location: reports/allure-report/index.html"
else
    echo "❌ Failed to generate Allure report"
    exit 1
fi

echo ""
echo "================================================"
echo "📄 Report Options"
echo "================================================"
echo ""
echo "1. 🌐 View HTML Report (Interactive)"
echo "   ./scripts/open_allure_report.sh"
echo ""
echo "2. 📑 Generate PDF Report (For Stakeholders)"
echo "   ./scripts/generate_pdf_report.sh"
echo ""
echo "3. 🚀 Serve Report (Live Server)"
echo "   allure serve reports/allure-results"
echo ""

# Ask user what they want to do
read -p "What would you like to do? (1=HTML, 2=PDF, 3=Serve, Enter=Skip): " choice

case $choice in
    1)
        echo ""
        echo "Opening HTML report..."
        ./scripts/open_allure_report.sh
        ;;
    2)
        echo ""
        echo "Generating PDF report..."
        ./scripts/generate_pdf_report.sh
        ;;
    3)
        echo ""
        echo "Starting Allure server..."
        allure serve reports/allure-results
        ;;
    *)
        echo ""
        echo "✅ Report generation complete!"
        echo "You can view reports anytime using the commands above."
        ;;
esac

echo ""
echo "================================================"
echo "✅ Process Complete!"
echo "================================================"
