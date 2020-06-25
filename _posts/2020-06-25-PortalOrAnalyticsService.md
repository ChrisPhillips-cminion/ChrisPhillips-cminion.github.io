---
layout: post
date: 2020-6-25 00:12:00
categories: APIConnect
title: "APIConnect v10 - Error while registering portal or analytics service. "
---



<!--more-->
The following error while registering the Portal or Analytics service means a step was missed when installing API Connect.

```
: Error: An error occurred communicating with the https://ai.apic10-507231-1ea39f2197613090e80c4981ab6eab96-0002.eu-de.containers.appdomain.cloud at '[object Object]' (status: undefined, response: '<html>
2020-06-25T17:57:18.708237099Z  <head>400 No required SSL certificate was sent
```


The solution is to ensure your ingress has SSL Passthrough enabled. please go here for more information.
[https://www.ibm.com/support/knowledgecenter/en/SSMNED_v10/com.ibm.apic.install.doc/tapic_install_K8s_ingress_ctl_reqs.html](https://www.ibm.com/support/knowledgecenter/en/SSMNED_v10/com.ibm.apic.install.doc/tapic_install_K8s_ingress_ctl_reqs.html)
