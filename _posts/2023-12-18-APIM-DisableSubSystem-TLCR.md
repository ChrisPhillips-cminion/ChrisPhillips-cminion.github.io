---
layout: post
date: 2023-12-18 01:00:00
categories: APIConnect
title: "API Connect Cluster object - disabling Portal/Analytics/Gateway"
draft: true
---

When deploying API Connect in OpenShift you can deploy the API Connect Cluster Object. *Sometimes this is referred to as the TopLevelCR.* This will deploy a management, analytics, portal, and gateway. If you are using CP4I it will also auto configure it as well.  

However, there are times that all subcomponents are not required.

<!--more-->
Inside the API Connect Cluster YAML you can set the `disabledServices` attribute under `spec` with the following values in an array.

If these attributes are present

|---|---|---|
| **Attribute** | **If attribute is present in the array** |
| analytics |  Does not deploy the Analytics Subsystem |
| portal |  Does not deploy the Portal Subsystem |
| gateway | Does not deploy the Gateway Subsyste m|
| configurator | *Ignored if run present without the Platform Navigator.* Does not register the API Manager into the Platform Navigator or subcomponents into the API Manager. |

Here is a complete YAML with all subsystems disabled for 10.0.7.0 CD release.  This works the same way for 10.0.5.x.

```yaml
kind: APIConnectCluster
apiVersion: apiconnect.ibm.com/v1beta1
metadata:
  annotations:
    apiconnect-operator/backups-not-configured: "true"
  labels:
    app.kubernetes.io/instance: apiconnect
    app.kubernetes.io/managed-by: ibm-apiconnect
    app.kubernetes.io/name: apiconnect-small
  name: chrisblog-demo
  namespace: chrisblog-ns
spec:
  analytics:
    mtlsValidateClient: true
  disabledServices:
   - configurator
   - analytics
   - portal
   - gateway
  license:
    accept: false
    license: L-MMBZ-295QZQ
    metric: VIRTUAL_PROCESSOR_CORE
    use: production
  portal:
    mtlsValidateClient: true
  profile: n1xc7.m48
  version: 10.0.7.0
```
