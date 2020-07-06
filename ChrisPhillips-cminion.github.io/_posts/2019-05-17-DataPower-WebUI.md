---
layout: post
date: 2019-05-17  00:00:00
categories: APIConnect
title: 'Enabling the WebUI in DataPower in Kubernetes for APIConnect 2018 [Guest Post by Nick Cawood]'
author: ["NickCawood"]
---

To access the DataPower UI with API Connect 2018.4.1.X values need to be set during the installation of the Gateway subsystem. These values are set using the extra-values-file parameter of the apicup tool:

`apicup subsys set <GWY-subsys name> extra-values-file=datapower-values.yaml`
<!--more-->
where the datapower-values.yaml file contains:

```
datapower:
 # Gateway MGMT variables
 # This value should either be 'enabled' or 'dislabled'. Default is disabled
 webGuiManagementState: "enabled"
 webGuiManagementPort: 9090
 webGuiManagementLocalAddress: 0.0.0.0
 # This value should either be 'enabled' or 'disabled'. Default is disabled
 gatewaySshState: "enabled"
 gatewaySshPort: 9022
 gatewaySshLocalAddress: 0.0.0.0
 # This value should either be 'enabled' or 'disabled'. Default is disabled
 restManagementState: "enabled"
 restManagementPort: 5554
 restManagementLocalAddress: 0.0.0.0
```

After the Gateway subsystem is installed the DataPower UI can be accessed as follows, first find the Gateway Service pod name:


```
$ kubectl get pods -n apiconnect | grep dynamic-gateway-service
r3133919d63-dynamic-gateway-service-0                         1/1     Running     0          2d23h
```

Use the r3133919d63-dynamic-gateway-service-0 pod name and run the following port-forwarding command:

```
$ kubectl port-forward r3133919d63-dynamic-gateway-service-0 9090:9090 -n apiconnect
Forwarding from [::1]:9090 -> 9090
Forwarding from 127.0.0.1:9090 -> 9090
```

You can now logon to the DataPower UI via a web-browser with `https://127.0.0.1:9090` (user/password: admin/admin) selecting either the new UI view "Blueprint Console" or the classic "WebGUI" graphical interfaces.
