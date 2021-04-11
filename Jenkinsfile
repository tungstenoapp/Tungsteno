pipeline {
    agent any

    environment {
        MAJOR_RELEASE = "1"
        MINOR_RELEASE = "4"
        RELEASE_TYPE = "stable"
        RELEASE_CAPTION = "v$MAJOR_RELEASE.$MINOR_RELEASE.$BUILD_ID ($RELEASE_TYPE)"
        GIT_LOCAL_BRANCH = "master"
    }

    stages {
        stage('Build') {
            steps {
                sh 'printenv'
            }
        }

        stage('Install all requirements packages') {
            steps {
                sh "pip3 install --user -r requirements.txt"
            }
        }

        stage('Test') {
            steps {
                sh "python3 -m unittest discover -s tests/ -p \"*_test.py\""
            }
        }

        stage('Generate build (Linux Binary)') {
            steps {
                sh "python3 -m eel app.py tsteno/gui/static --add-data tsteno:tsteno --onefile -n tungsteno"
                sh "mcli cp dist/tungsteno s3/tungsteno-releases/linux/$RELEASE_TYPE/tungsteno-amd64-$MAJOR_RELEASE.$MINOR_RELEASE.$BUILD_ID"
            }
        }

        stage('Generate build (Windows Binary)') {
            agent { label 'Windows' }
            steps{
                checkout scm

                bat "pip install --user -r requirements.txt"
                bat "python -m eel app.py tsteno/gui/static --add-data tsteno;tsteno --onefile -n tungsteno"
                bat "C:\\mc.exe cp dist/tungsteno.exe s3/tungsteno-releases/windows/%RELEASE_TYPE%/tungsteno-amd64-%MAJOR_RELEASE%.%MINOR_RELEASE%.%BUILD_ID%.exe"

                deleteDir()
            }
        }

        stage('Generate build (Docker)') {
            steps {
                sh "/bin/bash ./scripts/deploy_docker.sh"
            }
        }

        stage('Clean up') {
            steps {
                deleteDir()
            }
        }

    }
}