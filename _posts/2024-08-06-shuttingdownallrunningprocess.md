---
layout: post
date: 2024-08-06 10:00:00
categories: APIConnect
title: "Take offline the API Manager 10.0.5.x"
draft: true
---

While testing things like disaster recovery it is advisable to take offline the primary API Manager.

<!--more-->

## Take Offline

The safest way to do this is to update the Management CR and add the template section below into  `.spec`.


```
spec:
  template:
  - name: apim
    enabled: false
  - name: apim-schema
    enabled: false
  - name: apim-data
    enabled: false
  - name: taskmanager
    enabled: false
  - name: lur
    enabled: false
  - name: lur-schema
    enabled: false
  - name: lur-data
    enabled: false
  - name: analytics-proxy
    enabled: false
  - name: portal-proxy
    enabled: false
  - name: billing
    enabled: false
  - name: juhu
    enabled: false
  - name: websocket-proxy
    enabled: false
  - name: ui
    enabled: false
```

The Management CR can be editted with
`oc edit mgmt <mgmt cr name>`



If you are using The top Level CR you need to add the following into the Top Level CR `.spec`.

```
spec:
  management:
    template:
    - name: apim
      enabled: false
    - name: apim-schema
      enabled: false
    - name: apim-data
      enabled: false
    - name: taskmanager
      enabled: false
    - name: lur
      enabled: false
    - name: lur-schema
      enabled: false
    - name: lur-data
      enabled: false
    - name: analytics-proxy
      enabled: false
    - name: portal-proxy
      enabled: false
    - name: billing
      enabled: false
    - name: juhu
      enabled: false
    - name: websocket-proxy
      enabled: false
    - name: ui
      enabled: false
```

The Top Level CR can be editted with
`oc edit apiconnectcluster <top level cr name>`

## Bring back Online

Remove the template section from the CR.
