# Lesson 4: Container Logs and Metrics

- [Lesson 4: Container Logs and Metrics](#lesson-4-container-logs-and-metrics)
  - [Logging](#logging)
    - [Containers logging](#containers-logging)
    - [Logging in k8s/OpenShift](#logging-in-k8sopenshift)
  - [Metrics](#metrics)
    - [Container & metrics](#container--metrics)

## Logging 

### Containers logging 

Things to learn in this section:
- How should containers log and why?
- Where are container logs stored?
- Understand which log drivers are used.

Steps:
- Start container and watch logs
  - `podman run -it -p 8080:8080 --rm --name logtest -t quay.io/rhsacz/ed-app:0.3.0`
- Start Container in background 
  - `podman run -d -p 8080:8080 --rm --log-driver k8s-file  --name logtest -t quay.io/rhsacz/ed-app:0.3.0`
- View container logs
  - `podman logs -f logtest`
  - Try also `podman logs --latest`
- Make requests to generate logs
  - `curl localhost:8080`
- Check how logs are stored, explore directory 
  - Find logs location in `podman inspect --latest| less`
  - View logs in k8s file
    - `tail -f $(podman inspect --latest --format '{{ .HostConfig.LogConfig.Path }}')`

### Logging in k8s/OpenShift

Things to learn in this section:
- How Logging stack in OpenShift Works
- How to install logging stack in OpenShift
- How to observe logs of application running in OpenShift

Resources:
- [Presentation](./src/openshift-logging-metrics-presentation.pdf)

Steps:
- [Install logging stack](https://docs.openshift.com/container-platform/4.10/logging/cluster-logging-deploying.html) (instructor walkthrough)
- Deploy and expose application from container image `quay.io/rhsacz/ed-app:0.3.0`
  - Application code is [located at GitHub](https://github.com/jwerak/ed-app/tree/main/src)
- Open Kibana UI and view application logs

## Metrics

### Container & metrics

Things to learn in this section:
- Prometheus metrics basics
- How to expose Prometheus supported metrics
- Monitoring stack in OpenShift
- Metrics provided by node exporter
- Metrics provided by application

Resources:
- [Prometheus](https://prometheus.io/)
- [Prometheus exposition format](https://prometheus.io/docs/instrumenting/exposition_formats/)
- [Prometheus metrics types](https://prometheus.io/docs/concepts/metric_types/)
- [Presentation](./src/openshift-logging-metrics-presentation.pdf)

Steps:
- Walk through documentation
- [Create Service Monitor](https://docs.openshift.com/container-platform/4.10/monitoring/managing-metrics.html#specifying-how-a-service-is-monitored_managing-metrics) to pull custom app metrics
- [Observe metrics](https://docs.openshift.com/container-platform/4.10/applications/odc-monitoring-project-and-application-metrics-using-developer-perspective.html#monitoring-project-and-application-metrics-using-developer-perspective) exposed by deployed application 
- View metrics in OpenShift Console
