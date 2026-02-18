#!/bin/bash

###############################################################################
# Project Cleanup Script
# Removes unwanted files, caches, and temporary artifacts
###############################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔═══════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║        Project Cleanup - Remove Unwanted Files   ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════╝${NC}"
echo ""

# 1. Python cache files
echo -e "${YELLOW}🧹 Removing Python cache files...${NC}"
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true
find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
echo -e "${GREEN}✅ Python cache files removed${NC}"

# 2. Old log files (keep last 5 only)
echo -e "${YELLOW}🧹 Cleaning old log files (keeping last 5)...${NC}"
cd logs 2>/dev/null && ls -t automation_*.log | tail -n +6 | xargs rm -f 2>/dev/null && cd .. || true
LOG_COUNT=$(ls -1 logs/*.log 2>/dev/null | wc -l | tr -d ' ')
echo -e "${GREEN}✅ Cleaned logs (${LOG_COUNT} files remaining)${NC}"

# 3. Test reports (keeping structure)
echo -e "${YELLOW}🧹 Cleaning test reports...${NC}"
rm -rf reports/allure-results/* 2>/dev/null || true
rm -rf reports/allure-report/* 2>/dev/null || true
rm -rf reports/junit/* 2>/dev/null || true
rm -rf reports/html-report/* 2>/dev/null || true
echo -e "${GREEN}✅ Test reports cleaned${NC}"

# 4. System files
echo -e "${YELLOW}🧹 Removing system files...${NC}"
find . -type f -name ".DS_Store" -delete 2>/dev/null || true
find . -type f -name "Thumbs.db" -delete 2>/dev/null || true
echo -e "${GREEN}✅ System files removed${NC}"

# 5. Temporary documentation files
echo -e "${YELLOW}🧹 Removing temporary documentation...${NC}"
rm -f CHURCH_LOOKUP_COMPLETE.md 2>/dev/null || true
rm -f CHURCH_PAYMENT_COMPLETE.md 2>/dev/null || true
rm -f CHURCH_PAYMENT_OPTIONS_COMPLETE.md 2>/dev/null || true
rm -f CHURCH_PAYMENT_OPTIONS_QUICK_REF.md 2>/dev/null || true
rm -f CHURCH_PAYMENT_OPTIONS_SUCCESS.md 2>/dev/null || true
rm -f CHURCH_PAYMENT_QUICK_REF.md 2>/dev/null || true
rm -f CHURCH_PAYMENT_SUCCESS.md 2>/dev/null || true
rm -f DEPLOYMENT_SUCCESS.md 2>/dev/null || true
rm -f EMAIL_FEATURE_SUMMARY.md 2>/dev/null || true
rm -f SMOKE_TEST_FINAL_REPORT.md 2>/dev/null || true
rm -f SMOKE_TEST_RESULTS.md 2>/dev/null || true
rm -f SMOKE_TEST_SUMMARY.md 2>/dev/null || true
rm -f STEP_NAVIGATION_FIXED.md 2>/dev/null || true
rm -f YELLOW_LINES_FIX_GUIDE.md 2>/dev/null || true
rm -f pretty.output 2>/dev/null || true
echo -e "${GREEN}✅ Temporary documentation removed${NC}"

# 6. Coverage files
echo -e "${YELLOW}🧹 Removing coverage files...${NC}"
rm -rf .coverage 2>/dev/null || true
rm -rf htmlcov/ 2>/dev/null || true
rm -rf .tox/ 2>/dev/null || true
echo -e "${GREEN}✅ Coverage files removed${NC}"

# 7. Build artifacts
echo -e "${YELLOW}🧹 Removing build artifacts...${NC}"
rm -rf build/ 2>/dev/null || true
rm -rf dist/ 2>/dev/null || true
rm -rf *.egg-info 2>/dev/null || true
echo -e "${GREEN}✅ Build artifacts removed${NC}"

# Summary
echo ""
echo -e "${BLUE}╔═══════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║           Cleanup Complete!                       ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}Summary of cleaned items:${NC}"
echo -e "  ✅ Python cache files (__pycache__, *.pyc)"
echo -e "  ✅ Old log files (kept last 5)"
echo -e "  ✅ Test reports and artifacts"
echo -e "  ✅ System files (.DS_Store)"
echo -e "  ✅ Temporary documentation"
echo -e "  ✅ Coverage files"
echo -e "  ✅ Build artifacts"
echo ""

# Show current size
echo -e "${YELLOW}Current project size:${NC}"
du -sh . 2>/dev/null || true
echo ""
