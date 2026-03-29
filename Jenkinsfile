pipeline {
    agent any

    options {
        timestamps()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Check Python') {
            steps {
                sh 'python3 --version'
                sh 'pip3 --version'
            }
        }

        stage('Install dependencies') {
            steps {
                sh 'pip3 install --upgrade pip'
                sh 'pip3 install -r requirements.txt'
            }
        }

        stage('Test dataset') {
            steps {
                sh 'python3 -m pytest tests -v'
            }
        }

        stage('Run pipeline') {
            steps {
                sh 'python3 -m src.main'
            }
        }

        stage('Archive artifacts') {
            steps {
                archiveArtifacts artifacts: 'outputs/**', fingerprint: true
            }
        }
    }

    post {
        always {
            echo 'Pipeline terminado.'
        }
        success {
            echo 'Pipeline exitoso.'
        }
        failure {
            echo 'Pipeline falló. Revisa la consola y los artefactos.'
        }
    }
}