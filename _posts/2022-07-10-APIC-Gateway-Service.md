---
layout: post
categories: APIConnect
date: 2022-07-05 00:14:00
title: How many Gateway Services do you need?
draft: true
---

A Gateway Service in IBM API Connect is the runtime that sits in side DataPower. DataPower in contains are designed to have a single gateway service, however in other form factors (RPM,VM,Physical) it is simple to add multiple gateway services to provide a logical separation. However just because you can have one gateway service or ten gateway services (No known technical limits) for a single provider org what is the correct way.

<!--more-->

The primary reason to separate Gateway Services is by environment, though for Business Lines, Geography and API Priority I have also discussed, usually in addition to environments.

## Differences between the configuration.

If one Gateway Services is enabled for multiple environments, any environment specific configuration needs to be applied in the API Manager and so advanced configuration cannot be done in the DataPower.  Two examples
- If a Gateway extension is required it would be applied in the same way to all environments. Therefore an extension cannot be tested in a lower environment before it is applied to high environments.
- If HSM integration is needed it would be applied in the same way to all environments

The points above may be acceptable for where Gateway Services are shared per Business Lines, Geographies and API Priorities, but usually they are not for environments.

## Isolation

Isolation comes in two forms,
- Logical where a single Cluster of Datapower have multiple domains running. (I would advise against this for containers given the container flexibility and complexity in configuring).
- Physical where there are different Datapower Clusters
In this article we are focusing on the logical isolation.

If there is an outage it would impact all the catalogs working with this Gateway Services. I.e. if there is a human error and domain is disabled or a network problem, all environments would stop working.  Human's make mistakes from time to time.

If there is a requirement for environment specific objects like MQ QM to be configured they need to be configured for all environments in the same Datapower domain. This means that they can be accessed from any environment.

If there is only a single Gateway Service then the network needs be configured so that all environments can communicate with the same Datapower interface and ports.

## Price / Maintenance overhead

Having multiple Gateway Services in a single Datapower Cluster does require more effort than having a single Gateway Services. More certificates have to be managed, more Datapower objects need to be configured initially.  

Each Gateway Services will have a marginal overhead cost in terms of CPU and Memory. In my experience this is not measurable today and a single Gateway Service gets the same through put as multiple gateway services in terms of application traffic.

## Summary

To Summarise the pros and cons separating out gateway services.
Pros
- No Single point of failure for multiple environments
- Gateway Extensions can be unique for multiple environments
- Networking can be as flexible as it needs to be.
-

Cons
- Simpler to configure and maintain
#
