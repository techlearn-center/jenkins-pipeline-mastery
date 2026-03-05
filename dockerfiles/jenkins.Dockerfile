FROM jenkins/jenkins:lts
USER root
RUN apt-get update && apt-get install -y docker.io python3 python3-pip curl && apt-get clean
USER jenkins
RUN jenkins-plugin-cli --plugins \
  workflow-aggregator git pipeline-stage-view docker-workflow \
  credentials-binding configuration-as-code blueocean \
  junit jacoco sonar job-dsl
ENV JAVA_OPTS="-Djenkins.install.runSetupWizard=false"
