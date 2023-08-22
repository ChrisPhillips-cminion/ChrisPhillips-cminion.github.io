---
layout: post
date: 2023-08-21 00:01:00
categories: Openshift
title: "Useful Shell Commands - Update 1"
---

I take a bit of pride in my one-line shell commands. However, I always end up starting from first principles each time. This article will be a living document that will contain the useful commands that I use. These will start simple and get more complex towards the end.

<!--more-->
I have tried to grade each command with a risk as follows
- Non Destructive - Though it makes changes these changes are unlikely to cause problems. (Use at your own risk)
- Read Only - Does not make any changes

## 1. Watch the status of ZenService deployment
**Risk:**  Non Destructive
This command allows you to look at the status of the deployment of ZenService, and have it auto updated on the screen.

**Command:**
`watch "oc get zenservice -ojsonpath='{.items[0].status}'  | jq"`

**Response: this will auto refresh, Ctrl+c to end**

```json
{
  "Progress": "71%",
  "ProgressMessage": "Finished Role 0020-core",
  "conditions": [
    {
      "lastTransitionTime": "2023-04-03T09:28:42Z",
      "message": "Running reconciliation",
      "reason": "Running",
      "status": "True",
      "type": "Running"
    }
  ],
  "supportedOperandVersions": "4.8.2, 4.8.1, 4.8.0, 4.7.2, 4.7.1, 4.7.0, 4.5.7, 4.5.6, 4.5.5, 4.5.4, 4.5.3, 4.5.2, 4.5.1, 4.5.0, 4.4.4, 4.4.3, 4.4.2, 4.4.1, 4.4.0, 4.3.2, 4.3.1, 4.3.0, 4.2.0, 4.1.1, 4.1.0, 4.0.1, 4.0.0",
  "zenOperatorBuildNumber": "zen operator 1.8.2 build 46",
  "zenStatus": "InProgress"
}
```


## 2. Extract the admin password from ibm-common-services
**Risk:** Read Only
This command prints to the screen the admin password to login to the ZenService framework. This used by the CP4I integration platform.

**Command:**
`oc extract secret/platform-auth-idp-credentials      -n ibm-common-services --to=-`

**Response:**

```
chrisphillips@cminions-MacBook-Pro apic-2dcha % oc extract secret/platform-auth-idp-credentials      -n ibm-common-services --to=-
# admin_username
admin
# admin_password
TYcTHISISAPASSWORDMfoa3GOD5D0j
```
*The password above has been changed from the one shown on my test system.*


## 3. Find the OCP Console URL from a logged in CLI

**Command:**
`oc whoami --show-console`

**Response:**
```
https://console-openshift-console.mycluster-lon06-m3c-8x64-FAKEURL-0000.eu-gb.containers.appdomain.cloud
```
