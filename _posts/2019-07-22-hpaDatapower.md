---
layout: post
date: 2019-07-22 01:00:00
categories: Kubernetes
title: "HPA Policies and adding one to DataPower"
draft: true
---

HPA Policies provide a way to scale out kubernetes pods when the CPU utilization for that pod hits a configured threshold.


To create an HPA policy you need to create the object in kubernetes using the following template.

```yaml
```


Then run `kubectl apply -f "<hpa>.yaml"` where 'hpa' is the name of the file.


When deciding on the parameters for the policy you must conisder hown long it takes to scale up the pod. For example DataPower takes roughly three minutes to scale out. If we set the HPA policy CPU utilization threshold to 99% then the DataPower would not be started in time. I recommend a threshold of 60%, however this should be modified depending on your requirements



video goes here
