pipeline {
    agent any

    stages {
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t pytest-runner .'
            }
        }

        stage('Run Test Suites in Parallel') {
            parallel {
                stage('Regression Tests') {
                    steps {
                        sh 'docker run --rm pytest-runner -m regression --html=reports/regression.html --self-contained-html'
                    }
                }
                stage('Integration Tests') {
                    steps {
                        sh 'docker run --rm pytest-runner -m integration --html=reports/integration.html --self-contained-html'
                    }
                }
                stage('Sanity Tests') {
                    steps {
                        sh 'docker run --rm pytest-runner -m sanity --html=reports/sanity.html --self-contained-html'
                    }
                }
                stage('System Tests') {
                    steps {
                        sh 'docker run --rm pytest-runner -m system --html=reports/system.html --self-contained-html'
                    }
                }
            }
        }
         stage('Send Email') {
            steps {
                emailext (
                    subject: "Pytest Report",
                    body: "Test execution completed. Please find the attached HTML report.",
                    to: "deepthi1987.p@gmail.com",
                    attachLog: false,
                    attachmentsPattern: "reports/report.html"
                )
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'reports/*.html', allowEmptyArchive: true
        }
    }
}

