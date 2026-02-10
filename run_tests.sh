#!/bin/bash

###############################################################################
# Run Tests Script
# Execute API automation tests with various options
###############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
ENV="qa"
TAGS=""
PARALLEL=false
ALLURE=true

# Print banner
echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════╗"
echo "║                                                   ║"
echo "║   EcoCash API Automation Test Runner             ║"
echo "║                                                   ║"
echo "╚═══════════════════════════════════════════════════╝"
echo -e "${NC}"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -e|--env)
            ENV="$2"
            shift 2
            ;;
        -t|--tags)
            TAGS="$2"
            shift 2
            ;;
        -p|--parallel)
            PARALLEL=true
            shift
            ;;
        --no-allure)
            ALLURE=false
            shift
            ;;
        -h|--help)
            echo "Usage: ./run_tests.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  -e, --env <ENV>        Environment: dev, qa, uat (default: qa)"
            echo "  -t, --tags <TAGS>      Tags to run: smoke, payments, auth, etc."
            echo "  -p, --parallel         Run tests in parallel"
            echo "  --no-allure            Skip Allure report generation"
            echo "  -h, --help             Show this help message"
            echo ""
            echo "Examples:"
            echo "  ./run_tests.sh -e qa -t smoke"
            echo "  ./run_tests.sh --env uat --tags payments"
            echo "  ./run_tests.sh -e qa -p"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            echo "Use -h or --help for usage information"
            exit 1
            ;;
    esac
done

# Validate environment
if [[ ! "$ENV" =~ ^(dev|qa|uat)$ ]]; then
    echo -e "${RED}Error: Invalid environment '$ENV'. Must be one of: dev, qa, uat${NC}"
    exit 1
fi

# Print test configuration
echo -e "${GREEN}Test Configuration:${NC}"
echo -e "  Environment: ${YELLOW}$ENV${NC}"
echo -e "  Tags: ${YELLOW}${TAGS:-all}${NC}"
echo -e "  Parallel: ${YELLOW}$PARALLEL${NC}"
echo -e "  Allure Report: ${YELLOW}$ALLURE${NC}"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment not found. Creating...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate

# Install/update dependencies
echo -e "${BLUE}Checking dependencies...${NC}"
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Clear old test results to ensure fresh report
echo -e "${BLUE}Clearing old test results...${NC}"
rm -rf reports/allure-results/*
rm -rf reports/allure-report
rm -rf reports/html-report

# Create necessary directories
mkdir -p reports/allure-results
mkdir -p reports/html-report
mkdir -p reports/junit
mkdir -p logs

# Build behave command
BEHAVE_CMD="behave -D env=$ENV"

# Add tags if specified
if [ ! -z "$TAGS" ]; then
    BEHAVE_CMD="$BEHAVE_CMD --tags=$TAGS"
fi

# Add Allure formatter if enabled
if [ "$ALLURE" = true ]; then
    BEHAVE_CMD="$BEHAVE_CMD -f allure_behave.formatter:AllureFormatter -o reports/allure-results"
fi

# Add HTML formatter (always enabled for modern reports)
BEHAVE_CMD="$BEHAVE_CMD -f behave_html_formatter:HTMLFormatter -o reports/html-report/report.html"

# Add JUnit report
BEHAVE_CMD="$BEHAVE_CMD --junit --junit-directory reports/junit"

# Add parallel execution if enabled
if [ "$PARALLEL" = true ]; then
    echo -e "${YELLOW}Note: Parallel execution requires pytest-xdist${NC}"
    # BEHAVE_CMD="$BEHAVE_CMD --processes 4 --parallel-element scenario"
fi

# Run tests
echo ""
echo -e "${GREEN}Starting test execution...${NC}"
echo -e "${BLUE}Command: $BEHAVE_CMD${NC}"
echo ""

# Execute tests and capture exit code
set +e
eval $BEHAVE_CMD
TEST_EXIT_CODE=$?
set -e

echo ""

# Check test results
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ All tests passed!${NC}"
else
    echo -e "${RED}❌ Some tests failed (exit code: $TEST_EXIT_CODE)${NC}"
fi

# Generate Allure report if enabled
if [ "$ALLURE" = true ]; then
    echo ""
    echo -e "${BLUE}Generating Allure report...${NC}"
    
    if command -v allure &> /dev/null; then
        allure generate reports/allure-results -o reports/allure-report --clean
        echo -e "${GREEN}✅ Allure report generated: reports/allure-report/index.html${NC}"
        echo ""
        echo -e "${YELLOW}To view report, run: allure open reports/allure-report${NC}"
    else
        echo -e "${YELLOW}⚠️  Allure command-line tool not found. Install with:${NC}"
        echo -e "  brew install allure  # macOS"
        echo -e "  or download from: https://github.com/allure-framework/allure2/releases"
    fi
fi

# Display HTML report location
echo ""
echo -e "${GREEN}✅ Modern HTML report generated: reports/html-report/report.html${NC}"
echo -e "${YELLOW}To view HTML report, run: open reports/html-report/report.html${NC}"

# Send Email Report
echo ""
echo -e "${BLUE}Sending email report...${NC}"
if python3 scripts/send_email_report.py "$ENV" "$TAGS"; then
    echo -e "${GREEN}✅ Email report sent successfully${NC}"
else
    echo -e "${YELLOW}⚠️ Email report sending failed or skipped${NC}"
    echo -e "${YELLOW}   Check SMTP_PASSWORD environment variable${NC}"
    echo -e "${YELLOW}   For Gmail: Use App Password from https://myaccount.google.com/apppasswords${NC}"
fi

# Print log file location
LOG_FILE=$(ls -t logs/*.log 2>/dev/null | head -1)
if [ ! -z "$LOG_FILE" ]; then
    echo ""
    echo -e "${BLUE}Log file: $LOG_FILE${NC}"
fi

echo ""
echo -e "${BLUE}╔═══════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║          Test Execution Completed                ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════╝${NC}"

# Exit with test exit code
exit $TEST_EXIT_CODE
