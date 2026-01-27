# ⚡ Jenkins Quick Start Guide - 15 Minutes Setup

## Get Your Pipeline Running in 15 Minutes!

---

## 🎯 Quick Overview

This guide will help you set up Jenkins and get your first build running in **15 minutes**.

```
Step 1: Install Jenkins        (5 min)
Step 2: Install Plugins        (3 min)
Step 3: Create Job             (4 min)
Step 4: Run First Build        (3 min)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Time:                    15 min
```

---

## ⏱️ Step 1: Install Jenkins (5 minutes)

### Option A: Docker (Fastest - Recommended)

```bash
# 1. Pull and run Jenkins (1 command!)
docker run -d \
  --name jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  jenkins/jenkins:lts

# 2. Get admin password
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword

# 3. Open browser
open http://localhost:8080
```

### Option B: macOS (Homebrew)

```bash
# 1. Install Jenkins
brew install jenkins-lts

# 2. Start Jenkins
brew services start jenkins-lts

# 3. Get admin password
cat /usr/local/var/jenkins_home/secrets/initialAdminPassword

# 4. Open browser
open http://localhost:8080
```

### Initial Setup Wizard

1. **Unlock Jenkins**: Paste the admin password
2. **Install Plugins**: Click "Install suggested plugins" (wait 2-3 min)
3. **Create Admin**: Fill in your details
4. **Save and Finish**

✅ **Jenkins is now running!**

---

## ⏱️ Step 2: Install Required Plugins (3 minutes)

### Go to: Manage Jenkins → Plugins → Available Plugins

Install these **5 essential plugins**:

```
1. ✓ Allure Plugin
2. ✓ GitHub Plugin  
3. ✓ Pipeline Plugin
4. ✓ JUnit Plugin
5. ✓ Email Extension Plugin
```

**How to install:**
1. Search for plugin name
2. Check the checkbox
3. Click "Install without restart"
4. Wait for installation to complete

✅ **Plugins installed!**

---

## ⏱️ Step 3: Create Your First Job (4 minutes)

### 3.1 Add GitHub Credentials (1 min)

1. Go to: **Manage Jenkins** → **Credentials** → **System** → **Global credentials** → **Add Credentials**
2. Fill in:
   ```
   Kind: Username with password
   Username: sunilkumar-netizen
   Password: [Your GitHub Personal Access Token]
   ID: github-credentials
   Description: GitHub Access
   ```
3. Click **Create**

> **Get Token**: GitHub → Settings → Developer settings → Personal access tokens → Generate new token (classic)
> Select: `repo` and `admin:repo_hook` permissions

### 3.2 Create Pipeline Job (2 min)

1. Click **"New Item"**
2. Enter name: `EcoCash-API-Tests`
3. Select: **"Pipeline"**
4. Click **OK**

### 3.3 Configure Pipeline (1 min)

**General Section:**
```
Description: EcoCash API Test Automation
✓ GitHub project
  Project URL: https://github.com/sunilkumar-netizen/EcoCahSndbox-API-automation
```

**Pipeline Section:**
```
Definition: Pipeline script from SCM

SCM: Git
  Repository URL: https://github.com/sunilkumar-netizen/EcoCahSndbox-API-automation.git
  Credentials: github-credentials
  Branch: */main

Script Path: Jenkinsfile
```

Click **Save**

✅ **Job created!**

---

## ⏱️ Step 4: Run Your First Build (3 minutes)

### 4.1 Trigger Build

1. Click on your job: **"EcoCash-API-Tests"**
2. Click **"Build with Parameters"**
3. Select:
   ```
   ENVIRONMENT: qa
   TAGS: smoke
   PARALLEL_EXECUTION: false
   ```
4. Click **"Build"**

### 4.2 Monitor Execution

Watch the build progress:
```
Build #1 → Console Output

Expected output:
📥 Checking out code...           ✓
🔧 Setting up environment...      ✓
🔍 Running code linting...        ✓
🧪 Running smoke tests...         ✓
📊 Generating reports...          ✓
📤 Publishing results...          ✓
```

### 4.3 View Results

After build completes (2-3 min):

**Test Results:**
- Click **"Test Result"** → See pass/fail count
- Expected: 3 passed, 6 failed (due to token expiry)

