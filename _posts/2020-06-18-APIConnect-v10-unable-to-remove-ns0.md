---
layout: post
date: 2020-6-22 00:02:00
categories: APIConnect
title: "API Connect v10 - unable to delete namespace"
---

Deleting an entire namespace to clean up a failed installed is not an uncommon action.

<!--more-->

e.g.
`kubectl delete ns apic`


However if you have API Connect v10 deployed in that namespace the delete will stall because it is unable to delete the API Manager CR.

To validate this is the issue run

`kubectl get all -n <namespace>`
e.g.
`kubectl get mgmt -n apic`


The only object will be the api connect management cr.

This is the same error as [https://chrisphillips-cminion.github.io/apiconnect/2020/06/16/APIConnect-v10-unable-to-delete-mgmt-cr.html](https://chrisphillips-cminion.github.io/apiconnect/2020/06/16/APIConnect-v10-unable-to-delete-mgmt-cr.html)

and so it is the same solution


```
kubectl patch mgmt <mgmt-name>  -n <namespaec> -p '{"metadata":{"finalizers": []}}' --type=merge
```

Then you can delete the namespace  `kubectl delete ns apic`


Once you have deleted the namespace you must delete any stale webhooks in `MutatingWebhookConfiguration` and `ValidatingWebhookConfiguration`.

run `kubectl get ValidatingWebhookConfiguration,MutatingWebhookConfiguration`

```
NAME                                                                                                             CREATED AT
validatingwebhookconfiguration.admissionregistration.k8s.io/apic.datapowerservices.validator.datapower.ibm.com   2020-06-23T14:47:24Z
validatingwebhookconfiguration.admissionregistration.k8s.io/cert-manager-webhook                                 2020-06-19T08:32:16Z
validatingwebhookconfiguration.admissionregistration.k8s.io/managements.validator.subsystem.apiconnect.ibm.com   2020-06-23T14:47:28Z

NAME                                                                                                           CREATED AT
mutatingwebhookconfiguration.admissionregistration.k8s.io/apic.datapowerservices.defaulter.datapower.ibm.com   2020-06-23T14:47:24Z
mutatingwebhookconfiguration.admissionregistration.k8s.io/apicop-management-defaulter-ff1bff1e                 2020-06-23T14:47:28Z
mutatingwebhookconfiguration.admissionregistration.k8s.io/cert-manager-webhook                                 2020-06-23T14:43:59Z
```

Delete the entries for apic and datapower if they exist.

`kubectl delete mutatingwebhookconfiguration.admissionregistration.k8s.io/apic.datapowerservices.defaulter.datapower.ibm.com mutatingwebhookconfiguration.admissionregistration.k8s.io/apicop-management-defaulter-ff1bff1e   `


`kubectl delete validatingwebhookconfiguration.admissionregistration.k8s.io/apic.datapowerservices.validator.datapower.ibm.com  validatingwebhookconfiguration.admissionregistration.k8s.io/managements.validator.subsystem.apiconnect.ibm.com`


Your environment is now cleaned up
