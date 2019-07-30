---
layout: post
date: 2018-08-04  00:00:00
categories: APIConnect
title: 'ISTIO --- 404 when curling to confirming the app is running.'
---


So I spent a few hours this morning trying to get the ISTIO sample
running to see if i can rewrite some of my home micro sevices using
ISTIO.

```
curl -o /dev/null -s -w “%\n” http://$/productpage`
```

When i ran the above command i got a 404.

The GATEWAY\_URL that is generated from the commands listed on the page
were provided was incorrect.

If you do not have a Load Balancer run

```
kubectl get endpoints --all-namespaces | grep ingress
```

this returns

```
istio-system   istio-ingressgateway                    192.168.99.218:80,192.168.99.218:15030,192.168.99.218:15011 + 4 more...    40m
```

This will show you the IP and Port for the Gateway URL. in the example
above it is 192.168.99.218:80

As I have proven many times in the past I am terrible at reading
documentation so I am sure this is documented somewhere. However I am
sure I am not the only one.





By [Chris Phillips](https://medium.com/@cminion) on
[August 4, 2018](https://medium.com/p/9bf14c27e0a0).

[Canonical
link](https://medium.com/@cminion/istio-404-when-curling-to-confirming-the-app-is-running-9bf14c27e0a0)

Exported from [Medium](https://medium.com) on April 6, 2019.
