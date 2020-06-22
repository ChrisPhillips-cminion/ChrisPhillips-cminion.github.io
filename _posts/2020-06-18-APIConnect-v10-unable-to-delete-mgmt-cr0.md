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

Then you can delete the namespace again `kubectl delete ns apic`
