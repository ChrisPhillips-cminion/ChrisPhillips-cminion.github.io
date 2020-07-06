---
layout: post
date: 2018-07-24  00:00:00
categories: APIConnect
title: |
    Deploying IBM DataPower into IBM BlueMix Kubernetes Service for API
    Connect v2018
---
<!--more-->

This article goes through the steps required to deploy IBM DataPower to
the IBM Bluemix Kubernetes Services.

### PreRequisites

· Bluemix Kubernetes Services Deployed

· Bluemix Container Registry Deployed in the same data centre as the
Kubernetes Service

· Helm installed locally

· apicup installed locally

· kubectl installed locally

### Upload the DataPower image to the Container Registry
> docker pull ibmcom/datapower:latest
> docker tag ibmcom/datapower:latest \<bluemix> server\>/\<namespace\>/ibmcom/datapower:latest
> bx cr login \#log into the container registry
> docker push \<bluemix server\>/\<namespace\>/ibmcom/datapower:latest

Where

\<namespace\> is the container registry namespace configured

\<bluemix server\> the server the container registry is running on

### Create the Configuration

Set up kubectl
> ibmcloud cs cluster-config \<kubernetes cluster\>

Where

\<kubernetes cluster\> is the name of your cluster

Run the export command returned

If you are not running in the default namespace you must run the
following command
> kubectl get secret bluemix-default-secret-regional -o yaml \| sed> 's/default/\<kube namespace\>/g'

Run the following commands
> helm init
> apicup init dpIBMBlueMix
> cd dpIBMBlueMix
> apicup subsys create gw gateway --- k8s ;
> apicup endpoints set gw gateway> [gw.company.com](http://gw.company.com/)>; \#ensure this is regsitered in your dns> server pointing tothe worker node
> apicup endpoints set gw gateway-director> [gwd.company.com](http://gw.company.com/) \#ensure this is regsitered in your dns> server pointing tothe worker node
> apicup subsys set gw namespace "\<kube namespace\>" ;
> apicup subsys set gw max-cpu 2 ;
> apicup subsys set gw max-memory-gb 4 ;
> apicup subsys set gw replica-count 1 ;
> apicup subsys set gw image-repository \<bluemix> server\>/\<namespace\>/ibmcom/datapower\> apicup subsys set gw image-tag "latest"
> apicup subsys set gw registry-secret bluemix-\<kube> namespace\>-secret-regional
> apicup subsys set gw mode demo
> apicup subsys install gw

Where

\<namespace\> is the container registry namespace configured

\<bluemix server\> the server the container registry is running on

\<kube namespace\> the kubernetes namespace

[gw.company.com](http://gw.company.com/) is the API Endpoint Base

[gwd.company.com](http://gw.company.com/) is the Gateway Service endpoint

### Configure the DNS Server

run the following command
> ibmcloud cs cluster-get \<kubernetes cluster\> \| grep Subdomain

Where

\<kubernetes cluster\> is the name of your cluster

in the DNS Server create an alias between the two URLs in the previous
section and the result of the command above.

### Modify Ingress
> kubectl get ing

edit the the ingress file for the entries with dynamic-gateway-service
in the name
> kubectl edit ing \<release\>-dynamic-gateway-service -o yaml

and
> kubectl edit ing \<release\>-dynamic-gateway-service-gw -o yaml

Add the following lines to the metadata.annotations

![](https://cdn-images-1.medium.com/max/800/1*aYAw8WftlhkifzABKv3rKw.png)

### Conclusion

The datapower is now ready to be registered in the Cloud Manager of your
APIC 2018 stack.





By [Chris Phillips](https://medium.com/@cminion) on
[July 24, 2018](https://medium.com/p/7a63214ff399).

[Canonical
link](https://medium.com/@cminion/deploying-ibm-datapower-into-ibm-bluemix-kubernetes-service-7a63214ff399)

Exported from [Medium](https://medium.com) on April 6, 2019.
