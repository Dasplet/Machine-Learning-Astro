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

        stage('Setup Python') {
            steps {
                sh 'python3 --version'
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && python -m pip install --upgrade pip'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Test dataset') {
            steps {
                sh '. venv/bin/activate && python -m pytest tests -v'
            }
        }

        stage('Run pipeline') {
            steps {
                sh '. venv/bin/activate && python -m src.main'
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