---
layout: post
date: 2018-08-22  00:00:00
categories: APIConnect
title: 'ROOK CEPH --- Not provisioning in Kubernetes'
---

ROOK CEPH --- Not provisioning in Kubernetes 
============================================

 
We are deploying to a Kubernetes Environment using RookCeph.


 
 
 

------------------------------------------------------------------------


 
 
### ROOK CEPH --- Not provisioning in Kubernetes 

We are deploying to a Kubernetes Environment using RookCeph.

We hit an issue that the Rook Ceph operator was not requesting the block
storage to be provisioned. After some digging we found out that the
Operator was hitting an out of memory issues. We increased the memory
from 128MB to 512MB (1024MB limit). We then deleted the PVCs and Pods
for the deployment that failed. The Pods came back up with the PVC
requests and everything worked after (a very stressful) ten mins.

Simple fix but it was not clear what the issue was at first.





By [Chris Phillips](https://medium.com/@cminion) on
[August 22, 2018](https://medium.com/p/2b714124906).

[Canonical
link](https://medium.com/@cminion/rook-ceph-not-provisioning-in-kubernetes-2b714124906)

Exported from [Medium](https://medium.com) on April 6, 2019.
