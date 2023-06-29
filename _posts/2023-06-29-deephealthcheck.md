---
layout: post
date: 2023-06-29 00:01:00
categories: APIConnect
title: "Deep Health check against the API Manager"
---


Deep health check of the API Manager

It is important for a load balancer to know if the application is running. Deep health checks are used to validate that not only webpages are running but also the underlying application is working.

<!--more-->

When running a deep health check against the API Manager I recommend you run it against the identify provider api.  This API does not require any security, but it does validate the database is working as are the pods running the application. The identity provider API returns the list of user registries that are available at login. This could be against the CMC or against the Provider Organization.

This is a sample for a deployment in CP4I.
`https://cpd-apiconnect.ocpendpoint/integration/apis/apiconnect/small/api/cloud/provider/identity-providers`

And for non CP4I installs
`https://platformapi.apic/api/cloud/admin/identity-providers`

Example response

```json
{
    "total_results": 2,
    "results": [
        {
            "name": "default-idp-2",
            "title": "API Manager User Registry",
            "default": false,
            "registry_type": "lur",
            "user_managed": true,
            "realm": "provider/default-idp-2"
        },
        {
            "name": "common-services",
            "title": "Common Services User Registry",
            "default": true,
            "registry_type": "oidc",
            "user_managed": false,
            "realm": "provider/common-services",
            "oidc_type": "standard"
        }
    ]
}
```
