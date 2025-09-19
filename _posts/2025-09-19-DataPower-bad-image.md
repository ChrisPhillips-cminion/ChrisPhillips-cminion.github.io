---
layout: post
date: 2025-09-19 09:00:00
categories: DataPower
title: "Fixing a DataPowerService with an invalid image"
draft: true
---

When applying an image override for the DataPowerService human errors can sneak in. If there is a mistake in the image path causing it to be invalid the StatefulSet under the DataPowerService will have two `Running` pods and a third in an `ErrImagePull` state.

```
small-ocp-gw-0                                                   1/1     Running        0             23m
small-ocp-gw-1                                                   1/1     Running        0             20m
small-ocp-gw-2                                                   0/1     ErrImagePull   0             7s
```

<!--more-->


The consequence of this is that by default the DataPowerService will not apply updates to the StatefulSet while it is in an error state. Therefore correcting the image in the DataPowerService objects will not resolve this. In order to recover this without causing an outage, you can modify `spec.updateStrategy` from

```
spec:
  updateStrategy:
    mode: automatic
    rolloutHistoryLimit: 1

```

To

```
spec:
  updateStrategy:
    mode: manual
    partition: 2
```

This will allow the stateful set to be updated even if it is in an errored state.  I do recommend changing this back after the new image is rolled out. 

