---
layout: post
date: 2019-12-10 00:01:00
categories: APIConnect
title: "DataPower Quorums with two DataPowers"
---

Ways to handle the DataPower quorum when there is only enough Licenses for two DataPowers.


THIS HAS BEEN UPDATED - [https://chrisphillips-cminion.github.io/apiconnect/2022/10/19/APIC-DataPowerQuorum2Node0.html](https://chrisphillips-cminion.github.io/apiconnect/2022/10/19/APIC-DataPowerQuorum2Node0.html)
<!--more-->

This article assumes that there are only two DataPowers available to run as the  API Connect Gateway, whether v5c or api-gateway

There are two common solutions to this and I am regularly asked which is better. The answer is always it depends.

*~When a quorum is lost APIs can still be processed, however token management, publications of APIs and quota enforcement is not available.~*

In DataPower (only, not  other API Connect Components) a manual operation can be run re-enable the quorum with the available nodes.

### Three DataPower domains over two DataPower Instances.

![](/images/2node-1.png)

#### Availability Table

| Node 1     | Node 2     | Quorum Status |
| :------------- | :------------- |  :------------- |
| UP       | UP       | UP |
| UP       | DOWN       | UP |
| DOWN       | UP       | DOWN |
| DOWN       | DOWN       | DOWN |


This solution requires having two DataPower domains on Node 1 and one on Node 2. If Node 2 has an outage Node 1 continues with no problem. If Node 1 goes down then the quorum is lost.  If a split brain occurs (where network Communication between Node 2 and Node 1 occurs) Node 2 is considered out of quorum, but Node 1 can continue

### Two DataPower domains over  two DataPower Instances.


![](/images/2node-2.png)

#### Availability Table

| Node 1     | Node 2     | Quorum Status |
| :------------- | :------------- |  :------------- |
| UP       | UP       | UP |
| UP       | DOWN       | DOWN |
| DOWN       | UP       | DOWN |
| DOWN       | DOWN       | DOWN |

This solution allows for both DataPowers to be identical. In my opinion this makes it easier and has less risk for managing and governing the solution.  However if Node 1 or Node 2 or network connectivity between the nodes, the quorum is lost.

### Conclusion

Both of these solutions have their own merits. Three domains over two DataPowers provides slightly better availability however it is more complex to govern and manage because you cannot treat each DataPower equally.

If I was asked to make a decision with no requirements I would choose the second option as it is easier to manage and if the quorum is lost APIs can still be processed.

*TLDR: It depends on the requirements.*
