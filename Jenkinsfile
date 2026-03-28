pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install dependencies') {
            steps {
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && pip install --upgrade pip'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Run dataset tests') {
            steps {
                sh '. venv/bin/activate && pytest tests/ -v'
            }
        }

        stage('Run main pipeline') {
            steps {
                sh '. venv/bin/activate && python src/main.py'
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
            echo 'Pipeline finalizado.'
        }
        success {
            echo 'Ejecución exitosa.'
        }
        failure {
            echo 'La ejecución falló. Revisar logs.'
        }
    }
}