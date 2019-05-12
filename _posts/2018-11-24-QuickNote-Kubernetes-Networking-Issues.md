---
layout: post
date: 2018-11-24  00:00:00
categories: Kubernetes

title: 'QuickNote: Kubernetes --- Networking Issues'
---
# QuickNote: Kubernetes --- Networking Issues

I am writing this because I assume I am not the only idiot in the world.
This has caused me to waste days of effort.

**Symptoms**

Pods on the worker nodes are unable to connec to the API Server

Timeouts connecting to 10.96.0.1

But pods on the master (that may have been untainted) work fine.

**Solution**

When you kubeadm init you specify the pod-network-cidr. Ensure that the
IP of your host/main network is not in the subnet that you refer.

i.e. If your network runs on 192.168.\*.\* use 10.0.0.0/16

If your network is on 10.0.\*.\* use 192.168.0.0/16

I forgot how subnets work and so I did not realise that 192.168.0.1 was
in the same subnet as 192.168.100.0/16. In short when you use a 16
subnet marker it means use anything in 192.168.\*.\* .

As my network was running on 192.168.1.\* the master was running ok on
192.168.0.\* but my worker was failing to communicate because it was
attempting to run on 192.168.1.\* thus well causing routing issues on my
box.

I hope this saves one other person some pain.





By [Chris Phillips](https://medium.com/@cminion) on
[November 24, 2018](https://medium.com/p/78f1e0d06e12).

[Canonical
link](https://medium.com/@cminion/quicknote-kubernetes-networking-issues-78f1e0d06e12)

Exported from [Medium](https://medium.com) on April 6, 2019.
