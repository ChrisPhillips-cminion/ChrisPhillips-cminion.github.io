---
layout: post
date: 2021-10-17 00:13:00
categories: General
title: "What makes up an RTO?"
draft: true
---
Recovery Time Objective and Recovery Point Objective are the most important requirements designing a HA or DR solution. High Availability (HA) will have a very low RTO and RPO, is automatic and usually achieved by having multiple systems running concurrently. Disaster Recovery is normally a longer manual process that often is triggered when a DataCenter has had a disaster,  In this Article I will go through the time line that needs to be considered for an RTO. I will not go into RPO details here but I will probably do a follow up article if it is requested.

<!--more-->

My rough steps for an RTO timeline.

**Scenario:**  The event assumes that the engineer does not need support from the vendor to fix the problem. The issue involves the engineer logging on to a system and doing a corrective action.  E.e restart a VM or clearing a cache. The corrective change requires management approval as it may cause an interrupt to another service.

no | Stage | Description | Max Time between steps
---|---|---|---
1 | Problem Occurs | An outage event has occurred. | n/a
2 | Problem Detected | Monitoring Solution has detected there was a problem or it was discovered by a user | 30  Seconds
3 | Alert Sent | Alert is sent to the Operations Team (L2) | 1 second
4 | Alert Read | Alert is delivered to the Operations Team (L2) | 10 minutes
5 | Decision: Callout |  The operations team (L2) decides if they need to call  an engineer (L3).  | 10 Minutes
6 | Engineer Allocated | Engineer contact details are retrieved or pager duty is used to contact the engineer | 10 minutes
7 | Engineer Alert Sent | Alert is sent to the Engineer (L3) | 30 seconds
8 | Engineer Alert Read | Alert is Read by the Engineer | 30 minutes
9 | Engineer Logs on to the network | This may be 2am, so includes the engineer waking up. | 30 minutes
10 | Engineer Starts investigating | Engineer reviews the ticket | 5 minutes
11 | Engineer Determines Issue | Engineer understands the problem | *Unable to predict*
12 | Engineer Calls out Management for approval | In order to fix the existing issue a VM must be restarted that would impact another critical system for a control period of time.  | 5 minutes
13 | Management Alert Sent | Alert is sent to the Manager | 30 seconds
14 | Management Alert Read   | Alert is delivered to the Manager | 5 minutes
15 | Management Responds with a decisions  | Manager provide a go no go answer to the Engineer | 45 minutes
16 | Engineer Fixes | Engineer Fixes the problem | *Unable to predict*
17 | Problem Fixed | outage is complete | n/a
---|---|---|---


When I talk to many clients they want a near zero RTO for a DR, but they often do not consider the actions that need to be taken beyond fixing the issue. If they measure RTO as just the Engineer fixing the issue (which may be failing over to a second site) then we can usually achieve an RTO of sub an hour.

The decision to complete a DR should not be taken lightly and is usually a management decisions, sometimes going up to the CIO, this takes time. It is easy to say that a decision should only need to take five minutes but if the issue occurs at 2am the manager needs to wake up enough to make a thought out choice, and potentially wake his manager as well.
