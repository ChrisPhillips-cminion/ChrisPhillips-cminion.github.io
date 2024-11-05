---
layout: post
date: 2024-11-5 10:00:00
categories: APIConnect
title: "API Connect - Filtering by source IP on a gateway."
author: [ "ChrisPhillips", "AmitKumarSingh" ]
---

I am often asked if there is a way we can limit the range of IPs that we accept calling an API Gateway. This can be done with Global Policies and a little GatewayScript.

Amit Kumar Singh from my team built some GatewayScript that will do this check.


<!--more-->

The GatewayScript will look at the `X-Forwarded-For` headers and evaluate if it is in a hard coded CIDR.

GatewayScript is available here.- [https://github.ibm.com/Amit-Kumar-Singh11/apic-scripts](https://github.ibm.com/Amit-Kumar-Singh11/apic-scripts)

I have taken Amit's code and wrapped it into a GlobalPolicy extension. This must be applied via the CLI.  [https://gist.github.com/ChrisPhillips-cminion/4979bf545c0e806bcdb1c36cd320724e](https://gist.github.com/ChrisPhillips-cminion/4979bf545c0e806bcdb1c36cd320724e)

I modified the if statement so that if the request does not match, the request is rejected.

Amit also published his code to the IBM community -  [https://community.ibm.com/community/user/integration/blogs/amit-kumar-singh/2024/11/05/apic-gateway-script-for-check-source-ips-and?CommunityKey=2106cca0-a9f9-45c6-9b28-01a28f4ce947](https://community.ibm.com/community/user/integration/blogs/amit-kumar-singh/2024/11/05/apic-gateway-script-for-check-source-ips-and?CommunityKey=2106cca0-a9f9-45c6-9b28-01a28f4ce947)
