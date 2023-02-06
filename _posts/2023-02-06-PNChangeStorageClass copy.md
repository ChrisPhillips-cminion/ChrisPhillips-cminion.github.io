---
layout: post
date: 2023-02-06 00:01:00
categories: APIConnect
title: "Changing the storage class for a running Platform Navigator to allow"
---

The Platform Navigator has a requirement for two types of PVC. One of these is RWX and RWO. For many customers these can both be backed onto RWX but occasionally the RWX is not fast enough. One sympton of this is site unavailable error messages.

By default, the PN install puts both PVCs into RWX. This article will cover how to change the storage class and assumes you have a single running Platform Navigator already. 
<!--more-->
*Note: After this is done the user registry configuration will need to be reconfigured but the capabilities do not need to be reinstalled* 

1.	`oc edit cm ibm-zen-config` 
    *	Remove the ‘ownerReferences’ section
    *	Update `zenCoreMetaDbStorageClass` to your RWO storage class
2.	`oc get pn -oyaml > pn.yaml`
    *	Add the annotation ‘integration.ibm.com/reconcile-zen-configmap: "false"’ This will stop the CM changes above being over written. 
3.	`oc delete pn <pn name>`
    *	Delete the existing PN
4.	Wait 5 mins
5.	`oc get po, pvc`
    *	Check the PVC and Pods are gone
6.	`oc get po -n ibm-common-services`
    *	Check there are no pods in the terminating state
7.	`oc apply -f pn.yaml`
    *	Creates the new PN
    *	This will take 15-45mins to complete

The steps above were taken from a slightly different use-case documented https://www.ibm.com/docs/en/cloud-paks/cp-integration/2022.2?topic=ui-deploying-platform-rwo-storage#configmap

