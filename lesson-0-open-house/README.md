# Workshop pilot

## Recipe

### Part 1

0. Welcome everyone and introduce yourself
1. Introduce the workshop
   * Not OpenShift operations or provisioning
2. Show location of materials
3. Introduce OpenShift (short)
4. [Developer Sandbox - try OpenShift yourself easily](https://developers.redhat.com/developer-sandbox/get-started).
4. Talk about the difference between OpenShift and Kubernetes
5. [Open the demo](http://websockets-demo-ttomecek-dev.apps.sandbox.x8i5.p1.openshiftapps.com/), show URL so that everyone can open it too.
   * [https://bit.ly/3v9RcfA](https://bit.ly/3v9RcfA)
   * Click and fool around

### Part 2

1. [Open webconsole](https://console-openshift-console.apps.sandbox.x8i5.p1.openshiftapps.com/topology/ns/ttomecek-dev?view=graph)
   * Show the project (skip most of the webconsole elements - that's the course)
   * Briefly describe pod/deployment, service, route
   * Show metrics/logs
2. Showcase `oc` binary
   * "Copy login command"
   * status, get pods, describe, logs
   * login, whoami - explain the authentication mechanism

## Demo project

You can try it locally:
```
$ podman run -p 8081:8081 quay.io/tomastomecek/websockets-demo:latest
```

And then open [0.0.0.0:8081](https://0.0.0.0:8081/) in your browser.


## Workshop steps

Once you get your Sandbox cluster provisioned, get the login command and invoke it in your shell.

NEVER SHARE YOUR API TOKEN

```
$ oc login --token=sha256~$NUMBERS_LETTERS_UNICORNS --server=https://api.sandbox.x8i5.p1.openshiftapps.com:6443
```

### Get kubeconfig

Do we have access?
```
$ oc status
In project ttomecek-dev on server https://api.sandbox.x8i5.p1.openshiftapps.com:6443

You have no services, deployment configs, or build configs.
Run 'oc new-app' to create an application.

$ oc whoami
ttomecek
```

Yup!

Let's use the ttomecek-dev namespace for our app.

### Time to deploy

```
$ oc apply -f ./websockets-demo.yml
deployment.apps/websockets-demo created
service/websockets-demo created
route.route.openshift.io/websockets-demo created
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