**Allure Report:**
- Click **"Allure Report"** → Beautiful HTML report
- Browse test details, graphs, timeline

✅ **First build complete!**

---

## 🎉 Success Checklist

```
✓ Jenkins installed and running
✓ Required plugins installed  
✓ GitHub credentials configured
✓ Pipeline job created
✓ First build executed successfully
✓ Test results visible
✓ Allure report generated
```

---

## 🚀 What's Next?

### Immediate Next Steps (10 minutes)

#### 1. Set Up Email Notifications (5 min)

Go to: **Manage Jenkins** → **System** → **Extended E-mail Notification**

**Gmail Configuration:**
```
SMTP server: smtp.gmail.com
SMTP port: 587
Username: your-email@gmail.com
Password: [Your App Password]  ← Generate from Google Account
Use TLS: Yes

Default Recipients: your-team@company.com
```

**Test Email:**
```bash
# Add this to Jenkinsfile post section:
post {
    always {
        emailext(
            subject: "Test Results - ${env.BUILD_NUMBER}",
            body: "Build completed. Check ${env.BUILD_URL}",
            to: "your-email@company.com"
        )
    }
}
```

#### 2. Set Up Auto-Trigger via GitHub Webhook (5 min)

**In GitHub Repository:**
1. Go to: **Settings** → **Webhooks** → **Add webhook**
2. Configure:
   ```
   Payload URL: http://your-jenkins-url:8080/github-webhook/
   Content type: application/json
   Events: Just the push event
   Active: ✓
   ```
3. Click **Add webhook**

**Test:**
```bash
# Push a change
cd /Users/sunilkumar/EcoCash_API_Automation
echo "test" >> test.txt
git add test.txt
git commit -m "Test webhook"
git push

# Jenkins should auto-trigger within 10 seconds!
```

---

## 📊 Quick Reference

### Common Actions

| Action | Location |
|--------|----------|
| View all jobs | Jenkins Dashboard |
| Build job | Job → Build with Parameters |
| View build logs | Build # → Console Output |
| View test results | Build # → Test Result |
| View Allure report | Build # → Allure Report |
| Configure job | Job → Configure |
| Install plugins | Manage Jenkins → Plugins |
| Add credentials | Manage Jenkins → Credentials |

### Build Parameters

| Parameter | Options | Description |
|-----------|---------|-------------|
| ENVIRONMENT | qa, dev, uat | Test environment |
| TAGS | smoke, regression, payments, all | Test tags to run |
| PARALLEL_EXECUTION | true/false | Run tests in parallel |

### URLs

```
Jenkins Dashboard:    http://localhost:8080
Configuration:        http://localhost:8080/configure
Plugin Manager:       http://localhost:8080/pluginManager
Credentials:          http://localhost:8080/credentials
Your Job:             http://localhost:8080/job/EcoCash-API-Tests/
```

---

## 🐛 Quick Troubleshooting

### Issue: Jenkins won't start
```bash
# Check if port 8080 is already in use
lsof -i :8080

# Stop existing process or use different port
docker run -p 9090:8080 jenkins/jenkins:lts
```

### Issue: Can't install plugins
```
Solution: Check internet connection
Go to: Manage Jenkins → Plugin Manager → Advanced
Update site URL: https://updates.jenkins.io/update-center.json
Click "Check now"
```

### Issue: GitHub authentication fails
```
Solution: Use Personal Access Token (not password)
1. GitHub → Settings → Developer settings
2. Personal access tokens → Tokens (classic)
3. Generate new token
4. Select: repo, admin:repo_hook
5. Copy token and use as password in Jenkins
```

### Issue: Python not found
```bash
# For Docker Jenkins, install Python:
docker exec -u root jenkins bash -c "apt-get update && apt-get install -y python3 python3-pip python3-venv"

# For native Jenkins, ensure Python is in PATH
which python3  # Should show: /usr/bin/python3
```

### Issue: Tests not running
```
Check:
1. Jenkinsfile exists in repository
2. GitHub credentials are correct
3. Branch name is correct (main vs master)
4. Workspace has feature files
5. Python dependencies installed
```

---

## 💡 Pro Tips

