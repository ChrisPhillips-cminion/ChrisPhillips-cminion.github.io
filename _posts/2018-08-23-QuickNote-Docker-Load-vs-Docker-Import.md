---
layout: post
date: 2018-08-23  00:00:00
categories: APIConnect
title: 'QuickNote --- Docker Load vs Docker Import'
---

QuickNote --- Docker Load vs Docker Import
==========================================


As usual here is what I have been burnt with today.






------------------------------------------------------------------------




### QuickNote --- Docker Load vs Docker Import

As usual here is what I have been burnt with today.

Docker import and Docker load from a brief glance do the same thing,
however there is one big difference.

Docker import does not include the cmd to imitate the container. Docker
load does. I am unsure if there is anything else. This means that when
you run a docker image that has been imported you need to specify the
exec command. In kubernetes this will give you a CreateContainerError.

so instead of

`docker import package.tgz customname:customtag`

use

`docker load -i package.tgz`

and then retag the image if required.





By [Chris Phillips](https://medium.com/@cminion) on
[August 23, 2018](https://medium.com/p/ed1367b93721).

[Canonical
link](https://medium.com/@cminion/quicknote-docker-load-vs-docker-import-ed1367b93721)

Exported from [Medium](https://medium.com) on April 6, 2019.
