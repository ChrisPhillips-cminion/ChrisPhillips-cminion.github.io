---
layout: post
date: 2019-08-04 10:00:00
categories: Kubernetes
title: 'Local Storage in Kubernetes, what are the risks regarding HA'
draft: true
---

Kubernetes is a container orchestration system. In side a kubernetes deployment there are multiple worker nodes. Each worker node runs one or more pods. For a introduction on pods please watch https://www.cncf.io/the-childrens-illustrated-guide-to-kubernetes/. The Kubernetes master determines which pods run on which worker nodes. If a worker node goes down kubernetes will bring the pods back up on a different worker node.


<!--more-->
This is great if you do not need to persist state. However persisting state is hard. There are multiple methods of storing state today that fit into the following categories.

* Local Disk (Easiest)
* Multi Write at a time or FileSystem (More Flexible)
* Single Write at a time or Block Storage (More Performant)

### Local Disk

Local Disk Storage comes in two flavours Host Path and Local.

| Name | Description | Pro  | Con
| --- | --- | --- | --- |
| Local |   |   |   |
| Host Path |   |   |   |
|   |   |   |   |


### Multi
