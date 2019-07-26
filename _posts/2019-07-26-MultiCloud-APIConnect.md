---
layout: post
date: 2019-07-26 01:00:00
categories: IBMCloud
title: "API Connect - Deploying a Gateway in a different cloud than the manager."
draft: true
---



*This article builds on top of the API Connect WhitePaper, this may be included in the WhitePaper in a future revision*

API Connect supports that each component running in its own cloud. The most common use of this is the Gateway Service (DataPower) running in AWS, IBM Cloud, Azure, GCP or any cloud that provides a Kubernetes Runtime.



The common usecase for this is when exposing a service or system of record already deployed to that cloud.

![](/images/2019-07-03-multicloud-1.png)
*MultiCloud Deployment Diagram*

In the diagram above we show a Gateway being deployed in AWS, GCP and IBM Cloud as well as in the on-premise environment. OpenShift can be running on any of these clouds and on-premise.  The latency between the gateway and the management server needs to be less then the ingress timeout in the environment hosting the Gateway. By default, this is 30seconds. (Note seconds not milliseconds).

Each box in the diagram above signifies a self-manages cluster of a component.

Frequently we  are asked how do we efficiently route inside a particular cloud. Each cloud has its own selection of load balancers and networking services available.
The diagrams below shows two potential routing options in AWS. This can extrapolated for the other clouds.

## Routing to a Gateway Running in a cloud – Kubernetes DataPower
![](/images/2019-07-03-multicloud-2.png)



The Diagram above shows DataPower running in Kubernetes. The Management is running on premise in Open Shift and the gateway is in front of the System of Records and Services running in AWS. These may route tother SoR or Services on premise.

### Pros and Cons
**Pros**
* Supports Double Jeopardy i.e. can apply maintenance even during a site outage.
* Does not require three sites.
* Gateway and Analytics work in Active Active

**Cons**
* When the gateways are created the OAuth Secret must be the same. This is to allow both DataPowers to enforce all OAuth Tokens.
* Token Revocation is not synced between the gateways
* Quota Enforcement is not synced between the gateways
  *	Each Cluster will have its own Quota enforcements


## Routing to a Gateway Running in a cloud - Linux DataPower
![](/images/2019-07-03-multicloud-3.png)


The diagram above differs from Figure 6 Routing to a Gateway Running in a cloud – Kubernetes DataPower because DataPower is not deployed in Kubernetes but rather deployed in EC2.


### Pros and Cons
**Pros**
* Supports Double Jeopardy i.e. can apply maintenance even during a site outage.
* Does not require three sites.
* Gateway works in Active Active
* Gateway can share tokens and quota enforcement between sites while there is a quorum.

**Cons**
* Gateway cannot run in a Kubernetes cluster, thus does not benefit from kubernetes facilities.

The pros and cons between these solutions are discussed in the API Connect White paper in Section 8. [API Connect WhitePaper](https://www.ibm.com/downloads/cas/30YERA2R)
