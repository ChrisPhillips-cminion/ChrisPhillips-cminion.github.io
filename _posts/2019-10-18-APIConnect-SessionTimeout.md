---
layout: post
date: 2019-10-17 00:01:00
categories: APIConnect
title: Changing the session timeout - API Connect  2018.4.1.x
author: ["AnkPatel"]
---
Using CLI toolkit
<!--more-->

Configuring the session timeout can be configured using the API Connect CLI. For the instructions below the following variables are substituted.


| Term | Definition | Default |
| --- | --- | --- |
| server | The API Connect Cloud Manager Hostname | |
| user | The API Connect Manager Username |  |
| password | The API Connect Manager User Password | |
| realm | API Connect Cloud Manager  | admin/default-idp-1 |

* Login cloud console using CLI Command Toolkit:

```
apic login -s <server> -r <realm> -u <user> -p <password>
```

* Create a text file titled `cloud-setting.yaml` with the contents listed below with the desired timeout.

```
access_token_expires_in: 28800
```

* After changing the file value, Run below command to update the modified file within same directory

```
apic cloud-settings:update cloud-setting.yaml --server <server>
```

* Proceed to logout

```
apic logout --server <server>
```
