---
layout: post
categories: APIConnect
date: 2022-09-07 00:14:00
title: Debugging ICSP (Image Content Source Policies)  
---

In Openshift 4 ICSPs (Image Content Source Policies) are used to redirect crio in the worker nodes to retrieve images from a location that is different then the name of the image.

<!--more-->



For example. There is an image publicly available at `imagestore.co/repo/exampleimage:latest` . I have many pods that will be using this across many worker nodes and so I want to store a copy locally to reduce latency to start my pods, or I want an air gap solution where the worker nodes cannot reach the internet.  I would create an ICSP that has an entry similar to below.

```yaml
apiVersion: operator.openshift.io/v1alpha1
kind: ImageContentSourcePolicy
metadata:
  name: ibm-cp-common-services
spec:
  repositoryDigestMirrors:
  - mirrors:
    - nexus.cminion.cf/repo
    source: imagestore.co/repo/
```


This configuration after it is applied will force the OCP crio and podman to redirect requests for `imagestore.co/repo/exampleimage:latest` and instead route to `nexus.cminion.cf/repo/exampleimage:latest` . Now providing the image is available at the new location this would be invisible to all deployments that reference the image.

**Please note after applying a ICSP or updating an existing one please allow a few minutes for it to be applied to all worker node**


## How to debug

I have spent a lot of time learning to configure ICSP and even though they are simple I have found it a challenge to configure them with a working docker registry. The best way to debug these I have found using the example above.
