# Jenkinsfile for API Automation

pipeline {
    agent any
    
    parameters {
        choice(
            name: 'ENVIRONMENT',
            choices: ['qa', 'dev', 'uat'],
            description: 'Environment to run tests against'
        )
        choice(
            name: 'TAGS',
            choices: ['smoke', 'regression', 'payments', 'auth', 'users', 'all'],
            description: 'Test tags to execute'
        )
        booleanParam(
            name: 'PARALLEL_EXECUTION',
            defaultValue: false,
            description: 'Run tests in parallel'
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
                script {
                    def tagParam = params.TAGS == 'all' ? '' : "--tags=${params.TAGS}"
                    
                    sh """
                        . ${VENV_DIR}/bin/activate
                        mkdir -p ${REPORTS_DIR}/allure-results
                        mkdir -p ${REPORTS_DIR}/junit
                        
                        behave -D env=${params.ENVIRONMENT} ${tagParam} \
                            -f allure_behave.formatter:AllureFormatter \
                            -o ${REPORTS_DIR}/allure-results \
                            --junit --junit-directory ${REPORTS_DIR}/junit \
                            || true
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
            emailext(
                subject: "✅ API Tests PASSED - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <h2>Test Execution Successful</h2>
                    <p><strong>Environment:</strong> ${params.ENVIRONMENT}</p>
                    <p><strong>Tags:</strong> ${params.TAGS}</p>
                    <p><strong>Build:</strong> ${env.BUILD_NUMBER}</p>
                    <p><a href="${env.BUILD_URL}allure">View Allure Report</a></p>
                """,
                to: "${env.NOTIFICATION_EMAIL}",
                mimeType: 'text/html'
            )
        }
        
        failure {
            echo '❌ Pipeline failed!'
            emailext(
                subject: "❌ API Tests FAILED - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <h2>Test Execution Failed</h2>
                    <p><strong>Environment:</strong> ${params.ENVIRONMENT}</p>
                    <p><strong>Tags:</strong> ${params.TAGS}</p>
                    <p><strong>Build:</strong> ${env.BUILD_NUMBER}</p>
                    <p><a href="${env.BUILD_URL}console">View Console Output</a></p>
                    <p><a href="${env.BUILD_URL}allure">View Allure Report</a></p>
                """,
                to: "${env.NOTIFICATION_EMAIL}",
                mimeType: 'text/html'
            )
        }
        
        unstable {
            echo '⚠️ Pipeline is unstable!'
        }
    }
}