### Tip 1: Speed Up Builds
```groovy
// In Jenkinsfile, add caching:
stage('Setup') {
    steps {
        sh '''
            if [ ! -d "venv" ]; then
                python3 -m venv venv
            fi
            . venv/bin/activate
            pip install -r requirements.txt
        '''
    }
}
```

### Tip 2: Better Console Output
```
Install plugins:
- AnsiColor (colored output)
- Timestamper (timestamps)

Enable in Jenkinsfile:
options {
    ansiColor('xterm')
    timestamps()
}
```

### Tip 3: Slack Notifications
```groovy
// Add to post section:
post {
    success {
        slackSend(
            color: 'good',
            message: "✅ Tests passed! <${env.BUILD_URL}|View>"
        )
    }
}
```

### Tip 4: Schedule Regular Runs
```
Build Triggers → Build periodically:

H 2 * * *      # Daily at 2 AM
H */4 * * *    # Every 4 hours  
H 9-17 * * 1-5 # Hourly during business hours (weekdays)
```

### Tip 5: Create Build Badge
```
Add to GitHub README.md:

[![Build Status](http://your-jenkins:8080/buildStatus/icon?job=EcoCash-API-Tests)](http://your-jenkins:8080/job/EcoCash-API-Tests/)
```

---

## 📚 Learn More

### Essential Reading (Total: 30 min)

1. **Pipeline Syntax** (10 min)
   - https://www.jenkins.io/doc/book/pipeline/syntax/

2. **Jenkinsfile Examples** (10 min)
   - https://www.jenkins.io/doc/pipeline/examples/

3. **Best Practices** (10 min)
   - https://www.jenkins.io/doc/book/pipeline/best-practices/

### Video Tutorials

- Jenkins Tutorial for Beginners (YouTube)
- CI/CD with Jenkins (Jenkins.io)
- Allure Report Integration (Allure Framework)

---

## ✅ Final Checklist

Before going live:

```
Infrastructure:
✓ Jenkins accessible by team
✓ Adequate disk space (10GB+)
✓ Backup strategy in place
✓ SSL/HTTPS configured (production)

Configuration:
✓ All required plugins installed
✓ Email notifications working
✓ GitHub webhook configured
✓ Build retention policy set
✓ User access controls set

Testing:
✓ Manual build successful
✓ Auto-trigger working
✓ Reports generating correctly
✓ Notifications received
✓ Team can access Jenkins

Documentation:
✓ Team trained on Jenkins usage
✓ Troubleshooting guide shared
✓ Support contacts documented
```

---

## 🎊 Congratulations!

You now have:
- ✅ Working Jenkins server
- ✅ Automated test pipeline  
- ✅ Beautiful Allure reports
- ✅ Email notifications
- ✅ GitHub integration

**Time to celebrate!** 🎉

---

## 📞 Need Help?

### Quick Help Resources

| Issue | Resource |
|-------|----------|
| Jenkins setup | JENKINS_SETUP_GUIDE.md (detailed guide) |
| Test failures | SMOKE_TEST_RESULTS_JAN27.md |
| Framework usage | README.md |
| API details | CLIENT_PRESENTATION.md |

### Support Contacts

```
Jenkins Issues:     devops@company.com
Test Framework:     qa-team@company.com
GitHub Access:      git-admin@company.com
General Questions:  sunil.kumar@company.com
```

---

## 🚀 Advanced Features (Later)

Once comfortable with basics, explore:

1. **Multi-branch Pipeline** - Auto-create jobs for each branch
2. **Parallel Execution** - Run tests faster
3. **Docker Agents** - Isolated build environments
4. **Blue Ocean UI** - Modern Jenkins interface
5. **Pipeline Libraries** - Reusable pipeline code
6. **Integration with Jira** - Link builds to tickets
7. **Performance Monitoring** - Track build times
8. **Matrix Builds** - Test multiple configurations

All covered in: `JENKINS_SETUP_GUIDE.md`

---

**Document**: Jenkins Quick Start  
**Version**: 1.0  
**Date**: January 27, 2026  
**Time to Complete**: 15 minutes  
**Difficulty**: Beginner  
**Status**: ✅ Ready to Use  

---

*Get started now! Follow steps 1-4 and you'll have a running pipeline in 15 minutes.*
