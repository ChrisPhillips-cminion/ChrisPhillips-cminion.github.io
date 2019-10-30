---
layout: post
date: 2019-10-28 00:01:00
categories: OpenShift
title: "Ingress (or other pods) unable to route to pods in different namespaces"
author: ["ChrisPhillips","JamesHewitt"]
draft: true
---
This article explains the basics of error handling in APIs in API Connect 2018.
<!--more-->

If OpenShift is installed with the `ovs-multitenant` network plugin then by default pods cannot communicate with pods in other namespaces, with the exception of the default namespace.

With ICP on OpenShift ingress is installed into the `kube-system` namespace and so if `ovs-multitenant` is enabled then ingress cannot communicate to pods outside of the `kube-system` namespace.

In order to allow this communication runt he following command

```oc adm pod-network make-projects-global kube-system```
