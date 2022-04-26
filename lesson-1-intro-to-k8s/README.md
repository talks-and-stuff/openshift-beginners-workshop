# Lesson 1

## Introduction to Kubernetes (k8s)

Welcome to the first lesson of the Red Hat Czech's OpenShift course for beginners.


## What will you learn on the course?

* Kubernetes and how to use it.
* OpenShift.
* Web console, `oc`, `kubectl`.
* Basics of containerization.
* The most common objects and resources, and their purpose.
* Deploying applications into a cluster.
* Operating your application.
* Observability.
* Advanced concepts.

## Outside of our scope

* Installation of a cluster.
* Helping you with problems during the course on non-Red Hat operating systems.
* Basically any troubleshooting will be hard to do virtually, sorry!
* Serving coffee.


## Before we start...

* [Developer Sandbox - play with OpenShift whenever you want](https://developers.redhat.com/developer-sandbox/get-started).
* [Become friends with the k8s docs](https://kubernetes.io/docs/home/) and [OpenShift docs](https://docs.openshift.com/).
* Please ask questions, comment, speak up, sing: let's make this fun and interactive.
* Materials: [github.com/talks-and-stuff/openshift-beginners-workshop](https://github.com/talks-and-stuff/openshift-beginners-workshop)
* Instructions: [openhouse.redhat.com/cz/openshift](https://openhouse.redhat.com/cz/openshift/)


## Today

* Basics of k8s and OpenShift.
* Web console, `oc`.
* Authenticating with a cluster.
* Basics of containerization.
* Intro to `oc` and k8s resources.


## Intro

* Introduce ourselves
  * Please raise hand if you want to introduce yourself :)
* The difference between OpenShift and Kubernetes.
* OpenShift can feel complex and intimidating but don't worry! With some effort it will deliver.


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

And we're tired of the talking, let's finally do something!

Okay then, let's build a container image.
```
$ cat Containerfile
FROM fedora:35
RUN dnf install -y python3
USER 48
CMD ["python3", "-m", "http.server", "--bind", "0.0.0.0", "--directory", "/", "9999"]

$ podman build --tag http-server .
STEP 1/4: FROM fedora:35
STEP 2/4: RUN dnf install -y python3
Fedora 35 - x86_64                              3.9 MB/s |  79 MB     00:20    
Fedora 35 openh264 (From Cisco) - x86_64        1.5 kB/s | 2.5 kB     00:01    
Fedora Modular 35 - x86_64                      3.1 MB/s | 3.3 MB     00:01    
Fedora 35 - x86_64 - Updates                    4.5 MB/s |  29 MB     00:06    
Fedora Modular 35 - x86_64 - Updates            2.8 MB/s | 2.9 MB     00:01    
Fedora 35 - x86_64 - Test Updates               2.6 MB/s | 7.4 MB     00:02    
Fedora Modular 35 - x86_64 - Test Updates       467 kB/s | 559 kB     00:01    
Package python3-3.10.0~rc2-1.fc35.x86_64 is already installed.
Dependencies resolved.
Nothing to do.
Complete!
--> dbdfdd757c0
STEP 3/4: USER 48
--> 2c1e273cec3
STEP 4/4: CMD ["python3", "-m", "http.server", "--bind", "0.0.0.0", "--directory", "/", "9999"]
COMMIT http-server
--> bdd326fe09d
Successfully tagged localhost/http-server:latest
bdd326fe09d41a497a2b74082aeb6c609b7da7dc7a6b8d749e2d4f53a19e9ff9
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
   their own IP address](https://podman.io/getting-started/network).
4. [Podman](https://podman.io/) is a container manager (actually a pod manager
   😁) that doesn't require any service or a daemon to run - it's just a tool.
4. The resolution is to expose the HTTP server within the container to all the
   network interfaces.

```
$ podman run -p 9999:9999 http-server
```

```
$ curl http://0.0.0.0:9999
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>Directory listing for /</title>
</head>
<body>
<h1>Directory listing for /</h1>
<hr>
<ul>
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

```
10.0.2.100 - - [22/Apr/2022 08:23:05] "GET / HTTP/1.1" 200 -
```


## Cluster access

Link TBD

Open the URL and [log in](https://docs.openshift.com/container-platform/4.8/cli_reference/openshift_cli/getting-started-cli.html#cli-logging-in_cli-developer-commands) using the credentials we provided.

Once logged in...

Don't panic!

Take your time browsing OpenShift's Web console. Just an FYI, [Kubernetes has a different web interface](https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/).


## OpenShift interface

### Web console

You just saw it :)


### [CLI](https://docs.openshift.com/container-platform/4.8/cli_reference/openshift_cli/getting-started-cli.html#cli-getting-started)

```
$ oc
```

#### Getting the binary

You can [download the `oc` binary](https://access.redhat.com/downloads/content/290) from Red Hat's customer portal.

You can also use the [OKD](https://okd.io/) binary and download it from [OKD's releases](https://github.com/openshift/okd/releases).


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
NAME                               READY   STATUS        RESTARTS   AGE
websockets-demo-649b446d8c-qfdng   0/1     Terminating   0          6s
```

(we can use a pod definition from the first lesson)

After a while and fixing a root cause, we have a running pod:
```
$ oc get pods
NAME                               READY   STATUS    RESTARTS   AGE
websockets-demo-649b446d8c-2s6jc   1/1     Running   0          2m28s
```

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
