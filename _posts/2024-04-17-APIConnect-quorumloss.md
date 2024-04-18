---
layout: post
date: 2024-04-17 00:01:00
categories: APIConnect
title: Losing Quorums (Updated!)
---
When each API Connect component looses quorums it changes how the components work.

This is an updated to my 2019 article, which could have been clearer.
<!--more-->

## API Connect  on VMWare

This section covers subsystems that are running on VMWARE.

**Gateway**
* *without **TMS*** No downtime for your APIs - Gateway will continue to serve traffic
* *without **TMS*** OAuthTokens can be validated
* *with **TMS*** OAuthTokens cannot be validated, and so there may be an interruption for traffic.
* Unable to publish APIs
* Unable to store or share revoked OAuth Refresh tokens and Rate Limiting
*Can be fixed by fixed by manually making a remaining node primary - see [https://chrisphillips-cminion.github.io/apiconnect/2019/11/19/APIConnect-DataPower-SwitchPrimary.html](https://chrisphillips-cminion.github.io/apiconnect/2019/11/19/APIConnect-DataPower-SwitchPrimary.html)*

**API Management**, **Portal** and  **Analytics**
* Outage occurs - This is due to API Connect subsystems in VMWare depending on Kubernetes inside of the VMs.

## API Connect in OCP/Kubernetes
*This article is not going to describe the situation when the the Kuberentes/OCP loses quorum*

**Gateway**  (Same as above)
* *without **TMS*** No downtime for your APIs - Gateway will continue to serve traffic
* *without **TMS*** OAuthTokens can be validated
* *with **TMS*** OAuthTokens cannot be validated, and so there may be an interruption for traffic.
* Unable to publish APIs
* Unable to store or share revoked OAuth Refresh tokens and Rate Limiting
* ~Can be fixed by fixed by manually making a remaining node primary~

**Manager**
* API Manager will continue to be accessible and usable
* API Manager will be unable to communicate with the other subsystems

**Analytics**
* Access to data stored in the shards on the available nodes
* Ingestion continues as normal though capacity will be reduced.

**Portal**
* Portal is not accessible
* Unable to Register external consumers
* Unable to Register new Applications
* Unable to modify existing assets
