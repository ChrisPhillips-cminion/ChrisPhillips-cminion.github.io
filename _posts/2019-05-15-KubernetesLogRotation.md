---
layout: post
date: 2019-05-15  00:00:00
categories: Kubernetes
title: 'Enable Log Rotation in Kubernetes'
---

This week we had a number of issues with diagnosing a customer system because the kubernetes logs were rotating far too quickly.

We were unable to off box the logs to an external source for non tecbnical reasons.
<!--more-->
Kubernetes does not really handle logging. However docker does have the facility.


After a quick google this `https://success.docker.com/article/how-to-setup-log-rotation-post-installation` appeared.

For those that do not want to follow the link, it requires editing the Docker Config on each worker node `/etc/docker/daemon.json` and adding the following example into the json

```
{
"log-driver": "json-file",
"log-opts": {
    "max-size": "10m",
    "max-file": "3"
    }
}
```

After this you must restart the docker daemon
`systemctl restart docker`


I recommend applying this to the master nodes as well.

Please look at the original post here https://success.docker.com/article/how-to-setup-log-rotation-post-installation if you have any issues or need to understand the source of this information.
