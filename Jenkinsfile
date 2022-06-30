pipeline {
<<<<<<< HEAD
    agent { docker { image 'python:3.8' } }

    environment {
        VIRTUAL_ENV = '/var/jenkins_home/workspace/backupmanager_mb_main/venv'
    }
    stages {
        stage('Setup Python') {
            steps {
                sh "python -m venv ${env.VIRTUAL_ENV}"
            }
        }
        stage('Install') {
            steps {
                sh "export PATH=${env.VIRTUAL_ENV}/bin:$PATH && pip install -e \".[all]\""
            }
        }
        stage('Tests') {
            parallel {
                stage('Test') {
                    steps {
                        sh "export PATH=${env.VIRTUAL_ENV}/bin:$PATH && pytest"
                    }
                }
                stage('Type') {
                    steps {
                        sh "export PATH=${env.VIRTUAL_ENV}/bin:$PATH && mypy src/"
                    }
                }
                stage('lint') {
                    steps {
                        sh "export PATH=${env.VIRTUAL_ENV}/bin:$PATH && flake8 src/"
                    }
                }
            }
        }
=======
  agent any
  stages {
    stage('Hello') {
      steps {
        echo 'Hello World'
      }
>>>>>>> ea64d2d97daffd0bcc0ec095acc60e697fefa8c9
    }

  }
}