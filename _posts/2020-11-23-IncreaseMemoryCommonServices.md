---
layout: post
categories: CommonServices
date: 2020-11-23 00:14:00
title: Out Of Memory (OOMKilled) CertMan, secret watcher and ingress on install of Common Services
---

While installing IBM common services (a preq for CP4I) we hit an issue were some of the pods were terminating because of memory or CPU limits. This article will show how to increase these limits.

<!--more-->

*Please note, if you need to make these changes to your system raise a PMR with IBM before applying to production systems*


In kubernetes each pod can have a resources request and limit value for memory and or CPU. I highly recommend that this is set for your application. The request value is used as to determine how much resource needs to be available on a node in order to run the pod, where as the limit is the absolute maximum. If the limit value is reached the pod is cycled.

These values can be set on the Deployment (DaemonSet or StatefulSet). However in the new world of operators it is more common to have it set in the CR which will go and set the size in the deployment. This means if you change it in the CR the deployment will be overridden.


For IBM Common Services  the value in the CR is set by the OperandConfigs. Therefore if you change the CR the OperandConfigs will revert you back to the original value.

If you want to set custom limits in OperandConfig then you must put the changes in the CommonServices object to over ride these values.

`oc edit commonservice common-services`
and replace the spec section with content with content similar to the following


```yaml
spec:
  services:
  - name: ibm-cert-manager-operator
    spec:
      certManager:
        certManagerCAInjector:
          resources:
            limits:
              cpu: 1000m
              memory: 1024Mi
        certManagerController:
          resources:
            limits:
              cpu: 1000m
              memory: 1024Mi
        certManagerWebhook:
          resources:
            limits:
              cpu: 1000m
              memory: 1024Mi
        configMapWatcher:
          resources:
            limits:
              cpu: 1000m
              memory: 1024Mi
  - name: ibm-management-ingress-operator
    spec:
      managementIngress:
        replicas: 1
        resources:
          limits:
            cpu: 1000m
            memory: 1536Mi
  - name: ibm-monitoring-exporters-operator
    spec:
      exporter:
        kubeStateMetrics:
          resource:
            limits:
              cpu: 1540m
              memory: 1800Mi
  - name: ibm-iam-operator
    spec:
      secretwatcher:
        replicas: 1
        resources:
          limits:
            cpu: 1000m
            memory: 1450Mi
  size: small
```
