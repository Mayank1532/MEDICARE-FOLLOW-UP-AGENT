pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install') {
            steps {
                bat 'uv sync --frozen'
            }
        }

        stage('Quality') {
            steps {
                bat 'uv run ruff check app tests evaluation'
                bat 'uv run mypy app evaluation'
            }
        }

        stage('Test') {
            steps {
                bat 'uv run pytest -q --cov=app --cov-report=xml'
            }
        }

        stage('Docker Build') {
            steps {
                bat 'docker build -t medicare-followup-agent:ci .'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'coverage.xml', allowEmptyArchive: true
        }
    }
}
