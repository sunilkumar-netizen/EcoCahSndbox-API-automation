// Jenkinsfile for API Automation (uses run_tests.sh)
// Pipeline: Checkout -> Setup -> Lint -> Run Tests (run_tests.sh) -> Reports -> Publish
// Option A: agent any (requires python3-venv on the node - see README)
// Option B: Docker agent below - works without installing Python on Jenkins node (requires Docker Pipeline plugin)

pipeline {
    agent {
        docker {
            image 'python:3.10-slim'
            reuseNode true
        }
    }

    parameters {
        choice(
            name: 'ENVIRONMENT',
            choices: ['qa', 'dev', 'uat'],
            description: 'Environment to run tests against'
        )
        choice(
            name: 'TAGS',
            choices: ['smoke', 'regression', 'payments', 'auth', 'users', 'all'],
            description: 'Test tags to execute (use "all" for full suite)'
        )
        booleanParam(
            name: 'PARALLEL_EXECUTION',
            defaultValue: false,
            description: 'Run tests in parallel'
        )
        booleanParam(
            name: 'SKIP_LINT',
            defaultValue: false,
            description: 'Skip code linting stage'
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
                echo 'Checking out code...'
                checkout scm
            }
        }

        stage('Setup Environment') {
            steps {
                echo 'Setting up Python environment...'
                sh '''
                    set +e
                    for py in python3.10 python3.9 python3; do
                        if command -v $py >/dev/null 2>&1 && $py -m venv ${VENV_DIR} 2>/dev/null; then
                            break
                        fi
                        rm -rf ${VENV_DIR}
                    done
                    set -e
                    if [ ! -f ${VENV_DIR}/bin/activate ]; then
                        echo ""
                        echo "ERROR: Could not create Python virtual environment."
                        echo "On Debian/Ubuntu Jenkins agents install Python and venv, e.g.:"
                        echo "  sudo apt update && sudo apt install -y python3.10 python3.10-venv"
                        echo "  (or: sudo apt install -y python3.8-venv if using Python 3.8)"
                        exit 1
                    fi
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Lint Code') {
            when {
                expression { return !params.SKIP_LINT }
            }
            steps {
                echo 'Running code linting...'
                sh '''
                    . ${VENV_DIR}/bin/activate
                    pip install flake8 --quiet
                    flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics || true
                '''
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    def envLower = params.ENVIRONMENT?.toLowerCase() ?: 'qa'
                    def tagArg = (params.TAGS == 'all') ? '' : "-t ${params.TAGS}"
                    def parallelArg = params.PARALLEL_EXECUTION ? '-p' : ''
                    def cmd = "./run_tests.sh -e ${envLower} ${tagArg} ${parallelArg}".trim()
                    echo "Running: ${cmd}"
                    sh """
                        chmod +x run_tests.sh
                        ${cmd} || true
                    """
                }
            }
        }

        stage('Generate Reports') {
            steps {
                echo 'Test reports: see HTML Test Report in Publish Results (Allure plugin not installed on this Jenkins).'
            }
        }

        stage('Publish Results') {
            steps {
                echo 'Publishing test results and artifacts...'
                junit "${REPORTS_DIR}/junit/*.xml"
                publishHTML(target: [
                    allowMissing: true,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: "${REPORTS_DIR}/html-report",
                    reportFiles: 'report.html',
                    reportName: 'HTML Test Report'
                ])
                archiveArtifacts artifacts: 'logs/*.log', allowEmptyArchive: true
                archiveArtifacts artifacts: "${REPORTS_DIR}/**/*", allowEmptyArchive: true
                archiveArtifacts artifacts: 'reports/html-report/report.html', allowEmptyArchive: true
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
        success {
            echo 'Pipeline completed successfully.'
            script {
                if (env.NOTIFICATION_EMAIL?.trim()) {
                    emailext(
                        subject: "API Tests PASSED - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
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
                catchError(buildResult: null, message: 'Slack notification skipped') {
                    slackSend(
                        channel: '#api-automation-executions',
                        color: 'good',
                        message: """✅ *API Automation – PASSED*
Job: ${env.JOB_NAME} #${env.BUILD_NUMBER}
Environment: ${params.ENVIRONMENT} | Tags: ${params.TAGS}
<${env.BUILD_URL}|View Build> | <${env.BUILD_URL}HTML_20Test_20Report|HTML Report>"""
                    )
                }
            }
        }
        failure {
            echo 'Pipeline failed.'
            script {
                if (env.NOTIFICATION_EMAIL?.trim()) {
                    emailext(
                        subject: "API Tests FAILED - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
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
                catchError(buildResult: null, message: 'Slack notification skipped') {
                    slackSend(
                        channel: '#api-automation-executions',
                        color: 'danger',
                        message: """❌ *API Automation – FAILED*
Job: ${env.JOB_NAME} #${env.BUILD_NUMBER}
Environment: ${params.ENVIRONMENT} | Tags: ${params.TAGS}
<${env.BUILD_URL}console|View Console>"""
                    )
                }
            }
        }
        unstable {
            echo 'Pipeline is unstable (e.g. test failures).'
            script {
                catchError(buildResult: null, message: 'Slack notification skipped') {
                    slackSend(
                        channel: '#api-automation-executions',
                        color: 'warning',
                        message: """⚠️ *API Automation – UNSTABLE* (some tests failed)
Job: ${env.JOB_NAME} #${env.BUILD_NUMBER}
Environment: ${params.ENVIRONMENT} | Tags: ${params.TAGS}
<${env.BUILD_URL}|View Build> | <${env.BUILD_URL}HTML_20Test_20Report|HTML Report>"""
                    )
                }
            }
        }
    }
}
