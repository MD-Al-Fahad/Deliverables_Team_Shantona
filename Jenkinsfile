pipeline {
    agent any

    stages {
        stage('Setup Workspace') {
            steps {
                echo '--- 📂 Generaring Demo Files ---'
                sh 'mkdir -p app'
                sh '''
                echo "from flask import Flask, jsonify
app = Flask(__name__)

@app.route(\'/\')
def home():
    return \'<h1>Jenkins Deployment Success!</h1>\'

@app.route(\'/health\')
def health():
    return jsonify(status=\'UP\'), 200

if __name__ == \'__main__\':
    app.run(host=\'0.0.0.0\', port=5000)" > app/main.py
                '''
                sh '''
                echo "import unittest
from main import app

class BasicTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    def test_health(self):
        response = self.app.get(\'/health\')
        self.assertEqual(response.status_code, 200)

if __name__ == \'__main__\':
    unittest.main()" > app/test_app.py
                '''
                sh '''
                echo "FROM python:3.9-slim
WORKDIR /app
RUN pip install flask
COPY app/ .
CMD [\\"python\\", \\"main.py\\"]" > Dockerfile
                '''
                sh '''
                echo "version: \'3\'
services:
  web:
    build: .
    ports:
      - \\"5000:5000\\"
    container_name: demo-production" > docker-compose.yml
                '''
            }
        }

        stage('Install & Test') {
            steps {
                echo '--- 🧪 Running Unit Tests ---'
                sh 'pip install flask --break-system-packages'
                sh 'python3 app/test_app.py'
            }
        }

        stage('Build Image') {
            steps {
                echo '--- 🐳 Building Docker Image ---'
                sh 'docker-compose build'
            }
        }

        stage('Deploy') {
            steps {
                echo '--- 🚀 Deploying Container ---'
                sh 'docker-compose up -d --force-recreate'
            }
        }

        stage('Health Check') {
            steps {
                echo '--- 🏥 Verifying Deployment ---'
                sleep 10 
                script {
                    sh '''
                    python3 -c "import urllib.request, sys; 
try: 
    print(urllib.request.urlopen('http://host.docker.internal:5000/health').getcode())
except: 
    sys.exit(1)"
                    '''
                }
                echo "✅ SUCCESS: App is Healthy!"
            }
        }
    }
}