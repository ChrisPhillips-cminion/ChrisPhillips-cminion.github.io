---
layout: post
categories: APIConnect
date: 2021-04-22 00:15:00
title: Validating the Gateway Peering status

---
API Connect Gateways create a number of peering objeccts to ensure that everything is in sync between the cluster nodes.

![GatewayPeerStatus](/images/gwpeer.png)

<!--more-->

If you wish to validate the status in kubernetes attach to each gateway pod

```bash
oc attach -ti <gateway pod name> -n <namespace>
```

or

```bash
kubectl attach -ti <gateway pod name> -n <namespace>
```

You will be prompted to login with your datapower credentials.  If no secret is set on the Gateway Cluster CR the username and password is admin and admin. If this does not work look to see if there is a secret ending with `gw-admin`

e.g.

```
NAME                TYPE     DATA   AGE
minimum2-gw-admin   Opaque   1      75m
```

To get the passsord from the secret the following command  `oc get secret minimum2-gw-admin -ojson | jq .data.password | sed -e s/\"//g | base64 -d`


Then run the  following command

```
top;config;show gateway-peering-status
```

This returns the follow entries for each peer member.
```
 172.30.106.142 api-probe          0               0                  ok          yes     
 172.30.106.142 gwd                0               0                  ok          yes     
 172.30.106.142 rate-limit         0               0                  ok          yes     
 172.30.106.142 subs               0               0                  ok          yes     
```
