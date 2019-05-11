---
layout: post
date: 2018-12-26  00:00:00
categories: APIConnect
title: 'PiHole DNS Server running in Kubernetes --- Holiday Project Part 1'
---

PiHole DNS Server running in Kubernetes --- Holiday Project Part 1 
==================================================================

 
During my two weeks off of work I set myself the challenge to move as
much of my home network infrastructure to Kubernetes as possible. My...


 
 
 

------------------------------------------------------------------------


 
 
### PiHole DNS Server running in Kubernetes --- Holiday Project Part 1 

![](https://cdn-images-1.medium.com/max/800/1*EScuR6TCDCBgmvTrClI43g.png)

During my two weeks off of work I set myself the challenge to move as
much of my home network infrastructure to Kubernetes as possible. My
wife has often questioned "Why do you need any network Infrastructure,
other then a wifi point?". This article is **not** going to address that
question.

**What is PiHole (**<https://pi-hole.net/>)

![](https://cdn-images-1.medium.com/max/600/1*cvIMIEgd3RWs6aDQnW-VDA.png)

PiHole is an awesome DNS Server that includes an AdBlocker. I know
AdBlockers are controversial. I primarily use it to add custom domains
to my network and use the awesome web interface to review what sites my
kids go to. It was originally developed to run on the Raspberry Pi but
has since had a docker release.

**PiHole in Kubernetes**

At this point I am going to assume the readers her know about
Kubernetes. If you do not take a google and a browse.

![](https://cdn-images-1.medium.com/max/600/1*NLJsSiHaSmJE-XhemZo5Ew.png)

The Helm chart I have published here
<https://github.com/ChrisPhillips-cminion/pihole-helm> is a very basic
helm chart that deploys a single pod with a single pihole container.

In the values file, you can specify which domain the ingress should
listen to for the web interface. In addition you can specific any
additional dnsmaq entries. It includes a white list generated from the
scripts at <https://github.com/anudeepND/whitelist>.

I have only used it with Persistent storage but it should work without
it.





By [Chris Phillips](https://medium.com/@cminion) on
[December 26, 2018](https://medium.com/p/b0e3d01657f5).

[Canonical
link](https://medium.com/@cminion/pihole-dns-server-running-in-kubernetes-holiday-project-part-1-b0e3d01657f5)

Exported from [Medium](https://medium.com) on April 6, 2019.
