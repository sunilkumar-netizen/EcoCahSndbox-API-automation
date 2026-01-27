# 🚀 Setting Up EcoCash API Tests on Sasai Jenkins

## Step-by-Step Guide for https://build.sasaipaymentgateway.com/

**Jenkins URL**: https://build.sasaipaymentgateway.com/  
**Date**: January 27, 2026  
**Status**: Ready to configure

---

## 📋 Prerequisites Checklist

Before you start, ensure you have:

```
✅ Access to: https://build.sasaipaymentgateway.com/
✅ Permission to create items/jobs
✅ GitHub repository access: sunilkumar-netizen/EcoCahSndbox-API-automation
✅ GitHub Personal Access Token (or credentials)
✅ Email address for notifications
```

---

## 🎯 Quick Setup (20 Minutes)

### Step 1: Access Jenkins (1 min)

1. Open browser and go to: **https://build.sasaipaymentgateway.com/**
2. Login with your credentials
3. Verify you're on the Jenkins Dashboard

---

### Step 2: Add GitHub Credentials (3 minutes)

#### 2.1 Generate GitHub Personal Access Token (if you don't have one)

1. Go to: https://github.com/settings/tokens
2. Click: **"Generate new token"** → **"Generate new token (classic)"**
3. Fill in:
   ```
   Note: Jenkins - EcoCash API Automation
   Expiration: 90 days (or No expiration)
   
   Select scopes:
   ✓ repo (Full control of private repositories)
   ✓ admin:repo_hook (Full control of repository hooks)
   ```
