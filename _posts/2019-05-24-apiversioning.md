---
layout: post
date: 2019-05-24  00:00:00
categories: APIConnect
title: 'Four strategies to version APIs'
---
Originally published October 16, 2017



## Introduction
To manage and maintain any runtime system, you need a comprehensive versioning strategy. Without a clear strategy in place, how do you know which services and APIs are deployed and which version to use? This article highlights four strategies to help you manage API and service interfaces and implementations. It also presents the advantages and disadvantages for each strategy.

## The importance of versioning

When you define a versioning strategy, you focus on your requirements for the following two key areas:

* **Service or API interface**: When you change the interface, your users will need to change their code. Therefore, you must have a way to track and communicate to API and service consumers that they must change the version of their API or service interface.

* **Service or API implementation**: Each time that you change the implementation, your users should be aware of the change but might not have to change their code. However, your operations team will need to track which implementation a service or API uses.

## The minimum number of versions
Version strategies often have a clear system for getting new versions into production, but with little to no regard for how to retire a service. Consider an example of a platform that runs for a few years. It might have 30 services, each with 20 different versions. Without a plan to retire a service, the platform can end up with a total of 600 instances for just one service.

> For an API or service, keep no more than three of its most granular versions in production…

By coupling a sensible versioning strategy with your management system, such as IBM® API Connect, you can reduce the number of services. For an API or service, keep no more than three of its most granular versions in production for each combination of its higher-level versions. For example, if the versioning scheme is vX.Y, every X version can have only three Y values in production. For the scheme vX.X.Y, every X.X version can have only three Y values in production.

The three production versions at each level relate to the following states:

* **Live**: New consumers must use this version.
* **Superseded**: New consumers can subscribe to this version in extenuating circumstances.
* **Deprecated**: New consumers must not use this version.
The following table shows an example of a list with the maximum number of versions that are deployed with a one-dot strategy.

Maximum number of versions for a one-dot strategy


| Version | State      |
|---------|------------|
| V1.6    | Live       |
| V1.5    | Superseded |
| V1.3    | Deprecated |
| V2.5    | Live       |
| V2.4    | Superseded |
| V2.3    | Deprecated |
| V3.3    | Live       |
| V3.2    | Superseded |
| V3.1    | Deprecated |


In this example, the maximum number of deployments is the number of dots plus one to the power of three.

## Maximum number of deployments

| Version system | Maximum number of instances |
|----------------|-----------------------------|
| VX.Y           | 9                           |
| VX.X.Y         | 27                          |
| VX.X.X.Y       | 81                          |

When a new version is ready for release, it cannot go live until the following requirements are met:

* The existing *deprecated* version is retired.
* The *superseded* version becomes *deprecated*.
* The *live* version becomes *superseded*.

By using a good API management tool, such as API Connect, you can quickly determine which consumers are using each version. You must notify them when the service becomes deprecated or superseded. If they do not migrate to the latest version, they must understand that they risk breaking their application.

In the following strategies, each version has its own branch in the source code repository. These branches are called code streams.

## One-dot strategy
The one-dot strategy indicates the major version, followed by a dot, and then the minor version. This strategy has the following syntax:

`<Major>.<Minor>`

 Overview of a one-dot strategy


| Level | | Compatible with an earlier version | | New version of the implementation or interface | | Description |
|---|---|---|
| Major | | N | | Y | | Change of the interface that is not compatible with an earlier version |
| Minor | | Y |  | Y | | Non-breaking interface or implementation change |


This strategy has the following characteristics:

* It is simple.
* It offers tight coupling between the interface and the implementation.
* It has two code streams for you to manage and support.
* Potentially nine instances are deployed.
* It does not highlight significant redesigns.
* It is unclear when a minor change affects an interface or implementation change.

## Two-dot strategy
The two-dot strategy indicates the major version, a dot, the minor version, a dot, and then the fix number. This strategy has the following syntax:

`<Major>.<Minor>.<Fix>`

Overview of a two-dot strategy

