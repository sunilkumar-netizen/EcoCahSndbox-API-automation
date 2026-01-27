# EcoCash API Automation Framework

## 🚀 Enterprise-Grade Python BDD API Testing Framework

A comprehensive, production-ready API automation framework built with Python + Behave (BDD) for REST API testing. Designed for enterprise QA teams with scalability, maintainability, and best practices in mind.

---

## 📋 Table of Contents

- [Tech Stack](#tech-stack)
- [Framework Features](#framework-features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Writing Tests](#writing-tests)
- [Running Tests](#running-tests)
- [Reports](#reports)
- [CI/CD Integration](#cicd-integration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Language** | Python 3.10+ |
| **BDD Framework** | Behave |
| **HTTP Client** | Requests |
| **Assertions** | Pytest-style |
| **Reporting** | Allure |
| **Config Management** | YAML |
| **Logging** | Colorlog |
| **Data Generation** | Faker |
| **Schema Validation** | jsonschema |

---

## ✨ Framework Features

### Core Capabilities

✅ **BDD Implementation** - Gherkin syntax for business-readable test scenarios  
✅ **Reusable HTTP Client** - Generic API client with retry & timeout handling  
✅ **Multi-Environment Support** - dev, qa, uat, prod configurations  
✅ **Comprehensive Assertions** - Status code, headers, body, schema validation  
✅ **Centralized Logging** - Color-coded console + file logging  
✅ **Dynamic Test Data** - Faker-based realistic data generation  
✅ **JSON Schema Validation** - Contract testing support  
✅ **Allure Reporting** - Rich HTML reports with charts  
✅ **Error Handling** - Graceful failures with meaningful logs  
✅ **Data-Driven Testing** - Scenario Outline support  

### Advanced Features

🔐 **Authentication Support** - Bearer, Basic, API Key  
🔄 **Token Refresh** - Automatic token management  
⚡ **Retry Mechanism** - Configurable retry with backoff  
📊 **Response Time Validation** - Performance testing  
🎯 **Tag-Based Execution** - Run specific test groups  
🌐 **Parallel Execution** - Speed up test runs  

---

## 📁 Project Structure

```
api-automation-framework/
│
├── config/                      # Environment configurations
│   ├── dev.yaml                # Development environment
│   ├── qa.yaml                 # QA environment
│   └── uat.yaml                # UAT environment
│
├── features/                   # BDD feature files
│   ├── payments.feature       # Payment API scenarios
│   ├── auth.feature           # Authentication scenarios
│   └── user.feature           # User management scenarios
│
├── step_definitions/          # Step implementations
│   ├── payments_steps.py     # Payment step definitions
│   ├── auth_steps.py         # Auth step definitions
│   ├── user_steps.py         # User step definitions
│   └── common_steps.py       # Shared step definitions
│
├── core/                      # Core framework modules
│   ├── api_client.py         # HTTP client with retry
│   ├── base_test.py          # Base test class
│   ├── assertions.py         # Assertion utilities
│   └── logger.py             # Logging configuration
│
├── utils/                     # Utility modules
│   ├── config_loader.py      # YAML config loader
│   └── data_generator.py     # Test data generator
│
├── payloads/                  # Request payloads
│   ├── payment_request.json
│   ├── user_request.json
│   └── auth_request.json
│
├── schemas/                   # JSON schemas
│   └── (schema files)
│
├── reports/                   # Test reports
│   ├── allure-results/
│   └── junit/
│
├── logs/                      # Execution logs
│
├── requirements.txt           # Python dependencies
├── behave.ini                 # Behave configuration
├── environment.py             # Behave hooks
└── README.md                  # This file
```

---

## 📦 Prerequisites

- **Python**: 3.10 or higher
- **pip**: Latest version
- **Java**: 8+ (for Allure reports)
- **Git**: For version control

---

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd EcoCash_API_Automation
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Verify Installation

```bash
behave --version
allure --version
```

---

## ⚙️ Configuration

### Environment Configuration

Edit configuration files in `config/` directory:

```yaml
# config/qa.yaml
environment: qa

api:
  base_url: https://qa-api.ecocash.example.com
  timeout: 30
  retry_count: 3

auth:
  type: bearer
  token: your_qa_token_here

headers:
  Content-Type: application/json
  X-Client-Id: ecocash-automation
```

### Switch Environments

Use `-D env=<environment>` flag:

```bash
behave -D env=dev      # Development
behave -D env=qa       # QA (default)
behave -D env=uat      # UAT
```

---

## 🎯 Usage

### Quick Start

```bash
# Run all tests in QA environment
behave -D env=qa

# Run with specific tags
behave -D env=qa --tags=smoke

# Run with Allure reporting
behave -D env=qa -f allure_behave.formatter:AllureFormatter -o reports/allure-results
```

### Common Commands

```bash
# Run smoke tests only
behave --tags=smoke

# Run all payment tests
behave --tags=payments

# Run positive test cases
behave --tags=positive

# Exclude work-in-progress
behave --tags=-wip

# Run multiple tags
behave --tags=smoke,payments

# Dry run (check syntax)
behave --dry-run

# Show detailed output
behave --no-capture
```

---

## ✍️ Writing Tests

### Feature File Example

```gherkin
Feature: Payment API Testing
  As a merchant
  I want to process payments via API
  
  @smoke @payments
  Scenario: Create a new payment
    Given I have valid payment details
    When I send POST request to "/api/v1/payments"
    Then response status code should be 201
    And response body should contain "transaction_id"
    And response time should be less than 3000 ms
```

### Step Definition Example

```python
@given('I have valid payment details')
def step_have_payment_details(context):
    data_gen = DataGenerator()
    context.request_data = data_gen.generate_payment_data()

@when('I send POST request to "{endpoint}"')
def step_send_post(context, endpoint):
    context.response = context.base_test.api_client.post(
        endpoint=endpoint,
        json_data=context.request_data
    )

@then('response status code should be {status_code:d}')
def step_verify_status(context, status_code):
    assertions = context.base_test.assert_response(context.response)
    assertions.assert_status_code(status_code)
```

---

## 🏃 Running Tests

### Basic Execution

```bash
# Run all tests
behave

# Run with environment
behave -D env=qa

# Run specific feature
behave features/payments.feature

# Run specific scenario
behave features/payments.feature:10  # Line number
```

### Advanced Execution

```bash
# Parallel execution (requires pytest-xdist)
behave --processes 4 --parallel-element scenario

# Generate JUnit report
behave --junit --junit-directory reports/junit

# Verbose output
behave -v

# Stop on first failure
behave --stop

# Show skipped scenarios
behave --show-skipped
```

---

## 📊 Reports

### Allure Reports

#### Generate Report

```bash
# Run tests with Allure formatter
behave -D env=qa -f allure_behave.formatter:AllureFormatter -o reports/allure-results

# Serve report (opens in browser)
allure serve reports/allure-results

# Generate static HTML report
allure generate reports/allure-results -o reports/allure-report --clean
```

#### View Report

```bash
# Open generated report
allure open reports/allure-report
```

### Log Files

Execution logs are saved in `logs/` directory:

```
logs/
├── automation_20260120_143000.log
└── qa.log
```

---

## 🔄 CI/CD Integration

### GitHub Actions Example

```yaml
name: API Automation Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.10
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        behave -D env=qa -f allure_behave.formatter:AllureFormatter -o reports/allure-results
    
    - name: Generate Allure Report
      uses: simple-elf/allure-report-action@master
      with:
        allure_results: reports/allure-results
```

### Jenkins Pipeline

```groovy
pipeline {
    agent any
    
    stages {
        stage('Setup') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('Test') {
            steps {
                sh 'behave -D env=qa -f allure_behave.formatter:AllureFormatter -o reports/allure-results'
            }
        }
        
        stage('Report') {
            steps {
                allure includeProperties: false, 
                       jdk: '', 
                       results: [[path: 'reports/allure-results']]
            }
        }
    }
}
```

---

## 🎨 Best Practices

### 1. Feature Files
- Use clear, business-readable language
- Follow Given-When-Then pattern
- Keep scenarios focused and independent
- Use tags for organization

### 2. Step Definitions
- Make steps reusable across features
- Avoid hardcoded values
- Use context to share data between steps
- Follow naming conventions

### 3. Configuration
- Never commit sensitive data (tokens, passwords)
- Use environment variables for secrets
- Maintain separate configs per environment

### 4. Test Data
- Use Faker for dynamic data generation
- Avoid using production data
- Clean up test data after execution

### 5. Assertions
- Use meaningful assertion messages
- Validate all critical response fields
- Include schema validation for contracts

### 6. Logging
- Log all API requests/responses
- Mask sensitive information
- Use appropriate log levels

---

## 🐛 Troubleshooting

### Common Issues

#### Import Errors

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

#### Connection Errors

- Check base_url in config file
- Verify network connectivity
- Check VPN/proxy settings

#### Allure Report Not Generated

```bash
# Install Allure command-line tool
brew install allure  # macOS
# or download from: https://github.com/allure-framework/allure2/releases
```

#### Python Version Issues

```bash
# Check Python version
python --version

# Use specific Python version
python3.10 -m venv venv
```

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📝 License

This project is proprietary and confidential.

---

## 👥 Contact

**QA Automation Team**  
Email: qa-automation@ecocash.example.com

---

## 🙏 Acknowledgments

- Behave Documentation: https://behave.readthedocs.io/
- Requests Library: https://requests.readthedocs.io/
- Allure Framework: https://docs.qameta.io/allure/

---

**Last Updated**: January 2026  
**Framework Version**: 1.0.0
