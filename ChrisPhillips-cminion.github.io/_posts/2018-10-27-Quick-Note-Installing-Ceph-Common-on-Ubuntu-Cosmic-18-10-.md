---
layout: post
date: 2018-10-27  00:00:00
categories: APIConnect
title: 'Quick Note --- Installing Ceph Common on Ubuntu Cosmic (18.10)'
---
<!--more-->
If you are doing a fresh install of ubuntu cosmic you may come across a
package issue when install ceph-common.



![](https://cdn-images-1.medium.com/max/2560/1*XQi6sWSiU3HfBJlLXS2pOA.png)



This is because there a few hard dependencies that are required and
newer packages are proposed instead. I fixed it with the following
command.

`sudo apt install ceph-base ceph-common librbd1 librados2=12.2.4–0ubuntu1.1build1 python-cephfs libcephfs2=12.2.4–0ubuntu1.1build1`

The full text of the error is below

```
Reading package lists... Done
```

```
Building dependency tree
```

```
Reading state information... Done
```

```
Some packages could not be installed. This may mean that you have
```

```
requested an impossible situation or if you are using the unstable
```

```
distribution that some required packages have not yet been created
```

```
or been moved out of Incoming.
```

```
The following information may help to resolve the situation:
```

```
The following packages have unmet dependencies.
```

```
ceph-common : Depends: librbd1 (= 12.2.4-0ubuntu1.1build1) but it is not going to be installed
```

```
Depends: python-cephfs (= 12.2.4-0ubuntu1.1build1) but it is not going to be installed
```

```
Depends: python-rados (= 12.2.4-0ubuntu1.1build1) but it is not going to be installed
```

```
Depends: python-rbd (= 12.2.4-0ubuntu1.1build1) but it is not going to be installed
```

```
Depends: libradosstriper1 (>= 0.87) but it is not going to be installed
```

```
E: Unable to correct problems, you have held broken packages.
```





By [Chris Phillips](https://medium.com/@cminion) on
[October 27, 2018](https://medium.com/p/5b6901aa53c4).

[Canonical
link](https://medium.com/@cminion/quick-note-installing-ceph-common-on-ubuntu-cosmic-18-10-5b6901aa53c4)

Exported from [Medium](https://medium.com) on April 6, 2019.
