---
layout: post
date: 2019-07-09 01:00:00
categories: Misc
title: "What are the risks with running a Quorum over two sites in a Active Active Pattern. "
draft: true
---

Nearly every customer in the world has two data centres for a given solution or region.  In order for Quorums to work they require one or three plus DataCenters. This article  covers the complexities of quorums running over two sites.

### 1. - Background, What is a Quorum

A Quorum is a computer science pattern for allowing HA across multiple nodes or sites while removing the risk of HA.


In a Quorum a node can only write to a disk (or elect a primary) if it can connect to more then 50% of the total nodes. This means that if a node looses connectivity with 50% or more other nodes it shuts itself down greatly reducing the risk of split brain.

The key advantage of Quorums is the reduction of data corruption caused by split brain.

### 1.1. - 3 Node Quorum Example

| Node1 | Node2 | Node3 | Quorum Intact |
| ----- | ----- | ------ | ------------- |
| Up    | Up    | Up     | Yes           |
| Down  | Up    | Up     | Yes           |
| Down  | Down  | Up     | No            |

If you loose two nodes the quorum is lost.

### 1.2. - 4 Node Quorum Example

| Node1 | Node2 | Node3 | Node4 | Quorum Intact |
| ----- | ----- | ------ | ------ | ------------- |
| Up    | Up    | Up     | Up     | Yes           |
| Down  | Up    | Up     | Up     | Yes           |
| Down  | Down  | Up     | Up     | No            |

If you loose two nodes we still have lost quorum because we do not have more then 50% of the nodes available. Quroums are recomended to have an odd number of nodes as from an availability standpoint an even number has the same availability as one less.


### 2. - Active Active

There are three common anti patterns for Active Active deployments.

### 2.1 - Majority of nodes on one site

For this example I will use two nodes on  site 1 and one on site 2. This is true regardless of the number of nodes as long as they are not equal and there are only two sites.


| ------ | --- | ------ | ------------- | --- |
| Site 1 | | Site 2 | Quorum Intact  | Comment |
| ------ | --- | ------ | ------------- | --- |
| Node1  | Node2 | Node3 |              |     |
| Up |  Up | Up  | Yes | Eveything running as normal |
| Up |  Up | Outage  | Yes | Site 2 Outage |
| Outage |  Outage | Up  | No | Site 1 Outage |


In the event of a site 2 outage everything continues as normal. However in the event of a site 1 outage the quorum is list and we are unable to write or elect a primary.

This means that site 1 is a single point of failure and this solution provide no availability advantage over a single site solution.

### 2.2 - Equal number of nodes on each site


For this example I will use one node on  site 1 and one on site 2. This is true regardless of the number of nodes as long as they are equal and there are only two sites.


| ------ | ------ | ------------- | --- |
| Site 1 |  Site 2 | Quorum Intact  | Comment |
| ------ | ------ | ------------- | --- |
| Node1 |  Node2   | | |
| Up |  Up  | Yes | Eveything running as normal |
| ------ | ------ | ------------- | -- |
|    Up | Outage  | No | Site 2 Outage |
| Outage | Up  | No | Site 1 Outage |
| ------ | ------ | ------------- |

Regardless if there is an outage on site one or site two the quorum is unavailable as there is no majority.

This means that there are two critical points of failure and this solution provide worse availability over a single site solution.


### 2.3 - Floating node

For this example I will use one static node on each site and a third node that is replicated between the sites. If the second site detects that the first site is having an outage then it will active the third node in site 2 thus creating a majority.

This example brings in the concept of site connectivity. The site connectivity is the network connection linking the sites together.

| ------ | | | ------ | |------------- | --- |
| Site 1 | | Site Connectivity| Site 2 | |Quorum Intact  | Comment |
| ------ | | | ------ | |------------- | --- |
| Node1 | Floating Node3  | | Node2  | Floating Node3 | | |
| Up |  Up |Up | Up  | Standby | Yes | Eveything running as normal |
| Up |  Up |Up | Outage  | Outage | Yes | Site 2 Outage |
| Outage |  Outage |Up | Up  | Up | No | Site 1 Outage |
| Up |  Up | Down | Up  | Up | Yes but data Corruption | Split Brain, Connectivity lost between sites. |

With this pattern if we loose either Site 1 or Site 2 then the Quorum will be intact, allowing for RPO RTO.

However if a site connectivity issue occurs, site 2 will believe that site 1 is having an outage. This means that the floating VM will be activated on site 2.  Once this is activated on site 2 There are two quorums both writing to disk. In the event of this scenario you have data corruption as the data sets will not trivially be mergable as there is a high chance of data conflicts.

This pattern carries the most risk.

### 3. - Conclusion

From section two of this article I have shown the significant risks of having,
* A majority on one site
* An equal numbers on each site
* Replicating a node between sites.

Given the solutions above I would recommend getting a third site. If this is not possible I would  evaluate Active Passive along side any above other solution. Though the cost is more, the risk is greatly reduced.
