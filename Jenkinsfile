pipeline {
  agent any

  environment {
    REACT_DIR = 'frontend'
    DJANGO_DIR = 'backend'
  }

  stages {
    stage('Checkout') {
      steps {
        git url: 'https://github.com/remesnik/react-django-ci-app', branch: 'main'
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
          sh 'ls -la'
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
        sshagent (credentials: ['your-ssh-credential-id']) {
          sh 'rsync -avz -e ssh backend/ deploy@${DEPLOY_HOST}:/home/deploy/app/'
          sh 'ssh deploy@${DEPLOY_HOST} "cd /home/deploy/app && ./venv/bin/pip install -r requirements.txt"'
          sh 'ssh deploy@${DEPLOY_HOST} "cd /home/deploy/app && ./venv/bin/python manage.py collectstatic --noinput && ./venv/bin/python manage.py migrate"'
          sh 'ssh deploy@${DEPLOY_HOST} "sudo systemctl restart gunicorn"'
        }
      }
    }
  }
}
