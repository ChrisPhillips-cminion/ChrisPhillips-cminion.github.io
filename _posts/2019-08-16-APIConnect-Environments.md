---
layout: post
date: 2019-08-16 01:00:00
categories: APIConnect
title: "Designing Environments for API Connect"
---

When designing your enterprise API Connect environment there are a number of different patterns that can be followed.  In the [API Connect WhitePaper](https://www.ibm.com/downloads/cas/30YERA2R) I present two common patterns. This article is a third pattern that I will propose to put into a future release of the WhitePaper.


<!--more-->

Today organizations want to decentralise their development of their APIs but keep single teams for Test and Operations.

This article assumes the following teams types exist:

| Team Type           | Description                                                                                                                                                                            |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Infrastructure      | One central team that is responsible for Infrastructure in all environments. This covers patches, configuration changes and new deployment configurations.                                 |
| Application Support | A series of teams that are responsible for the APIs running in Production. This includes deployment as well as reviewing logs when problems are reported.                              |
| Operations          | Overarching management level team that is responsible for delegating  when changes occur in Production, deligate performing changes in a controlled manner to the required team.      |
| Test                | A central team that is responsible for non-functional and cross team testing. This team may be split into different sub test teams covering testing areas. e.g. Perf, e2e, System Test |
| Development Team    | A series of teams producing APIs. Each Team will be aligned with either business lines in organization or functional requirements of organization.                                                                                    |

In order to do this effectively I advise that arleast four API Clouds are used.

| API Cloud      | Purpose |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Production     | Production                                                                                                                                                  |
| Non Production | Test environment that is used to validate APIs prior to going into production                                                                               |
| Infrastructure | Environment owned by the Infrastructure team. This is used to test upgrades and new configurations prior to rolling out to the other environments |
| Development            | Used by the development teams to build the APIs.                                                                                                            |

### Production

Production is the most important environment. In production each channel is represented as a catalog.

The operations team is responsible for approving all changes, and triggering the changes via Dev Ops. The Infrastructure team backs up the Operations team if any tasks need to be completed that are available by Dev Ops.

The only exception in a decentralised environment is the  Application Support team is responsible for approving changes into their spaces, similar to Operations. This includes the approval of publishing APIs.  Spaces allow teams to only have access to the APIs they are responsible for.

The table below shows the roles for production and which team is responsible for completing them.

| Task                                   | Owner                     |
| -------------------------------------- | ------------------------- |
| Approve Deployment into Production     | Application Support |
| Manages at Cloud Manager Level         | Operations with Infrastructure |
| Manages at Provider Organization Level | Operations with Infrastructure |
| Manages at Catalog Level               | Operations with Infrastructure |
| Manages at Space Level                 | Application Support |


 Drafts should not be accessible in Production. Any API Changes should be made in Development and follow the same route to live.

### Development

This environment is used by the different development teams to build APIs. Like all API Clouds the  Infrastructure team is responsible for managing and maintaining at the Cloud Manager level.  Each Development team is given a Provider Organization which they are responsible for managing. A developer will only have access to the Provider Organizations that they require access to.  The aim of this is to empower each development team to be responsible for adding new team members, and deciding when APIs can be deployed into Dev.

Once the development team have  completed an API it is committed to source control. The test team is alerted that the API is ready.

The development team can decide how to use channels to sub divide their development environment if needed.

| Task                                   | Owner                     |
| -------------------------------------- | ------------------------- |
| Approve Deployment into Dev            | Development Team          |
| Manages at Cloud Manager Level         | Infrastructure            |
| Manages at Provider Organization Level | Development Team          |
| Manages at Catalog Level               | Development Team          |
| Manages at Space Level                 | Not Needed               |

### Non Production

Each Test subteam has their own Provider Organization. Unlike Development where these are separated by business line these are separated by test area. Some examples are listed below. This list is not exhaustive and not all organizations will need all environments.

-   End to End
-   Consumer Test
-   Performance
-   System Test
-   Pre Production

If multiple instances of the same test area is required then a second provider organization is created. However these environments should be monitored to ensure they are being used. If environmnets are determined to no longer be needed they should be shutdown.

Each Non Production Provider Organization will have the same number of Catalogs as Production.

The Test Manager who owns their provider organization is responsible for on boarding team members. Team members may be spread between multiple Test Teams. In addition the Test Manager is responsible for approving the deployments of the APIs for testing, though this can be delegated to the test team.

 If issues are found during a testing phase the API is returned to development. If no issues are found the API continues to the next test environment in sequence.

| Task                                       | Owner                     |
| ------------------------------------------ | ------------------------- |
| Approve Deployment into a Test Environment | Test Team                 |
| Manages at Cloud Manager Level             | Infrastructure |
| Manages at Provider Organization Level     | Test Team                 |
| Manages at Catalog Level                   | Test Team                 |
| Manages at Space Level                     | Test Team                 |

 Drafts should not be accessible in Non Production. Any API Changes should be made in Development and follow the same route to live.

### Infrastructure

This API Cloud is there for the Infrastructure team to allow them to validate patches and configuration changes prior to rolling out to other environment.

Where possible this environment should have the same APIs as those in production. All aspects of this environment is used in the same way as production.

| Task                                   | Owner                     |
| -------------------------------------- | ------------------------- |
| Approve Deployment into Infrastructure | Infrastructure |
| Manages at Cloud Manager Level         | Infrastructure |
| Manages at Provider Organization Level | Infrastructure |
| Manages at Catalog Level               | Infrastructure |
| Manages at Space Level                 | Infrastructure |

 Drafts can  be accessible in Infrastructure but APIs should not be developed in this environment.
