---
layout: post
categories: APIConnect
date: 2020-11-30 00:14:00
title: API Gateway what's the difference -  V5c, Native and V5e
draft: true
---

API Connect has seen a number of changes in its API Gateway in the last few years. This article will go through the current gateways how they compare and what the elusive V5e is.

<!--more-->

API Connect uses DataPower as its runtime. This has been true for many years and is still true today. Inside DataPower there are two types of Gateways that API Connect can use.

* V5 Compatible (aka V5c or DataPower-Gateway)
* Native API Gateway  (aka apigw or DataPower-API-Gateway)

The purpose of V5c is to allow users to take APIs from their existing API Connect V5 and publish them to their v10 API Connect with near zero changes. By doing this they can sunset their V5 estate and run on the  latest and greatest API Connect and so making use of many of the new features with minimal migration work.  V5c will see a noticeable performance increase compared to V5 in many workloads.

The Native API Gateway is a ground up rewritten gateway that aims to provide ten times the performance when compared to V5. I have personally seen in some niche workloads the performance improvement is 1200% when compared to V5. The Native API Gateway can not run V5 or V5c APIs straight away because of how it is implemented. The API Migration Utility (AMU) will translate much of the V5 API to the Native API Gateway format but these will often require additional manual changes.

V5e was designed to assist moving from V5c to the Native API Gateway. Though my self and many other people have positioned V5e as third gateway type, it is not. V5e is simply an additional set of policies that provide identical function when compared to V5 that runs on the Native API Gateway. This will give significant performance improvement over V5 but not as much as the Native API Gateway. In a basic workload I have seen a 700% performance improvement.  The API Migration Utility (AMU) will translate the V5 API to a Native API Gateway using both Native API Gateway and V5e policies. Additional work should not be required to run the APIs.
