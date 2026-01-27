# 📊 Test Reports Generation Guide

## 🎯 Overview

This framework generates professional **HTML** and **PDF** test execution reports using **Allure Report**. These reports can be shared with stakeholders and management.

---

## 🚀 Quick Start

### Generate All Reports (Automated)
```bash
./generate_reports.sh
```

This single command will:
1. ✅ Run all Sasai app token tests
2. ✅ Generate Allure HTML report
3. ✅ Generate PDF report
4. ✅ Open report in browser

---

## 📋 Manual Report Generation

### Step 1: Run Tests with Allure Formatter
```bash
source venv/bin/activate

behave -D env=qa features/appToken.feature --tags=sasai \
  -f allure_behave.formatter:AllureFormatter \
  -o reports/allure-results \
  --no-capture
```

### Step 2: Generate HTML Report
```bash
allure generate reports/allure-results -o reports/allure-report --clean
```

### Step 3: View HTML Report
```bash
# Option 1: Open in browser automatically
allure open reports/allure-report

# Option 2: Open manually
open reports/allure-report/index.html
```

### Step 4: Generate PDF Report (Optional)
```bash
# Install wkhtmltopdf (first time only)
brew install --cask wkhtmltopdf

# Generate PDF
wkhtmltopdf \
  --enable-local-file-access \
  --page-size A4 \
  --margin-top 10mm \
  --margin-right 10mm \
  --margin-bottom 10mm \
  --margin-left 10mm \
  reports/allure-report/index.html \
  reports/Test_Report_$(date +%Y%m%d).pdf
```

---

## 📁 Report Locations

After running tests, reports will be available at:

```
reports/
├── allure-results/          # Raw test data (JSON files)
│   ├── *-result.json
│   ├── *-container.json
│   └── *-attachment.*
│
├── allure-report/           # HTML report (interactive)
│   ├── index.html          # Main report page
│   ├── widgets/            # Report widgets
│   ├── data/               # Report data
│   └── history/            # Execution history
│
└── Test_Execution_Report_*.pdf   # PDF report for stakeholders
```

---

## 📊 Allure Report Features

### 1. **Overview Dashboard**
- ✅ Total scenarios: passed/failed/skipped
- ✅ Pass rate percentage
- ✅ Execution duration
- ✅ Test environment details
- ✅ Execution trends over time

### 2. **Test Cases**
- ✅ Detailed step-by-step execution
- ✅ Request/response data
- ✅ Screenshots (if configured)
- ✅ Logs and attachments
- ✅ Execution history

### 3. **Graphs & Charts**
- ✅ Success rate pie chart
- ✅ Test duration graph
- ✅ Severity distribution
- ✅ Feature coverage
- ✅ Historical trends

### 4. **Categorization**
- ✅ By feature
- ✅ By tag (@smoke, @appToken, @sasai)
- ✅ By severity
- ✅ By status (passed/failed)

### 5. **Timeline**
- ✅ Chronological test execution
- ✅ Parallel execution visualization
- ✅ Duration of each test

---

## 🎨 Customizing Reports

### Add Custom Categories
Create `categories.json` in `reports/allure-results/`:

```json
[
  {
    "name": "Authentication Issues",
    "matchedStatuses": ["failed"],
    "messageRegex": ".*401.*|.*403.*|.*authentication.*"
  },
  {
    "name": "API Errors",
    "matchedStatuses": ["failed", "broken"],
    "messageRegex": ".*50[0-9].*|.*timeout.*"
  },
  {
    "name": "Product Defects",
    "matchedStatuses": ["failed"],
    "messageRegex": ".*assert.*"
  }
]
```

### Add Environment Info
Create `environment.properties` in `reports/allure-results/`:

```properties
Environment=QA
Base.URL=https://sandbox.sasaipaymentgateway.com
Browser=N/A (API Testing)
OS=macOS
Python.Version=3.13.3
Tester=QA Team
Build.Version=1.0.0
```

### Add Test Executor Info
Create `executor.json` in `reports/allure-results/`:

```json
{
  "name": "Jenkins",
  "type": "jenkins",
  "url": "http://jenkins.example.com",
  "buildOrder": 123,
  "buildName": "Sasai API Tests #123",
  "buildUrl": "http://jenkins.example.com/job/sasai-api-tests/123",
  "reportUrl": "http://jenkins.example.com/job/sasai-api-tests/123/allure",
  "reportName": "Allure Report"
}
```

---

## 📤 Sharing Reports with Stakeholders

### Option 1: PDF Report (Recommended)
```bash
# Generate PDF
./generate_reports.sh

# PDF will be in: reports/Test_Execution_Report_YYYYMMDD_HHMMSS.pdf
# Email or share this file
```

