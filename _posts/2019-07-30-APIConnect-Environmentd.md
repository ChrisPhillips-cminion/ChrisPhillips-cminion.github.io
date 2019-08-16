---
layout: post
date: 2019-07-29 01:00:00
categories: APIConnect
title: "Desiging Environments for API Connect"
draft: true
---

When designing your enterprise API Connect environment there are a number of different patterns that can be followed.  In the [API Connect WhitePaper](https://www.ibm.com/downloads/cas/30YERA2R) I present two common patterns. This article is a third pattern that I will propose to put into a future release of the WhitePaper.


<!--more-->

Today Organizations want to decentralise their development of their APIs but keep a single teams for Test and Operations.

This article assumes the following teams types exist.

| Team Type           | Description                                                                                                                                                                            |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Infrastructure      | One Central team that is responsible for all Infrastructure in all environments. This covers patches, config changes and new deployment configuration.                                 |
| Application Support | A series of teams that are responsible for the APIs running in Production. This includes deployment as well as reviewing logs when problems are reported.                              |
| Operations          | Overarching management Level team that is responsible for determinging when changes occur in Production, deligate performing changes in a controlled manner to the required team.      |
| Test                | A Central team that is responsible for Non Functional and Cross Team testing. This team may be split into different sub test teams covering testing areas. e.g. Perf, e2e, System Test |
| Develpoment Team    | A series of teams producing APIs. Each Team will be aligned with either a part of the organization.                                                                                    |

In order to to this effectively I advise that five API Clouds are used.

| API Cloud      | Purpose |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Production     | Production                                                                                                                                                  |
| Non Production | Test Environment that is used to validate APIs prior to going into production                                                                               |
| Infrastructure | Environment Owned by the Infrastructure Team. This is used to test upgrades and new configurations prior to roling out to the other environments |
| Dev            | Used by the development teams to build the APIs.                                                                                                            |

### Production

Production is the most important environment. In production each channel is represented as a Catalog.

The Operations Team is responsible for Approving all changes, and triggering the changes via Dev Ops. The Infrastructure team backs up the Operations team if any tasks need to be completed that are available by Dev Ops.

The only exception in a decentralised environment is the  Application Support team is resonsible approving changes into their spaces as Operations would.  Spaces allow teams to only have access to the APIs they are responsible for. The Proivder Organisation and the Cloud Manager would be owned and managed by the Infrastructure team.

The Application Support team are responsible for approving the deployment of APIs.

The table below shows the roles for production and which team is responsible for completing them.

| Task                                   | Owner                     |
| -------------------------------------- | ------------------------- |
| Approve Deployment into Production     | Application Support |
| Manages at Cloud Manager Level         | Infrastructure |
| Manages at Provider Organization Level | Infrastructure |
| Manages at Catalog Level               | Infrastructure |
| Manages at Space Level                 | Application Support |


 Drafts should not be accessible in Production. Any API Changes should be made in Development and follow the same route to live.

### Dev

This environment is used by the different development teams to build APIs. Like all API Clouds this Operation Infrastructure team is responsible for managing and maintaining at the Cloud Manager level.  Each Development team is given a Provider Organization which they are responsible for managing. A developer will only have access to the Provider Organizations that they require access to.  The aim of this is to empower each development team to be responsible for adding new team members, and deciding when APIs can be deployed into Dev.

Once the development team have  completed an API it is commited to source control. The test team is alerted that the API is ready.

The development team can decide how to use Channels to sub divide their development environment if needed.

| Task                                   | Owner                     |
| -------------------------------------- | ------------------------- |
| Approve Deployment into Dev            | Development Team          |
| Manages at Cloud Manager Level         | Infrastructure            |
| Manages at Provider Organization Level | Development Team          |
| Manages at Catalog Level               | Development Team          |
| Manages at Space Level                 | Not Needed               |

### Non Production

Each Test subteam has their own Provider Organization. Unlike Developent where these are seperated by business line these are seperated by test area. Some examples are listed below. This list is not exhuastive and not all organizations will need all environments.

-   End to End
-   Consumer Test
-   Performance
-   System Test
-   Pre Production

If multiple instances of the same test area is required then a second provier organization is created. However these environments should be monitored to ensure they are being used. If environmnets are determined to no longer be needed they should be shutdown.

Each Non Production Provider Org will have the same number of Catalogs as Production.

The Test Manager who owns their provider organization has responsible for on boarding Team Members. Team Members may be spread between multiple Test Teams. In addition the Test Manager is responsible for approving the deployments of the APIs for testing, though this can be delegated to the test team themself.

 If issues are found during a testing phase the API is returned to Development. If no issues are found the API continues to the next Test Environment in sequence.

| Task                                       | Owner                     |
| ------------------------------------------ | ------------------------- |
| Approve Deployment into a Test Environment | Test Team                 |
| Manages at Cloud Manager Level             | Infrastructure |
| Manages at Provider Organization Level     | Test Team                 |
| Manages at Catalog Level                   | Test Team                 |
| Manages at Space Level                     | Test Team                 |

 Drafts should not be accessible in Non Production. Any API Changes should be made in Development and follow the same route to live.

### Infrastructure

This API Cloud is there just for the Infrastructure team to allow them to validate patches and configuration changes prior to roling out to other enviornments.

Where possible this environment should have the same APIs as those in production. All aspects of this environment is used in the same way as production.

| Task                                   | Owner                     |
| -------------------------------------- | ------------------------- |
| Approve Deployment into Infrastructure | Infrastructure |
| Manages at Cloud Manager Level         | Infrastructure |
| Manages at Provider Organization Level | Infrastructure |
| Manages at Catalog Level               | Infrastructure |
| Manages at Space Level                 | Infrastructure |

 Drafts can  be accessible in Infrastructure but APIs should not be developed in this environment.
