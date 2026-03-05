# Module 03: Declarative Pipeline Fundamentals

| | |
|---|---|
| **Time** | 5 hours |
| **Difficulty** | Intermediate |
| **Prerequisites** | Module 02 completed |

---

## Learning Objectives

- Master `agent`, `stages`, `steps`, `environment`, `parameters`
- Use `when` conditions for conditional stages
- Implement `post` sections for cleanup
- Work with credentials in pipelines

---

## Hands-On Lab

### Exercise 1: Parameterized Pipeline

```groovy
pipeline {
    agent any

    parameters {
        choice(name: 'ENV', choices: ['dev', 'staging', 'prod'], description: 'Target environment')
        string(name: 'VERSION', defaultValue: '1.0.0', description: 'App version')
        booleanParam(name: 'SKIP_TESTS', defaultValue: false, description: 'Skip test stage?')
    }

    environment {
        APP_NAME = 'myservice'
        BUILD_TS = sh(script: 'date +%Y%m%d-%H%M%S', returnStdout: true).trim()
    }

    stages {
        stage('Info') {
            steps {
                echo "Deploying ${APP_NAME} v${params.VERSION} to ${params.ENV}"
                echo "Build timestamp: ${BUILD_TS}"
            }
        }
        stage('Build') {
            steps {
                sh 'echo "Building artifact..."'
                sh 'mkdir -p dist && echo "${APP_NAME}-${BUILD_TS}" > dist/build.txt'
            }
        }
        stage('Test') {
            when { expression { !params.SKIP_TESTS } }
            steps {
                sh 'echo "Running test suite..."'
                sh 'echo "47 tests passed, 0 failed"'
            }
        }
        stage('Deploy to Dev') {
            when { expression { params.ENV == 'dev' } }
            steps { echo 'Deployed to dev!' }
        }
        stage('Deploy to Staging') {
            when { expression { params.ENV == 'staging' } }
            steps { echo 'Deployed to staging!' }
        }
        stage('Deploy to Prod') {
            when { expression { params.ENV == 'prod' } }
            steps {
                input message: 'Approve production deployment?', ok: 'Deploy'
                echo 'Deploying to production...'
            }
        }
    }

    post {
        success { echo "SUCCESS: ${APP_NAME} v${params.VERSION} deployed to ${params.ENV}" }
        failure { echo "FAILED: Check logs above" }
        always  { sh 'rm -rf dist/' }
    }
}
```

Run this pipeline, then click **Build with Parameters** to see the parameter form.

### Exercise 2: Credentials Binding

First add a credential in Jenkins:
1. Manage Jenkins → Credentials → Global → Add Credentials
2. Kind: **Secret text**, ID: `my-api-token`, Secret: `sk-test-abc123`

Then use it:

```groovy
pipeline {
    agent any
    environment {
        API_TOKEN = credentials('my-api-token')
    }
    stages {
        stage('Use Secret') {
            steps {
                sh 'echo "Token length: ${#API_TOKEN}"'
                // Jenkins masks the secret in console output!
                sh 'echo "Token: $API_TOKEN"'
            }
        }
    }
}
```

Notice that Jenkins replaces the actual secret value with `****` in the console output.

### Exercise 3: Archiving Artifacts

```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh '''
                    mkdir -p artifacts
                    echo "Build output v${BUILD_NUMBER}" > artifacts/app.jar
                    echo "Build log" > artifacts/build.log
                    tar czf release-${BUILD_NUMBER}.tar.gz artifacts/
                '''
            }
        }
        stage('Archive') {
            steps {
                archiveArtifacts artifacts: 'release-*.tar.gz', fingerprint: true
                archiveArtifacts artifacts: 'artifacts/build.log'
            }
        }
    }
}
```

After building, you can download the artifacts from the build page.

---

## Self-Check Questions

1. What is the difference between `environment` at pipeline level vs stage level?
2. How does Jenkins handle secrets in console output?
3. What does `input` do and who can approve it?
4. When does the `post { always }` block run?

**Next: [Module 04 →](../04-pipeline-advanced-features/)**
