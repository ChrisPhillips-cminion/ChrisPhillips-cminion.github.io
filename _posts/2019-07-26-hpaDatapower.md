---
layout: post
date: 2019-07-26 01:00:00
categories: Kubernetes
title: "HPA Policies and adding one to DataPower"
draft: true
---
<!--more-->
HPA Policies provide a way to scale out kubernetes pods when the CPU utilization for that pod hits a configured threshold.

To create an HPA policy can run the following command **or** use the yaml file blow.

`kubectl autoscale deployment <deployment Name> --cpu-percent=50 --min=1 --max=10`

There attributes for both the command above and the yaml below are in this table.

| Attribute | Definition |
| --------- | ---------- |
| Deployment Name | This is the name of the deployment you wish to enable autoscaling on |
| Namespace   |  The namespace containing the deployment |
| cpu-percentage / cpu utilization | The CPU threshold do you want to trigger the auto scaling. I.e. when the CPU utilization exceeds this level another pod is spun up. |
| min  / minReplicas  | The minimum number of pods   |
| max / maxReplicas  | The maximum number of pods   |

```yaml
piVersion: autoscaling/v2beta2
kind: HorizontalPodAutoscaler
metadata:
  name: <Deployment Name>-hpa
  namespace: <Namespace>
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: <Deployment Name>
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

Then run `kubectl apply -f "<hpa>.yaml"` where 'hpa' is the name of the file.

When deciding on the parameters for the policy you must conisder hown long it takes to scale up the pod. For example DataPower takes roughly three minutes to scale out. If we set the HPA policy CPU utilization threshold to 99% then the DataPower would not be started in time. I recommend a threshold of 50%, however this should be modified depending on your requirements

video goes here
