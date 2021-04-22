---
layout: post
categories: APIConnect
date: 2022-04-22 00:15:00
title: Validating the Gateway Peering status

---
API Connect Gateways create a number of peering objeccts to ensure that everything is in sync between the cluster nodes.

<!--more-->

If you wish to validate the status in kubernetes attach to each gateway pod

```bash
oc attach -ti <gateway pod name> -n <namespace>
```

or

```bash
kubectl attach -ti <gateway pod name> -n <namespace>
```

and run the following command

```
top;co;sh gateway-peering-st
```

This return the follow entries for each peer member.

```
 172.30.106.142 api-probe          0               0                  ok          yes     
 172.30.106.142 gwd                0               0                  ok          yes     
 172.30.106.142 rate-limit         0               0                  ok          yes     
 172.30.106.142 subs               0               0                  ok          yes     
```
