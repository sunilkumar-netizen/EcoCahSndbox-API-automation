# 🔧 Jenkins Setup Guide - EcoCash API Test Automation

## Complete Guide to Setting Up Jenkins Job and Pipelines

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Jenkins Installation](#jenkins-installation)
3. [Required Plugins](#required-plugins)
4. [Jenkins Configuration](#jenkins-configuration)
5. [Creating Jenkins Job](#creating-jenkins-job)
6. [Pipeline Configuration](#pipeline-configuration)
7. [Setting Up Credentials](#setting-up-credentials)
8. [Webhook Configuration](#webhook-configuration)
9. [Testing Your Pipeline](#testing-your-pipeline)
10. [Troubleshooting](#troubleshooting)

---

## 🎯 Prerequisites

### System Requirements
```
✓ Jenkins 2.387+ (LTS recommended)
✓ Java 11 or 17
✓ Python 3.10+
✓ Git
✓ Minimum 4GB RAM
✓ Minimum 10GB disk space
```

### Access Requirements
```
✓ Jenkins admin access
✓ GitHub repository access
✓ Email server (for notifications)
✓ Network access to test environment
```

---

## 📦 Jenkins Installation

### Option 1: Docker Installation (Recommended)

```bash
# Pull Jenkins image
docker pull jenkins/jenkins:lts

# Run Jenkins container
docker run -d \
  --name jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins/jenkins:lts

# Get initial admin password
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

### Option 2: Native Installation (macOS)

```bash
# Install Jenkins using Homebrew
brew install jenkins-lts

# Start Jenkins service
brew services start jenkins-lts

# Access Jenkins at: http://localhost:8080
```

### Option 3: Native Installation (Ubuntu/Debian)

```bash
# Add Jenkins repository
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee \
  /usr/share/keyrings/jenkins-keyring.asc > /dev/null

echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null

# Install Jenkins
sudo apt-get update
sudo apt-get install jenkins

# Start Jenkins service
sudo systemctl start jenkins
sudo systemctl enable jenkins
```

### Initial Setup

1. **Access Jenkins**: Open `http://localhost:8080` in your browser
2. **Unlock Jenkins**: Enter the initial admin password
3. **Install Suggested Plugins**: Select "Install suggested plugins"
4. **Create Admin User**: Set up your admin account
5. **Instance Configuration**: Set Jenkins URL (e.g., `http://localhost:8080`)

---

## 🔌 Required Plugins

### Install These Plugins (Manage Jenkins → Plugins)

#### Essential Plugins
```
✓ Git Plugin                    - Git integration
✓ GitHub Plugin                 - GitHub integration
✓ Pipeline                      - Pipeline support
✓ Pipeline: Stage View          - Visual pipeline stages
✓ Allure Plugin                 - Allure report integration
✓ JUnit Plugin                  - JUnit test results
✓ Email Extension Plugin        - Advanced email notifications
✓ Workspace Cleanup Plugin      - Clean workspace
✓ Timestamper Plugin            - Add timestamps to console
✓ AnsiColor Plugin              - Color console output
```

#### Optional but Recommended
```
✓ Blue Ocean                    - Modern UI
✓ Dashboard View                - Custom dashboards
✓ Build Monitor View            - Build status monitor
✓ Slack Notification Plugin     - Slack integration
✓ HTML Publisher Plugin         - Publish HTML reports
✓ Parameterized Trigger Plugin  - Trigger jobs with parameters
```

### How to Install Plugins

1. Go to: **Manage Jenkins** → **Plugins** → **Available Plugins**
2. Search for each plugin
3. Check the checkbox
4. Click **"Install without restart"** or **"Download now and install after restart"**

---

## ⚙️ Jenkins Configuration

### 1. Configure System Tools

#### Navigate to: **Manage Jenkins** → **Tools**

#### Git Configuration
```
Name: Default
Path to Git executable: git
(or specific path like /usr/bin/git)
```

#### Python Configuration
```bash
# Install Python plugin first
# Then configure:
Name: Python 3.10
Install automatically: Yes
Version: Python 3.10.x
```

### 2. Configure Allure Commandline

#### Navigate to: **Manage Jenkins** → **Tools** → **Allure Commandline**

```
Name: Allure
Install automatically: Yes
Version: 2.24.0 (or latest)
From: Maven Central
```

### 3. Configure Email Notifications

#### Navigate to: **Manage Jenkins** → **System** → **Extended E-mail Notification**

```
SMTP server: smtp.gmail.com (or your SMTP server)
SMTP port: 587
Use SMTP Authentication: Yes
User Name: your-email@gmail.com
Password: your-app-password
Use SSL: No
Use TLS: Yes

Default Recipients: your-team@company.com
Default Subject: $PROJECT_NAME - Build # $BUILD_NUMBER - $BUILD_STATUS!
Default Content: ${JELLY_SCRIPT,template="html"}
```

---

## 🆕 Creating Jenkins Job

### Method 1: Pipeline from SCM (Recommended)

#### Step 1: Create New Item
```
1. Click "New Item" from Jenkins dashboard
2. Enter name: "EcoCash-API-Automation"
3. Select: "Pipeline"
4. Click "OK"
```

#### Step 2: General Configuration
```
Description: EcoCash Sasai Payment Gateway API Test Automation
✓ Discard old builds
  - Days to keep builds: 30
  - Max # of builds to keep: 50
✓ GitHub project
  - Project URL: https://github.com/sunilkumar-netizen/EcoCahSndbox-API-automation
```

#### Step 3: Build Triggers
```
✓ GitHub hook trigger for GITScm polling
✓ Poll SCM (optional backup)
  - Schedule: H/15 * * * * (every 15 minutes)
```

#### Step 4: Pipeline Configuration
```
Definition: Pipeline script from SCM

SCM: Git
  - Repository URL: https://github.com/sunilkumar-netizen/EcoCahSndbox-API-automation.git
  - Credentials: [Select your GitHub credentials]
  - Branch Specifier: */main

Script Path: Jenkinsfile

✓ Lightweight checkout
```

#### Step 5: Save
Click **"Save"** to create the job.

---

### Method 2: Freestyle Project (Alternative)

#### Step 1: Create New Item
```
1. Click "New Item"
2. Enter name: "EcoCash-API-Automation-Freestyle"
3. Select: "Freestyle project"
4. Click "OK"
```

#### Step 2: Source Code Management
```
Git:
  - Repository URL: https://github.com/sunilkumar-netizen/EcoCahSndbox-API-automation.git
  - Credentials: [Select your GitHub credentials]
  - Branch: */main
```

#### Step 3: Build Triggers
```
✓ GitHub hook trigger for GITScm polling
```

#### Step 4: Build Environment
```
✓ Delete workspace before build starts
✓ Add timestamps to the Console Output
✓ Color ANSI Console Output
```

#### Step 5: Build Steps
Add Execute Shell:
```bash
#!/bin/bash
set -e

echo "🔧 Setting up environment..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "🧪 Running tests..."
./run_tests.sh -e ${ENVIRONMENT} -t ${TAGS}

echo "📊 Generating reports..."
allure generate reports/allure-results -o reports/allure-report --clean
```

#### Step 6: Post-build Actions
```
✓ Publish JUnit test result report
  - Test report XMLs: reports/junit/*.xml

✓ Allure Report
  - Path: reports/allure-results

✓ Archive the artifacts
  - Files to archive: reports/**/*,logs/*.log

✓ Email Notification
  - Recipients: your-team@company.com
```

---

## 🔐 Setting Up Credentials

### Add GitHub Credentials

#### Navigate to: **Manage Jenkins** → **Credentials** → **System** → **Global credentials**

#### Method 1: Username with Password
```
Kind: Username with password
Scope: Global
Username: sunilkumar-netizen
Password: [Your GitHub Personal Access Token]
ID: github-credentials
Description: GitHub Credentials for EcoCash Repo
```

#### Method 2: SSH Username with private key (More Secure)
```
Kind: SSH Username with private key
Scope: Global
ID: github-ssh
Description: GitHub SSH Key
Username: git
Private Key: [Enter directly or from file]
  - Paste your SSH private key (~/.ssh/id_rsa)
Passphrase: [If your key has one]
```

### Generate GitHub Personal Access Token

1. Go to: **GitHub** → **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
2. Click **"Generate new token"**
3. Select scopes:
   - ✓ repo (Full control of private repositories)
   - ✓ admin:repo_hook (Full control of repository hooks)
4. Copy the token (save it securely!)
5. Use this token as password in Jenkins credentials

---

## 📊 Pipeline Configuration

### Understanding the Jenkinsfile

Your repository already has a `Jenkinsfile`. Here's what it does:

```groovy
pipeline {
    agent any  // Run on any available agent
    
    parameters {
        // User can select environment
        choice(name: 'ENVIRONMENT', choices: ['qa', 'dev', 'uat'])
        
        // User can select test tags
        choice(name: 'TAGS', choices: ['smoke', 'regression', 'payments', 'auth', 'users', 'all'])
        
        // User can enable parallel execution
        booleanParam(name: 'PARALLEL_EXECUTION', defaultValue: false)
    }
    
    stages {
        stage('Checkout') { ... }      // Clone repository
        stage('Setup') { ... }          // Install dependencies
        stage('Lint') { ... }           // Code quality checks
        stage('Run Tests') { ... }      // Execute tests
        stage('Generate Reports') { ... } // Create Allure reports
        stage('Publish Results') { ... }  // Publish JUnit + artifacts
    }
    
    post {
        success { ... }  // Send success email
        failure { ... }  // Send failure email
        always { ... }   // Cleanup workspace
    }
}
```

### Customizing the Pipeline

#### Add Environment Variables

Edit `Jenkinsfile` to add custom variables:

```groovy
environment {
    PYTHON_VERSION = '3.10'
    VENV_DIR = 'venv'
    REPORTS_DIR = 'reports'
    NOTIFICATION_EMAIL = 'your-team@company.com'
    TEST_BASE_URL = 'https://sandbox.sasaipaymentgateway.com'
}
```

#### Add Slack Notifications (Optional)

Add to `post` section:

```groovy
post {
    success {
        slackSend(
            color: 'good',
            message: "✅ Tests PASSED - ${env.JOB_NAME} #${env.BUILD_NUMBER}\n<${env.BUILD_URL}allure|View Report>"
        )
    }
    failure {
        slackSend(
            color: 'danger',
            message: "❌ Tests FAILED - ${env.JOB_NAME} #${env.BUILD_NUMBER}\n<${env.BUILD_URL}console|View Logs>"
        )
    }
}
```

---

## 🪝 Webhook Configuration

### Set Up GitHub Webhook for Auto-Trigger

#### Step 1: Configure Jenkins URL
```
Manage Jenkins → System → Jenkins Location
  - Jenkins URL: http://your-jenkins-server:8080
  - System Admin e-mail: admin@company.com
```

#### Step 2: Add GitHub Webhook

1. Go to your GitHub repository: https://github.com/sunilkumar-netizen/EcoCahSndbox-API-automation
2. Click **Settings** → **Webhooks** → **Add webhook**
3. Configure:
   ```
   Payload URL: http://your-jenkins-server:8080/github-webhook/
   Content type: application/json
   Secret: [Leave empty or add secret]
   
   Which events would you like to trigger this webhook?
   ✓ Just the push event
   
   ✓ Active
   ```
4. Click **Add webhook**

#### Step 3: Test Webhook
```
1. Go to Webhooks page
2. Click on your webhook
3. Scroll to "Recent Deliveries"
4. Click "Redeliver" to test
5. Check response is 200 OK
```

---

## 🧪 Testing Your Pipeline

### Manual Test Run

#### Step 1: Build with Parameters
```
1. Go to job: "EcoCash-API-Automation"
2. Click "Build with Parameters"
3. Select:
   - ENVIRONMENT: qa
   - TAGS: smoke
   - PARALLEL_EXECUTION: false
4. Click "Build"
```

#### Step 2: Monitor Execution
```
1. Click on build number (e.g., #1)
2. View:
   - Console Output (live logs)
   - Pipeline Steps (stage view)
   - Test Results (after completion)
   - Allure Report (after completion)
```

### Verify Reports

#### Check JUnit Results
```
Build page → Test Result
- Should show: 3 passed, 6 failed (smoke tests)
- Click on failed tests for details
```

#### Check Allure Report
```
Build page → Allure Report
- Overview dashboard
- Test suites
- Graphs and timeline
- Test body details
```

### Automated Test (GitHub Push)

```bash
# Make a small change
cd /Users/sunilkumar/EcoCash_API_Automation
echo "# Jenkins test" >> JENKINS_TEST.md

# Commit and push
git add JENKINS_TEST.md
git commit -m "Test Jenkins webhook trigger"
git push origin main

# Jenkins should automatically trigger within seconds
# Check Jenkins dashboard for new build
```

---

## 📧 Email Configuration Examples

### Gmail SMTP Configuration

```
SMTP Server: smtp.gmail.com
SMTP Port: 587
Use TLS: Yes
Username: your-email@gmail.com
Password: [App-specific password]

Note: Enable 2FA and create App Password:
https://myaccount.google.com/apppasswords
```

### Office 365 SMTP Configuration

```
SMTP Server: smtp.office365.com
SMTP Port: 587
Use TLS: Yes
Username: your-email@company.com
Password: [Your Office 365 password]
```

### Custom SMTP Configuration

```
SMTP Server: mail.company.com
SMTP Port: 25 (or 587, 465)
Use SSL/TLS: As required
Username: smtp-user
Password: smtp-password
```

---

## 🎨 Creating Custom Views

### Dashboard View

#### Navigate to: Jenkins Dashboard → **"+"** (New View)

```
View name: API Test Dashboard
View type: Dashboard

Configure:
✓ Show test statistics
✓ Show test trend chart
✓ Show latest test results

Jobs to include:
- EcoCash-API-Automation
```

### Pipeline View

```
View name: API Pipeline View
View type: Build Pipeline View

Configure:
Initial Job: EcoCash-API-Automation
Display Options:
- Number of displayed builds: 5
- Refresh frequency: 10 seconds
```

---

## 🔄 Setting Up Scheduled Builds

### Cron Syntax for Jenkins

```
# Field order: MINUTE HOUR DAY MONTH DAYOFWEEK

Examples:
H 2 * * *           # Daily at 2 AM (H = hash for load balancing)
H */4 * * *         # Every 4 hours
H 0 * * 1-5         # Weekdays at midnight
H 22 * * 0          # Sundays at 10 PM
H/15 * * * *        # Every 15 minutes
```

### Configure in Job

```
Build Triggers:
✓ Build periodically
  Schedule:
    # Smoke tests every hour (business hours, weekdays)
    H 9-17 * * 1-5
    
    # Full regression tests daily at 2 AM
    H 2 * * *
    
    # Weekend full suite
    H 0 * * 0
```

---

## 🔍 Monitoring and Maintenance

### Build History

```
Job page → Build History
- View all builds
- Filter by status (success/failure)
- Trend analysis
```

### Console Output

```
Build page → Console Output
- Real-time logs
- Error messages
- Test execution details
```

### Test Trends

```
Job page → Test Result Trend
- Pass/fail trends over time
- Performance metrics
- Flaky test detection
```

### Disk Space Management

```
Manage Jenkins → System Information → Disk Usage
Monitor:
- JENKINS_HOME size
- Build artifacts size
- Workspace size

Cleanup:
- Set "Discard old builds" policy
- Regularly clean workspaces
- Archive important artifacts only
```

---

## 🐛 Troubleshooting

### Common Issues and Solutions

#### Issue 1: Python Not Found
```
Error: python3: command not found

Solution:
1. Install Python in Jenkins environment
2. Configure Python in Global Tool Configuration
3. Use explicit Python path in Jenkinsfile:
   sh '/usr/bin/python3 -m venv venv'
```

#### Issue 2: Permission Denied
```
Error: Permission denied

Solution:
1. Check Jenkins user permissions
2. Make scripts executable:
   chmod +x run_tests.sh
3. Add to Jenkinsfile:
   sh 'chmod +x *.sh'
```

#### Issue 3: GitHub Authentication Failed
```
Error: Authentication failed

Solution:
1. Check GitHub credentials are correct
2. Use Personal Access Token (not password)
3. Verify token has required permissions
4. Re-add credentials in Jenkins
```

#### Issue 4: Allure Report Not Generated
```
Error: Allure command not found

Solution:
1. Install Allure Plugin in Jenkins
2. Configure Allure Commandline in Tools
3. Verify allure-results directory exists
4. Check Allure version compatibility
```

#### Issue 5: Tests Not Running
```
Error: No tests collected

Solution:
1. Verify feature files exist in workspace
2. Check tags parameter is correct
3. Verify behave.ini configuration
4. Check Python dependencies installed
```

#### Issue 6: Email Not Sending
```
Error: Failed to send email

Solution:
1. Test SMTP configuration
2. Check firewall/network restrictions
3. Verify email credentials
4. Enable "Less secure apps" (Gmail)
5. Use App-specific password (Gmail with 2FA)
```

#### Issue 7: Workspace Cleanup Fails
```
Error: Cannot delete workspace

Solution:
1. Stop Jenkins
2. Manually delete workspace directory
3. Restart Jenkins
4. Or disable workspace cleanup temporarily
```

---

## 📊 Best Practices

### Pipeline Design

```
✓ Keep Jenkinsfile in source control
✓ Use parameterized builds
✓ Implement proper error handling
✓ Use stages for clear visualization
✓ Add timeout for each stage
✓ Clean workspace after build
✓ Archive only necessary artifacts
```

### Resource Management

```
✓ Set build retention policy (30 days)
✓ Limit concurrent builds
✓ Use lightweight checkout
✓ Clean workspace before build
✓ Compress large artifacts
```

### Security

```
✓ Use credentials plugin for secrets
✓ Don't hardcode passwords
✓ Use role-based access control
✓ Enable CSRF protection
✓ Regular Jenkins updates
✓ Use HTTPS for Jenkins URL
```

### Notifications

```
✓ Send email on failure only (reduce noise)
✓ Include relevant build information
✓ Link to Allure report
✓ Use different channels (email, Slack)
✓ Notify responsible team/person
```

---

## 🎯 Advanced Configuration

### Multi-Branch Pipeline

Create a multi-branch pipeline to automatically create jobs for each branch:

```
1. New Item → Multibranch Pipeline
2. Name: EcoCash-API-Automation-MultiBranch
3. Branch Sources → Add source → GitHub
4. Repository: sunilkumar-netizen/EcoCahSndbox-API-automation
5. Credentials: [Select credentials]
6. Behaviors:
   - Discover branches
   - Discover pull requests from origin
7. Build Configuration:
   - Mode: by Jenkinsfile
   - Script Path: Jenkinsfile
8. Scan Multibranch Pipeline Triggers:
   - Periodically if not otherwise run: 1 hour
9. Save
```

### Parallel Execution

Modify Jenkinsfile for parallel test execution:

```groovy
stage('Run Tests in Parallel') {
    parallel {
        stage('Smoke Tests') {
            steps {
                sh './run_tests.sh -e qa -t @smoke'
            }
        }
        stage('Auth Tests') {
            steps {
                sh './run_tests.sh -e qa -t @auth'
            }
        }
        stage('Payment Tests') {
            steps {
                sh './run_tests.sh -e qa -t @payments'
            }
        }
    }
}
```

### Docker Agent

Use Docker containers as build agents:

```groovy
pipeline {
    agent {
        docker {
            image 'python:3.10'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
    // ... rest of pipeline
}
```

---

## 📚 Useful Jenkins URLs

```
Dashboard:              http://localhost:8080
Configuration:          http://localhost:8080/configure
Plugin Manager:         http://localhost:8080/pluginManager
Credentials:            http://localhost:8080/credentials
System Log:             http://localhost:8080/log
Script Console:         http://localhost:8080/script
Build Queue:            http://localhost:8080/queue
Node Management:        http://localhost:8080/computer
```

---

## 🎓 Quick Reference Commands

### Jenkins CLI

```bash
# Download Jenkins CLI
curl -O http://localhost:8080/jnlpJars/jenkins-cli.jar

# Build a job
java -jar jenkins-cli.jar -s http://localhost:8080 build EcoCash-API-Automation

# Get build status
java -jar jenkins-cli.jar -s http://localhost:8080 get-build EcoCash-API-Automation 1

# Install plugin
java -jar jenkins-cli.jar -s http://localhost:8080 install-plugin allure-jenkins-plugin

# Restart Jenkins
java -jar jenkins-cli.jar -s http://localhost:8080 safe-restart
```

### Groovy Script Examples

Execute in Jenkins Script Console (`http://localhost:8080/script`):

```groovy
// List all jobs
Jenkins.instance.getAllItems(Job.class).each { 
    println it.name 
}

// Get last build status
def job = Jenkins.instance.getJob('EcoCash-API-Automation')
def build = job.getLastBuild()
println "Status: ${build.result}"

// Trigger a build
def job = Jenkins.instance.getJob('EcoCash-API-Automation')
job.scheduleBuild(0, new hudson.model.Cause.UserIdCause())
```

---

## ✅ Setup Checklist

### Pre-Setup
- [ ] Jenkins installed and running
- [ ] Access to Jenkins admin account
- [ ] GitHub repository accessible
- [ ] Python 3.10+ installed on Jenkins server

### Plugin Installation
- [ ] Git Plugin installed
- [ ] GitHub Plugin installed
- [ ] Pipeline Plugin installed
- [ ] Allure Plugin installed
- [ ] JUnit Plugin installed
- [ ] Email Extension Plugin installed

### Configuration
- [ ] Git configured in Tools
- [ ] Allure Commandline configured
- [ ] Email SMTP configured
- [ ] GitHub credentials added
- [ ] Jenkins URL set correctly

### Job Creation
- [ ] Pipeline job created
- [ ] GitHub repository connected
- [ ] Jenkinsfile located
- [ ] Build triggers configured
- [ ] Parameters set up

### Testing
- [ ] Manual build successful
- [ ] Webhook trigger working
- [ ] Reports generated correctly
- [ ] Email notifications working
- [ ] Artifacts archived properly

---

## 🚀 Next Steps

After successful setup:

1. **Run First Build**
   - Execute manual smoke test
   - Verify all stages pass
   - Check Allure report

2. **Configure Notifications**
   - Set up email recipients
   - Configure Slack (optional)
   - Test notifications

3. **Set Up Monitoring**
   - Create dashboard views
   - Set up build trends
   - Monitor disk space

4. **Team Training**
   - Share Jenkins URL
   - Train team on running builds
   - Document custom procedures

5. **Optimization**
   - Tune build times
   - Optimize parallel execution
   - Set up caching

---

## 📞 Support and Resources

### Documentation
- Jenkins Official Docs: https://www.jenkins.io/doc/
- Allure Jenkins Plugin: https://github.com/allure-framework/allure-jenkins-plugin
- Pipeline Syntax: https://www.jenkins.io/doc/book/pipeline/syntax/

### Community
- Jenkins User Mailing List
- Stack Overflow: #jenkins
- Jenkins Subreddit: r/jenkinsci

### Internal Contacts
- DevOps Team: devops@company.com
- QA Team Lead: qa-lead@company.com
- Jenkins Admin: jenkins-admin@company.com

---

**Document**: Jenkins Setup Guide  
**Version**: 1.0  
**Date**: January 27, 2026  
**Author**: DevOps Team  
**Status**: ✅ Complete  

---

*For questions or issues, contact your DevOps team or refer to the Jenkins documentation.*
