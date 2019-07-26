---
layout: post
date: 2019-07-05 01:00:00
categories: IBMCloud
title: "API Connect - Deploying a Gateway in a different cloud than the manager."
draft: hidden
---


---
It would be good to touch upon  flexibility in deploying to any cloud that they like

also personally i think its good to briefly list the pros and cons of each approach and then point them to white paper for digging deeper

Pros and Cons

----


*This article builds on top of the API Connect WhitePaper, this may be included in the WhitePaper in a future revision*

API Connect supports that each component running in its own cloud. The most common use of this is the Gateway Service (DataPower) running in AWS, IBM Cloud or GCP. This is commonly used when exposing a service or system of record already running in that cloud.

![](/images/2019-07-03-multicloud-1.png)
*MultiCloud Deployment Diagram*

In the diagram above we show a Gateway being deployed in AWS, GCP and IBM Cloud as well as in the on-premise environment. OpenShift can be running on any of these clouds and on-premise.  The latency between the gateway and the management server needs to be less then the ingress timeout in the environment hosting the Gateway. By default, this is 30seconds. (Note seconds not milliseconds).

Each box in the diagram above signifies a self-manages cluster of a component.

The diagrams below shows two potential routing options.

![](/images/2019-07-03-multicloud-2.png)
*Routing to a Gateway Running in a cloud – Kubernetes DataPower*


The Diagram above shows DataPower running in Kubernetes. The Management is running on premise in Open Shift and the gateway is in front of the System of Records and Services running in AWS. These may route tother SoR or Services on premise.

![](/images/2019-07-03-multicloud-3.png)
*Routing to a Gateway Running in a cloud - Linux DataPower*

The diagram above differs from Figure 6 Routing to a Gateway Running in a cloud – Kubernetes DataPower because DataPower is not deployed in Kubernetes but rather deployed in EC2.

The pros and cons between these solutions are discussed in the API Connect White paper in Section 8. [API Connect WhitePaper](https://www.ibm.com/downloads/cas/30YERA2R)
