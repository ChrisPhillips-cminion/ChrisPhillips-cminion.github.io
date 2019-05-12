---
layout: post
date: 2019-02-03  00:00:00
categories: APIConnect
title: 'Quick Note --- Egress Whitelisting in Kubernetes'
---
# Quick Note --- Egress Whitelisting in Kubernetes

I got bored flying back from Germany last week and so I tried to solve a
problem our test team were hitting. They needed to whitelist access to
the internet for all the pods of one application

I had wanted to play with K8s network policies for ages, finally I got
an excuse.

```
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: foo-deny-external-egress
spec:
  podSelector:
  policyTypes:
  - Egress
  egress:
  - to:
    - ipBlock:
      cidr: <IP to WhiteList>/32
    ports:
      - port: 443
        protocol: TCP
  - ports:
    - port: 53
      protocol: UDP
    - port: 53
      protocol: TCP
```





By [Chris Phillips](https://medium.com/@cminion) on
[February 3, 2019](https://medium.com/p/a8815f8afc22).

[Canonical
link](https://medium.com/@cminion/quick-note-egress-whitelisting-in-kubernetes-a8815f8afc22)

Exported from [Medium](https://medium.com) on April 6, 2019.