| Level | Compatible with an earlier version | New implementation version | New interface version | Description |
|---|---|---|---|
| Major | N | Y | Y | Change of the interface that is not compatible with an earlier version |
| Minor | Y | Y | Y | Non-breaking interface change |
| Fix | Y | Y | N | No interface change |

This strategy has the following characteristics:

* At the Fix level, you can version a service without versioning the interface. All new deployments of the implementation * increment the version even if the interface is not changed.
* It couples the interface and implementation version without tightly binding them.
* It has three code streams for you to manage and support.
* Potentially 27 instances are deployed if three versions per version level are deployed.
* It does not highlight when major redesigns occur, such as when many existing interfaces are redesigned. If significant rework is required, it is not apparent.

## Three-dot strategy
The three-dot strategy is similar to the Version, Release, Modification, and Fixpack (VRMF) strategy that is used in IBM product versioning. This strategy indicates the release version, a dot, the major version, a dot, the minor version, a dot, and then the fix version. This strategy has the following syntax:

`<Release>.<Major>.<Minor>.<Fix>`

Overview of a three-dot strategy

| Level | Compatible with an earlier version | New implementation version | New interface version | Description |
|---|---|---|---|---|
| Release | N | Y | Y | Significant redesign of the release |
| Major | N | Y | Y | Change of the interface that is not compatible with an earlier version |
| Minor | Y | Y | Y | Non-breaking interface change |
| Fix | Y | Y | N | No interface change |

This strategy has the following characteristics:

* It offers more precision across versions.
* It can version a service without versioning the interface, which means you do not have to update any catalog or developer portals.
* It can couple the interface and implementation version without tightly binding them.
* It has four code streams to manage and support.
* Potentially 81 instances are deployed if three versions per version level are deployed.
* It highlights when major redesigns occur, such as when many existing interfaces are redesigned. If significant rework is required, it is not apparent.

## Decoupled strategy

The interface and implementation are versioned independently. In this strategy, both the interface and the implementation follow a one-dot strategy. However, they can follow a more complex strategy, such as a two-dot or three-dot strategy.

This strategy has the following characteristics:

* It has two code repositories with two streams in each repository.
* It hides the implementation version from the user.
* The implementation and interface have a complete disconnect.
* Developers and designers must align on the same strategy but not on the same version number movements.
* Developers and designers must agree on guidelines for how the interface and implementation version numbers move. For example, they might agree that implementations must always have the same major version number as their interface but that the minor versions can be different.
* Potentially nine instances of the interface and nine instances of the implementation are deployed if three versions per version level are deployed.
* It is more difficult to track because of the two distinct numbers.
* It is difficult to quickly determine which implementation that a particular interface is using.

## Summary of strategies

The following table compares the four strategies to help you make the best choice for your services and APIs.

Strategy comparison

| Characteristic | One-dot V0.0 | Two-dot V0.0.0 | Three-dot V0.0.0.0 | Decoupled (one dot) V0.0 V0.0 |
|---|---|---|---|---|
| Simple, clear, obvious | Yes | No | No | No |
| Couples the interface to the implementation | Tight | Loose | Loose | None |
| Number of streams to manage | 2 | 3 | 4 | 2 2 |
| Version number informs users of all changes to the interface and implementation | Yes | Yes | Yes | No (interface only) |
| Allows for automatic migration of changes that are compatible with an earlier version | Yes | Yes | Yes | Yes |
| Highlights when major redesigns occur | No | No | Yes | No |
| Maximum number of versions for a single service that is deployed in production across all version levels when:Each level has three instances. Changes that are compatible with an earlier version are not automatically migrated. | 9 | 27 | 81 | 9 9 |
| Maximum number of versions for a single service that is deployed in production across all version levels when: Each level has three instances. All changes that are compatible with an earlier version are automatically migrated. | 3 | 3 | 9 | 3 3 |

## Conclusion

In this article, you learned about the importance of versioning and four strategies to help you manage it. Many more strategies are possible that were not addressed in this article. Keep in mind that no strategy is a single perfect fit.
