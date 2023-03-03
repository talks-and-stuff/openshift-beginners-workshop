
Scheduling
==========

default scheduler is described at: https://kubernetes.io/docs/concepts/scheduling-eviction/kube-scheduler/


The scheduler is working in multiple phases
1) finding a feasible set of nodes 
1) scoring feasible nodes so it can decide where workload will be placed

Why this is so important? Because it can make your application not behave correctly and lead to potential downtime. Imagine situations like:

1) all application pods running on the same node
1) all application pods running on node on the same physical host
1) pods which should be together are spread among multiple nodes
1) ...

We can prevent this by concept likes affinities and anti-affinities. They are described in a docs at: https://docs.openshift.com/container-platform/4.10/nodes/scheduling/nodes-scheduler-node-affinity.html


As an example to practice this we will create a three pods: 
- p1 - which defines "security" to value "S1"

``` yaml
apiVersion: v1
kind: Pod
metadata:
  name: p1
  labels:
    security: S1
spec:
  containers:
  - name: security-s1
    image: docker.io/ocpqe/hello-pod
```

- p2 - which has affinity to be run on same node as "p1" using the selector be scheduled on same node as the pods with label "security" set to "S1"


``` yaml
apiVersion: v1
kind: Pod
metadata:
  name: p2
  labels:
    security: S1
spec:
  containers:
  - name: security-s1
    image: docker.io/ocpqe/hello-pod
    podAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchExpressions:
          - key: security
            operator: In
            values:
            - S1
```

- p3 - which has antiAffinity to NOT be run on same node as "p1" using the selector be scheduled on same node as the pods with label "security" set to "S1"

``` yaml
apiVersion: v1
kind: Pod
metadata:
  name: p3
spec:
  affinity:
    podAntiAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchExpressions:
          - key: security
            operator: In
            values:
            - S1
        topologyKey: kubernetes.io/hostname
  containers:
  - name: pod-antiaffinity
    image: docker.io/ocpqe/hello-pod
```
 
Now you can use `oc` command to double check if everything is running correctly.

``` bash
oc get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.nodeName}{"\n"}'
```

As a task for yourself please create pod "p4" which will be scheduled on same node as pod "p3".
You can also expand JSONPath filter to print the value of "security" label.

If you are interested more in JSONPath you can find the docs at https://kubernetes.io/docs/reference/kubectl/jsonpath/


To cleanup the environment we will run
``` bash
oc delete pod p1 p2 p3 p4
```

You can use these selector for more stuff. If you propagate your server placements, availability zones or HW equipment to labels. But be aware of bad resource utilization which can come with a complex rules and can even end up with upgrade issues.

Also think about scalability. For example if you need two services to be running on the same node consider them being part of one pod - then they can scale easily together.


Custom Scheduler
=================

Custom scheduler is a little bit overhead in a lot of cases. We are using it to prove that it is possible and to demonstrate how to access k8s api from pods. The complete source of the scheduler can be viewed in the `scheduler/app.py`. In this scenario we will:

- setup OpenShift build for the scheduler app
- build it
- create service account and set th required permissions
- run scheduler in OpenShift pod
- Schedule a new pod using this scheduler


So let's start with creating a binary build. This will enable us to build container in OpenShift using files on local filesystem. So run:
``` bash
oc new-build --binary --name=sched
```




Then we ask OpenShift to build our container by uploading the content of a "scheduler" directory. Before executing this please change "NAME_SPACE" in the `scheduler/app.py` to the project/namespace you are running your pods in. And then execute:

``` bash
oc start-build sched --from-dir scheduler
```

we need to wait for build to succeed - we can check it the status by running
``` bash
oc get builds -w
```

to see the log of a build you can run
``` bash
oc logs sched-1-build --follow
```

When the job in the state of "Complete" we can continue by creating the service account. It doesn't have enough permissions - but we will fix this in next step by making it cluster-admin.

``` bash
oc create sa sched
```

Now please ask in google meet chat for adding permissions to your service account. If you are on your cluster you can do it by command:

``` bash
oc adm policy add-cluster-role-to-user cluster-admin -z sched
```


We are ready to deploy it into OpenShift cluster. So please apply this manifest to K8s. Don't forget to change IMAGE_STREAM_URL placeholder to the url revealed by `oc get is` command.
``` yaml
cat <<EOF | oc apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: sched
spec:
  serviceAccountName: sched
  containers:
  - name: sched
    image: IMAGE_STREAM_URL
EOF
```
Notice the serviceAccountName in specs - yes this is used to specify different service account for a pod.
Please check that pod is running correctly by examining its status and log.


Now we will try to schedule three pods. One will be scheduled by the default scheduler, one by ours and one will end up with a pending state.

First pod:
``` yaml
cat <<EOF | oc apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: testsched1
spec:
  schedulerName: test
  containers:
  - name: hello
    image: docker.io/ocpqe/hello-pod
EOF
```

Second pod:
``` yaml
cat <<EOF | oc apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: testsched2
spec:
  schedulerName: PrgContSched
  containers:
  - name: hello
    image: docker.io/ocpqe/hello-pod
EOF
```

Third pod:
``` yaml
cat <<EOF | oc apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: testsched3
spec:
  containers:
  - name: hello
    image: docker.io/ocpqe/hello-pod
EOF
```

Can you now explain which pod is scheduled by which scheduler and why the one is in Pending state?

Quality of Service
==================

One of the part of workload scheduling is also working with Quality of Service to assure that we have enough resources
to fulfill the needs of our workload.
Quality of Service is determined by setting request and limits
you know from previous sessions. In OpenShift we have 3 quality of service classes:


Best Effort
This is for a pod without limit and request set. This kind of workload gets typically killed first if there is starvation for resources in the cluster.

You can create such by applying following manifest:

``` yaml
apiVersion: v1
kind: Pod
metadata:
  name: prime1
spec:
  containers:
  - image: quay.io/dbecvarik/primes
    imagePullPolicy: Always
    name: primes
```

Burstable
This class is for a workload with a minimal resource guarantee and consume more if there is enough resources in the cluster. Typically you achieve it by setting only requests for cpu or memory.

You can create such by applying following manifest:

``` yaml
apiVersion: v1
kind: Pod
metadata:
  name: prime2
spec:
  containers:
  - image: quay.io/dbecvarik/primes
    imagePullPolicy: Always
    name: primes
    resources:
      requests:
        cpu: 300m
      limits:
        cpu: "0.5"
```

Guaranteed
This is for the applications which are business critical and we need to guarantee them all resources needed. You can get this class by setting both request and limits for cpu and memory for all the containers inside the pod (even init containers).

You can create such by applying following manifest:

``` yaml
apiVersion: v1
kind: Pod
metadata:
  name: prime3
spec:
  containers:
  - image: quay.io/dbecvarik/primes
    imagePullPolicy: Always
    name: primes
    resources:
      requests:
        cpu: 300m
        memory: 20M
      limits:
        cpu: 300m
        memory: 20M
```

and now you can check quality of service class of each pod by executing:

``` bash
oc get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.qosClass}{"\n"}'
```

You can read more on this topic at https://kubernetes.io/docs/tasks/configure-pod-container/quality-service-pod/


