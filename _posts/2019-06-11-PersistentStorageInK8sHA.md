---
layout: post
date: 2019-06-10 10:00:00
categories: Kubernetes
title: 'Local Storage in Kubernetes, what are the risks regarding HA'
draft: true
---

Kubernetes is a container orchestration system. In side a kubernetes deployment there are multiple worker nodes. Each worker node runs one or more pods. For a introduction on pods please watch https://www.cncf.io/the-childrens-illustrated-guide-to-kubernetes/. The Kubernetes master determines which pods run on which worker nodes. If a worker node goes down kubernetes will bring the pods back up on a different worker node.

This is great if you do not need to persist state. However persisting state is hard. There are multiple methods of storing state today that fit into the following categories.

* Local Disk (Easiest)
* Multi Write at a time or FileSystem (More Flexible)
* Single Write at a time or Block Storage (More Performant)

Local Disk is by far the simplest to setup. However the Local Disk does not have any in built replication between the worker nodes.  This means that if a pod moves from one node to another it looses the attached persisted disk.
