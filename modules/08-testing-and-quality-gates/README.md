# Module 08: Testing & Quality Gates

| | |
|---|---|
| **Time** | 5 hours |
| **Difficulty** | Advanced |
| **Prerequisites** | Module 07 completed |

---

## Learning Objectives

- Publish JUnit test reports in Jenkins
- Integrate SonarQube for code quality analysis
- Implement quality gates that block deployments

---

## Hands-On Lab

### Exercise 1: JUnit Reports

```groovy
pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                sh '''
                    mkdir -p test-results
                    cat > test-results/results.xml << XMLEOF
<?xml version="1.0" encoding="UTF-8"?>
<testsuite name="MyApp" tests="3" failures="0" time="1.5">
  <testcase classname="com.example.AppTest" name="testAdd" time="0.5"/>
  <testcase classname="com.example.AppTest" name="testSub" time="0.3"/>
  <testcase classname="com.example.AppTest" name="testMul" time="0.7"/>
</testsuite>
XMLEOF
                '''
            }
            post {
                always {
                    junit 'test-results/*.xml'
                }
            }
        }
    }
}
```

After running, Jenkins shows a **Test Result Trend** graph on the job page.

### Exercise 2: SonarQube Integration

```bash
# SonarQube is already running at http://localhost:9000
# Default login: admin / admin
# Create a project and token in SonarQube UI
```

```groovy
pipeline {
    agent any
    environment {
        SONAR_TOKEN = credentials('sonar-token')
    }
    stages {
        stage('SonarQube Analysis') {
            steps {
                sh '''
                    # For a Python project:
                    pip install sonar-scanner-cli || true
                    sonar-scanner \
                      -Dsonar.projectKey=myapp \
                      -Dsonar.sources=. \
                      -Dsonar.host.url=http://sonarqube:9000 \
                      -Dsonar.token=$SONAR_TOKEN || true
                '''
            }
        }
        stage('Quality Gate') {
            steps {
                echo 'In production, use: waitForQualityGate abortPipeline: true'
                echo 'This blocks the pipeline if code quality is below threshold'
            }
        }
    }
}
```

**Next: [Module 09 →](../09-docker-and-kubernetes-integration/)**
