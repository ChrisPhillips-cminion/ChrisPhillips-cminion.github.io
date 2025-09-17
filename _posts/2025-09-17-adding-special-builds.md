---
layout: post
date: 2025-09-17 09:00:00
categories: APIConnect
title: "Special Builds, how to us the internal OCP Image Registry"
author: ["ChrisPhillips","JPSchiller"]
draft: true
---

Occasionally you may need to be given a special build from IBM containing fixes for a KnownIssue before they are shipped in a fixpack or a build which can be used to gather additional diagnostics. This is something I try to avoid but if support require additional diagnostic information it is often required.

<!--more-->

Special Builds are not published via Fix Central or IBM Entitled Image Registy. You might need to download via a special link provided by IBM Support. Once you downloaded the image provided by IBM Support you need to push it
to an image registry of your choice e.g. the local Red Hat OpenShift Image Registry.  This can be done with skopeo, podman or docker. 

For more information on the OCP Image Registry - [https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/registry/registry-overview-1](https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/registry/registry-overview-1)

My example here is using podman

**1 Load the image into podman**

```
>> podman load -i datapower-10.6.0.6em5.tgz
Loaded image: localhost/ibmcom/datapower:10.6.0.6em5.377125em5-prod
```

**2 Confirm that the image is now loaded into podman with images**

```
>> podman images | grep "localhost/ibmcom/datapower"
localhost/ibmcom/datapower      10.6.0.6em5.377125em5-prod 111811108e14  6 weeks ago    1.84 GB
```

**3 Now we must retag the image with the target location. My OCP image registry is set to `default-route-openshift-image-registry.apps.myocp.com` and it is recommended that you include the namespace that you will deploy the image to.**

```
>> podman tag localhost/ibmcom/datapower:10.6.0.6em5.377125em5-prod  default-route-openshift-image-registry.apps.myocp.com/apic2/datapower:10.6.0.6em5.377125em5-prod
```

**4 Confirm that the image is now tagged**

```
>> podman images | grep default-route-openshift-image-registry.apps.myocp.com/apic2/datapower     
default-route-openshift-image-registry.apps.myocp.com/apic2/datapower   10.6.0.6em5.377125em5-prod 622841208e14  6 weeks ago    1.84 GB
```

**5 Now we must login to the target OCP image registry**

```
>> podman login -u cp -p $(oc whoami -t) default-route-openshift-image-registry.apps.myocp.com --tls-verify=false
Login Succeeded!
```

**6 Push the image**

```
>> podman push default-route-openshift-image-registry.apps.myocp.com/apic2/datapower:10.6.0.6em5.377125em5-prod --tls-verify=false
Getting image source signatures
Copying blob sha256:44a66aa7e9ca439a5f53b99099085ac3321daf9c8ad78b01058409b41ab2ac5d
Copying blob sha256:5f70bf18a086007016e948b04aed3b82103a36bea41755b6cddfaf10ace3c6ef
Copying blob sha256:482daf0f1e0048c15dbd11f60e78419d4e9263eb31e35e3b7dec8be16b008fe8
Copying blob sha256:7464a97bfce5ca6d97025912f0049cff78802611f13207367ddfc63cc170ddb7
Copying blob sha256:5f70bf18a086007016e948b04aed3b82103a36bea41755b6cddfaf10ace3c6ef
Copying blob sha256:550bd723ef7404832e77dbc1ce099cf9d4e0d3ca44fce781239fad8c0139a4e0
Copying blob sha256:23f2e6cfe66e3189e8ff13afded92d189975fedd0a6c55f1f62302d593ba1e20
Copying blob sha256:677970ec14eafa5b2297fb111dee37f6060cfb8adcfa7a207f759191302c8c4a
Copying blob sha256:5f70bf18a086007016e948b04aed3b82103a36bea41755b6cddfaf10ace3c6ef
Copying blob sha256:87684642d1d62c13d954609d9e2de12cadd383cbb21559518c717dbe527e8799
Copying blob sha256:5ce8ab65c169218fbeba4ad56661c11dd8d11a098d1b604e5117abf8c153a3a7
Copying blob sha256:5c89d233ce0e532441e6debc95e0a0a6e0a89787d69ac584dad2cacab9ddebc8
Copying blob sha256:28f7418781b612525b7932256f2cd8facbcc826999d106c8bb8a9777e38f1d39
Copying blob sha256:bba9139fe523a125951b7d6a28f81fa47bd26751a185738bbf5d3fb3ce65b57a
Writing manifest to image destination
```

**7 Validate that the image is in the registry**

```
>> oc get images | grep datapower
sha256:460b2d30b08cbae6799de29025106bf775f47671f4bcc829b09fceb58af4e427   image-registry.openshift-image-registry.svc:5000/apic2/datapower@sha256:460b2d30b08cbae6799de29025106bf775f47671f4bcc829b09fceb58af4e427
```

Make a note of the image url that starts `image-registry.openshift-image-registry.svc` as we will use this in the image location. Note: Its the service url of the image registry that we used before as the image will be pulled by the pod inside the cluster and not via the route and not the route that we tagged and pushed it to. 

**8 Get the name of the service account that has access to this image. Assuming the OCP permissions are default I would use the following command**

```
oc get secret | grep default-dockercfg
default-dockercfg-h7vwqq  kubernetes.io/dockercfg  1  168d
```

Make a note of the default-dockercfg secret name.

**9  Update the object that needs the new  image and add the service account to the imagePullSecrets**

In the example here are updating the gatewayservice object.

```
>> oc edit gatewawyservice small-gw
```
Make the following changes

```
spec:
  imagePullSecrets:
  - default-dockercfg-h7vwqq    
  - ibm-entitlement-key
```
and update the image

```
spec:
  image: image-registry.openshift-image-registry.svc:5000/apic2/datapower@sha256:460b2d30b08cbae6799de29025106bf775f47671f4bcc829b09fceb58af4e42
```

**10 Automatically the required objects will be updated, in this example the DataPower object and then the Stateful set will then be updated.**