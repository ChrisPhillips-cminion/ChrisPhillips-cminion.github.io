---
layout: post
date: 2019-07-08 01:00:00
categories: Kubernetes
title: "Openshift Console redirects to 127.0.0.1"
---
As I spent about an hour this issue I imagine I will not be the only one.

When trying to go to the openshift console on a remote machine with `http://<IP or hostname>:8443/console` it redirects  you to 127.0.0.1.

This happens if you have already completed one install without setting the public host. The easiest way to fix this is by following these steps.

**Warning** This will nuke your cluster

1. oc cluster down
2. delete the  openshift.local.clusterup directory `rm -rf  openshift.local.clusterup`
3. redeploy the cluster `ov cluster up --public-hostname=<IP or hostname>`
4. go to `http://<IP or hostname>:8443/console`

![](/images/2019-7-08-openshift.png)


In order to give full credit where it is due, I found the solution here
 [https://github.com/openshift/origin/issues/20726#issuecomment-467464588](https://github.com/openshift/origin/issues/20726#issuecomment-467464588)
