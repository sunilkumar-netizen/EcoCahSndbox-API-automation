#!/bin/bash
# Open Allure HTML Report in Browser
# This script opens the generated Allure report in your default browser

echo "🚀 Opening Allure Report..."
echo "=========================================="

# Check if Allure report exists
ALLURE_REPORT_DIR="reports/allure-report"

if [ ! -f "$ALLURE_REPORT_DIR/index.html" ]; then
    echo "❌ Allure report not found!"
    echo ""
    echo "📋 Generating Allure report first..."
    allure generate reports/allure-results --clean -o reports/allure-report
    
    if [ $? -ne 0 ]; then
        echo "❌ Failed to generate Allure report"
        exit 1
    fi
fi

echo "✅ Allure report found!"
echo "📍 Location: $ALLURE_REPORT_DIR/index.html"
echo ""
echo "🌐 Opening report in browser..."

# Open report based on OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open "$ALLURE_REPORT_DIR/index.html"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    xdg-open "$ALLURE_REPORT_DIR/index.html"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    # Windows
    start "$ALLURE_REPORT_DIR/index.html"
else
    echo "⚠️ Unable to detect OS. Please open manually:"
    echo "   $ALLURE_REPORT_DIR/index.html"
fi

echo ""
echo "✅ Allure report opened successfully!"
echo ""
echo "📊 Report Features:"
echo "   - Test results overview"
echo "   - Pass/Fail statistics"
echo "   - Test case details"
echo "   - Timeline charts"
echo "   - Categories and trends"
echo "   - Attachments (logs, screenshots)"
