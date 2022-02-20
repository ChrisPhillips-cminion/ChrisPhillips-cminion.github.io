---
layout: post
categories: OpenShift
date: 2022-02-10 00:14:00
title: Forcing a namespace to deploy to defined worker nodes
---

When using OCP licenses provided with IBM Cloud Pak for Integration it is recommended that CP4I is deployed to assigned worker nodes.

<!--more-->

In order to ensure that CP4I is is only asigned to certain worker nodes you must complete the following steps.

1. label the worker nodes
`oc label no <nodename> nodeuse=cp4i  `
2. Annotate the namespace
`oc annotate namespace <namespace> openshift.io/node-selector='nodeuse=cp4i'`

Now delete all pods in the namespaces and they will be recreated on the selected nodes. \

The second phase is to stop other namespaces deploying to the workeers designated as CP4I.

1. Label the other worker nodes
`oc label no <nodename> nodeuse-general=true`
2. Create a cluster wide node select
`oc edit scheduler cluster`
Set the `spec.defaultNodeSelector` to `nodeuse-general=true`

Delete the pods running on the incorrect worker nodes and everything should spin up on the right nodes.

As we have used a different label key for the general label, we can set worker nodes to be used for both general and cp4i.
