# Module 07: Credentials & Security

| | |
|---|---|
| **Time** | 3 hours |
| **Difficulty** | Intermediate |
| **Prerequisites** | Module 06 completed |

---

## Learning Objectives

- Add and manage credentials (passwords, SSH keys, tokens, certificates)
- Use withCredentials for secure access in pipelines
- Configure Role-Based Access Control (RBAC)

---

## Hands-On Lab

### Exercise 1: Add Credentials

In Jenkins UI: Manage Jenkins → Credentials → System → Global credentials → Add:

1. **Username with password** — ID: `docker-hub`, Username: `myuser`, Password: `mypass`
2. **Secret text** — ID: `api-token`, Secret: `sk-prod-abc123xyz`
3. **Secret file** — ID: `kubeconfig`, upload a file

### Exercise 2: Use Credentials in Pipeline

```groovy
pipeline {
    agent any
    stages {
        stage('Login to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'docker-hub',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh 'echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin'
                }
            }
        }
        stage('Call API') {
            steps {
                withCredentials([string(credentialsId: 'api-token', variable: 'TOKEN')]) {
                    sh 'curl -H "Authorization: Bearer $TOKEN" https://httpbin.org/get'
                }
            }
        }
    }
}
```

**Key point:** Jenkins automatically masks credential values in console output with `****`.

### Exercise 3: Folder-Scoped Credentials

1. Create a folder: New Item → `team-alpha` → Folder
2. Inside the folder, add credentials scoped to it
3. Jobs outside the folder **cannot** access these credentials
4. This provides team-level isolation

**Next: [Module 08 →](../08-testing-and-quality-gates/)**