4. Click **"Generate token"**
5. **IMPORTANT**: Copy the token immediately (you won't see it again!)

#### 2.2 Add Credentials to Jenkins

1. In Jenkins, go to: **Manage Jenkins** → **Credentials**
2. Click on: **System** → **Global credentials (unrestricted)**
3. Click: **"Add Credentials"** (left sidebar)
4. Fill in:
   ```
   Kind: Username with password
   Scope: Global (Jenkins, nodes, items, all child items, etc)
   Username: sunilkumar-netizen
   Password: [Paste your GitHub Personal Access Token]
   ID: github-ecocash-api
   Description: GitHub - EcoCash API Automation
   ```
5. Click **"Create"**

✅ **Credentials saved!**

---

### Step 3: Create Pipeline Job (5 minutes)

#### 3.1 Create New Item

1. From Jenkins Dashboard, click: **"New Item"** (left sidebar)
2. Enter item name: `EcoCash-API-Automation`
3. Select: **"Pipeline"**
4. Click: **"OK"**

#### 3.2 Configure General Settings

In the job configuration page:

**General Section:**
```
✓ Description: 
  EcoCash Sasai Payment Gateway API Test Automation
  - 9 APIs automated
  - 183 test scenarios
  - Allure HTML reports

✓ Discard old builds:
  - Strategy: Log Rotation
  - Days to keep builds: 30
  - Max # of builds to keep: 50

✓ GitHub project:
  - Project url: https://github.com/sunilkumar-netizen/EcoCahSndbox-API-automation/
```

#### 3.3 Configure Build Triggers

**Build Triggers Section:**
```
✓ GitHub hook trigger for GITScm polling
  (This enables automatic builds on git push)

✓ Build periodically (optional - for scheduled runs):
  Schedule: H 2 * * *
  (This runs daily at 2 AM - adjust as needed)
```

**Schedule Examples:**
```
H 2 * * *          # Daily at 2 AM
H */4 * * *        # Every 4 hours
H 9-17 * * 1-5     # Hourly during business hours (weekdays)
0 9,14,18 * * *    # Three times a day: 9 AM, 2 PM, 6 PM
```

#### 3.4 Configure Pipeline

**Pipeline Section:**
```
Definition: Pipeline script from SCM

SCM: Git

Repositories:
  Repository URL: https://github.com/sunilkumar-netizen/EcoCahSndbox-API-automation.git
  Credentials: github-ecocash-api (the one you just created)

Branches to build:
  Branch Specifier: */main

Repository browser: (Auto)

Script Path: Jenkinsfile

✓ Lightweight checkout
```

#### 3.5 Save Configuration

Click **"Save"** at the bottom of the page.

✅ **Pipeline job created!**

---

### Step 4: Configure Build Parameters (2 minutes)

After saving, go back to job configuration:

1. Click: **"Configure"** (left sidebar)
2. Scroll to **"General"** section
3. Check: **"This project is parameterized"**
4. Add the following parameters:

#### Parameter 1: Environment

```
Type: Choice Parameter
Name: ENVIRONMENT
Choices (one per line):
  qa
  dev
  uat
Description: Environment to run tests against
```

#### Parameter 2: Test Tags

```
Type: Choice Parameter
Name: TAGS
Choices (one per line):
  smoke
  regression
  payments
  auth
  all
Description: Test tags to execute (smoke = quick, regression = full)
```

#### Parameter 3: Parallel Execution

```
Type: Boolean Parameter
Name: PARALLEL_EXECUTION
Default Value: false
Description: Enable parallel test execution (faster but requires more resources)
```

5. Click **"Save"**

✅ **Parameters configured!**

---

### Step 5: Install Required Plugins (5 minutes)

Check if these plugins are installed:

1. Go to: **Manage Jenkins** → **Plugins** → **Installed Plugins**
2. Search for each plugin below
3. If missing, go to **Available Plugins** tab and install

**Required Plugins:**
```
✓ Allure Plugin               (for Allure reports)
✓ Git Plugin                  (for Git integration)
✓ GitHub Plugin               (for GitHub integration)
✓ Pipeline Plugin             (should be pre-installed)
✓ JUnit Plugin                (for test results)
✓ Email Extension Plugin      (for notifications)
✓ Timestamper Plugin          (for timestamps in logs)
✓ AnsiColor Plugin            (for colored console output)
```

**To Install Missing Plugins:**
1. Go to: **Manage Jenkins** → **Plugins** → **Available Plugins**
2. Search for plugin name
3. Check the checkbox
4. Click: **"Install without restart"** or **"Download now and install after restart"**

✅ **Plugins installed!**

---

### Step 6: Configure Allure Commandline (3 minutes)

1. Go to: **Manage Jenkins** → **Tools**
2. Scroll to: **Allure Commandline installations**
3. Click: **"Add Allure Commandline"**
4. Configure:
   ```
   Name: Allure
   ✓ Install automatically
   Install from Maven Central
   Version: 2.24.0 (or latest available)
   ```
5. Click: **"Save"**

✅ **Allure configured!**

---

### Step 7: Configure Email Notifications (5 minutes)

#### 7.1 Configure SMTP Server

1. Go to: **Manage Jenkins** → **System**
2. Scroll to: **Extended E-mail Notification**
3. Configure based on your email provider:

**Option A: Gmail (If using Gmail)**
```
SMTP server: smtp.gmail.com
SMTP Port: 587

✓ Use SMTP Authentication:
  User Name: your-email@gmail.com
  Password: [Your Gmail App Password]

Use SSL: No
Use TLS: Yes
Charset: UTF-8

Default Recipients: your-team@sasaipaymentgateway.com
Default Subject: $PROJECT_NAME - Build # $BUILD_NUMBER - $BUILD_STATUS!
Default Content: ${JELLY_SCRIPT,template="html"}
```

**Option B: Company SMTP (Sasai/EcoCash Email)**
```
SMTP server: [Ask your IT team]
SMTP Port: 25 or 587 or 465

✓ Use SMTP Authentication:
  User Name: [Your company email]
  Password: [Your email password]

Use SSL/TLS: [As required by your company]
Charset: UTF-8

Default Recipients: qa-team@sasaipaymentgateway.com
Default Subject: $PROJECT_NAME - Build # $BUILD_NUMBER - $BUILD_STATUS!
```

#### 7.2 Configure Email Extension

Scroll down to: **E-mail Notification**
```
SMTP server: [Same as above]
Default user e-mail suffix: @sasaipaymentgateway.com

✓ Use SMTP Authentication:
  User Name: [Same as above]
  Password: [Same as above]

✓ Use SSL
✓ SMTP Port: [Same as above]
```

4. Click: **"Save"**

#### 7.3 Test Email Configuration

```
Scroll to bottom of System Configuration
Click: "Test configuration by sending test e-mail"
Enter: your-email@sasaipaymentgateway.com
Click: "Test configuration"

Should see: "Email was successfully sent"
```

✅ **Email configured!**

**Note**: If using Gmail, you need an **App Password**:
1. Go to: https://myaccount.google.com/apppasswords
2. Generate new app password for "Jenkins"
3. Use this password in Jenkins (not your regular Gmail password)

---

### Step 8: Run Your First Build (2 minutes)

#### 8.1 Trigger Build

1. Go to your job: **EcoCash-API-Automation**
2. Click: **"Build with Parameters"**
3. Select:
   ```
   ENVIRONMENT: qa
   TAGS: smoke
   PARALLEL_EXECUTION: false
   ```
4. Click: **"Build"**

#### 8.2 Monitor Execution

1. You'll see: **Build #1** appear in "Build History" (left sidebar)
2. Click on: **#1**
3. Click: **"Console Output"** to watch live logs

**Expected Pipeline Stages:**
```
1. Checkout          ✓ (Clone repository)
2. Setup Environment ✓ (Install Python dependencies)
3. Lint Code         ✓ (Code quality check)
4. Run Tests         ✓ (Execute smoke tests)
5. Generate Reports  ✓ (Create Allure report)
6. Publish Results   ✓ (Publish JUnit + artifacts)
```

**Expected Duration**: 1-2 minutes for smoke tests

#### 8.3 View Results

After build completes:

**Test Results:**
1. Click on: **Build #1**
2. Click: **"Test Result"**
3. Should see: **3 passed, 6 failed** (expected - token expiry issue)

**Allure Report:**
1. From build page, click: **"Allure Report"**
2. Browse beautiful HTML report with:
   - Overview dashboard
   - Test suites
   - Graphs and charts
   - Timeline
   - Test details

✅ **First build complete!**

---

## 🪝 Set Up GitHub Webhook (Optional - Auto Trigger)

### Configure Webhook in GitHub

1. Go to: https://github.com/sunilkumar-netizen/EcoCahSndbox-API-automation
2. Click: **Settings** → **Webhooks** → **Add webhook**
3. Configure:
   ```
   Payload URL: https://build.sasaipaymentgateway.com/github-webhook/
   Content type: application/json
   Secret: [Leave empty or ask Jenkins admin]
   
   Which events would you like to trigger this webhook?
   ○ Just the push event
   
   ✓ Active
   ```
4. Click: **"Add webhook"**

### Test Webhook

1. Go back to: **Webhooks** page
2. Click on your webhook
3. Scroll to: **"Recent Deliveries"**
4. Should see green checkmark (✓) for successful delivery

**Test Auto-Trigger:**
```bash
# Make a small change
cd /Users/sunilkumar/EcoCash_API_Automation
echo "# Webhook test" >> WEBHOOK_TEST.md

# Commit and push
git add WEBHOOK_TEST.md
git commit -m "Test webhook trigger"
git push origin main

# Jenkins should auto-trigger within 10 seconds!
```

✅ **Webhook configured!**

---

## 📊 Understanding Your Build

### Pipeline Stages Explained

```
Stage 1: Checkout (10-15 seconds)
├─ Clones your GitHub repository
├─ Switches to main branch
└─ Verifies Jenkinsfile exists

Stage 2: Setup Environment (20-30 seconds)
├─ Creates Python virtual environment
├─ Installs dependencies from requirements.txt
└─ Verifies installations

Stage 3: Lint Code (10-15 seconds)
├─ Runs Flake8 linting
├─ Checks for syntax errors
└─ Reports code quality issues

Stage 4: Run Tests (20 sec - 40 min depending on tags)
├─ Executes Behave scenarios
├─ Generates allure-results
├─ Creates JUnit XML reports
└─ Smoke: ~20 sec | Regression: ~38 min

Stage 5: Generate Reports (5-10 seconds)
├─ Processes allure-results
├─ Creates HTML Allure report
└─ Adds graphs and timeline

Stage 6: Publish Results (5 seconds)
├─ Publishes JUnit test results
├─ Archives artifacts (logs, reports)
└─ Triggers email notification
```

### Expected Test Results

**Smoke Tests (9 scenarios):**
```
✅ 3 Passed:
   - App Token API
   - OTP Request API
   - OTP Verify API

❌ 6 Failed (Expected - Token Expiry):
   - PIN Verify API
   - Login Devices API
   - Merchant Lookup API
   - Payment Options API
   - Utility Payment API
   - Order Details API

Duration: ~20 seconds
```

**Full Regression (183 scenarios):**
```
✅ 154 Passed (~84%)
❌ 29 Failed (External dependencies)

Duration: ~38 minutes
```

---

## 📧 Email Notification Example

After build completes, you'll receive an email:

**Success Email:**
```
From: Jenkins <jenkins@build.sasaipaymentgateway.com>
To: qa-team@sasaipaymentgateway.com
Subject: ✅ API Tests PASSED - EcoCash-API-Automation #1

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Test Execution Successful
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Environment:  QA
Tags:         smoke
Build:        #1
Duration:     1 min 45 sec

Results:
✅ 3 scenarios passed
❌ 6 scenarios failed (known issue - token expiry)

View Allure Report:
https://build.sasaipaymentgateway.com/job/EcoCash-API-Automation/1/allure

View Console Logs:
https://build.sasaipaymentgateway.com/job/EcoCash-API-Automation/1/console
```

---

## 🎯 Build Parameters Guide

### When to Use Each Option

#### ENVIRONMENT Parameter

```
qa:   For QA testing (most common)
      Use: Daily testing, smoke tests, regression
      
dev:  For development environment
      Use: Testing new features, development validation
      
uat:  For user acceptance testing
      Use: Pre-production validation, client demos
```

#### TAGS Parameter

```
smoke:      Quick smoke tests (9 scenarios)
            Duration: ~20 seconds
            Use: After every commit, quick validation

regression: Full test suite (183 scenarios)
            Duration: ~38 minutes
            Use: Nightly builds, before releases

payments:   Payment-related APIs only
            Duration: ~15 minutes
            Use: When payment features change

auth:       Authentication APIs only
            Duration: ~10 minutes
            Use: When auth features change

all:        Everything (same as regression)
            Duration: ~38 minutes
            Use: Complete validation
```

#### PARALLEL_EXECUTION Parameter

```
false:  Sequential execution (default)
        Pros: More stable, easier to debug
        Cons: Slower
        Use: Most of the time

true:   Parallel execution
        Pros: Faster execution
        Cons: Requires more resources, harder to debug
        Use: When you need results quickly
```

---

## 🔄 Daily Usage Scenarios

### Scenario 1: Quick Check After Code Change

```
1. Make code changes locally
2. git push origin main
3. Jenkins auto-triggers (webhook)
4. Smoke tests run (~20 sec)
5. Get email notification
6. Review Allure report
7. Fix if needed, push again
```

### Scenario 2: Manual Full Regression

```
1. Go to: EcoCash-API-Automation job
2. Click: "Build with Parameters"
3. Select:
   - ENVIRONMENT: qa
   - TAGS: regression
   - PARALLEL_EXECUTION: false
4. Click: "Build"
5. Come back in 40 minutes
6. Review results
```

### Scenario 3: Scheduled Nightly Build

```
Already configured with cron:
- Runs daily at 2 AM
- Full regression suite
- Environment: qa
- Email sent on completion
- No manual intervention needed
```

---

## 📈 Monitoring Your Builds

### Jenkins Dashboard

```
URL: https://build.sasaipaymentgateway.com/job/EcoCash-API-Automation/

Widgets you'll see:
├─ Build History (last 10 builds)
├─ Test Result Trend (pass/fail over time)
├─ Build Time Trend (duration over time)
└─ Stage View (visual pipeline)
```

### Key Metrics to Monitor

```
✓ Pass Rate: Should be >90% (after external issues fixed)
✓ Build Time: Smoke <2 min, Regression <40 min
✓ Failure Rate: <10%
✓ Build Success Rate: >95%
```

---

## 🐛 Troubleshooting

### Issue 1: Build Fails at "Checkout" Stage

**Error**: `Could not clone repository`

**Solution**:
```
1. Check GitHub credentials are correct
2. Verify repository URL is correct
3. Test credentials: Manage Jenkins → Credentials → Test Connection
4. Ensure Jenkins has internet access
```

### Issue 2: Build Fails at "Setup Environment"

**Error**: `pip: command not found` or `Python not found`

**Solution**:
```
1. Check if Python is installed on Jenkins server
2. Ask Jenkins admin to install Python 3.10+
3. Or use Docker agent with Python pre-installed
```

### Issue 3: Build Fails at "Run Tests"

**Error**: `No tests collected`

**Solution**:
```
1. Verify Jenkinsfile exists in repository
2. Check feature files exist in repository
3. Verify branch name is correct (main vs master)
4. Check workspace is not empty
```

### Issue 4: Allure Report Not Showing

**Error**: `Allure command not found`

**Solution**:
```
1. Verify Allure Plugin is installed
2. Configure Allure Commandline in Tools
3. Restart Jenkins if needed
```

### Issue 5: Email Not Sending

**Error**: `Failed to send email`

**Solution**:
```
1. Test SMTP configuration: System → Test email
2. Check firewall/network restrictions
3. Verify email credentials are correct
4. For Gmail: Use App Password (not regular password)
5. Check spam folder for test emails
```

### Issue 6: Webhook Not Triggering

**Error**: `Build doesn't start on git push`

**Solution**:
```
1. Verify webhook is active in GitHub
2. Check Recent Deliveries for errors
3. Ensure Jenkins URL is accessible from internet
4. Check "GitHub hook trigger" is enabled in job
5. Verify payload URL: https://build.sasaipaymentgateway.com/github-webhook/
```

---

## ✅ Success Checklist

### Verify Everything is Working

```
Configuration:
☑ Jenkins job created
☑ GitHub credentials added
☑ Build parameters configured
☑ Required plugins installed
☑ Allure commandline configured
☑ Email notifications configured

First Build:
☑ Manual build successful
☑ Test results visible (3 passed, 6 failed)
☑ Allure report generated
☑ JUnit results published
☑ Artifacts archived
☑ Email notification received

Automation:
☑ GitHub webhook configured (optional)
☑ Auto-trigger tested (optional)
☑ Scheduled builds configured

Access:
☑ Team members can access Jenkins
☑ Team can view reports
☑ Team can trigger builds
```

---

## 🎊 Congratulations!

You now have:

```
✅ EcoCash API Tests integrated with Sasai Jenkins
✅ Automated pipeline running
✅ Beautiful Allure reports
✅ Email notifications
✅ Parameterized builds (Environment + Tags)
✅ Scheduled nightly runs
✅ GitHub integration (optional webhook)
```

---

## 📚 Quick Reference

### Important URLs

```
Jenkins Server:         https://build.sasaipaymentgateway.com/
Your Job:               https://build.sasaipaymentgateway.com/job/EcoCash-API-Automation/
GitHub Repository:      https://github.com/sunilkumar-netizen/EcoCahSndbox-API-automation
```

### Common Tasks

```
Run Build:              Job → Build with Parameters
View Results:           Build # → Test Result
View Allure Report:     Build # → Allure Report
View Console Logs:      Build # → Console Output
Configure Job:          Job → Configure
View Trends:            Job → Test Result Trend
```

### Build Parameters

```
Quick Smoke Test:
- ENVIRONMENT: qa
- TAGS: smoke
- Duration: ~20 seconds

Full Regression:
- ENVIRONMENT: qa
- TAGS: regression
- Duration: ~38 minutes
```

---

## 📞 Support

### Need Help?

```
Jenkins Issues:          [Your Jenkins Admin]
GitHub Access:           git-admin@sasaipaymentgateway.com
Test Framework Issues:   qa-team@sasaipaymentgateway.com
Email Configuration:     it-support@sasaipaymentgateway.com
```

### Documentation

```
Complete Setup Guide:    JENKINS_SETUP_GUIDE.md
Quick Reference:         JENKINS_QUICKSTART.md
Visual Overview:         JENKINS_VISUAL_SUMMARY.md
Framework Details:       CLIENT_PRESENTATION.md
Test Results:            SMOKE_TEST_RESULTS_JAN27.md
```

---

## 🚀 Next Steps

### Week 1: Validation
```
☐ Run daily smoke tests
☐ Monitor build stability
☐ Fix any issues
☐ Train team members
```

### Week 2: Optimization
```
☐ Optimize build times
☐ Fine-tune notifications
☐ Add more test tags
☐ Document procedures
```

### Ongoing: Maintenance
```
☐ Weekly: Review trends
☐ Monthly: Update dependencies
☐ Quarterly: Optimize pipeline
☐ Continuous: Add new tests
```

---

**Document**: Sasai Jenkins Setup Guide  
**Jenkins URL**: https://build.sasaipaymentgateway.com/  
**Version**: 1.0  
**Date**: January 27, 2026  
**Status**: ✅ Ready to Configure  

---

*Follow this guide step-by-step to set up your EcoCash API Test Automation on Sasai Jenkins. Estimated time: 20-30 minutes.*
