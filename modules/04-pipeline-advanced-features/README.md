# Module 04: Pipeline Advanced Features

| | |
|---|---|
| **Time** | 4 hours |
| **Difficulty** | Intermediate |
| **Prerequisites** | Module 03 completed |

---

## Learning Objectives

- Run stages in parallel for faster builds
- Use matrix builds for multi-platform testing
- Implement retry, timeout, and error handling

---

## Hands-On Lab

### Exercise 1: Parallel Stages

```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps { sh 'echo "Building..." && sleep 2' }
        }
        stage('Parallel Tests') {
            parallel {
                stage('Unit Tests') {
                    steps { sh 'echo "Unit tests..." && sleep 3' }
                }
                stage('Integration Tests') {
                    steps { sh 'echo "Integration tests..." && sleep 4' }
                }
                stage('Security Scan') {
                    steps { sh 'echo "Security scan..." && sleep 2' }
                }
            }
        }
        stage('Deploy') {
            steps { sh 'echo "Deploying..."' }
        }
    }
}
```

The three test stages run **simultaneously**. Total test time = 4s (longest) instead of 9s (sum).

### Exercise 2: Matrix Builds

```groovy
pipeline {
    agent any
    stages {
        stage('Test Across Platforms') {
            matrix {
                axes {
                    axis {
                        name 'PLATFORM'
                        values 'linux', 'macos', 'windows'
                    }
                    axis {
                        name 'JAVA_VER'
                        values '11', '17', '21'
                    }
                }
                excludes {
                    exclude {
                        axis { name 'PLATFORM'; values 'windows' }
                        axis { name 'JAVA_VER'; values '11' }
                    }
                }
                stages {
                    stage('Test') {
                        steps {
                            echo "Testing on ${PLATFORM} with Java ${JAVA_VER}"
                        }
                    }
                }
            }
        }
    }
}
```

This generates 3x3=9 combinations minus 1 exclusion = **8 parallel test runs**.

### Exercise 3: Retry and Timeout

```groovy
pipeline {
    agent any
    options {
        timeout(time: 30, unit: 'MINUTES')
        timestamps()
    }
    stages {
        stage('Flaky Deploy') {
            steps {
                retry(3) {
                    sh '''
                        RANDOM_NUM=$((RANDOM % 3))
                        if [ $RANDOM_NUM -eq 0 ]; then
                            echo "Deploy succeeded!"
                        else
                            echo "Deploy failed, retrying..."
                            exit 1
                        fi
                    '''
                }
            }
        }
        stage('Wait for Health') {
            steps {
                timeout(time: 2, unit: 'MINUTES') {
                    sh 'echo "Health check passed"'
                }
            }
        }
    }
}
```

**Next: [Module 05 →](../05-shared-libraries/)**
