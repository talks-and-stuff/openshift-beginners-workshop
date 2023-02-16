# Lesson 1

## Introduction to Kubernetes (k8s)

Welcome to the first lesson of the Red Hat Czech's OpenShift course for beginners.

* Let's introduce ourselves: teachers and organizers.
  * Please mute your microphone by default.
  * Ask questions as needed: "Raise hand" button works great for that.
  * In person, you can raise your real hand :hand:
  * Let's make a round of introdcutions: why are here and what you expect to learn?


## What will you learn on the course?

* Kubernetes: what it is and how to use it.
* OpenShift.
* Web console, `oc`, `kubectl`.
* Basics of containerization.
* The most common objects, resources, and their purpose.
* Deploying applications into a cluster.
* Operating your application.
* Observability.
* Advanced concepts.


## Outside of our scope

* Installation of a cluster.
* Helping you with problems during the course on non-Red Hat operating systems.
* Provide support outside of this course. We are happy to help here.
* Serving coffee.


## Before we start...

* [Developer Sandbox - play with OpenShift whenever you want](https://developers.redhat.com/developer-sandbox/get-started).
* [Become friends with the k8s docs](https://kubernetes.io/docs/home/) and [OpenShift docs](https://docs.openshift.com/).
* Please ask questions, comment, speak up, sing: let's make this fun and interactive.
* Materials: [github.com/talks-and-stuff/openshift-beginners-workshop](https://github.com/talks-and-stuff/openshift-beginners-workshop)
* Instructions: [openhouse.redhat.com/cz/openshift](https://openhouse.redhat.com/cz/openshift/)


## Lesson 1 agenda

* Basics of k8s and OpenShift.
* Web console, `oc`.
* Authenticating with a cluster.
* Basics of containerization.
* Intro to `oc` and k8s resources.


## Intro

* The difference between [OpenShift](https://docs.openshift.com/) and [Kubernetes](https://github.com/kubernetes/kubernetes).
* OpenShift can feel complex and intimidating but don't worry, at the end of this course, you'll be comfortable with it.


### Motivation

Separate host OS from the app OS.

![Traditional → Containerized](https://d33wubrfki0l68.cloudfront.net/26a177ede4d7b032362289c6fccd448fc4a91174/eb693/images/docs/container_evolution.svg)

It's easy to automate building and hosting of container images, and the subsequent deployment.

Hence continuous integration (CI) and deployment (CD) will make you iterate faster and increase your confidence that code changes are working.

Observability and metrics: with [Prometheus](https://prometheus.io/) and [Grafana](https://grafana.com/) you can get charts to introspect your application and the cluster.

![Sample Grafana k8s dashboard](https://grafana.com/api/dashboards/8588/images/5333/image)

Run the same containers during local development and in production.

Utilize, distribute and measure resources efficiently.


### Sample kube cluster

![The cluster](https://d33wubrfki0l68.cloudfront.net/2475489eaf20163ec0f54ddc1d92aa8d4c87c96b/e7c81/images/docs/components-of-kubernetes.svg)


## Containers

THE building block of Kubernetes.

![CZ containers](https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/Loudilka%2C_kontajnery.jpg/640px-Loudilka%2C_kontajnery.jpg)

Not these... C'mon!


### Demo

Let's build a container image.
```
$ cat Containerfile
FROM fedora:37
RUN dnf install -y python3
USER 48
EXPOSE 9999
CMD ["python3", "-m", "http.server", "--bind", "0.0.0.0", "--directory", "/", "9999"]

$ podman build --tag http-server .
STEP 1/5: FROM fedora:37
STEP 2/5: RUN dnf install -y python3
Fedora 37 - x86_64                              4.3 MB/s |  82 MB     00:18    
Fedora 37 openh264 (From Cisco) - x86_64        3.0 kB/s | 2.5 kB     00:00    
Fedora Modular 37 - x86_64                      3.0 MB/s | 3.8 MB     00:01    
Fedora 37 - x86_64 - Updates                    2.1 MB/s |  23 MB     00:11    
Fedora Modular 37 - x86_64 - Updates            1.8 MB/s | 2.9 MB     00:01    
Package python3-3.11.0-1.fc37.x86_64 is already installed.
Dependencies resolved.
Nothing to do.
Complete!
--> d2f9687c7f9
STEP 3/5: USER 4848
--> ee10a2a913d
STEP 4/5: EXPOSE 9999
--> 65e13674959
STEP 5/5: CMD ["python3", "-m", "http.server", "--bind", "0.0.0.0", "--directory", "/", "9999"]
COMMIT http-server
--> e868be0feb3
Successfully tagged localhost/http-server:latest
e868be0feb33970b97b8fd8d96cc48d045c374a20f1b8634e039cd6ccbb01b49
```

And now let's run a container:
```
$ podman run http-server

// this is actually blank, no output here
```

And in a separate console:
```
$ curl http://0.0.0.0:9999
curl: (7) Failed to connect to 0.0.0.0 port 9999 after 0 ms: Connection refused
```

(you can also try open that URL in your browser)

Also, do you know what "0.0.0.0" and "localhost" mean?

Anyway, what's wrong up there? And what the heck are we actually trying to do?

1. The demonstration shows that your application with all its dependencies,
   content and metadata is packaged in a container image which is independent
   of the host OS - similar, but more lightweight, to virtual machines.
2. The HTTP content is being served within the container and that's not exposed
   to all network interfaces.
3. The commands above utilize rootless podman containers and those [don't get
   their own IP address](https://github.com/containers/podman/blob/main/docs/tutorials/basic_networking.md).
4. [Podman](https://podman.io/) is a container manager (actually a pod manager
   😁) that doesn't require any service or a daemon to run - it's just a tool.
4. The resolution is to expose the HTTP server within the container to all the
   network interfaces.

```
$ podman run -p 9999:9999 http-server
```

```
$ curl http://0.0.0.0:9999
<!DOCTYPE HTML>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Directory listing for /</title>
</head>
<body>
<h1>Directory listing for /</h1>
<hr>
<ul>
<li><a href="afs/">afs/</a></li>
<li><a href="bin/">bin@</a></li>
<li><a href="boot/">boot/</a></li>
<li><a href="dev/">dev/</a></li>
<li><a href="etc/">etc/</a></li>
<li><a href="home/">home/</a></li>
<li><a href="lib/">lib@</a></li>
<li><a href="lib64/">lib64@</a></li>
<li><a href="lost%2Bfound/">lost+found/</a></li>
<li><a href="media/">media/</a></li>
<li><a href="mnt/">mnt/</a></li>
<li><a href="opt/">opt/</a></li>
<li><a href="proc/">proc/</a></li>
<li><a href="root/">root/</a></li>
<li><a href="run/">run/</a></li>
<li><a href="sbin/">sbin@</a></li>
<li><a href="srv/">srv/</a></li>
<li><a href="sys/">sys/</a></li>
<li><a href="tmp/">tmp/</a></li>
<li><a href="usr/">usr/</a></li>
<li><a href="var/">var/</a></li>
</ul>
<hr>
</body>
</html>
```

And in the log of the container:
```
10.0.2.100 - - [22/Apr/2022 08:23:05] "GET / HTTP/1.1" 200 -
```

Will this work?
```
$ curl http://localhost:9999
```


## Cluster access

If you need a cluster, you can use the Developer Sandbox mentioned above. For
basic experiments with vanilla Kubernetes, have a look at
[kind](https://kind.sigs.k8s.io/).

Open a URL to the cluster and [log in](https://docs.openshift.com/container-platform/4.8/cli_reference/openshift_cli/getting-started-cli.html#cli-logging-in_cli-developer-commands) using the credentials we provided.

Once logged in...

Don't panic!

Take your time browsing OpenShift's Web console. Just an FYI, [Kubernetes has a different web interface](https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/).


## OpenShift interface

### Web console

![Empty webconsole](/lesson-1-intro-to-k8s/webconsole-empty.png)

### [CLI](https://docs.openshift.com/container-platform/4.8/cli_reference/openshift_cli/getting-started-cli.html#cli-getting-started)

```
$ oc
```

#### Getting the binary

You can [download the `oc` binary](https://access.redhat.com/downloads/content/290) from Red Hat's customer portal.

You can also use the [OKD](https://okd.io/) binary and download it from [OKD's releases](https://github.com/openshift/okd/releases).

Unfortunately, `oc` is not packaged in Fedora Linux.


#### CLI Basics

You'll need this for the 2nd lesson.

`oc` has a pretty good documentation built-in, try it out :)

```
$ oc
$ oc help
```

These are the N most-used subcommands:

1. `login` — Log in to a server
2. `status` — Show an overview of the current project
3. `project` — Switch to another project
4. `explain` — Documentation for API resources and their fields.
4. `apply` — Apply a configuration to a resource by filename or stdin
5. `get` — Display one or many resources
6. `describe` — Show details of a specific resource or group of resources
7. `logs` — Print the logs for a resource
8. `rsh` — Open a remote shell session to a container

We have the basics, let's try this out!

Let's connect our local `oc` with our cluster. Click on your name top-right and "Copy login command".
```
$ oc login --token=$NEVER_SHARE_THIS_ESPECIALLY_POST_IT_PUBLICLY --server=https://api.sandbox-m2.ll9k.p1.openshiftapps.com:6443
```

**Bonus**: run the second `curl` command.


### Resources

[A snippet from k8s' API description](https://kubernetes.io/docs/reference/kubernetes-api/):

> Kubernetes resources and "records of intent" are all stored as API objects,
> and modified via RESTful calls to the API. The API allows configuration to be
> managed in a declarative way. Users can interact with the Kubernetes API
> directly, or via tools like kubectl. The core Kubernetes API is flexible and
> can also be extended to support custom resources.

Let's use `pod` as a resource example:
```
$ oc get pods
No resources found in ttomecek-dev namespace.
```

With this command, we ask OpenShift to show us all pods (whatever that is) in
the current namespace (also that).

And there are none, because the cluster is empty (kind of).


### `oc explain`

Let's look how resources are defined so we know what to type in our object definitions.

```
$ oc explain pod
KIND:     Pod
VERSION:  v1

DESCRIPTION:
     Pod is a collection of containers that can run on a host. This resource is
     created by clients and scheduled onto hosts.

FIELDS:
   apiVersion   <string>
     APIVersion defines the versioned schema of this representation of an
     object. Servers should convert recognized schemas to the latest internal
     value, and may reject unrecognized values. More info:
     https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources

   kind <string>
     Kind is a string value representing the REST resource this object
     represents. Servers may infer this from the endpoint the client submits
     requests to. Cannot be updated. In CamelCase. More info:
     https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds

   metadata     <Object>
     Standard object's metadata. More info:
     https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

   spec <Object>
     Specification of the desired behavior of the pod. More info:
     https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status

   status       <Object>
     Most recently observed status of the pod. This data may not be up to date.
     Populated by the system. Read-only. More info:
     https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status
```

We can also query a specific field if we know the path in the hierarchy:
```
$ oc explain pod.spec.containers.image
KIND:     Pod
VERSION:  v1

FIELD:    image <string>

DESCRIPTION:
     Docker image name. More info:
     https://kubernetes.io/docs/concepts/containers/images This field is
     optional to allow higher level config management to default or override
     container images in workload controllers like Deployments and StatefulSets.
```

### Getting our http-server into OpenShift

Thanks to our wonderful attendees from the run in 2022, we have a followup.

The question on the course was: how do we get the "http-server" container image
to our OpenShift cluster and run it there?


#### Set up a new project

We need a space in our cluster where the container will run. So let's create a new project for us.

Please select a descriptive name so it's clear for you what's running inside:
```
$ oc new-project lesson1-http-server
```

#### Upload the image

Next, we need to bring our local container image to the cluster. There are
several ways how to do such a thing. Let's push the image to [quay.io
registry](https://quay.io/).
```
$ podman login quay.io
```

We need to tag the image properly and push it to the registry.
```
$ podman tag http-server quay.io/tomastomecek/http-server
```

Now that we have the image tagged properly, we can push it to the registry:
```
$ podman push quay.io/tomastomecek/http-server
Getting image source signatures
Copying blob 0975862b2056 done  
Copying blob f71d895171a4 skipped: already exists  
Copying config e868be0feb done  
Writing manifest to image destination
Storing signatures
```


#### Run `http-server` in OpenShift

OpenShift's `oc` client has a fascinating command to run a selected container
image and set up a lot of things automatically.

Make sure the Quay repository is public, otherwise OpenShift won't be able to
access it.
```
$ oc new-app quay.io/tomastomecek/http-server
--> Found container image e868be0 (29 hours old) from quay.io for "quay.io/tomastomecek/http-server"

    * An image stream tag will be created as "http-server:latest" that will track this image

--> Creating resources ...
    imagestream.image.openshift.io "http-server" created
    deployment.apps "http-server" created
    service "http-server" created
--> Success
    Application is not exposed. You can expose services to the outside world by executing one or more of the commands below:
     'oc expose service/http-server' 
    Run 'oc status' to view your app.
```

Let's run the `get pods` command again:
```
NAME                           READY   STATUS    RESTARTS   AGE
http-server-5cd8885f9b-6gxdq   1/1     Running   0          72s
```

Our http-server is now running but we cannot access it because the application is not exposed to the public.


#### Expose to public

```
$ oc expose --port 9999 service/http-server
route.route.openshift.io/http-server exposed
```

OpenShift will do its own internal "magic" to make your http-server accessible to the public.


Here's our http-server:
```
$ oc get route/http-server
NAME          HOST/PORT                                                            PATH   SERVICES      PORT   TERMINATION   WILDCARD
http-server   http-server-ttomecek-dev.apps.sandbox-m2.ll9k.p1.openshiftapps.com          http-server   9999                 None
```

The host/port is the location where you can connect and check it out.


### How does that work? I need to know more!

Join us on lesson 2 to find out :)

