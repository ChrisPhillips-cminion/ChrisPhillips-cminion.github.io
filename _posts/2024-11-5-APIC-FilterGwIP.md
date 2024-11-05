---
layout: post
date: 2024-11-5 10:00:00
categories: APIConnect
title: "API Connect - Filtering by source IP on a gateway."
author: [ "ChrisPhillips", "AmitKumarSingh" ]
---

I am often asked if there is a way we can limit the range of IPs that we accept calling an API Gateway. This can be done with Global Policies and a little GatewayScript.

Amit Kumar Singh from my team built some gateway script that will do this check.


<!--more-->

This code will look at the `X-Forwarded-For` headers and evaluate if it is in a CIDR. This can easily be modified for a direct match to.

Code is available here.- [https://github.ibm.com/Amit-Kumar-Singh11/apic-scripts](https://github.ibm.com/Amit-Kumar-Singh11/apic-scripts)

I have taken Amit's code and wrapped it into a gw extension. This code can then be place in a global policy extension. This must be applied via the CLI.  [https://gist.github.com/ChrisPhillips-cminion/4979bf545c0e806bcdb1c36cd320724e](https://gist.github.com/ChrisPhillips-cminion/4979bf545c0e806bcdb1c36cd320724e)

I modified the if statement so that request is rejected if it does not match.
