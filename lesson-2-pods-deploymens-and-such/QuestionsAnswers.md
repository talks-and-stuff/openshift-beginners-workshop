# Questions & Answers

## How can I get my questions answered?

Just ask us during the lecture, drop us an email or create an issue [in the
lecture
repo](https://github.com/talks-and-stuff/openshift-beginners-workshop/issues/new).

---

## Can we have some more info for the readiness and liveness probes?

[Here's a document that covers
it](https://docs.openshift.com/container-platform/4.8/applications/application-health.html).
If you are familiar with
[healthchecks](https://docs.docker.com/engine/reference/builder/#healthcheck)
in Dockerfiles, the probes serve a similar purpose.


## Can I have a custom domain for my app?

Yes! [Even though this document is meant for OpenShift
v3](https://docs.openshift.com/online/pro/dev_guide/routes.html), it applies to
OpenShift v4 as well. We are using v4 in our lectures.


## How do I secure my route with my own certificate?

[You can place the certificate inside a route's
definition](https://docs.openshift.com/container-platform/4.8/networking/routes/secured-routes.html).


## How to convert Docker Compose files into Kubernetes objects?

There is a tool, [kompose](https://github.com/kubernetes/kompose), which
generates Kubernetes objects from Docker Compose files.

