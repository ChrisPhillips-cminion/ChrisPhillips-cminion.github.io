---
layout: post
date: 2019-06-12 1:00:00
categories: APIConnect
title: "API Connect  - DataPower (Gateway) not forward logging events to Analytics"
draft: true
---

*Thanks to August Ziesemer for helping me here*

If you are using API Connect with DataPower in Production you need to have the AO License file in order send on the analytics.

However if DataPower is running in Kubernetes and the pod gets restarted the applied license is lost.


If you are not in Production the best solution to this issue is  use the Non Production DataPower image.

However if you are in Production the solution to this is to build your own DataPower image. The instructions can be found [here](https://www.ibm.com/support/knowledgecenter/SS9H2Y_7.7.0/com.ibm.dp.doc/docker_features.html) .

Once this is done the image needs pushing to your enterprise docker registry, ensure you tag this with a unique tag e.g. `aoproduction-2018.4.1.6`. Update the APICUP config with the new tag and path of the image.


```
image:
   repository: enterprise-docker-registry/images/datapower
   tag: aoproduction-2018.4.1.6
```
*Sample from the apicup configuration file.*

Now when you deploy it will pick up the new image that has the license file persisted to disk.
