---
layout: post
date: 2023-02-06 00:01:00
categories: APIConnect
title: "Simplifying Network Comms to help debug ingress traffic."
---


Recently at a client we were hit with a high latency connection. In order to prove this was not a problem with API Connect we decided to execute a curl command as close to the datapower as possible. 

<!--more-->

With the API Gateway of  API Connect in Kubernetse or Openshift this is simple. 

1. `oc get po | grep gw`
* Select the POD Name for one of the Gateways
2. `oc exec -ti <podname> -- bash`
* This will bring up a bash shell in the same pod as the datapower. 
3. `curl -vk https://127.0.0.1:9443/<API Path>`
* Execute the curl command changing the hostname and port to 127.0.0.1:9443



This will bypass any, firewall, load balancers and infrastructure. 