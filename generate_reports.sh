#!/bin/bash
# Generate Test Reports - Allure HTML & PDF
# Usage: ./generate_reports.sh

set -e

echo "════════════════════════════════════════════════════════════"
echo "  📊 Generating Test Execution Reports"
echo "════════════════════════════════════════════════════════════"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Activate virtual environment
echo -e "${BLUE}🔧 Activating virtual environment...${NC}"
source venv/bin/activate

# Run tests with Allure formatter
echo -e "${BLUE}🧪 Running tests and generating Allure results...${NC}"
behave -D env=qa features/appToken.feature --tags=sasai \
  -f allure_behave.formatter:AllureFormatter \
  -o reports/allure-results \
  --no-capture || true  # Continue even if tests fail

echo ""
echo -e "${GREEN}✅ Test execution completed${NC}"
echo ""

# Generate Allure HTML report
echo -e "${BLUE}📄 Generating Allure HTML report...${NC}"
allure generate reports/allure-results -o reports/allure-report --clean

echo -e "${GREEN}✅ Allure HTML report generated${NC}"
echo ""

# Check if wkhtmltopdf is installed for PDF generation
if command -v wkhtmltopdf &> /dev/null; then
    echo -e "${BLUE}📑 Generating PDF report...${NC}"
    
    # Generate PDF from Allure report (Overview page)
    wkhtmltopdf \
        --enable-local-file-access \
        --page-size A4 \
        --margin-top 10mm \
        --margin-right 10mm \
        --margin-bottom 10mm \
        --margin-left 10mm \
        --encoding UTF-8 \
        reports/allure-report/index.html \
        reports/Test_Execution_Report_$(date +%Y%m%d_%H%M%S).pdf
    
    echo -e "${GREEN}✅ PDF report generated${NC}"
else
    echo -e "${YELLOW}⚠️  wkhtmltopdf not installed. Installing...${NC}"
    echo ""
    echo "Installing wkhtmltopdf via Homebrew..."
    brew install --cask wkhtmltopdf
    
    echo ""
    echo -e "${BLUE}📑 Generating PDF report...${NC}"
    wkhtmltopdf \
        --enable-local-file-access \
        --page-size A4 \
        --margin-top 10mm \
        --margin-right 10mm \
        --margin-bottom 10mm \
        --margin-left 10mm \
        --encoding UTF-8 \
        reports/allure-report/index.html \
        reports/Test_Execution_Report_$(date +%Y%m%d_%H%M%S).pdf
    
    echo -e "${GREEN}✅ PDF report generated${NC}"
fi

echo ""
echo "════════════════════════════════════════════════════════════"
echo -e "${GREEN}  ✅ Reports Generated Successfully!${NC}"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "📁 Generated Reports:"
echo "   1. HTML Report: reports/allure-report/index.html"
echo "   2. PDF Report:  reports/Test_Execution_Report_*.pdf"
echo "   3. Log Files:   logs/automation_*.log"
echo ""
echo "🌐 To view HTML report in browser:"
echo "   allure open reports/allure-report"
echo ""
echo "Or open manually:"
echo "   open reports/allure-report/index.html"
echo ""
