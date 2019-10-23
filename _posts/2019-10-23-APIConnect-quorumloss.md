---
layout: post
date: 2019-10-23 00:01:00
categories: APIConnect
title: Loosing Quorums
---
When each API Connect component looses quorums it changes how the components work.,
<!--more-->
These notes state what is happens after a quorum is lost.

**Gateway**
* NO downtime for your APIs - Gateway will continue to serve traffic
* Unable to publish APIs
* Unable to store or share revoked OAuth Refresh tokens and Rate Limiting
~* Can be fixed by fixed by manually making a remaining node primary~

**Manager**
* API Manager will continue to serve traffic and will support all read transactions
* New creation of resources and deployment will not be possible e.g
	*  No API Publication
	*  Unable to create Applications

**Analytics**
* Continue to view analytics data that is already captured
* New ingestion data from the gateway would not be possible

**Portal**
* Portal is not accessible
* Unable to Register external consumers
* Unable to Register new Applications
