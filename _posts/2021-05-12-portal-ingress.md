---
layout: post
categories: APIConnect
date: 2021-05-12 00:15:00
title: Exposing a developer portal through a non default hostname.
---

When deploying API Connect with  a Developer portal you specify the end point that end users must to connect to the developer portal. However some deployments require a subset of the developer portal sites to be accesible from a different hostname.

<!--more-->
e.g.

Public API Catalog `developer.public.company.com`

B2B API Catalog    `developer.b2b.company.com`

If we assume that the developer portal was installed with the endpoint  `developer.public.company.com` we need to create an additional ingress entry to allow the routing to `developer.b2b.company.com`.

To do this we need to extract the original ingress and then modify. The sample code below will extract the relievent parts of the original ingress.

```bash
cat > ingressjson.json <<EOF
{
  "apiVersion": "route.openshift.io/v1",
  "kind": "Route",
  "metadata": {
    "name": "apis-minim-62c733a3-portal-web",
    "namespace": "apic-v10-0"
  }, "spec":
EOF
oc get route apis-minim-62c733a3-portal-web  -ojson  | jq  ".spec" >> ingressjson.json
cat >>ingressjson.json <<EOF
}
EOF
```

Then edit the json file that has been extracted update the following values

* metadata.name
* metadata.namespace
* spec.host

Then apply the `oc apply -f ingressjson.json`


Please Note: That as API Connect changes in the future this ingress file may need to be regenerated.
