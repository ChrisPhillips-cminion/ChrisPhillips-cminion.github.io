---
layout: post
date: 2025-10-03 08:00:00
categories: APIConnect
title: "Replacing a member from Gateway Service"
author: ["ChrisPhillips","EricFan"]
---

When running an APIConnect Gateway outside of Kubernetes it is often required to replace a DataPower VM or physical appliance. These steps listed here what is suggested as the process for completing this.
<!--more-->

1) Make sure the DataPower that you are going to remove is not the Primary for each of the gateway peering objects. 
[https://www.ibm.com/docs/en/datapower-gateway/10.6.x?topic=mode-viewing-statistics-about-peers-in-peer-groups](https://www.ibm.com/docs/en/datapower-gateway/10.6.x?topic=mode-viewing-statistics-about-peers-in-peer-groups)
 
1b) If it is the primary, please switch another gateway peering member to the Primary:
[https://www.ibm.com/docs/en/datapower-gateway/10.6.x?topic=enforcement-switching-replica-primary](https://www.ibm.com/docs/en/datapower-gateway/10.6.x?topic=enforcement-switching-replica-primary)

2) In the DataPower that you are going to remove, disable the APIC domain.

3) In the remaining DataPower, for each of the gateway peering objects, remove the DataPower in the “peers” list that you are removing and add the new DataPower into the list.

4) In the two existing physical IDG, for each of the gateway peering objects, click Remove stale peers:
[https://www.ibm.com/docs/en/datapower-gateway/10.6.x?topic=mode-removing-stale-peers-from-peer-group](https://www.ibm.com/docs/en/datapower-gateway/10.6.x?topic=mode-removing-stale-peers-from-peer-group)

5) Start the replacement DataPower and configure the API Connect Gateway Service so that it has the same details as the exisiting ones.

6) In the new DataPower, for each of the gateway peering objects, add the existing DataPower into the "peers" list.

