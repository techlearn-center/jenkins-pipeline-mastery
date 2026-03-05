# Module 09: Docker & Kubernetes Integration

| | |
|---|---|
| **Time** | 5 hours |
| **Difficulty** | Advanced |
| **Prerequisites** | Module 08 completed |

---

## Learning Objectives

- Build Docker images inside Jenkins pipelines
- Push images to container registries
- Deploy to Kubernetes from Jenkins

---

## Hands-On Lab

### Exercise 1: Full Docker Build Pipeline

```groovy
pipeline {
    agent any
    environment {
        REGISTRY = 'localhost:5000'
        IMAGE = 'myapp'
        TAG = "${BUILD_NUMBER}"
    }
    stages {
        stage('Build Image') {
            steps {
                sh '''
                    cat > /tmp/Dockerfile << DEOF
FROM python:3.11-slim
RUN pip install flask
COPY . /app
WORKDIR /app
CMD ["python", "app.py"]
DEOF
                    mkdir -p /tmp/myapp
                    echo 'from flask import Flask; app = Flask(__name__)' > /tmp/myapp/app.py
                    docker build -t ${REGISTRY}/${IMAGE}:${TAG} -f /tmp/Dockerfile /tmp/myapp
                    docker tag ${REGISTRY}/${IMAGE}:${TAG} ${REGISTRY}/${IMAGE}:latest
                '''
            }
        }
        stage('Push Image') {
            steps {
                sh '''
                    docker push ${REGISTRY}/${IMAGE}:${TAG}
                    docker push ${REGISTRY}/${IMAGE}:latest
                '''
            }
        }
        stage('Verify') {
            steps {
                sh 'curl -s http://${REGISTRY}/v2/${IMAGE}/tags/list'
            }
        }
    }
    post {
        always {
            sh "docker rmi ${REGISTRY}/${IMAGE}:${TAG} || true"
        }
    }
}
```

### Exercise 2: Kubernetes Deployment

```groovy
stage('Deploy to K8s') {
    steps {
        sh '''
            kubectl set image deployment/myapp \
              myapp=${REGISTRY}/${IMAGE}:${TAG}
            kubectl rollout status deployment/myapp --timeout=120s
        '''
    }
}
```

**Next: [Module 10 →](../10-production-pipeline-patterns/)**
