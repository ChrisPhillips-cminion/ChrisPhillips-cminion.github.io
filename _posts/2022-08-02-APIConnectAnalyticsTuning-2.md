---
layout: post
categories: APIConnect
date: 2022-08-02 00:14:00
title: Tuning API Connect Analytics - CORRECTION!
draft: true
---

8 months ago I wrote up on how to tune Analytics. There was lots of bad suggestions in that article and this article is here to correct the original.

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
1. Edit the Analytics CR
* Change `spec.storage.type` to `shared`.
* Add the storageclass to `spec.storage.shared.volumeClaimTemplate.storageClassName`
* wait 5mins for the new storage pods to come up
2. Edit the storage-shared  statefulset  
* Increase the CPU limit to 2
* Increase the memory limit to 8GB
* Change the ES_JAVA_OPTS env to -Xms4g -Xmx4g
* Change the PROCESSORS environment variable from 2. and increase the limit to 2 cores and
2. Storage Data pods will automatically restart, this will take a couple of mins.

Second I would increase the number of Workers on the ingestion pod.
1. Edit the Analytics CR and edit the following lines
```yaml
pipeline.workers: 2
pipeline.batch.size: 4400
pipeline.batch.delay: 0
```
2. Manually restart the Ingestion pods
*These values may need to be tuned for your workload but they are my starting point.*

Third I would modify the DataPower settings. If you are using DataPower in a container you would need to create a gateway extension to persist this. This guide will tell you the commands to run on each DataPower via the cli. This needs to be done to each DataPower in the cluster.
1. `ssh` or `oc attach` into the DataPower
2. Go to the apiconnect domain and enter config G.g. `sw apiconnect; config`
3. type `analytics-endpoint a7s;  max-records 4096 ; exit`
4. type `exit` again
*These values may need to be tuned for your workload but they are my starting point.*

When you have applied the above settings validate the DataPower log and see if it reports any problems.
