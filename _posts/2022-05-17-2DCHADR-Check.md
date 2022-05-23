---
layout: post
categories: Kubernetes
date: 2022-04-4 00:14:00
title: Egress Block but allow intra cluster communication
---

I needed to produce a network policy that would allow egress to a single server (for back ups) but otherwise restricted all egress traffic to staying in the cluster.
<!--more-->

*egress traffic is traffic that starts in side the namespace*

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-external-egress
spec:
  egress:
  - to:
    - ipBlock:
        cidr: BACKUPSERVER/32
    - ipBlock:
        cidr: 172.21.0.0/16
    - ipBlock:
        cidr: 10.0.0.0/16
    - ipBlock:
        cidr: OCPExLB/32
  podSelector: {}
  policyTypes:
    - egress
```

* `BACKUPSERVER` was the SFTP server IP  that we were connecting to. This needs to be replaced with an IP Address
* `OCPExLB` was the IP of the external Load Balancer for OCP
* `172.21.0.0/16` is the service network
* `10.0.0.0/16` is the pod network network