### Option 2: HTML Report (Interactive)
```bash
# Zip the entire report directory
cd reports
zip -r allure-report.zip allure-report/

# Share allure-report.zip
# Recipients can extract and open index.html
```

### Option 3: Host on Web Server
```bash
# Copy report to web server
scp -r reports/allure-report/ user@server:/var/www/html/test-reports/

# Share URL: http://server/test-reports/allure-report/
```

### Option 4: Allure Server (Enterprise)
```bash
# Send results to Allure Server
allure-server send reports/allure-results --url http://allure-server:5050
```

---

## 🔄 Continuous Reporting

### Schedule Daily Reports
Add to crontab:
```bash
# Run tests and generate reports daily at 9 AM
0 9 * * * cd /path/to/EcoCash_API_Automation && ./generate_reports.sh && mail -s "Daily Test Report" stakeholders@company.com < reports/Test_Report_*.pdf
```

### CI/CD Integration

#### Jenkins
```groovy
stage('Generate Reports') {
    steps {
        sh './generate_reports.sh'
        
        allure([
            includeProperties: false,
            jdk: '',
            properties: [],
            reportBuildPolicy: 'ALWAYS',
            results: [[path: 'reports/allure-results']]
        ])
        
        archiveArtifacts artifacts: 'reports/*.pdf', fingerprint: true
    }
}
```

#### GitHub Actions
```yaml
- name: Generate Reports
  run: ./generate_reports.sh
  
- name: Upload PDF Report
  uses: actions/upload-artifact@v3
  with:
    name: test-report-pdf
    path: reports/Test_Execution_Report_*.pdf
    
- name: Publish Allure Report
  uses: simple-elf/allure-report-action@master
  with:
    allure_results: reports/allure-results
    allure_history: allure-history
```

---

## 🎯 Report Examples

### Sample Report Structure:

```
┌─────────────────────────────────────────────────────────┐
│  SASAI PAYMENT GATEWAY - TEST EXECUTION REPORT          │
│                                                          │
│  ✅ Test Summary                                         │
│  ├─ Total: 8 scenarios                                  │
│  ├─ Passed: 6 (75%)                                     │
│  ├─ Failed: 2 (25%)                                     │
│  └─ Duration: 5.7s                                      │
│                                                          │
│  📊 Test Suites                                          │
│  └─ Sasai Payment Gateway - App Token API Testing       │
│     ├─ ✅ Get app token with valid credentials         │
│     ├─ ✅ Get app token with Sasai credentials         │
│     ├─ ✅ Get app token with invalid credentials       │
│     ├─ ✅ Get app token with missing tenantId          │
│     ├─ ✅ Get app token with missing clientId          │
│     ├─ ✅ Validate app token response structure        │
│     ├─ ❌ Access protected endpoint without token      │
│     └─ ❌ Access protected endpoint with valid token   │
│                                                          │
│  📈 Performance Metrics                                  │
│  ├─ Average Response Time: 591ms                        │
│  ├─ Fastest: 519ms                                      │
│  └─ Slowest: 1681ms                                     │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠️ Troubleshooting

### Issue: Allure command not found
```bash
# Install Allure
brew install allure
```

### Issue: wkhtmltopdf not found
```bash
# Install wkhtmltopdf
brew install --cask wkhtmltopdf
```

### Issue: Permission denied for generate_reports.sh
```bash
chmod +x generate_reports.sh
```

### Issue: Empty Allure report
```bash
# Check if results were generated
ls reports/allure-results/

# Re-run tests with Allure formatter
behave -D env=qa features/appToken.feature --tags=sasai \
  -f allure_behave.formatter:AllureFormatter \
  -o reports/allure-results
```

### Issue: PDF generation fails
```bash
# Check wkhtmltopdf installation
which wkhtmltopdf

# Test wkhtmltopdf
wkhtmltopdf https://www.google.com test.pdf

# If still fails, use alternative
brew reinstall --cask wkhtmltopdf
```

---

## 📚 Additional Resources

- **Allure Documentation**: https://docs.qameta.io/allure/
- **Allure Behave**: https://github.com/allure-framework/allure-python
- **wkhtmltopdf**: https://wkhtmltopdf.org/

---

## 🎉 Summary

### What You Get:
✅ **Professional HTML Reports** - Interactive, feature-rich  
✅ **PDF Reports** - Ready to email stakeholders  
✅ **Historical Trends** - Track progress over time  
✅ **Detailed Test Steps** - Step-by-step execution details  
✅ **Performance Metrics** - Response times and duration  
✅ **Easy Sharing** - Multiple formats for different audiences  

### One Command:
```bash
./generate_reports.sh
```

**That's it! Your reports are ready to share! 📊✨**
