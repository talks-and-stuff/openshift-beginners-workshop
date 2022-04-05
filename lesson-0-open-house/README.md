# Workshop pilot

## Recipe

### Part 1

0. Welcome everyone and introduce yourself
1. Introduce the workshop
2. Show location of materials
3. Introduce OpenShift (short)
4. Talk about the difference between OpenShift and Kubernetes
5. Open the demo, show URL so that everyone can open it too. (link TBD)
   * Click and fool around

### Part 2

1. Open webconsole (link TBD)
   * Show the project (skip most of the webconsole elements - that's the course)
   * Briefly describe pod/deployment, service, route
   * Show metrics/logs
2. Showcase `oc` binary
   * status, get pods, describe, logs
   * login, whoami - explain the authentication mechanism

## Demo project

You can try it locally:
```
$ podman run -p 8081:8081 quay.io/tomastomecek/websockets-demo:latest
```

And then open [0.0.0.0:8081](https://0.0.0.0:8081/) in your browser.


## Workshop steps

Here are the steps for our specific internal cluster how to reproduce the workshop. I'll update with one that is publicly accessible.

### Get kubeconfig

First, `curl` the kubeconfig and then expose it:
```
export KUBECONFIG=kubeconfig
```

Do we have access?
```
$ oc get nodes
NAME                          STATUS    ROLES     AGE       VERSION
cyborg-4rtft-master-0         Ready     master    9d        v1.22.5+5c84e52
cyborg-4rtft-master-1         Ready     master    9d        v1.22.5+5c84e52
cyborg-4rtft-master-2         Ready     master    9d        v1.22.5+5c84e52
cyborg-4rtft-worker-0-4cbv5   Ready     worker    9d        v1.22.5+5c84e52
cyborg-4rtft-worker-0-jmz4f   Ready     worker    9d        v1.22.5+5c84e52
cyborg-4rtft-worker-0-vfx5c   Ready     worker    9d        v1.22.5+5c84e52

$ oc whoami
system:admin
```

Yup!

### New project

```
$ oc new-project ttomecek-websockets-demo
```

### Time to deploy

```
$ oc apply -f ./websockets-demo.yml
deployment.apps/websockets-demo created
service/websockets-demo created
route.route.openshift.io/websockets-demo exposed
```

Whoopsie, the image repo was set to private:
```
NAME                               READY     STATUS             RESTARTS   AGE
websockets-demo-5597f99989-5v24q   0/1       ImagePullBackOff   0          2m41s
```

Now it works properly, after I made the image public:
```
$ oc get all
NAME                                   READY     STATUS    RESTARTS   AGE
pod/websockets-demo-5597f99989-ghgbf   1/1       Running   0          4h18m

NAME                      TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)   AGE
service/websockets-demo   ClusterIP   172.30.29.9   <none>        80/TCP    4h18m

NAME                              READY     UP-TO-DATE   AVAILABLE   AGE
deployment.apps/websockets-demo   1/1       1            1           4h18m

NAME                                         DESIRED   CURRENT   READY     AGE
replicaset.apps/websockets-demo-5597f99989   1         1         1         4h18m

NAME                                       HOST/PORT                                                              PATH      SERVICES          PORT      TERMINATION   WILDCARD
route.route.openshift.io/websockets-demo   websockets-demo-ttomecek-websockets-demo.apps.cyborg.osci.redhat.com             websockets-demo   8081                    None
```
