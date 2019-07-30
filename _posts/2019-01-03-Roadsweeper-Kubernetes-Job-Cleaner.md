---
layout: post
date: 2019-01-03  00:00:00
categories: Kubernetes
title: 'Roadsweeper - Kubernetes Job Cleaner'
image: 'https://cdn-images-1.medium.com/max/800/1*fT5FZirLsGVFYmFQf-PHew.png'
---
## Holiday Project Part 3

*During my two weeks off of work I set myself the challenge to move as
much of my home network infrastructure to Kubernetes as possible. My
wife has often questioned "Why do you need any network Infrastructure,
other then a wifi point?". This article is still* ***not*** *going to
address that question.*

![](https://cdn-images-1.medium.com/max/800/1*fT5FZirLsGVFYmFQf-PHew.png)

One of my projects over xmas was to build my own build engine, im not
happy with it to publish it (yet) but one of the problems it did
highlight was that cronjobs did not nicely clean up completed jobs.

I created ROADSWEEPER to clean up completed pods and their jobs. This
itself is also a cronjob that runs every five minutes by default.

Written in nodejs with the kubernetes-client module, every five minutes
it runs a job that polls list of pods in the desired namespace and if
one is in the succeeded phase it deletes the pod and the corresponding
job.

The code is available here
<https://github.com/ChrisPhillips-cminion/roadsweeper>

The docker container is published here
<https://hub.docker.com/r/cminion/roadsweeper>





By [Chris Phillips](https://medium.com/@cminion) on
[January 3, 2019](https://medium.com/p/790a359dfee2).

[Canonical
link](https://medium.com/@cminion/roadsweeper-kubernetes-job-cleaner-790a359dfee2)

Exported from [Medium](https://medium.com) on April 6, 2019.
