pipeline {
  agent any

  environment {
    REACT_DIR = 'frontend'
    DJANGO_DIR = 'backend'
    DEPLOY_DIR = '/home/deploy/app'
    DATABASE_URL = credentials('DATABASE_URL')
    TEST_DATABASE_URL = credentials('TEST_DATABASE_URL')
  }

  options {
    skipDefaultCheckout true // optional: prevents double checkout
  }

  stages {
    stage('Clean Workspace') {
      steps {
        cleanWs()
      }
    }

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
        sshagent (credentials: ['deploy-key']) {
          sh 'ssh-keyscan -H pkcoaches.com >> ~/.ssh/known_hosts'
          sh "rsync -avz --exclude 'venv' -e ssh backend/ deploy@${DEPLOY_HOST}:/home/deploy/app/"  
          // Sync built React files to backend static directory
          sh """
            rsync -avz -e ssh frontend/build/ deploy@${DEPLOY_HOST}:${DEPLOY_DIR}/static/
          """
          sh """
            ssh deploy@${DEPLOY_HOST} '
              cd /home/deploy/app &&
              python3.12 -m venv venv &&
              ./venv/bin/pip install --upgrade pip &&
              ./venv/bin/pip install -r requirements.txt &&
              ./venv/bin/python manage.py collectstatic --noinput &&
              ./venv/bin/python manage.py migrate &&
              sudo /bin/systemctl restart gunicorn
            '
          """
        }
      }
    }
  }
}
