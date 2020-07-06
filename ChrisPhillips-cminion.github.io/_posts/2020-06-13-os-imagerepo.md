---
layout: post
date: 2020-6-13 00:01:00
categories: OpenShift
title: "OpenShift enabling the Image Registry route and pushing image. "
---
When installing openshift 4.3+ there is no default route created for the image registry. Therefore we are unable to load in images from outside of the cluster.
<!--more-->

To enable the route you must run the following command.

```shell
oc patch configs.imageregistry.operator.openshift.io/cluster --type merge -p '{"spec":{"defaultRoute":true}}'
```

Then to load images in from outside of the cluster first we find the url of the route.
```shell
oc get route -n openshift-image-registry
```
returns
```
NAME             HOST/PORT                                                                                                               PATH      SERVICES         PORT      TERMINATION          WILDCARD
default-route    default-route-openshift-image-registry.apicv10-number-0000.eu-gb.containers.appdomain.cloud             image-registry   <all>     reencrypt            None
```

Then to log into docker we run the following
```
docker login <HOST from above> --username admin --password $(oc whoami -t)
```

The username can be anything. The password is a token that can be retrieve from the oc client.

Now tag your images
```
docker tag <image>:<tag> <HOST from above>/<namespace>/<image>:<tag>
```
And push them up
```
docker push <HOST from above>/<namespace>/<image>:<tag>
```
and you are good to go.
