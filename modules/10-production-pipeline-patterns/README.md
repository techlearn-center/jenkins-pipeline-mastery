# Module 10: Production Pipeline Patterns

| | |
|---|---|
| **Time** | 5 hours |
| **Difficulty** | Advanced |
| **Prerequisites** | Module 09 completed |

---

## Learning Objectives

- Implement blue-green deployments
- Build canary release pipelines
- Configure multi-branch pipelines
- Add approval gates for production

---

## Hands-On Lab

### Exercise 1: Blue-Green Deployment

```groovy
pipeline {
    agent any
    environment {
        ACTIVE = 'blue'
        INACTIVE = 'green'
    }
    stages {
        stage('Deploy to Inactive') {
            steps {
                echo "Deploying new version to ${INACTIVE} environment..."
                sh "echo 'v${BUILD_NUMBER}' > /tmp/${INACTIVE}-version.txt"
            }
        }
        stage('Smoke Test') {
            steps {
                sh "cat /tmp/${INACTIVE}-version.txt"
                echo "Smoke tests passed on ${INACTIVE}!"
            }
        }
        stage('Switch Traffic') {
            steps {
                input message: "Switch traffic from ${ACTIVE} to ${INACTIVE}?", ok: 'Switch!'
                echo "Switching load balancer to ${INACTIVE}..."
                echo "Traffic now serving from ${INACTIVE}"
            }
        }
        stage('Cleanup Old') {
            steps {
                echo "Old ${ACTIVE} environment kept for rollback"
            }
        }
    }
}
```

### Exercise 2: Multi-Environment Pipeline with Approval

```groovy
pipeline {
    agent any
    stages {
        stage('Build & Test') {
            steps {
                sh 'echo "Build and test passed"'
            }
        }
        stage('Deploy to Dev') {
            steps {
                sh 'echo "Deployed to dev"'
            }
        }
        stage('Deploy to Staging') {
            steps {
                sh 'echo "Deployed to staging"'
            }
        }
        stage('Staging Tests') {
            steps {
                sh 'echo "Integration and E2E tests passed on staging"'
            }
        }
        stage('Production Approval') {
            steps {
                input message: 'Deploy to production?',
                      submitter: 'admin',
                      parameters: [
                          string(name: 'TICKET', defaultValue: '', description: 'Change ticket #')
                      ]
            }
        }
        stage('Deploy to Production') {
            steps {
                echo "Deploying with change ticket: ${TICKET}"
                sh 'echo "Rolling update: 25% -> 50% -> 100%"'
            }
        }
    }
}
```

### Exercise 3: Multi-Branch Pipeline

1. **New Item** → `my-multibranch` → **Multibranch Pipeline**
2. Add Git source (point to a repo with Jenkinsfiles)
3. Jenkins auto-discovers branches:
   - `main` branch → production pipeline
   - `develop` branch → staging pipeline
   - `feature/*` branches → test-only pipeline

```groovy
// Jenkinsfile that behaves differently per branch
pipeline {
    agent any
    stages {
        stage('Build') {
            steps { sh 'echo "Building..."' }
        }
        stage('Deploy to Prod') {
            when { branch 'main' }
            steps { echo 'Production deployment!' }
        }
        stage('Deploy to Staging') {
            when { branch 'develop' }
            steps { echo 'Staging deployment!' }
        }
    }
}
```

**Next: [Capstone Project →](../../capstone/)**
