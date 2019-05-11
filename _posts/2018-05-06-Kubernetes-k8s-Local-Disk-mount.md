---
layout: post
date: 2018-05-06  00:00:00
categories: APIConnect
title: 'Kubernetes (k8s) --- Local Disk mount'
---

Kubernetes (k8s) --- Local Disk mount
=====================================


So I have spent far to long trying to mount a local disk into my k8s
cluster. My aim is to run pihole on my home system in k8s, primarily...






------------------------------------------------------------------------




### Kubernetes (k8s) --- Local Disk mount

So I have spent far to long trying to mount a local disk into my k8s
cluster. My aim is to run [pihole](https://pi-hole.net/) on my home system in k8s, primarily to educate me.

So after a night out (maybe with some alcohol) and an old friend John he
suggested I look at the latest beta which contains local. He also talked
me into buying a server rack from ebay but that is another story.

I have got my head around helm and so I was keen to keep using it. I
copied and pasted the pv into my local helm chart.

```
apiVersion: v1
```

```
kind: PersistentVolume
```

```
metadata:
```

```
   name: }-pv
```

```
spec:
```

```
  capacity:
```

```
  storage: 5Gi
```

```
  # volumeMode field requires BlockVolume Alpha feature gate to be enabled.
```

```
  volumeMode: Filesystem
```

```
  accessModes:
```

```
  - ReadWriteOnce
```

```
  persistentVolumeReclaimPolicy: Delete
```

```
  storageClassName: local-storage
```

```
  local:
```

```
    path: /mnt/pihole
```

```
  nodeAffinity:
```

```
    required:
```

```
      nodeSelectorTerms:
```

```
      - matchExpressions:
```

```
        - key: kubernetes.io/hostname
```

```
          operator: In
```

```
          values:
```

```
            - example-node
```

This ran successfully but the pod would not bind with the pvc. After
hitting my head against the wall for 30mins, i sat down and read the
yaml above.

> kubernetes.io/hostname

So i changed example-node to my hostname and it all magically worked!

**Moral of the story, read the sample config before you use it.**

<https://kubernetes.io/docs/concepts/storage/volumes/>


[**kubernetes-incubator/external-storage**\
*external-storage - External storage plugins, provisioners, and helper
libraries*github.com](https://github.com/kubernetes-incubator/external-storage/tree/master/local-volume "https://github.com/kubernetes-incubator/external-storage/tree/master/local-volume")[](https://github.com/kubernetes-incubator/external-storage/tree/master/local-volume)






By [Chris Phillips](https://medium.com/@cminion) on
[May 6, 2018](https://medium.com/p/6731a385135).

[Canonical
link](https://medium.com/@cminion/kubernetes-k8s-local-disk-mount-6731a385135)

Exported from [Medium](https://medium.com) on April 6, 2019.
