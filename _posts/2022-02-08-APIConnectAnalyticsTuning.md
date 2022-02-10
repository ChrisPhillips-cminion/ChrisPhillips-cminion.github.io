---
layout: post
categories: APIConnect
date: 2022-02-08 00:14:00
title: Tuning API Connect Analytics
---

As our customers grow their requirements grow. Recently I have been asked to tune the API Connect analytics subsystem for a through put of multi thousand transactions pers seconds.

<!--more-->

The exact settings that are required will change from client to client depending on the hardware they have available and their requirements (e.g. payload size if its enabled)

## Storage
You will need a fast block storage. Faster the better. The majority of the configuration I have seen are throttled because the content cannot be written to the disk fast enough. Recently I used a SAN that I could create PVCs directly on. This SAN does not need to be used for all APIConnect storage just the analytics data.

## Understanding the bottlenecks

Requests come into the Analytics Subsystem

<div class="mermaid">
sequenceDiagram
    DataPower->>+Analytics MTLS GW: Invokes
    Analytics MTLS GW->>Analytics Ingestion: Invokes
    Analytics Ingestion->>Analytics Storage Data: Invokes
    Analytics Storage Data->>Disk: Writes
 </div>


### Storage Data
As I wrote above the majority of the bottlenecks come from the Storage Data pod not being able to write data fast enough. To see if the bottle neck is here follow these steps.
1. Run your predicted workload through the API GW.
2. Load a terminal in the storage data pod.
3. Run top
4. Look at the cpu wait time. If this is above 10% then it is probable that the disk is being thrashed.
![https://chrisphillips-cminion.github.io/images/cpuwait.png](https://chrisphillips-cminion.github.io/images/cpuwait.png)

### CPU Utilisation
Assuming the above is ok,
1. Run your predicted workload through the API GW.
2. Look at the CPU metrics using `oc adm top po` or `kubectl top po` and see if the CPU is hitting the limit of the ingestion and storage data pods. If this is less then 50% consumed then we can increase the thread counts.

### Logs
The final areas to check for bottlenecks is in the DataPower logs. DataPower will report unable to connect to analytics or that it is being throttled.  


## Tuning

First of all I would increase the number of threads on the Storage Data Pod, this will drive up the CPU wait time, as we are sending more data at the same time to the disk .
1. Edit the storage data statefulset  to increase the PROCESSORS environment variable from 4 (default) to 50. We can set a higher limit here as many threads will be stuck waiting for the SAN to respond and so we can spawn additional threads.
2. Storage Data pods will automatically restart, this will take a couple of mins.
3. Repeat the storage data test above.

Second I would increase the number of Workers on the ingestion pod.
1. Edit the Analytics CR and edit the following lines
```yaml
pipelineBatchDelay: 10
pipelineBatchSize: 350
pipelineWorkers: 100
```
2. These values may need to be tuned for your workload but they are my starting point.
3. Manually restart the Ingestion pods

When you have applied the above settings validate the DataPower log and see if it reports any problems.

# Conclusion
So this article shows how you can increase your analytics throughput without increasing the CPU or Memory. Though please note if you are seeing CPU utilisation of the Ingestion or Storage DataPod increasing you will need to increase the CPU limit of those pods.
