---
layout: post
date: 2019-09-04 01:00:00
categories: APIConnect
title: "HPA Policies and adding one to DataPower"
---

HPA Policies provide a way to scale out Kubernetes pods when the CPU utilisation for that pod reaches a predefined threshold.

<!--more-->
To create an HPA policy can run the following command **or** use the yaml file blow.

`kubectl autoscale deployment <Name> --cpu-percent=50 --min=1 --max=10`
or
`kubectl autoscale statefulset <Name> --cpu-percent=50 --min=1 --max=10`

The attributes for both the command above and the yaml below are in this table.

| Attribute | Definition |
| --------- | ---------- |
|  Name | This is the name of the Deployment or StatefulSet you wish to enable autoscaling on |
| Namespace   |  The namespace containing the Deployment or StatefulSet |
| cpu-percentage / cpu utilisation | The CPU threshold at which additional pods will be deployed. i.e. when the CPU utilisation exceeds this level another pod is spun up. |
| min  / minReplicas  | The minimum number of pods   |
| max / maxReplicas  | The maximum number of pods   |

```yaml
piVersion: autoscaling/v2beta2
kind: HorizontalPodAutoscaler
metadata:
  name: <Name>-hpa
  namespace: <Namespace>
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: <Name>
  minReplicas: 1
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
```
or
```yaml
piVersion: autoscaling/v2beta2
kind: HorizontalPodAutoscaler
metadata:
  name: <Name>-hpa
  namespace: <Namespace>
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: StatefulSet
    name: <Name>
StatefulSet  minReplicas: 1
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
```
Then run `kubectl apply -f "<hpa>.yaml"` where 'hpa' is the name of the file.

When deciding on the parameters for the policy you must consider how long it takes to scale up the pod. For example DataPower takes roughly three minutes to scale out. If we set the HPA policy CPU utilisation threshold to 99% then the DataPower would not be started in time. I recommend a threshold of 50%, however this should be determined depending on your requirements
