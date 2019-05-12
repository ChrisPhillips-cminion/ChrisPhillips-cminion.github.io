---
layout: post
date: 2018-11-02  00:00:00
categories: APIConnect
title: Enabling the DataPower WebUI in a Kubernetes Deployment
---


In order to access the DataPower WebUI please follow these steps.

1.  [Save the following yaml file as gw-extras.yaml]

```
datapower:
 # Gateway MGMT variables
 # This value should either be ‘enabled’ or ‘dislabled’. Default is disabled
 webGuiManagementState: “enabled”
 webGuiManagementPort: 9090
 webGuiManagementLocalAddress: 0.0.0.0
 # This value should either be ‘enabled’ or ‘disabled’. Default is disabled
 gatewaySshState: “enabled”
 gatewaySshPort: 9022
 gatewaySshLocalAddress: 0.0.0.0
 # This value should either be ‘enabled’ or ‘disabled’. Default is disabled
 restManagementState: “enabled”
 restManagementPort: 5554
 restManagementLocalAddress: 0.0.0.0
```

2\. In your apicup yaml file add the following lines to the gateway
section

`extra-values-file: gw-extras.yaml`

3\. Deploy the DataPower again

4\. Once it is deployed run `kubectl get po -n <namespace>` to get the pod name for DataPower. Then run
`kubectl port-forward <pod> 9090:9090` to
forward the port to your local machine.

5\. The DataPower web console is now available on
<https://127.0.0.1:9090>

The Username and Password is admin:admin by default.





By [Chris Phillips](https://medium.com/@cminion) on
[November 2, 2018](https://medium.com/p/33fc8c9ca4be).

[Canonical
link](https://medium.com/@cminion/enabling-the-datapower-webui-in-a-kubernetes-deployment-33fc8c9ca4be)

Exported from [Medium](https://medium.com) on April 6, 2019.
