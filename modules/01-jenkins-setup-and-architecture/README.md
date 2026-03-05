# Module 01: Jenkins Setup & Architecture

| | |
|---|---|
| **Time** | 3 hours |
| **Difficulty** | Beginner |
| **Prerequisites** | Docker installed |

---

## Learning Objectives

- Understand Jenkins architecture (controller, agents, executors, plugins)
- Install Jenkins using Docker with auto-configured plugins
- Navigate the Jenkins UI and create your first job
- Understand the Jenkinsfile concept

---

## Concepts

### Jenkins Architecture

```
┌─────────────────────────────┐
│     Jenkins Controller       │
│  ┌─────────┐ ┌───────────┐ │
│  │ Web UI  │ │ Pipeline  │ │
│  │ :8080   │ │ Engine    │ │
│  └─────────┘ └───────────┘ │
│  ┌─────────┐ ┌───────────┐ │
│  │ Plugins │ │ Credential│ │
│  │ Manager │ │ Store     │ │
│  └─────────┘ └───────────┘ │
└──────────┬──────────────────┘
           │ JNLP / SSH
    ┌──────┴──────┐
┌───┴───┐   ┌───┴───┐
│Agent 1│   │Agent 2│
│Maven  │   │Node.js│
└───────┘   └───────┘
```

**Controller:** The brain — schedules builds, serves UI, manages plugins.
**Agent:** The hands — executes build steps. Can be Docker containers, VMs, or bare metal.
**Executor:** A thread on an agent. 2 executors = 2 parallel builds on that agent.
**Plugin:** Extends Jenkins. There are 1800+ plugins for everything from Git to Slack.

---

## Hands-On Lab

### Step 1: Start Jenkins

```bash
cd jenkins-pipeline-mastery
docker compose up -d --build

# Wait ~2 minutes for Jenkins to initialize
# Watch the logs:
docker logs -f jenkins
# When you see "Jenkins is fully up and running", press Ctrl+C
```

### Step 2: Access the Dashboard

Open http://localhost:8080

The setup wizard is disabled. Jenkins is ready to use with pre-installed plugins.

### Step 3: Create Your First Freestyle Job

1. Click **New Item**
2. Name: `hello-world` → Select **Freestyle project** → OK
3. Under **Build Steps** → **Add build step** → **Execute shell**:

```bash
echo "=== Hello from Jenkins! ==="
echo "Build Number: $BUILD_NUMBER"
echo "Workspace:    $WORKSPACE"
echo "Node:         $NODE_NAME"
echo "Java Version: $(java -version 2>&1 | head -1)"
date
```

4. Click **Save** → **Build Now**
5. Click build **#1** → **Console Output**

**Expected output:**
```
=== Hello from Jenkins! ===
Build Number: 1
Workspace:    /var/jenkins_home/workspace/hello-world
Node:         built-in
Java Version: openjdk version "17.0.x"
Finished: SUCCESS
```

### Step 4: Create Your First Pipeline Job

1. **New Item** → Name: `first-pipeline` → **Pipeline** → OK
2. In the **Pipeline** section, paste:

```groovy
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
            }
        }
        stage('Build') {
            steps {
                sh 'echo "Compiling application..."'
                sh 'mkdir -p build && echo "compiled binary" > build/app'
            }
        }
        stage('Test') {
            steps {
                sh 'echo "Running 42 tests... ALL PASSED"'
            }
        }
        stage('Deploy') {
            steps {
                sh 'echo "Deploying to staging environment..."'
            }
        }
    }

    post {
        success { echo 'Pipeline completed successfully!' }
        failure { echo 'Pipeline failed!' }
    }
}
```

3. **Save** → **Build Now** → Click the build → **Console Output**

You should see each stage execute in sequence and the **Stage View** on the job page shows columns for each stage.

### Step 5: Explore Blue Ocean

1. Click **Open Blue Ocean** in the left sidebar
2. See the visual pipeline view
3. Click on any stage to see its logs

---

## Common Mistakes

| Mistake | Fix |
|---|---|
| Jenkins stuck on loading | Wait 3-5 min. Check: `docker logs jenkins` |
| Port 8080 already in use | Stop the other service or change the port in docker-compose.yml |
| Plugins not installed | Rebuild: `docker compose down && docker compose up -d --build` |

---

## Self-Check Questions

1. What is the difference between the controller and an agent?
2. What is an executor and how does it relate to parallelism?
3. Why use Pipeline jobs instead of Freestyle jobs?
4. What does `agent any` mean in a Jenkinsfile?
5. Where does Jenkins store its data inside the container?

---

## You Know You Have Completed This Module When...

- [ ] Jenkins is running at http://localhost:8080
- [ ] You created and ran a Freestyle job
- [ ] You created and ran a Pipeline job
- [ ] You can see the Stage View for your pipeline
- [ ] Validation script passes

**Next: [Module 02 →](../02-freestyle-to-pipeline/)**
