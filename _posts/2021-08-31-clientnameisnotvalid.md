---
layout: post
date: 2021-06-21 00:13:00
categories: CP4I
title: "CWOAU0061E: The OAuth service provider could not find the client because the client name is not valid. Contact your system administrator to resolve the problem."
---

Occasionally we delete the wrong object from the wrong OCP cluster, at least I did. This caused the error above to occur.

<!--more-->

If you are seeing the message above please firstly raise a PMR and follow the steps provided by IBM Support. What I am suggesting below may void supporting going forward and if done incorrectly may involve a complete reinstall.

1. Get a list of all the zen clients
`oc get client -A | grep zenclient`

2. Delete all the zen clients in each namespace.
`oc delete client -n cp4ba-ent-01  zenclient-cp4ba-ent-01 & `
This process will not complete so you may need to ctrl+c to escape.

3. In edit each zen client to remove the finalizer.
`oc edit client -n cp4ba-ent-01  zenclient-cp4ba-ent-01`

```
apiVersion: v1
items:
- apiVersion: oidc.security.ibm.com/v1
  kind: Client
  metadata:
    annotations:
      kubectl.kubernetes.io/last-applied-configuration: |
        {"apiVersion":"oidc.security.ibm.com/v1","kind":"Client","metadata":{"annotations":{},"name":"zenclient-amc","namespace":"amc","ownerReferences":[{"apiVersion":"apps/v1","kind":"Deployment","name":"usermgmt","uid":"f7c03a2b-e956-40c7-998f-a294c746837c"}]},"spec":{"oidcLibertyClient":{"post_logout_redirect_uris":["https://cpd-amc.swat-dev-01-464887bc828751e1b00625ca9211fbca-0000.eu-de.containers.appdomain.cloud/auth/doLogout"],"redirect_uris":["https://cpd-amc.swat-dev-01-464887bc828751e1b00625ca9211fbca-0000.eu-de.containers.appdomain.cloud/auth/login/oidc/callback"],"trusted_uri_prefixes":["https://cpd-amc.swat-dev-01-464887bc828751e1b00625ca9211fbca-0000.eu-de.containers.appdomain.cloud"]},"secret":"cpd-oidcclient-secret","zenInstanceId":"c9148e23-fe71-4331-8862-74d47929df54","zenProductNameUrl":"https://cpd-amc.swat-dev-01-464887bc828751e1b00625ca9211fbca-0000.eu-de.containers.appdomain.cloud/v1/preauth/config"}}
    creationTimestamp: "2021-08-31T09:39:09Z"
    finalizers:
    - fynalyzer.client.oidc.security.ibm.com
    generation: 2
    ...
```
 
becomes

```
apiVersion: v1
items:
- apiVersion: oidc.security.ibm.com/v1
  kind: Client
  metadata:
    annotations:
      kubectl.kubernetes.io/last-applied-configuration: |
        {"apiVersion":"oidc.security.ibm.com/v1","kind":"Client","metadata":{"annotations":{},"name":"zenclient-amc","namespace":"amc","ownerReferences":[{"apiVersion":"apps/v1","kind":"Deployment","name":"usermgmt","uid":"f7c03a2b-e956-40c7-998f-a294c746837c"}]},"spec":{"oidcLibertyClient":{"post_logout_redirect_uris":["https://cpd-amc.swat-dev-01-464887bc828751e1b00625ca9211fbca-0000.eu-de.containers.appdomain.cloud/auth/doLogout"],"redirect_uris":["https://cpd-amc.swat-dev-01-464887bc828751e1b00625ca9211fbca-0000.eu-de.containers.appdomain.cloud/auth/login/oidc/callback"],"trusted_uri_prefixes":["https://cpd-amc.swat-dev-01-464887bc828751e1b00625ca9211fbca-0000.eu-de.containers.appdomain.cloud"]},"secret":"cpd-oidcclient-secret","zenInstanceId":"c9148e23-fe71-4331-8862-74d47929df54","zenProductNameUrl":"https://cpd-amc.swat-dev-01-464887bc828751e1b00625ca9211fbca-0000.eu-de.containers.appdomain.cloud/v1/preauth/config"}}
    creationTimestamp: "2021-08-31T09:39:09Z"
    generation: 2
    ...
```




3. Get a list of all the iam-config jobs
`oc get job -A | grep iam-config`

4. Delete these jobs

5. Delete the zen operator pod
`oc get po -n  ibm-common-services | grep ibm-zen-operator`
then
`oc delete po -n ibm-common-services ibm-zen-operator-7f99df767-4w8cq`

6. Have a coffee i.e. wait 5mins
