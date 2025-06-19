pipeline {
  agent any

  environment {
    REACT_DIR = 'frontend'
    DJANGO_DIR = 'backend'
  }

  stages {
    stage('Checkout') {
      steps {
        git 'https://github.com/your-username/your-repo.git'
      }
    }

    stage('Install Backend Dependencies') {
      steps {
        dir("${DJANGO_DIR}") {
          sh 'python3 -m venv venv'
          sh './venv/bin/pip install -r requirements.txt'
        }
      }
    }

    stage('Install Frontend Dependencies') {
      steps {
        dir("${REACT_DIR}") {
          sh 'npm install'
        }
      }
    }

    stage('Build React') {
      steps {
        dir("${REACT_DIR}") {
          sh 'npm run build'
        }
      }
    }

    stage('Collect Static & Migrate') {
      steps {
        dir("${DJANGO_DIR}") {
          sh './venv/bin/python manage.py migrate'
          sh './venv/bin/python manage.py collectstatic --noinput'
        }
      }
    }

    stage('Deploy') {
      steps {
        sh 'rsync -a frontend/build/ /var/www/frontend/'
        sh 'sudo systemctl restart gunicorn'
      }
    }
  }
}
