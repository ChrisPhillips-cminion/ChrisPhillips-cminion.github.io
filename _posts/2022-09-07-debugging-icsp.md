---
layout: post
categories: openshift
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

I have spent a lot of time learning to configure ICSP and even though they are simple I have found it a challenge to configure them with a working docker registry. In order to simply validate if the ICSP is working I use the following steps.

1. oc debug no/<any worker node>
2. chroot /host
3. podman pull imagestore.co/repo/exampleimage:latest --log-level debug

This will print a load of text and fail if your local registry is secured. However ignore the errors at the end and scroll up to see if there are lines similar to

```
DEBU[0000] Loading registries configuration "/etc/containers/registries.conf"
DEBU[0000] Loading registries configuration "/etc/containers/registries.conf.d/000-shortnames.conf"
DEBU[0000] Loading registries configuration "/etc/containers/registries.conf.d/001-rhel-shortnames.conf"
DEBU[0000] Loading registries configuration "/etc/containers/registries.conf.d/002-rhel-shortnames-overrides.conf"
DEBU[0000] Attempting to pull candidate imagestore.co/repo/exampleimage:latest for imagestore.co/repo/exampleimage:latest
DEBU[0000] parsed reference into "[overlay@/var/lib/containers/storage+/var/run/containers/storage]imagestore.co/repo/exampleimage:latest"
Trying to pull imagestore.co/repo/exampleimage:latest...
DEBU[0000] Copying source image //imagestore.co/repo/exampleimage:latest to destination image [overlay@/var/lib/containers/storage+/var/run/containers/storage]imagestore.co/repo/exampleimage:latest
DEBU[0000] Trying to access "nexus.cminion.cf/repo/exampleimage:latest"
DEBU[0000] Trying to access "nexus.cminion.cf/repo/exampleimage:latest"
DEBU[0000] No credentials for nexus.cminion.cf found
DEBU[0000] Using registries.d directory /etc/containers/registries.d for sigstore configuration
DEBU[0000]  Using "default-docker" configuration        
DEBU[0000]  No signature storage configuration found for nexus.cminion.cf/repo/exampleimage:latest, using built-in default file:///var/lib/containers/sigstore
DEBU[0000] Looking for TLS certificates and private keys in /etc/docker/certs.d/nexus.cminion.cf
DEBU[0000] GET https://nexus.cminion.cf/v2/          
DEBU[0000] Ping https://nexus.cminion.cf/v2/ status 401
DEBU[0000] GET https://nexus.cminion.cf/v2/repo/exampleimage:latest
DEBU[0003] Content-Type from manifest GET is "application/json"
DEBU[0003] Accessing "nexus.cminion.cf/repo/exampleimage:latest" failed: Error reading manifest sha256:4d2a8f485c104f52d9a9ed98fb590ef3093259027cac0dbe5df6359db25e169b in nexus.cminion.cf/openshift-release-dev/ocp-v4.0-art-dev: manifest unknown: manifest unknown
....
```


Providing  you can see your local registry referenced towards the top of the log the ICSP is working correctly.
