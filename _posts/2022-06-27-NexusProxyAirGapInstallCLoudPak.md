---
layout: post
categories: CP4I
date: 2022-06-27 00:14:00
title: Installing IBM CloudPaks with a Nexus Proxy Docker Registry
draft: true
---


Nexus is a third party docker registry that allows users to configure it as a proxy. This means that when a request comes for an image it is downloaded directly and stored in nexus.  If you are not wanting to use nexus as a proxy you can follow the instructions here. [https://www.ibm.com/docs/es/cpfs?topic=plugin-bastion-host](https://www.ibm.com/docs/es/cpfs?topic=plugin-bastion-host)

<!--more-->

There are many advantages of using a proxy repository
- Each time an image is first requested it is downloaded from the internet and then each subsequent request can download it from the proxy registry.  
- Nexus offers tools to help check for vulnerabilities in the container images that stored in it.
- Only one system needs internet connectivity so when new nodes are added they do not need additional network rules enable to allow internet access.

This guide assumes you already have a nexus repository setup and have an open shift command line tool logged into your cluster.

## Install IBM-Pak
These steps are taken directly form [https://www.ibm.com/docs/es/cpfs?topic=plugin-bastion-host](https://www.ibm.com/docs/es/cpfs?topic=plugin-bastion-host)
1. Download `https://github.com/IBM/ibm-pak-plugin`
2. Move the file to your path, `mv oc-ibm_pak-linux-amd64 /usr/local/bin/oc-ibm_pak`
3. Check that `oc ibm-pak --help` returns a help page for the ibm-pak tool

## Set the environment variables for the product you wish to install

Set the following environmental variables
```
export CASE_NAME=ibm-cp-common-services
export CASE_VERSION=1.15.0
export TARGET_REGISTRY=nexus.phillips11.cf
```

Where CASE_NAME is the ibm product name and the CASE_VERSION is the version of the case file. These can be retrieved from the knowledge centre of the product you are trying to install. However for API Connect I usually take them from
[https://github.com/IBM/cloud-pak/tree/master/repo/case/](https://github.com/IBM/cloud-pak/tree/master/repo/case/)

## Generate the catalog sources and imagecontentsourcepolicy


The following commands will download the case details containing the information about the containers required then generate the imagecontentsourcepolicy and catalogsources required.

```
oc ibm-pak get $CASE_NAME --version $CASE_VERSION
oc ibm-pak generate mirror-manifests \
   $CASE_NAME \
   $TARGET_REGISTRY \
   --version $CASE_VERSION --generate-catalog-source
```

## Access the imagecontentsourcepolicy and catalogsource
Goto `cd ~/.ibm-pak/data/mirror/$CASE_NAME/$CASE_VERSION`

This will have the image content source policy and the catalog sources.
`image-content-source-policy.yaml` is applied to the OCP cluster and tells OCP to route the request for the listed registries to the local nexus registry.
`catalog-sources.yaml` contains the catalog source to be applied to OCP. This tell the catalog source  where to get to get the information for the operator hub.
There may be additional catalog sources if multiple catalog sources are required for the requested cases.

The catalog sources require two changes to them.
1. Remove the periods(.) from the `metadata.name`
2. Change the `spec.image` so that the local registry hostname (only) is replaced with `icr.io`


Apply the ImageContentSourcePolicy and wait twenty minutes. `oc apply -f image-content-source-policy.yaml` This will apply a number  changes to all nodes in the cluster and takes some time.  


Apply the catalog source(s) `oc apply -f catalog-sources.yaml` (note: please apply any other catalog sources that are generated). If the pods come up in the openshift-marketplace the install can begin. If they do not wait a few more minutes for the ImageContentSourcePolicy to apply and delete the pods.
