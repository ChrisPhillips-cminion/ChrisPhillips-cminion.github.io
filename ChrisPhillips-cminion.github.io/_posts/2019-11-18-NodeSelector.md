---
layout: post
date: 2019-11-18 00:02:00
categories: APIConnect
title: "API Connect - Deploying Components to specific Nodes"
---

API Connect has four components, there is a requirement to deploy the DataPower Gateway to their own worker nodes in Kubernetes.

<!--more-->

By deploying DataPower to their own WorkerNodes this reduces the risk of memory or connection leaks from other things deployed in the same Kubernetes cluster.

### Node Selector

In Kubernetes node selectors can be configured on the Pods to ensure the pod is only deployed to a node with a specific label.  This is set in the Deployment, DaemonSet, StatefulSet, etc. For more information please take a look at [https://kubernetes.io/docs/concepts/configuration/assign-pod-node/]("https://kubernetes.io/docs/concepts/configuration/assign-pod-node/")

### Labelling the Worker Nodes

_A label is a key and value that is attached to an object as a annotation._

In order for a pod to use a NodeSelector the a worker node must exist with the corresponding label. If no worker node exists with the required label the pod is not deployed and is left in the pending state.

To set a label on a worker node use the following command  

`kubectl label nodes <Node Name> <Label Key>=<Label Value>`

Where

| Term        | Definition                                              |
| :---------- | :------------------------------------------------------ |
| Node Name   | The name of the node that will have the label attached. |
| Label Key   | The label key                                           |
| Label value | The label value                                         |

### Node Selector on the API Manager / Analytics / Portal

In order to configure the NodeSelector on the non DataPower components extra values files must be used. For more information take a look at [https://www.ibm.com/support/knowledgecenter/en/SSMNED_2018/com.ibm.apic.install.doc/tapic_install_extraValues_Kubernetes.html](https://www.ibm.com/support/knowledgecenter/en/SSMNED_2018/com.ibm.apic.install.doc/tapic_install_extraValues_Kubernetes.html).

A sample extra value file is below, if the deployment you are extending already uses an extra values file these changes should be merged into it. In the example below we are deploying all of these components to nodes with the following label.
`node: apic`


*API Manager v2018.4.1.8*
```yaml
cassandra:
  affinity:
    podAntiAffinity:
     preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 1
        podAffinityTerm:
          topologyKey: kubernetes.io/hostname
          labelSelector:
            matchLabels:
              app: cassandra
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: node
            operator: In
            values:
            - apic
analytics-proxy:
  nodeSelector:
    node: apic
apim:
  nodeSelector:
    node: apic
client-downloads-server:
  nodeSelector:
    node: apic
juhu:
  nodeSelector:
    node: apic
ldap:
  nodeSelector:
    node: apic
lur:
  nodeSelector:
    node: apic
ui:
  nodeSelector:
    node: apic
```

*Developer Portal v2018.4.1.8*
```yaml
apic-portal-www:
  nodeSelector:
    node: apic

apic-portal-db:
  nodeSelector:
    node: apic
```

*Analytics v2018.4.1.8*
```yaml
apic-analytics-client:
  nodeSelector:
    node: apic
apic-analytics-ingestion:
  nodeSelector:
    node: apic
apic-analytics-message-queue:
  nodeSelector:
    node: apic
apic-analytics-operator:
  nodeSelector:
    node: apic
apic-analytics-storage:
  nodeSelector:
    node: apic
```

Once these extra values file are configured redeploy the API Connect environment with `apicup`. This will cause pods to be terminated as required to ensure everything is running on the correct node.  

### Node Selector on the Gateway

DataPower does not natively set the NodeSelector value from a helm value parameter. In order to configure DataPower to deploy to specific nodes, the helm chart must be directly modified.

In order to do this I created the following script.   

```
mv gwy gwy-$(date +%s)                       #Backup the old gw file.
apicup subsys install gwy --out  gwy         #Save the helm chart but dont deploy it.
cd gwy/helm/                                 #Go into the helm chart directory
tar zxvf dynamic-gateway-service-1.0.49.tgz  #Extract the helm chart.

# Inject the node selector into the datapowoer statefulset
sed -e s/volumes:/nodeSelector:\\\n\ \ \ \ \ \ \ \ service:\ dpgw\\\n\ \ \ \ \ \ volumes:/ dynamic-gateway-service/templates/statefulset.yaml > dynamic-gateway-service/templates/statefulset.yaml.new
mv dynamic-gateway-service/templates/statefulset.yaml.new dynamic-gateway-service/templates/statefulset.yaml

# Inject the node selector into the datapowoer Monitor
sed -e s/containers:/nodeSelector:\\\n\ \ \ \ \ \ \ \ service:\ dpgw\\\n\ \ \ \ \ \ containers:/ dynamic-gateway-service/templates/datapower-monitor.yaml  > dynamic-gateway-service/templates/datapower-monitor.yaml.new
mv dynamic-gateway-service/templates/datapower-monitor.yaml.new dynamic-gateway-service/templates/datapower-monitor.yaml

#Re-tar the helm chart
tar czvf dynamic-gateway-service-1.0.49.tgz dynamic-gateway-service

ls
cd ../..

#kick off the install with saved helm chart
apicup subsys install gwy --plan-dir gwy
```
