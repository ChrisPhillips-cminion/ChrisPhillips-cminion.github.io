---
layout: post
categories: CommonServices
date: 2020-11-23 00:14:00
title: Out Of Memory (OOMKilled) CertMan, secret watcher and ignress on install of Common Services
---

While installing IBM common services (a preq for CP4I) we hit an issue were some of the pods were terminating because of memory or CPU limits. This article will show how to increase these limits.

<!--more-->

*Please note, if you need to make these changes to your system raise a PMR with IBM before applying to production systems*


In kubernetes each pod can have a resources request and limit value for memory and or CPU. I highly recommend that this is set for your application. The request value is used as to determine how much resource needs to be available on a node in order to run the pod, where as the limit is the absolute maximum. If the limit value is reached the pod is cycled.

These values can be set on the Deployment (DaemonSet or StatefulSet). However in the new world of operators it is more common to have it set in the CR which will go and set the size in the deployment. This means if you change it in the CR the deployment will be overridden.


For IBM Common Services  the value in the CR is set by the OperandConfigs. Therefore if you change the CR the OperandConfigs will revert you back to the original value.


Therefore in order to persist the changes you need to update the OperandConfigs.

1. Verify the name of the OperandConfigs, run the following command
```
oc get  operandconfigs.operator.ibm.com
```
This will provide a response like below.

```
NAME             AGE    PHASE     CREATED AT
common-service   172m   Running   2020-11-23T11:17:47Z
```

2. Edit the OperandConfig, Run the following command
```
oc edit  operandconfigs.operator.ibm.com common-service
```
This will load a text editor with the contents of the file.

3. Change the limits (not requests) of the following sections

I increased CPU and memory.
```
- name: ibm-cert-manager-operator
   spec:
     certManager:
       certManagerCAInjector:
         resources:
           limits:
             cpu: 1000m
             memory: 1024Mi
           requests:
             cpu: 30m
             memory: 230Mi
       certManagerController:
         resources:
           limits:
             cpu: 1000m
             memory: 1024Mi
           requests:
             cpu: 50m
             memory: 175Mi
       certManagerWebhook:
         resources:
           limits:
             cpu: 1000m
             memory: 1024Mi
           requests:
             cpu: 30m
             memory: 70Mi
       configMapWatcher:
         resources:
           limits:
             cpu: 1000m
             memory: 1024Mi
           requests:
             cpu: 10m
             memory: 50Mi
     certificate: {}
     clusterIssuer: {}
     issuer: {}
```

Increase memory in
```
- name: ibm-management-ingress-operator
  spec:
    managementIngress:
      replicas: 1
      resources:
        limits:
          cpu: 1000m
          memory: 1536Mi
        requests:
          cpu: 60m
          memory: 110Mi
    operandBindInfo: {}
    operandRequest: {}
```

Increase memory in
```
- name: ibm-monitoring-exporters-operator
    spec:
      exporter:
....        
        kubeStateMetrics:
          resource:
            limits:
              cpu: 1540m
              memory: 1800Mi
            requests:
              cpu: 500m
              memory: 150Mi
....
      operandRequest: {}
```



4. Delete the following pods
```
cert-manager-controller-
ibm-monitoring-kube-state-
secret-watcher-
```
