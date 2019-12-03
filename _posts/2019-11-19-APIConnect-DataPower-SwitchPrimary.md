---
layout: post
date: 2019-11-19 00:02:00
categories: APIConnect
title: "API Connect - Switching the DataPower Peering Primary"
---

In the event that a DataPower quorum is lost the remaining DataPowers can be forced into a working quorum.

<!--more-->


**Note: Please note that a human must decide when this takes place so there is reduced risk of split brain**


1. SSH into thee DataPower pod that you wish to become master

2. login with admin  / admin  (or whatever the user has changed it to previously)

3. Run the following command
`sw apiconnect ; top ; co ; gateway-peering-switch-primary subs ; gateway-peering-switch-primary rate-limit ; gateway-peering-switch-primary gwd ; gateway-peering-switch-primary tms ;  exit ; exit`


*Update 4/12/2019* - Added the two additional peering tables that need to be made primary for 418.
