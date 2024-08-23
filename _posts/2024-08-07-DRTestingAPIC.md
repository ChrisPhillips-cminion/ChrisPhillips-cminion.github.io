---
layout: post
date: 2024-08-07 10:00:00
categories: APIConnect
title: "Take offline the API Manager 10.0.5.x in OpenShift and Kubernetes"
---

While testing  disaster recovery it is advisable to take offline the primary API Manager. This instructions will cover OpenShift and Kubernetes.
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
  template:
  - name: mgmt-apim
    enabled: false
  - name: mgmt-apim-schema
    enabled: false
  - name: mgmt-apim-data
    enabled: false
  - name: mgmt-taskmanager
    enabled: false
  - name: mgmt-lur
    enabled: false
  - name: mgmt-lur-schema
    enabled: false
  - name: mgmt-lur-data
    enabled: false
  - name: mgmt-analytics-proxy
    enabled: false
  - name: mgmt-portal-proxy
    enabled: false
  - name: mgmt-billing
    enabled: false
  - name: mgmt-juhu
    enabled: false
  - name: mgmt-websocket-proxy
    enabled: false
  - name: mgmt-ui
    enabled: false
```

The Top Level CR can be editted with
`oc edit apiconnectcluster <top level cr name>`

Once this is complete the database should be shut down following the steps in the knowledge centre. [https://www.ibm.com/docs/en/api-connect/10.0.5.x_lts?topic=factor-shutting-down-postgres-database](https://www.ibm.com/docs/en/api-connect/10.0.5.x_lts?topic=factor-shutting-down-postgres-database)


## Bring back Online

Start the dabase by following these steps [https://www.ibm.com/docs/en/api-connect/10.0.5.x_lts?topic=factor-shutting-down-postgres-database#ffm_postgres__title__4](https://www.ibm.com/docs/en/api-connect/10.0.5.x_lts?topic=factor-shutting-down-postgres-database#ffm_postgres__title__4)

Once the DataBase has started remove the template section from the CR.
