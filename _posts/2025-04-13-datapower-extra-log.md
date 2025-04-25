---
layout: post
categories: DataPower
date: 2025-04-13 00:14:00
title: Additional suggested logs for DataPower
draft: true
---

When configuring IBM DataPower there are a number of different logging options to select from. In this article we are suggesting five differnt logging topics that can be enabled. 

<!--more-->


| type | Description | Collection information | 
|---|---|---| 
|System Usage Table | The System Usage Table states the current work list that is awaiting to be scheduled. We recommend that the following fields are collected • Load Percentage • CPU Percentage • Worklist • File Count | Table is available by the REST or SOMA interface. |
|---|---|---|
| Gateway Director (GWD) | Provides the logs for the API synchronization - Communication between API Manager and the IBM DataPower. This enabled by default in containers. | Log target for the following subscriptions. `event apic-gw-service debug` In a Kubernetes environment the log target should send this to the default log in the default domain to allow Kubernetes to collect this as part of the pod logs. | 
|---|---|---|
| Collection Log | Provides the logs for the API synchronization – Creating of IBM DataPower objects. | Log target for the following subscriptions. `event cli debug event mgmt info` In a Kubernetes environment the log target should send this to the default log in the default domain to allow Kubernetes to collect this as part of the pod logs. |
|---|---|---|
| dpMon | nmon snapshot files containing detailed system metrics. The snapshot files contain by default 900s of data per file with 9 rotations. |  These files should be copied from the default domain every two hours while debugging or capacity analysis is being done. This is due to the quantity of long- term storage required to store the files outside of IBM DataPower. In a Kubernetes environment this can be done with kubectl cp. |
|---|---|---|
| extLatency | Provides detailed latency information for transactions going through the IBM DataPower domain.  In addition to latency, it is suggested to include the memory report. | Log target for the following subscriptions. `event extlatency info` `event memory-report debug` In a Kubernetes environment the log target should send this to the default log in the default domain to allow Kubernetes to collect this as part of the pod logs. |
