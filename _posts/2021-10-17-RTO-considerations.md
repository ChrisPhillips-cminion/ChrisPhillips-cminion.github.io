---
layout: post
date: 2021-10-17 00:13:00
categories: General
title: "What needs to be considered when comng up with an RTO value time."
---
Recovery Time Objective and Recovery Point Objective are the most important requirements designing a HA or DR solution. High Availability (HA) will have a very low RTO and RPO, is automatic and usually achieved by having multiple systems running concurrently. Disaster Recovery is normally a longer manual process that often is triggered when a DataCenter has had a disaster,  In this Article I will go through the time line that needs to be considered for an RTO. I will not go into RPO details here but I will probably do a follow up article if it is requested.

<!--more-->

My rough steps for an RTO timeline.
**Scenario:**  The event assumes that the engineer does not need support from the vendor to fix the problem. The issue involves the engineer logging on to a system and doing a corrective action. E.e restart a VM or clearing a cache.

Stage | Description | Rough time since previous step
---|---|---
Problem Occurs | An outage event has occurred. | n/a
Problem Detected | Monitoring Solution has detected there was a problem or it was discovered by a user | Sub 5 Seconds
Alert Sent | Alert is sent to the Operations Team (L2) | Sub 1 Second
Alert Delivered | Alert is delivered to the Operations Team (L2) | Sub 15 Second
Decision: Callout |  The operations team (L2) decides if they need to call  an engineer (L3).  | Sub 10 Minutes
Engineer Allocated | Engineer contact details are retrieved or pager duty is used to contact the engineer | Sub 5 minutes
Engineer Alert Sent | Alert is sent to the Engineer (L3) | Sub 5 Second
Engineer Alert Delivered | Alert is delivered to the Engineer | Sub 5 minutes
Engineer Logs on to the network | This may be 2am. | Sub 30mins
Engineer Starts investigating | Engineer reads up on the ticket to understand where to look then jumps in | Sub 5mins
Engineer Determines Issue | Engineer understands the problem | Unable to predict
Engineer Calls out Management for approval (Optional) | In this scenario, in order for the change to be applied a manager must make a decision to fail over to DR or potentially impact another running component. | Sub 5 minutes
Management Alert Sent  (Optional)  | Alert is sent to the Manager | Sub 5 Second
Management Alert Delivered  (Optional)  | Alert is delivered to the Manager | Sub 5 minutes
Management Responds with  a decisions  (Optional)  | Manager provide a go no go answer to the Engineer | Sub 45 minutes
Engineer Fixes | Engineer Fixes the problem | Unable to predict.
Problem Fixed | outage is complete | n/a
---|---|---


When I talk to many clients they want a near zero RTO for a DR, but they often do not consider the actions that need to be taken beyond fixing the issue. If they measure DR as just the Engineer fixing the issue (which may be failing over to a second site) then we can usually achieve an RTO of sub an hour. Many of the steps cab be automated but often are not today. If a decision needs to be done this takes time, it is easy to say that a decision should only need to take five minutes but if the issue occurs at 2am the manager needs to wake up enough to make a thought out choice.
