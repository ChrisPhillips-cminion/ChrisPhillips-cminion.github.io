---
layout: post
date: 2023-02-01 01:00:00
categories: DataPower
title: "Slow Start in Kubernetes"
draft: true
---
"Slow Start" patterns are convenient when a POD is ready to receive traffic, but we may want to only send a small workload of traffic until we have established that it is ready to receive all traffic.
<!--more-->
I was asked this week to come up with a solution to the above problem, primarily when HPA scales out to more pods.

## Problem Statement

- When the HPA scales out a pod there must be a way to send a small proportion of traffic only to it.
- There must be a manual way increase the traffic to a given percentage
- There must be three such levels.

## Solution

![](RackMultipart20240201-1-ouv410_html_4c2279577fa1a76c.png)

### Services

We create two additional services so that we have a total of three.

Each service will represent a % of traffic.

The default service will route to all of the target pods.

The new services will have an additional label selector that will look for a label of rate and a value of either 50 or 100. It does not matter what the label is it does not co-respond to the traffic being routed to it.

The Pods that are expecting to handle majority of the load must have an additional label called rate: 100. Pods that are expected to be at the middle tier must have an additional label called rate: 50.

From what we have configured so far.

- When the default service is called it will route traffic to any of the three pods
- When the new service with the label selector for rate:100 is called it will invoke pods only that have the rate:100 label.
- When the new service with the label selector for rate:50 is called it will invoke pods only that have the rate:50 label.

### OpenShift Router

Though I believe this will work similarly for ingress I tested this with OpenShift.

In the routing config we can configure the weighting

```yaml
spec:
  alternateBackends:
  - kind: Service
    name: small-gw-datapower-10
    weight: 10
  host: small-gw-gateway-apic.lbg-420eb34f056ae68f3969289d61f61851-0000.eu-gb.containers.appdomain.cloud
  port:
    targetPort: 9443
  to:
    kind: Service
    name: small-gw-datapower
    weight: 3
  wildcardPolicy: None
```

In the sample above you can see there is two `alternativeBackends` and one `to` section. Each has their own weight. I like to make as few changes to the original consent as possible. The `to` section will route to the original service but I would reduce the weight as low as possible. By adding the `alternativeBackends` section we can point these routes to the new services with some desired weights.

When calculating the proportion of traffic there must be consideration for the original service that routes to all pods.

Using the above example for the weighting we have the following situation.

| Pod | Label | Maths | Amount of traffic |
| --- | --- | --- | --- |
| A | Kind: DataPower Rate : 10 | 10 / 23 / 1 + 3 / 23 / 3 | 48% |
| B | Kind: DataPower Rate : 10 | 10 / 23 / 1 + 3 / 23 / 3 | 48% |
| C | Kind: DataPower | 3 / 23 / 3 | 4% |
