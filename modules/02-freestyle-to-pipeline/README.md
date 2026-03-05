# Module 02: Freestyle to Pipeline

| | |
|---|---|
| **Time** | 3 hours |
| **Difficulty** | Beginner |
| **Prerequisites** | Module 01 completed |

---

## Learning Objectives

- Understand why pipelines replace freestyle jobs
- Migrate a freestyle job to a Jenkinsfile
- Store Jenkinsfiles in Git (Pipeline as Code)
- Know Declarative vs Scripted syntax

---

## Concepts

### Why Pipelines Win

| Feature | Freestyle | Pipeline |
|---|---|---|
| Config stored in | Jenkins UI (not in Git) | Jenkinsfile (in Git) |
| Code review | Not possible | PR review on Jenkinsfile |
| Complex logic | Very limited | Full programming (parallel, conditions) |
| Shared across projects | Copy-paste | Shared libraries |
| Disaster recovery | Reconfigure manually | Jenkinsfile recreates everything |

### Declarative vs Scripted

**Declarative** (use this 95% of the time):
```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps { sh 'make build' }
        }
    }
}
```

**Scripted** (when you need full Groovy flexibility):
```groovy
node {
    stage('Build') {
        sh 'make build'
    }
}
```

---

## Hands-On Lab

### Exercise 1: Migrate a Freestyle Job

Take the freestyle job from Module 01 and convert it to a pipeline:

1. **New Item** → `migrated-pipeline` → **Pipeline**
2. Pipeline script:

```groovy
pipeline {
    agent any
    stages {
        stage('System Info') {
            steps {
                sh '''
                    echo "=== System Information ==="
                    echo "Build: #${BUILD_NUMBER}"
                    echo "Node: ${NODE_NAME}"
                    uname -a
                    java -version 2>&1 | head -1
                    python3 --version
                '''
            }
        }
        stage('Disk Check') {
            steps {
                sh 'df -h /var/jenkins_home'
            }
        }
    }
}
```

### Exercise 2: Jenkinsfile in a Git Repository

Create a Jenkinsfile for the sample Python app:

```bash
# On your local machine (not inside Jenkins container)
cat > sample-apps/python-app/Jenkinsfile << 'JFILE'
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
                sh '''
                    cd sample-apps/python-app
                    python3 -m pip install --user -r requirements.txt
                '''
            }
        }
        stage('Lint') {
            steps {
                sh '''
                    cd sample-apps/python-app
                    python3 -m pip install --user flake8
                    python3 -m flake8 app/ --max-line-length=120 || true
                '''
            }
        }
        stage('Test') {
            steps {
                sh '''
                    cd sample-apps/python-app
                    python3 -m pytest tests/ -v --tb=short
                '''
            }
        }
    }

    post {
        always { echo 'Pipeline finished.' }
        success { echo 'All stages passed!' }
        failure { echo 'Something failed. Check the logs above.' }
    }
}
JFILE
```

---

## Self-Check Questions

1. Why is "Pipeline as Code" better than UI-configured jobs?
2. What happens to your Jenkins jobs if the server crashes with Freestyle vs Pipeline?
3. When would you use Scripted syntax over Declarative?

---

## You Know You Have Completed This Module When...

- [ ] You migrated a freestyle job to a pipeline
- [ ] You created a Jenkinsfile for a real application
- [ ] You understand Declarative vs Scripted syntax

**Next: [Module 03 →](../03-declarative-pipeline-fundamentals/)**
