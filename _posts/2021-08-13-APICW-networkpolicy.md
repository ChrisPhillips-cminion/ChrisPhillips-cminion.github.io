---
layout: post
date: 2021-08-12 00:13:00
categories: APIConnect
title: "Running a passive API Manger"
draft: true
---

Frequently customers have asked me how do they test the Active Passive DR. (back up from region one and apply to region 2) with out the second region control all the sub components.

<!--more-->


With API Connect you can registered multiple gateways to each API Manager. This can cause complications when running an Ative Passive approach as the passive api manager if configured will  connect and claim the gateways. The common way to handle this is to not have any content in the passive api manager. However this means there is no clear way to to test the back up / restore of any API Connect system.

I created this "network bung" that is a couple of network policies that stop the API Manager and Portal having any ingress/egress content that is not from inside their own component.

l
