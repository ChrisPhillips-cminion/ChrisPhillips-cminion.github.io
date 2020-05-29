---
layout: post
date: 2020-5-29 00:01:00
categories: APIConnect
title: "Vanity URLs in APIConnect v2018 and onwards"
---

API Connect v2018 has the ability to configure vanity Urls for the API Endpoints	. Vanity URLs allow the api developer/administrator to change how the endpoint is rendered in the API Connect Developer portal. This is useful if you wish to go via a CDN or there is a requirement for each catalog having a different URL subdomain.

<!--more-->

Instructions on how to configure this in API Connect can be found here  https://www.ibm.com/support/knowledgecenter/SSMNED_2018/com.ibm.apic.apionprem.doc/create_env.html (step 15)


However once you have configured this in API Connect though you ned to ensure that there is network connectivity on that address to the gateway endpoint.  If you have changed the hostname or domain one or two additional steps are required.
1. Configure the dns entry for the new hostname
2. Configure the ingress/routes (only if API Connect is working on v2018 with ingress/routes).


### Configure the dns entry for the new hostname
This is a simple standard task for your enterprises network team. They need to ensure that the DNS entry points to either the gateway (if not in k8s) or the ingress (if in k8s). This would be  a standard a-name or c-name record pointing to the IP / Hostname of the gateway or ingress.


### Configure the the ingress  / routes
In order to ensure we are routing on the new hostname in ingress to the correct pod in Kubernetes we need to create an ingress/routes entry.

Note: Routes is the open shift version of ingress, though opens shift often runs both routes and ingress in parallel.

#### Sample routes

```yaml
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  annotations:
    haproxy.router.openshift.io/balance: roundrobin
    ingress.kubernetes.io/ssl-redirect: "true"
  name: <vanityhost-ref-name>-gw
  namespace: apic02
spec:
  host: gw2.ibmcp4i.com
  port:
    targetPort: 9443
  tls:
    termination: passthrough
  to:
    kind: Service
    name: <GatewayService>
    weight: 100
  wildcardPolicy: None
```
