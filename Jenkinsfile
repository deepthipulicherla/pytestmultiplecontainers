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
                        sh '''
                            docker rm -f temp-regression || true
                            docker create --name temp-regression pytest-runner python -m pytest -m regression --html=reports/report.html --self-contained-html
                            docker start -a temp-regression
                            docker cp temp-regression:/app/reports/report.html reports/regression.html || echo "Report not found"
                            docker rm temp-regression
                        '''
                    }
                }
                stage('Integration Tests') {
                    steps {
                        sh '''
                            docker rm -f temp-integration || true
                            docker create --name temp-integration pytest-runner python -m pytest -m integration --html=reports/report.html --self-contained-html
                            docker start -a temp-integration
                            docker cp temp-integration:/app/reports/report.html reports/integration.html || echo "Report not found"
                            docker rm temp-integration
                        '''
                    }
                }
                stage('Sanity Tests') {
                    steps {
                        sh '''
                            docker rm -f temp-sanity || true
                            docker create --name temp-sanity pytest-runner python -m pytest -m sanity --html=reports/report.html --self-contained-html
                            docker start -a temp-sanity
                            docker cp temp-sanity:/app/reports/report.html reports/sanity.html || echo "Report not found"
                            docker rm temp-sanity
                        '''
                    }
                }
                stage('System Tests') {
                    steps {
                        sh '''
                            docker rm -f temp-system || true
                            docker create --name temp-system pytest-runner python -m pytest -m system --html=reports/report.html --self-contained-html
                            docker start -a temp-system
                            docker cp temp-system:/app/reports/report.html reports/system.html || echo "Report not found"
                            docker rm temp-system
                        '''
                    }
                }
            }
        }

        stage('Send Email') {
            steps {
                emailext (
                    subject: "Pytest Report",
                    body: "Test execution completed. Please find the attached HTML reports.",
                    to: "deepthi1987.p@gmail.com",
                    attachLog: false,
                    attachmentsPattern: "reports/*.html"
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
