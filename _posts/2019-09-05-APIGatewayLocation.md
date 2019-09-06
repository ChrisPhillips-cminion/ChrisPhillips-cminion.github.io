---
layout: post
date: 2019-09-04 01:00:00
categories: APIConnect
title: "API Gateway in DMZ or after the DMZ"
Location: "Black Phoenix Pub - Southampton"
author: [ "KursadYildirim","UsameGoksun", "ChrisPhillips" ]
---

The API Gateway can be placed in a DMZ or it can be placed behind the DMZ with a reverse proxy in front of it. Here we will discuss the pros and cons regarding each option.

<!--more-->

There is no right answer to this question as it depends on the requirements and procedures of the organisation.

### Option 1 - Gateway behind DMZ
![](/images/gatewayloc-option1.png)

Pros

-   Latency between subsystems between the Gateway and other API Connect Subsystems will be minimal
-   Container environment is isolated from outside world
-   Clear separation of responsibility between API Connect team and other teams.
-   Fewer ports need to be opened between the DMZ and private network.


Cons

-   Reverse proxy must be provided in the DMZ to route traffic to the Gateway.
    -   This is already required for exposing the Developer Portal.
-   If Security policies require SSL Termination in the DMZ, MTLS is not possible using the API Connect functionality.

### Option 2 - Gateway in the DMZ
![](/images/gatewayloc-option2.png)

Pro

-   Production proven technology IBM DataPower Gateway Virtual Appliance
-   Reverse Proxy is not required for routing API traffic.
-   Can be used as a reverse proxy for the Developer Portal.
-    If Security policies require SSL Termination in the DMZ, MTLS is possible using the API Connect functionality.

Con

-   Three virtual DataPower appliances are required
-   Additional latency between Gateway and other API Connect Subsystems
-   Additional bidirectional firewall ports must be opened between the Gateway and other API Connect Subsystems

### Summary

| Requirement    | Option 1                           | Option 2                                                                                                                                 |
| -------------- | ---------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| Latency        | MIN                                | MAX                                                                                                                                      |
| Kubernetes     | Everything in a Kubernetes Cluster | For Management-Analytics-Portal in one Kubernetes cluster, Gateway is either in its own Kubernetes cluster or not deployed to Kubernetes |
| Firewall ports | MIN                                | MAX                                                                                                                                      |
| Endpoint Type  | API endpoint is reverse proxy      | API endpoint is Load Balancer in front of  the Gateway                                                                                   |  

### My opinion

If there were no requirements or policies impacting my decision I would go with Option 1. There is no technical advantage of one over the other, however less firewall ports need to be opened into the DMZ and it provides a clear separation of responsibilities.

### Additional

Though in this article we have discussed putting the API Gateway into the DMZ, no other API Connect component should put in the DMZ.

### Thanks

Thanks to my two Co Authors for reminding me of this question and allowing me to reuse their pros and cons.
