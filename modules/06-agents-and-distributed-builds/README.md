# Module 06: Agents & Distributed Builds

| | |
|---|---|
| **Time** | 4 hours |
| **Difficulty** | Intermediate |
| **Prerequisites** | Module 05 completed |

---

## Learning Objectives

- Use Docker containers as ephemeral build agents
- Assign different agents per stage
- Understand Kubernetes-based dynamic agents

---

## Hands-On Lab

### Exercise 1: Docker Agent

```groovy
pipeline {
    agent {
        docker {
            image 'python:3.11-slim'
            args '-v $HOME/.cache/pip:/root/.cache/pip'
        }
    }
    stages {
        stage('Check Python') {
            steps {
                sh 'python --version'
                sh 'pip --version'
            }
        }
        stage('Install & Test') {
            steps {
                sh 'pip install requests pytest'
                sh 'python -c "import requests; print(requests.__version__)"'
            }
        }
    }
}
```

Jenkins pulls the Docker image, runs the pipeline inside it, then destroys the container. **Clean environment every time.**

### Exercise 2: Different Agents per Stage

```groovy
pipeline {
    agent none

    stages {
        stage('Build Java') {
            agent { docker { image 'maven:3.9-eclipse-temurin-17' } }
            steps {
                sh 'mvn --version'
                sh 'echo "Java build done"'
            }
        }
        stage('Build Frontend') {
            agent { docker { image 'node:20-alpine' } }
            steps {
                sh 'node --version'
                sh 'npm --version'
                sh 'echo "Frontend build done"'
            }
        }
        stage('Deploy') {
            agent { docker { image 'alpine:latest' } }
            steps {
                sh 'echo "Deploying from lightweight container..."'
            }
        }
    }
}
```

Each stage uses the **perfect container** for that specific task.

### Exercise 3: Kubernetes Pod Template

```groovy
pipeline {
    agent {
        kubernetes {
            yaml '''
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: maven
    image: maven:3.9-eclipse-temurin-17
    command: ['sleep', '3600']
  - name: docker
    image: docker:dind
    securityContext:
      privileged: true
'''
        }
    }
    stages {
        stage('Build') {
            steps {
                container('maven') {
                    sh 'mvn --version'
                }
            }
        }
        stage('Docker') {
            steps {
                container('docker') {
                    sh 'docker --version'
                }
            }
        }
    }
}
```

**Next: [Module 07 →](../07-credentials-and-security/)**
