---
layout: post
date: 2018-08-26  00:00:00
categories: APIConnect
title: 'How to: Use Rook Ceph with Kubernetes'
---
# How to: Use Rook Ceph with Kubernetes 

![](https://cdn-images-1.medium.com/max/600/1*gJQ7_l2Q03aX7cYeCYpiFQ.png)

I have spent the last few months getting CephFS to work. 99% of the
issues I had were user error. This article goes through the steps I used
to get it working.

What you will need,

-   [Kubernetes]
-   [An additional block device on each worker node (This can be only on
    certain worker nodes but I wont be covering it here)]
-   [git]

1.  [Check out the config files from my git. These are based off the
    instructions found here.
    <https://github.com/rook/rook.github.io/blob/master/docs/rook/master/block.md>]

```
git clone https://github.com/ChrisPhillips-cminion/kubernetes-rook-ceph
```







------------------------------------------------------------------------




2\. Before applying these configs run the following command on each node.

```
sudo sgdisk /dev/sdb1 -Z
```

Where sdb1 is the block device. If this hangs or fails do a **hard**
**reset** on the vm.
<https://medium.com/@cminion/quick-note-hard-reset-from-inside-the-linux-os-38a39812848b>

I have never had it return from a soft reset. I have not yet
investigated why.







------------------------------------------------------------------------




3\. Now apply the configuration you cloned from git.

```
kubectl apply -f <file name>
```

In 5--10 minutes the rook ceph will be up and running.







------------------------------------------------------------------------




4\. To determine if it is up, run the following command

```
kubectl get pvc --all-namespaces
```

Pvc-test will be bound when ceph is ready

Any issues please leave a comment below or raise an issue on the github.







------------------------------------------------------------------------




**Notes:**

-   [I have limited the CPU of each pod because at times it was eating
    all available CPU]
-   [I increased the memory of the ceph-operator pod as at times it
    would OOM.]
-   [Any reset of of any of these VMs now need to be hard
    resets.]
-   [I use the following hacky script to wait for pvc to be
    bound]

```
wc=0
```

```
while [ "$wc" -ne "1" ] ; do
```

```
  wc=$(kubectl get pvc | grep testpvc | grep Bound | wc -l )
```

```
  echo "sleeping ofr 10sec and trying again";
```

```
  kubectl get pvc
```

```
  sleep 10s
```

```
done
```

```
kubectl get pvc | grep testpvc | grep Bound
```





By [Chris Phillips](https://medium.com/@cminion) on
[August 26, 2018](https://medium.com/p/424a7a65173e).

[Canonical
link](https://medium.com/@cminion/how-to-use-rook-ceph-with-kubernetes-424a7a65173e)

Exported from [Medium](https://medium.com) on April 6, 2019.
