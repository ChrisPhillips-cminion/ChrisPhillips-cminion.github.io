---
layout: post
date: 2023-06-30 01:00:00
categories: APIConnect
title: "API Connect registration without access to an external load balancer."

draft: true
---


In API Connect 10.0.5.3+ and 10.0.6.0+ we can register sub systems without the need for an external load balancer. This is only possible for Kubernetes, OpenShift and CloudPak for Integration.

<!--more-->

This is useful for scenarios where it is not desired to have traffic between the manager and the subcomponents does not have to go out of the cluster and back in.

To enable this on the registration instead of using an external URL we must simply use the Kubernetes service hostname.

1.	Get a list of all services and take a note of the ones highlighted in red. You may well have a different prefix (small) or none.

![image](/images/svclist.png)

2.	For my set up its these three example entries, but yours may be different.

| Component | URL format | Example |
| ------ | ------------------------ | ----------------------- |
| Gateway| <gw-svc>.<namespace>.svc | small-gw.apiconnect.svc |
| A7s    | <a7s-svc>.<namespace>.svc | small-a7s.apiconnect.svc |
| Portal | <portal-svc>.<namespace>.svc | small-portal.apiconnect.svc |


3.	When you register the subcomponents you use this end points for the internal management/director endpoints.


That’s it! When the registration completes the internal routes will be used.
