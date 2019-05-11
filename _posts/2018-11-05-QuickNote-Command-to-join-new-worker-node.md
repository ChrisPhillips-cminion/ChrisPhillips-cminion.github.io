---
layout: post
date: 2018-11-05  00:00:00
categories: APIConnect
title: 'QuickNote: Command to join new worker node'
---

QuickNote: Command to join new worker node 
==========================================

 
When you want to add a new worker node to a k8s master just run the
command above on the master and it will give you the exact command to...


 
 
 

------------------------------------------------------------------------


 
 
### QuickNote: Command to join new worker node 

``` 
sudo kubeadm token create --print-join-command
```

When you want to add a new worker node to a k8s master just run the
command above on the master and it will give you the exact command to
run on the new worker.

Saves a LOT of hassle.





By [Chris Phillips](https://medium.com/@cminion) on
[November 5, 2018](https://medium.com/p/60d4bb86e5f4).

[Canonical
link](https://medium.com/@cminion/quicknote-command-to-join-new-worker-node-60d4bb86e5f4)

Exported from [Medium](https://medium.com) on April 6, 2019.
