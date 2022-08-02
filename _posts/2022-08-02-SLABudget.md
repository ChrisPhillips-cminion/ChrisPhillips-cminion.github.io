---
layout: post
categories: Day2-Ops
date: 2022-08-02 00:19:00
title: SLA Budgetting - The 99.9999% Fallacy
draft: true
---

Often project owners state that their application needs an availability of 99.97%.  Though I will be referring to API Connect in this article it is applicable to any application.

99.97% SLA matches on to 2h37m47s of total outage a year.  

Though this is useful it doesn’t provide quite enough information.

<!--more-->
## Dependencies

Though the SLA is for a particular application, it needs to factor in the availability of its dependencies. For API Connect this is the Kubernetes, Storage and Network plus other factors I am sure I am missing.  Many people think that in order to reach an SLA of 99.97% each layer needs to be able to be 99.97%. This is a fallacy. Instead you must multiply the SLA of each dependency to find what is available for the application.

For Example


| Dependency | SLA | Outage per year|
| :---        |    :----:   |          ---: |
| Monitoring | 99.999% (0.99999) | 5m15s|
| LogForwarding | 99.998% (0.99998) | 10m31s|
| Network | 99.997% (0.99997) | 15m45s|
| Storage | 99.996% (0.99996) | 21m2s|
| Kubernetes | 99.995% (0.99995) |  26m 17s|


We then multiply the SLA of each layer to get the availability for the dependencies, 0.99999 * 0.99998  * 0.99997 * 0.99996 * 0.99995 is 0.99985 or 99.985% (1h18m53s). This means the application must designed to have at most 1h18m54s (2h37m47s take away 1h18m53s) of outages a year.

## Planned  / Unplanned Outage

Does the total outage time include both planned and unplanned outages?
- A planned outage is down for maintenance activities
- An unplanned outage is a sudden problem.

Many applications can be patched without outage however this changes when state needs to be factored in. Also ensure the decisions above is the same for all dependencies.

When determining host long an outage may last it is worth considering the the RTO budget. See [https://chrisphillips-cminion.github.io/day2-ops/2021/11/08/RTO-considerations.html](https://chrisphillips-cminion.github.io/day2-ops/2021/11/08/RTO-considerations.html)

## Components

API Connect has multiple components not all of them are required to provide the runtime. The Gateway can serve API traffic without any other components being available however business change is not possible without the Manager and/or Portal. Therefore the Gateway may have a more aggressive SLA over the other components as they can tolerate more down time.

--

To conclude this article. When defining SLAs ensure you have a validated and tested understanding of dependencies and the individual requirements of each components.
