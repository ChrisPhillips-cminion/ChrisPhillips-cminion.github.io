---
layout: post
date: 2022-11-12 00:01:00
categories: HomeLab
title: "VPN when the target network is the same as the source network."
---
As I spend a lot of time working away from home, I VPN into my home lab so that I can play. However for the first time my homelab was on the same network range as the hotel I was in, and so when I vpned in, nothing would route.

To get around this I created an addition entry in the routing table for each server you want to connect to, this will be lost after a reboot.

```
sudo route add 192.168.31.1 -interface ppp0
```

`ppp0` is the tunnel interface from `ifconfig` and `192.168.31.1` is the IP of the target you want to connect to.
