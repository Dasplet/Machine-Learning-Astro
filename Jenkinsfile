pipeline {
    agent {
        docker {
            image 'python:3.11-slim'
            args '-u root:root'
        }
    }

    options {
        timestamps()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install dependencies') {
            steps {
                sh 'python --version'
                sh 'pip install --upgrade pip'
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Test dataset') {
            steps {
                sh 'python -m pytest tests -v'
            }
        }

        stage('Run pipeline') {
            steps {
                sh 'python -m src.main'
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