---
layout: post
date: 2018-07-03  00:00:00
categories: APIConnect
title: 'Deploying API Connect 2018 for a POT without a DNS Server.'
---
<!--more-->

Though these steps will make your pods contactable I recommend that you
only do this in a POT environment

This works by setting an endpoint with a hostname that resolves to the
ingress public address. There are a few services that offer this freely
on the internet. For this example I am going to use <https://nip.io>

For each endpoint you need to set run the appropriate command like below
replacing \<ingress ip\> with the ip of your ingress. note: you may need
to change the gw, gateway and gateway-director for the sub system you
are installing.

```
apicup endpoints set gw gateway gw.<ingress ip>.nip.io ;
```

```
apicup endpoints set gw gateway-director gwd.<ingress ip>.nip.io ;
```

Now continue your install as normal.

The nip link is set to always resolve any domain with .\<ip\>.ntp to the
ip spefified. i.e. gw.192.168.1.1.nip.io will resolve to 192.168.1.1.
The DNS Server does not need to directly connect to the host so this
works fine.





By [Chris Phillips](https://medium.com/@cminion) on
[July 3, 2018](https://medium.com/p/18eaacb1d88e).

[Canonical
link](https://medium.com/@cminion/deploying-api-connect-2018-for-a-pot-without-a-dns-server-18eaacb1d88e)

Exported from [Medium](https://medium.com) on April 6, 2019.
