---
layout: post
date: 2023-05-11 00:01:00
categories: OpenShift
title: "0/9 nodes are available: 9 node(s) had volume node affinity conflict"
---

When deploying a kubernetes application and a pod displays an event with

`0/9 nodes are available: 9 node(s) had volume node affinity conflict`

There are two common reasons for this.
<!--more-->

The first two thigns to check are
1. StorageClass is correctly set on the PV
2. That the StorageClass has the correct `volumeBindingMode`. For API COnnect this must be set to `WaitForFirstConsumer`
