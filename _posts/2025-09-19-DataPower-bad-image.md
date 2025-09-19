---
layout: post
date: 2025-09-19 09:00:00
categories: APIConnect
title: "Fixing a GatewayService or DataPowerService with an invalid image"
draft: true
---

When applying an image override for the GatewayService or  DataPowerService human errors can sneak in. If there is a mistake in the image path causing it to be invalid the StatefulSet under the DataPowerService will have two `Running` pods and a third in an `ErrImagePull` state. This is only an issue when the DataPowerService has `spec.updateStrategy.mode` is set to `automatic` which is the default for API Gateways.  

Currently, automatic rollouts only relevant for DataPowerServices with gateway peering configuration and whose corresponding DataPowerMonitor has `.spec.monitorGatewayPeering` set to true, such as those deployed as part of an API Connect GatewayCluster.

```
small-ocp-gw-0                                                   1/1     Running        0             23m
small-ocp-gw-1                                                   1/1     Running        0             20m
small-ocp-gw-2                                                   0/1     ErrImagePull   0             7s
```

<!--more-->
The consequence of this is that by default the DataPowerService will not apply updates to the StatefulSet while it is in an error state. Therefore correcting the image in the DataPowerService objects will not resolve this. In order to recover this without causing an outage, you can modify the API Gateway Object with the following overide. These overides are then set in the DataPowerService object

```
spec:
  image: imagurl.com/cp/datapower@sha:123123123123123
  dataPowerOveride:
    updateStrategy:
      mode: manual
      partition: 0
```

This will allow the stateful set to be updated even if it is in an errored state.  I do recommend removing the `spec.DataPowerOveride.updateStrategy` after the new image is rolled out. 