---
layout: post
date: 2022-11-30 00:01:00
categories: API Connect
title: "Readiness when restarting API GW Pods"
author: [  "RGeorgeInness", "ChrisPhillips" ]
draft: true
---

The API Gateway consists of one or more DataPower pods. These are listed as `Ready` in the pod list. This article explains what we mean by ready.

<!--more-->

*Note:* The recommendation is never to use two, rather one or three because of the requirements for quorum. The DataPower pods do not store the API Config to disk rather cache it in memory so the API Connect Manager stays the single point of truth.


If less then half of API Gateway (DataPower) pods in a cluster are restarted for any reason (manual or automatic) on a working DataPower Service, when the service is marked as `Ready` the APIs are configured and are ready to be served.

If half or more API Gateway (DataPower) pods in a cluster are restarted for any reason on a working cluster at the same time, then this may require a resync with the API Manager. When the pods are market as `Ready` this means the cluster is operational but does not mean that the APIs have synchronised from the API Manager. This can take up to fifteen minutes after the ready state is reported.
