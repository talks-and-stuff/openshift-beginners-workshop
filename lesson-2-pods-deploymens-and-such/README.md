%title: Introduction To Pods and Pod Controllers
%author: Stanislav Láznička

-> ▛▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▜ <-

-> # Introduction To Pods and Pod Controllers <-

-> ▙▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▟ <-


---

## Pod

- basic building stone of kubernetes
- defines what to run and how to run it
    - container image
    - ports
    - host ports
    - volumes
    - environment variables
    - security attributes
    - ...

---

## Pod

- may consist of multiple containers
- container types
    - init containers - run before any other container is run
    - normal containers
    - new (1.23 - beta) - [ephemeral containers](https://k8s.io/docs/concepts/workloads/pods/ephemeral-containers/)
        - for debugging purposes
- design pattern - sidecar container

---

## Pod Lifecycle

- observable in *pod.status*
- pod life phases:
    - _*Pending*_
        - pod created, waiting for scheduling, volumes, image pull
    - _*Running*_
        - pod is bound to node
        - at least one container is still running or starting
    - _*Succeeded/Failed*_
        - all containers finished
    - _*Unknown*_
        - error communicating the state of the pod from the node
- pods will not survive eviction or node failure

---

## Pod Demo

$ oc apply -f example/pod/pod.yaml
$ oc apply -f example/pod/
$ oc port-forward local:target

---

## Service

- pods each get an IP address
    - these change!
- service keeps stable IP and hostname
- can point to multiple pods using a label selector
- provides load balancing
- can be used to make an external service be available inside the cluster

---

## Service Demo

- connect to the httpbin pod from a different pod
    - use _example/fedorapod.yaml_
    - $ oc rsh
    - $ curl
$ oc get svc
$ curl https://httpbin-svc.<nsname>.svc.cluster.local:8080/get

---

## Route

- allows connections from outside of the cluster
- provide DNS A records
- wire external access through HAProxy
- different modes of TLS termination
    - edge (yuck!)
    - reencrypt
    - passthrough

---

## Route Demo

- connecting from laptops to the service

---

## Service Accounts

- created with every namespace
- service account tokens
- every pod is affiliated with a service account
    - previously in secrets
    - now - projected volumes!

---

## Deployment

- ensures an *n* replicas of a pod are running
- does that through *ReplicaSets*
- allows simple scaling and keeps history of rollouts

---

## Deployment Demo

$ oc apply -f example/deployment.yaml
$ oc scale deployment httpbin-deployment --replicas 2

---

## StatefulSets

- similar to deployment, maintains pod identity in pod deployments
- pod identity
    - based on ordinals
    - used to distinguish type of a deployment
- maintains order of pod deployment
- API directly allows requesting PVs
    - for stable storage access
    - *spec.volumeClaimTemplates*

---

## StatefulSets Demo

- [Deploying a replicated MySQL database](https://kubernetes.io/docs/tasks/run-application/run-replicated-stateful-application/)

---

## Requesting and Limiting Resources for Pods

- requesting and limiting system resources
    - *container.resources.{limits,resources}*
    - cpu
        - 1 unit == 1 CPU
        - 0.5 or 100m
        - limit applies to CPU time
        - request applies as a weight
    - memory
        - requested in bytes
        - 100M, 20Mi, 3G,...
        - limit might cause EOMs
        - request for scheduling

---

## Reference

- [Kubernetes API Reference](https://k8s.io/docs/reference/generated/kubernetes-api/v1.23/)
- [Pods]( https://k8s.io/docs/concepts/workloads/pods/)
- [Pod Lifecycle](https://k8s.io/docs/concepts/workloads/pods/pod-lifecycle/)
- [Service](https://k8s.io/docs/concepts/services-networking/service/)
- [Routes](https://docs.openshift.com/container-platform/latest/networking/routes/route-configuration.html)
- [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment:)
- [StatefulSets](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/)
- [Resources and Limits](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#resource-units-in-kubernetes)
- see [QuestionsAnswers.md](QuestionsAnswers.md) file for questions asked during the lecture

---

-> ## Thank you all for attention <-
