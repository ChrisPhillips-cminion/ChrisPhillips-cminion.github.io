---
layout: post
date: 2019-06-20 01:00:00
categories: Misc
title: "101 Rules for Deploying with Dev Ops"
---

Deployment automation is at the heart of DevOps. The purpose of this article is to explain some ground rules that must be considered to start any DevOps journey. I have seen a number of clients run into issues because they did not properly plan or consider how DevOps could be best used for their business.
<!--more-->
## Rule No. 001
### The right number of  Environments

What is the right number of environments? The answer is 42 (HG2G Reference). There is no perfect answer to this question. Some enterprises want two environments (Prod and Non Prod), some what four (Dev, FT, NFT, Prod) and some want 10s. (Dev1, Dev2, Dev3, Dev4 ,.. FT1, FT2, ... NFT24, ...Prod ). Some customers want the ability to spin up environments when and where they need.

**Every single opinion can easily be justified for one or more perspectives.**

I recommend that everyone starts with four and then scales out to additional ones if need be. The four are

| **Environment** | **Purpose of the Environment**                                                                                                                                                                                                        |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Production      | Environment used for business operations. If this goes down the business is considered down.                                                                                                                                          |
| Non Production  | The e2e test environment. Where all functional integration tests place for Application/Service/Asset being built takes place. If there is no NFT environment this is also done here                                                                       |
| Sandbox         | The Infrastructure Team use this environment to test upgrades and infrastructure changes prior to rolling them out to the other environments. After testing the changes are applied to each environment in order, from Dev through to Production. |
| Dev             | Where developers develop their Application/Service/Asset.                                                                                                             |

If there are funds available and need I would also add the following Environments

| **Optional Environments** | **Purpose of the Environment**   |
| NFT                       | Where non functional testing takes place, 'ilitility testing, performance testing. etc                                                                                                                                                |
| Pre Production            | An environment identical to production, used by operations to validate that any changes will not impact production.   This should be a mirror of production.                                                                          |
| Consumer Test             | Used to allow consumers of this Application/Service/Asset service or api to validate their code works. This should be a mirror of production.                                                                                                       |

Dynamic environments are a contenous subject, because these are hard to track the usage of and may mean environments are stood up but never used, increasing running costs and overheads. In short, they are stood up but rarely taken down again.

**Continually critically analyse the need of each environments. If an environment is not being used determine why and if it is needed.**

## Rule No. 010
### Environment agnostic Scripts and Assets and a Single Point of Truth

The purpose of multiple environments is to ensure that all testing has been completed on representative environments before going into production.

One of the most common errors is caused by deployment scripts or assets being different between environments.

Each environment must use the same set of deployments script with different parameters. The deployment scripts will take in environmental parameters but will not have environment specific logic.  This greatly reduces the risk of failed deployments due to issues with the scripts.

Each environment would have its own set of variables that would be passed into the deployment script passing values for deployment targets, credentials and so on.

By architecting this carefully, new environments can easily be added or old ones removed with minimal maintenance to the deployment system

**There is no magical environmental design, just some that are not as bad as others**

## Rule No. 011
### Look up variables at deploy time not runtime

It is common to have a series of environmental variables set in the application the running application. In ACE (IIB) these are called User Defined Properties. However I have witnessed a number of customers looking-up these values from a remote system even though these values are static and only change once every few months. This lookup adds significant overhead both for the end-to-end latency and the increased number of objects that need to be managed and maintained.

These static application variables should be provided at deploy time not looked-up at runtime. This reduces not only the lookup latency but also reduces the activity on the service/api that provides the values.

The biggest risk is when these values change. If the values change but the change is not tested and propagated through all environments then there is significant risk that problems will occur. By ensuring  a value changing requires a redeployment you can be certain that this has gone through all environments before production.

**An environment variable change is as serious as code change and should have the same level of testing.**

## Rule No. 100
### Approvals prior to deployments

As with all deployments they should be carried out with minimal impact to the consumers of each environment. In production this is minimal impact to consumers, in test environments this is minimal impact to the test team.

Each environment should have its own dedicated gate keeper who determines which deployments happen and the scheduling of the deployment. These are people who are responsible for the purpose of the environment.

| **Environment**           | **Example Owner**   | **Example Owners motivation**                                                      |
| ------------------------- | ------------------- | ---------------------------------------------------------------------------------- |
| Production                | Operations          | - Environment cannot go down.                                                      |
|                           |                     | - Rather not deploy than deploy with risk                                          |
| Non Production            | Test Manager        | - Everything must go through the same testing process                              |
|                           |                     | - Nothing leaves test until it is signed off                                       |
|                           |                     | - Nothing can bypass test.                                                         |
| Sandbox                   | Infrastructure Team | - Infrastructure changes must not impact an environment.                           |
|                           |                     | - All environments, even development cannot have an unplanned outage                |
| Dev                       | Development Lead    | - Work is done in an environment that is representative to production.             |
| ------------------------- | ------------------- | ---------------------------------------------------------------------------------- |
| **Optional Environments** | **Example Owner**   | **Example Owners motivation**                                                      |
| ------------------------- | ------------------- | ---------------------------------------------------------------------------------- |
| NFT                       | Test Manager        | - Every application must be able to handle Disaster scenarios.                     |
|                           |                     | - The performance profile of each asset needs to be understood                     |
| Pre Production            | Operations          | - Everything must go via Pre Production                                            |
|                           |                     | - This environment must mirror Production not just be representative               |
|                           |                     | - Any issue seen in this environment suggests the same issue happens in production |
| Consumer Test             | Operations          | - Consumers must have confidence the downstream applications and apis work.       |
|                           |                     | - Any issue seen in this environment suggests the same issue happens in production |

**Each owner must decide what level of approval they require for any changes to their environment. The owner also carries the responsibility for the environment.**

## Rule No. 101
### DevOps Infrastructure not just Applications/Service/Assets aka Infrastructure as Code

It is common place to see DevOps being used to roll out Applications/Service/Assets, however the automation of deploying new environments or scaling / patching an existing one can be automated as well.

**By Automating the management of environments you create a simpler system to manage.**
<br><br>
<hr>
<br><br>
*Doesn't everyone count in binary?*
