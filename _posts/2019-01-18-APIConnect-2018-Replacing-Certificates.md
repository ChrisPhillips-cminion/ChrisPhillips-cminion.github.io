---
layout: post
date: 2019-01-18  00:00:00
categories: APIConnect
title: 'APIConnect 2018: Replacing Certificates'
---

APIConnect 2018: Replacing Certificates
=======================================


This post assumes that you have already generated your certificates. If
you have not read this post...






------------------------------------------------------------------------




### APIConnect 2018: Replacing Certificates

This post assumes that you have already generated your certificates. If
you have not read this post
<https://medium.com/@cminion/custom-certs-in-api-connect-2018-c7aacecd7b44?source=user_profile---------8------------------>.







------------------------------------------------------------------------




Once you have created the certificate you need to run the following
command in your apicup project directory.

`apicup certs set <component> cloud-admin-ui <path to cert> <path to priv key> <path to ca/chain>`

e.g.

```
apicup certs set manager cloud-admi-ui ../cert.pem ../privkey.pem ../chain.pem
```

Once you have done that you need to run

`apicup subsys install manager`

and the certificates will be replaced.

To get a list of endpoints you can run

`apicup certs list <component>`





By [Chris Phillips](https://medium.com/@cminion) on
[January 18, 2019](https://medium.com/p/635c94c9b796).

[Canonical
link](https://medium.com/@cminion/apiconnect-2018-replacing-certificates-635c94c9b796)

Exported from [Medium](https://medium.com) on April 6, 2019.
