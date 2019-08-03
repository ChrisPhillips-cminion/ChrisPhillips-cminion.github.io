---
layout: post
date: 2019-07-18 01:00:00
categories: APIConnect
title: "Scaling out pods in Kubernetes with DataPower"
---

Kubernetes is a container orchestration system that provides many advantages. In this article I am going to describe how DataPower or any pod can be scaled out with a simple request. There are ways to solve this.
<!--more-->

### Using APICUP (Helm)

**Recommended Approach**

APICUP is the installer for API Connect. If you have installed API Connect you will have used APICUP.

In order to scale out with APICUP ensure you are in the project directory containing the `apiconnect-up.yml` for the deployment you want to scale.

Run the following command to increase the replica count in the config.
`apicup subsys set <subcomponent name> replica-count=<desired no of replicas> `

Then deploy the updated config
`apicup subsys install <subcomponent name>`


**Pros**
 - If you patch or make config changes the replica value is stored

**Cons**
 - It requires access to the APICUP project

### Using Kubectl

This is the standard way to scale out Kubernetes StatefulSets.

`kubectl get statefulset -n <namespace>`

This returns

```
NAME                                  DESIRED   CURRENT   AGE
r62bf86f4e0-dynamic-gateway-service   3         3         1h
```

Find from the list the StatefulSet you wish to scale. e.g.
`r62bf86f4e0-dynamic-gateway-service`

Run the following command to scale in or out with the desired replica number.

`kubectl scale statefulset/<StatefulSet selected above> --replicas=<Desired no of replicas>  -n <namespace>`

e.g.
```
kubectl scale statefulset/r62bf86f4e0-dynamic-gateway-service --replicas=3  -n apic
```

**Pros**
 - Faster
 - Does not require access the APICUP project or the APICUP binary.

**Cons**
 - If config changes are made or the environment is patched then the replica changes are lost.
