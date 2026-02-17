# Jenkinsfile for API Automation

pipeline {
    agent any
    
    parameters {
        choice(
            name: 'ENVIRONMENT',
            choices: ['qa', 'uat', 'dev'],
            description: 'Environment to run tests against'
        )
        choice(
            name: 'TAGS',
            choices: ['smoke', '@sasai', 'regression', 'payments', 'auth', 'payment_request', 'all'],
            description: 'Test tags to execute (smoke and @sasai use global auth optimization)'
        )
        booleanParam(
            name: 'PARALLEL_EXECUTION',
            defaultValue: false,
            description: 'Run tests in parallel'
        )
        booleanParam(
            name: 'SEND_EMAIL_REPORT',
            defaultValue: true,
            description: 'Send email report after test execution'
        )
    }
    
    environment {
        PYTHON_VERSION = '3.10'
        VENV_DIR = 'venv'
        REPORTS_DIR = 'reports'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo '📥 Checking out code...'
                checkout scm
            }
        }
        
        stage('Setup Environment') {
            steps {
                echo '🔧 Setting up Python environment...'
                sh '''
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Lint Code') {
            steps {
                echo '🔍 Running code linting...'
                sh '''
                    . ${VENV_DIR}/bin/activate
                    pip install flake8
                    flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics || true
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                echo "🧪 Running ${params.TAGS} tests in ${params.ENVIRONMENT} environment..."
                echo "ℹ️  Note: 'smoke' and '@sasai' tags use global authentication optimization (97% fewer auth API calls)"
                script {
                    def tagParam = params.TAGS == 'all' ? '' : "--tags=${params.TAGS}"
                    
                    sh """
                        . ${VENV_DIR}/bin/activate
                        mkdir -p ${REPORTS_DIR}/allure-results
                        mkdir -p ${REPORTS_DIR}/junit
                        mkdir -p ${REPORTS_DIR}/html-report
                        mkdir -p logs
                        
                        # Run tests with Behave
                        behave -D env=${params.ENVIRONMENT} ${tagParam} \
                            -f allure_behave.formatter:AllureFormatter \
                            -o ${REPORTS_DIR}/allure-results \
                            -f behave_html_formatter:HTMLFormatter \
                            -o ${REPORTS_DIR}/html-report/report.html \
                            --junit --junit-directory ${REPORTS_DIR}/junit \
                            || true
                        
                        # Send email report if enabled
                        if [ "${params.SEND_EMAIL_REPORT}" = "true" ]; then
                            echo "📧 Sending email report..."
                            python3 scripts/send_email_report.py ${params.ENVIRONMENT} ${params.TAGS} || true
                        fi
                    """
                }
            }
        }
        
        stage('Generate Reports') {
            steps {
                echo '📊 Generating test reports...'
                script {
                    allure([
                        includeProperties: false,
                        jdk: '',
                        properties: [],
                        reportBuildPolicy: 'ALWAYS',
                        results: [[path: "${REPORTS_DIR}/allure-results"]]
                    ])
                }
            }
        }
        
        stage('Publish Results') {
            steps {
                echo '📤 Publishing test results...'
                junit "${REPORTS_DIR}/junit/*.xml"
                
                // Archive artifacts
                archiveArtifacts artifacts: 'logs/*.log', allowEmptyArchive: true
                archiveArtifacts artifacts: "${REPORTS_DIR}/**/*", allowEmptyArchive: true
            }
        }
    }
    
    post {
        always {
            echo '🧹 Cleaning up...'
            cleanWs()
        }
        
        success {
            echo '✅ Pipeline completed successfully!'
            script {
                def optimizationNote = (params.TAGS == 'smoke' || params.TAGS == '@sasai') ? 
                    '<p><strong>🚀 Performance:</strong> Global authentication optimization enabled (97% fewer API calls)</p>' : ''
                
                emailext(
                    subject: "✅ OneApp API Tests PASSED - ${params.ENVIRONMENT} - ${params.TAGS} - Build #${env.BUILD_NUMBER}",
                    body: """
                        <h2>✅ Test Execution Successful</h2>
                        <p><strong>Environment:</strong> ${params.ENVIRONMENT}</p>
                        <p><strong>Tags:</strong> ${params.TAGS}</p>
                        <p><strong>Build:</strong> ${env.BUILD_NUMBER}</p>
                        ${optimizationNote}
                        <p><a href="${env.BUILD_URL}allure">📊 View Allure Report</a></p>
                        <p><a href="${env.BUILD_URL}console">📋 View Console Output</a></p>
                    """,
                    to: "sunil.kumar8@kellton.com, vishnu@sasaifintech.com",
                    mimeType: 'text/html'
                )
            }
        }
        
        failure {
            echo '❌ Pipeline failed!'
            emailext(
                subject: "❌ OneApp API Tests FAILED - ${params.ENVIRONMENT} - ${params.TAGS} - Build #${env.BUILD_NUMBER}",
                body: """
                    <h2>❌ Test Execution Failed</h2>
                    <p><strong>Environment:</strong> ${params.ENVIRONMENT}</p>
                    <p><strong>Tags:</strong> ${params.TAGS}</p>
                    <p><strong>Build:</strong> ${env.BUILD_NUMBER}</p>
                    <p><a href="${env.BUILD_URL}console">📋 View Console Output</a></p>
                    <p><a href="${env.BUILD_URL}allure">📊 View Allure Report</a></p>
                    <p><strong>⚠️ Action Required:</strong> Please investigate the failures</p>
                """,
                to: "sunil.kumar8@kellton.com, vishnu@sasaifintech.com",
                mimeType: 'text/html'
            )
        }
        
        unstable {
            echo '⚠️ Pipeline is unstable!'
        }
    }
}
