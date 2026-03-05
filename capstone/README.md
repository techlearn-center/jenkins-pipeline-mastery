# Capstone: Microservices CI/CD Pipeline

## The Challenge

Build a complete CI/CD pipeline for 3 microservices:

| Service | Language | Port | Build Tool |
|---|---|---|---|
| order-service | Python | 5000 | pip/pytest |
| product-service | Node.js | 3000 | npm/jest |
| java-app | Java | 8080 | Maven |

### Pipeline Requirements

Each microservice must have a Jenkinsfile with:
1. **Checkout** from Git
2. **Build** the application
3. **Test** with published JUnit reports
4. **Security Scan** (lint or SAST)
5. **Docker Build** and push to local registry
6. **Deploy** with health check verification

### Shared Library Requirements

Create a shared library with:
- `standardBuild()` - common build steps
- `dockerPublish()` - build and push Docker images
- `healthCheck()` - verify deployment health

### Acceptance Criteria

- [ ] 3 Jenkinsfiles (one per microservice)
- [ ] Shared library with 3+ custom steps
- [ ] Docker images pushed to `localhost:5000`
- [ ] SonarQube quality gate configured
- [ ] Production deployment requires approval
- [ ] All validation checks pass

## Getting Started

```bash
# The sample apps are in sample-apps/
ls sample-apps/

# Start the lab environment
docker compose up -d

# Create your pipelines in Jenkins at http://localhost:8080
```
