---
layout: post
date: 2019-07-26 01:00:00
categories: Kubernetes
title: "HPA Policies and adding one to DataPower"
draft: true
---

HPA Policies provide a way to scale out kubernetes pods when the CPU utilization for that pod hits a configured threshold.


To create an HPA policy can run the following command **or** use the yaml file blow.

`kubectl autoscale deployment <deployment Name> --cpu-percent=50 --min=1 --max=10`

There attributes for both the command above and the yaml below are in this table. 


```yaml
piVersion: autoscaling/v2beta2
kind: HorizontalPodAutoscaler
metadata:
  name: php-apache
  namespace: default
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: php-apache
  minReplicas: 1
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
status:
  observedGeneration: 1
  lastScaleTime: <some-time>
  currentReplicas: 1
  desiredReplicas: 1
  currentMetrics:
  - type: Resource
    resource:
      name: cpu
      current:
        averageUtilization: 0
        averageValue: 0
```


Then run `kubectl apply -f "<hpa>.yaml"` where 'hpa' is the name of the file.


When deciding on the parameters for the policy you must conisder hown long it takes to scale up the pod. For example DataPower takes roughly three minutes to scale out. If we set the HPA policy CPU utilization threshold to 99% then the DataPower would not be started in time. I recommend a threshold of 60%, however this should be modified depending on your requirements



video goes here
