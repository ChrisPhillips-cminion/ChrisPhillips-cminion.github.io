---
layout: post
date: 2019-05-13  00:00:00
categories: Kubernetes
title: 'Setting vm.max_map_count on Kubernetes [Guest Post by Nick Cawood]'
---

*This is a guest post by Nick Cawood*

I've recently been installing API Connect 2018.4.1X on a Kubernetes Container Service (IKS - IBM Cloud Kubernetes Service). I can highly recommend this experience as many of the complexities of setting up Kubernetes are handled by the Container Service. However some of the unique settings that APIC needs are not covered implicitly (or access to the Nodes as root is required, which is not possible via IKS) so some work is needed to manage these:


As any experienced APIC 2018 installer knows this parameter needs to be set to 1048575 in order for all the components to install and then function as required.

To set this value on your [IKS] Cluster, create the following file (I call mine vm.max_map_count.yaml):


```
apiVersion: "extensions/v1beta1"
kind: "DaemonSet"
metadata:
 name: "navigator-elasticsearch-sysctl"
 namespace: "kube-system"
spec:
 template:
   metadata:
     labels:
       app: "navigator-elasticsearch-sysctl"
   spec:
     containers:
     - name: "apply-sysctl"
       image: "busybox:latest"
       resources:
         limits:
           cpu: "10m"
           memory: "8Mi"
         requests:
           cpu: "10m"
           memory: "8Mi"
       securityContext:
         privileged: true
       command:
       - "/bin/sh"
       - "-c"
       - |
         set -o errexit
         set -o xtrace
         while sysctl -w vm.max_map_count=1048575
         do
           sleep 60s
         done
```
Then logon to your master and run the following command to instantiate the new value:

`$ kubectl apply -f vm.max_map_count.yaml`

You see output something like this:

`daemonset.extensions/navigator-elasticsearch-sysctl configured`

Your [IKS] Cluster will now use 1048575 for this parameter!
