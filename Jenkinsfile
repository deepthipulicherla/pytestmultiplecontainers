pipeline {
    agent any

    stages {
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t pytest-runner .'
            }
        }

        stage('Prepare Workspace') {
            steps {
                sh 'mkdir -p reports'
            }
        }

        stage('Run Test Suites in Parallel') {
            parallel {
                stage('Regression Tests') {
                    steps {
                        sh '''
                            docker rm -f temp-regression || true
                            docker create --name temp-regression pytest-runner python -m pytest -m regression --html=reports/regression.html --self-contained-html
                            docker start -a temp-regression
                            docker cp temp-regression:/app/reports/regression.html reports/regression.html || echo "Report not found"
                            
                        '''
                    }
                }

                stage('Sanity Tests') {
                    steps {
                        sh '''
                            docker rm -f temp-sanity || true
                            docker create --name temp-sanity pytest-runner python -m pytest -m sanity --html=reports/sanity.html --self-contained-html
                            docker start -a temp-sanity
                            docker cp temp-sanity:/app/reports/sanity.html reports/sanity.html || echo "Report not found"

                        '''
                    }
                }
                stage('Parametrize Tests') {
                    steps {
                        sh '''
                            docker rm -f temp-system || true
                            docker create --name temp-system pytest-runner python -m pytest -m parametrize --html=reports/parametrize.html --self-contained-html
                            docker start -a temp-system
                            docker cp temp-system:/app/reports/parametrize.html reports/parametrize.html || echo "Report not found"

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
