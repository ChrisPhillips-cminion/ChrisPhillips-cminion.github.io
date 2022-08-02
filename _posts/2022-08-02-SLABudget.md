---
layout: post
categories: Day2-Ops
date: 2022-08-02 00:19:00
title: SLA Budgetting - 99.999% Fallacy
draft: true
---

Often project owners state that their application needs an availability of 99.99%.  Though I will be referring to API Connect in this article it is applicable to any application.

99.99% SLA matches on to 52m36s of total outage a year.  

Though this is useful it doesn’t provide quite enough information.

<!--more-->
## Dependencies

Though the SLA is for a particular application, it needs to factor in the availability of its dependencies. For API Connect this is the Kubernetes, Storage and Network plus other factors I am sure I am missing.  Many people think that in order to reach an SLA of 99.99% each layer needs to be able to be 99.99%. This is a fallacy. Instead you must multiply the SLA of each dependency to find what is available for the application.

For Example


| Dependency | SLA | Outage per year|
| :---        |    :----:   |          ---: |
| Network | 99.999% (0.99999) | 5m15s|
| Storage | 99.998% (0.99998) | 10m31s|
| Kubernetes | 99.997 (0.99997) |  15m45s|


We then multiply the SLA of each layer to get the availability for the dependencies, 0.99999 * 0.99998  * 0.99997 is 0.99994 or 99.994%(31m33s). This means the application must designed to have at most 21m3s (52m36s take away 31m33s) of outages a year.

## Planned  / Unplanned Outage

Does the total outage time include both planned and unplanned outages?
- A planned outage is down for maintenance activities
- An unplanned outage is a sudden problem.

Many applications can be patched without outage however this changes when state needs to be factored in. Also ensure the decisions above is the same for all dependencies.

When determining host long an outage may last it is worth considering the the RTO budget. See [https://chrisphillips-cminion.github.io/day2-ops/2021/11/08/RTO-considerations.html](https://chrisphillips-cminion.github.io/day2-ops/2021/11/08/RTO-considerations.html)

## Components

API Connect has multiple components not all of them are required to provide the runtime. The Gateway can serve API traffic without any other components being available however business change is not possible without the Manager and/or Portal. Therefore the Gateway may have a more aggressive SLA over the other components as they can tolerate more down time.

--

To conclude this article. When defining SLAs ensure you have an understanding of dependencies and the individual requirements of each components.
