---
layout: post
date: 2018-10-04  00:00:00
categories: APIConnect
title: 'APIConnect 2018 --- JUHU Stuck in CrashLoop during install'
---
<!--more-->

So a common problem that people seem to hit is that juhu seems to be
stuck in a crash loop

> apiconnect-juhu-\<id\> 0/1 CrashLoopBackOff 9

e.g.
<https://developer.ibm.com/answers/questions/470234/what-is-authentication-gateway-service-on-manager.html>

I have seen this happen because Kubernetes cannot copy the dns
configuration of the host. This occurs when the search term used in the
resolve.conf is not resolvable in the dns.

To fix this edit your`/etc/resolv.conf`
If the last line of the file is starts with `search` then comment out the line. Then delete the juhu pod
using

`kubectl delete pod apiconnect-juhu-<id>`

where `<id>` is the unique identified of
the pod.





By [Chris Phillips](https://medium.com/@cminion) on
[October 4, 2018](https://medium.com/p/1fc0eb292024).

[Canonical
link](https://medium.com/@cminion/apiconnect-2018-juhu-stuck-in-crashloop-during-install-1fc0eb292024)

Exported from [Medium](https://medium.com) on April 6, 2019.
