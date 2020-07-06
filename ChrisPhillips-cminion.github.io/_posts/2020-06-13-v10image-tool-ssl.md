---
layout: post
date: 2020-6-13 00:02:00
categories: APIConnect
title: "APIConnect v10 unable to load images into registry because of  x509: certificate signed by unknown authority - Sellf signed certificate  "
---
When using the image-tool to load images into  your docker registry with a self signed certificate you will see the following error.
<!--more-->
```
❯❯❯ docker run --rm -v ~/.docker:/root/.docker --user 0 apiconnect-image-tool-10.0.0.0 upload  image-registry.openshift-image-registry.svc:5000  --debug

time="2020-06-13T10:47:26Z" level=info msg="uploading datapower-operator:1.0.0"
Getting image source signatures
time="2020-06-13T10:47:26Z" level=fatal msg="Error trying to reuse blob sha256:8d420cfaafb5a490c6fd332e4bd8d40e7dd051bd298ea9b96966025f939cdd71 at destination: error pinging docker registry image-registry.openshift-image-registry.svc:5000: Get https://image-registry.openshift-image-registry.svc:5000/v2/: x509: certificate signed by unknown authority"
Error: failed to upload /images-dir/datapower-operator/1.0.0: exit status 1
```

This is very simple to get around by simply adding the following parameter

```docker run --rm -v ~/.docker:/root/.docker --user 0 apiconnect-image-tool-10.0.0.0 upload  image-registry.openshift-image-registry.svc:5000  --debug --tls-verify false
```

Now sit back and wait as the images llload
