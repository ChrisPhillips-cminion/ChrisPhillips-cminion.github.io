---
layout: post
date: 2019-01-11  00:00:00
categories: APIConnect
title: 'QuickNote: Deploying on ICP 3.1.1 and you don''t know what you are doing.'
---


ICP 3.1.1 is locked down.

I used the following PSP to remove all the locked down settings. Please
only use this for POC and POTs, and be aware you are weakening your
environment.

```
apiVersion: extensions/v1beta1
kind: PodSecurityPolicy
metadata:
  annotations
    seccomp.security.alpha.kubernetes.io/allowedProfileNames: docker/default
    seccomp.security.alpha.kubernetes.io/defaultProfileName: docker/default
  name: ibm-unrestricted
spec:
  allowPrivilegeEscalation: true
  allowedCapabilities:
  - '*'
  allowedUnsafeSysctls:
  - '*'
  fsGroup:
    rule: RunAsAny
  hostIPC: true
  hostNetwork: true
  hostPID: true
  hostPorts:
  - max: 65535
    min: 0
  privileged: true
  runAsUser:
    rule: RunAsAny
  seLinux:
    rule: RunAsAny
  supplementalGroups:
    rule: RunAsAny
  volumes:
  - '*'
```





By [Chris Phillips](https://medium.com/@cminion) on
[January 11, 2019](https://medium.com/p/ebe860d13eef).

[Canonical
link](https://medium.com/@cminion/quicknote-deploying-on-icp-3-1-1-and-you-dont-know-what-you-are-doing-ebe860d13eef)

Exported from [Medium](https://medium.com) on April 6, 2019.
