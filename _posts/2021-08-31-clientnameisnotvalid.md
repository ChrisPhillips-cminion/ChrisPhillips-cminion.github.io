---
layout: post
date: 2021-08-31 00:13:00
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
`oc edit client -n cp4ba-ent-01  zenclient-cp4ba-ent-01` then remove `metadata.finalizer` and its children

4. Get a list of all the iam-config jobs
`oc get job -A | grep iam-config`

5. Delete these jobs

6. Delete the zen operator pod
`oc get po -n  ibm-common-services | grep ibm-zen-operator`
then
`oc delete po -n ibm-common-services ibm-zen-operator-7f99df767-4w8cq`

7. Have a coffee i.e. wait 5mins
