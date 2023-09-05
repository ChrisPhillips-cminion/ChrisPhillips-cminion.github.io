---
layout: post
date: 2023-09-04 01:00:00
categories: APIConnect
title: "API Connect v10 Replacing DataPower API Invocation SSL Certificate"
---

API Connect sends DataPower the certifcate it needs to present to end users. This needs to be replaced manually during certificate rotation.

<!--more-->

To change the certificate
1. Log into the cloud admin console
![](/images/ssl1.png)
2. Go to Manage Resources
![](/images/ssl2.png)
3. Go to TLS
4. Click on the Key Store entry that is used by your TLS Server Profile. If you do not know which one you can find your TLS Server Profile from the topology view. From inside the TLS Server Profile it will list the keystore.
![](/images/ssl3.png)
5. Scroll to the end of the page and upload a new private key and public key.
![](/images/ssl4.png)
6. Press Save

The SSL Certificate should now be updated for the API Invocation endpoint.
