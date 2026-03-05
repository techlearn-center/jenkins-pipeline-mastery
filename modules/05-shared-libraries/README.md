# Module 05: Shared Libraries

| | |
|---|---|
| **Time** | 4 hours |
| **Difficulty** | Advanced |
| **Prerequisites** | Module 04 completed |

---

## Learning Objectives

- Create a shared library with vars/, src/, resources/
- Write custom pipeline steps as Groovy functions
- Use `@Library` in Jenkinsfiles across projects

---

## Hands-On Lab

### Library Structure

```
shared-library/
  vars/
    standardPipeline.groovy   # Custom pipeline step
    notifySlack.groovy        # Notification helper
    dockerBuild.groovy        # Docker build helper
  src/
    com/example/Utils.groovy  # Groovy class
  resources/
    deploy-template.yaml      # Template files
```

### Exercise 1: Create a Custom Step

Create `vars/standardPipeline.groovy`:

```groovy
// This becomes a callable step: standardPipeline(appName: 'myapp')
def call(Map config = [:]) {
    def appName = config.appName ?: 'app'
    def testCmd = config.testCmd ?: 'echo "no tests"'
    def dockerImage = config.dockerImage ?: "${appName}:latest"

    pipeline {
        agent any
        stages {
            stage('Checkout') {
                steps { checkout scm }
            }
            stage('Build') {
                steps { sh "echo Building ${appName}..." }
            }
            stage('Test') {
                steps { sh testCmd }
            }
            stage('Docker Build') {
                steps {
                    sh "docker build -t ${dockerImage} ."
                }
            }
        }
        post {
            success { echo "${appName} pipeline succeeded!" }
            failure { echo "${appName} pipeline FAILED!" }
        }
    }
}
```

### Exercise 2: Use in a Jenkinsfile

```groovy
@Library('my-shared-lib') _

standardPipeline(
    appName: 'user-service',
    testCmd: 'python -m pytest tests/',
    dockerImage: 'registry:5000/user-service:latest'
)
```

Now every microservice uses the **same pipeline logic** with different parameters. Update the library once, all pipelines benefit.

### Exercise 3: Helper Functions

Create `vars/dockerBuild.groovy`:

```groovy
def call(String imageName, String tag = 'latest') {
    sh "docker build -t ${imageName}:${tag} ."
    sh "docker push ${imageName}:${tag}"
    echo "Pushed ${imageName}:${tag}"
}
```

Use it in any Jenkinsfile:
```groovy
stage('Build Image') {
    steps {
        dockerBuild('registry:5000/myapp', env.BUILD_NUMBER)
    }
}
```

**Next: [Module 06 →](../06-agents-and-distributed-builds/)**
