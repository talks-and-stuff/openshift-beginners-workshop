from kubernetes import client, config, watch

import json
import math
import random
import signal
import time


class GracefulKiller:
  kill_now = False
  signals = {
    signal.SIGINT: 'SIGINT',
    signal.SIGTERM: 'SIGTERM'
  }

  def __init__(self):
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)

  def exit_gracefully(self, signum, frame):
    print("\nReceived {} signal".format(self.signals[signum]))
    print("Cleaning up resources. End of the program")
    self.kill_now = True

# following line authenticate you inside the cluster
config.load_incluster_config()
#config.load_kube_config()
v1=client.CoreV1Api()

def scheduler(name, node, namespace="NAME_SPACE"):
    print ("Scheduling pod %s on node %s" % (name, node))
    target=client.V1ObjectReference()
    target.kind = "Node"
    target.apiVersion = "v1"
    target.name = node

    meta = client.V1ObjectMeta()
    meta.name = name

    body = client.V1Binding(metadata=meta, target=target)
    res = v1.create_namespaced_binding(namespace, body, _preload_content=False)
    time.sleep(1)
    return res


def nodes_available():
    ready_nodes = []
    for n in v1.list_node().items:
            for status in n.status.conditions:
                if status.status == "True" and status.type == "Ready":
                    ready_nodes.append(n.metadata.name)
    return ready_nodes


def main():
    try:
        print ("nodes for scheduling %s" % nodes_available())
        print("Starting scheduler")
        w = watch.Watch()
        print("Watching for pod events")
        for event in w.stream(v1.list_namespaced_pod, "NAME_SPACE"):
            print("pod: '%s', phase: '%s' %s." % (event['object'].metadata.name,
                                               event['object'].status.phase,
                                               event['object'].spec.scheduler_name))
            if event['object'].status.phase == "Pending" and event['object'].spec.scheduler_name == "PrgContSched":
                    res = scheduler(event['object'].metadata.name, random.choice(nodes_available()))
    except Exception as e:
        time.sleep(1)
        print(e)

killer = GracefulKiller()
while(not killer.kill_now):
    main()

