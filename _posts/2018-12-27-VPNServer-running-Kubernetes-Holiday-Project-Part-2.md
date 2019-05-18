---
layout: post
date: 2018-12-27  00:00:00
categories: APIConnect
title: 'VPNServer running Kubernetes'
image: 'https://cdn-images-1.medium.com/max/800/1*EScuR6TCDCBgmvTrClI43g.png'
---
##  Holiday Project Part 2

![](https://cdn-images-1.medium.com/max/800/1*EScuR6TCDCBgmvTrClI43g.png)

*During my two weeks off of work I set myself the challenge to move as
much of my home network infrastructure to Kubernetes as possible. My
wife has often questioned "Why do you need any network Infrastructure,
other then a wifi point?". This article is still* ***not*** *going to
address that question.*

**What is VPN?**

In short by having a VPN Server allows me to connect to my home network
securely from any location. As I travel around the world I find this
useful for backing up files, fixing computer issues and many other
reasons.

**VPN in Kubernetes**

This uses the hwdsl2/ipsec-vpn-server container.

The helm chart can be downloaded from
<https://github.com/ChrisPhillips-cminion/vpn-helm>.

Update the values.yaml file then run helm install \<path to directory\>

The values file must contain these entries

```
VPN_IPSEC_PSK: shared-password
VPN_USER: cminion
VPN_PASSWORD: password
#Public IP
EXTERNALIP: 1.1.1.1
```

-   [VPN\_IPSEC\_PSK - The share password]
-   [VPN\_USER - username]
-   [VPN\_PASSWORD - User Password]
-   [ExternalIP: The IP you will be connecting to, for me this is my
    houses public IP, it is required to route through
    Kubernetes.]





By [Chris Phillips](https://medium.com/@cminion) on
[December 27, 2018](https://medium.com/p/76998814705d).

[Canonical
link](https://medium.com/@cminion/vpnserver-running-kubernetes-holiday-project-part-2-76998814705d)

Exported from [Medium](https://medium.com) on April 6, 2019.
