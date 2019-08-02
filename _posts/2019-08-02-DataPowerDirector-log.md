---
layout: post
date: 2019-08-02 01:00:00
categories: APIConnect
title: "Enabling GW Director Logs in DataPower"
draft: true
---

DataPower is the gateway/runtime for API Connect. In order for API Connect to synchronise APIs with the Gateway it uses a new DataPower piece of function called the Gateway Directory. When you deploy DataPower in Kubernetes with APIC UP a special log target is configured to store the gateway director logs. However on all other forms of DataPower this is needs to be enabled.


### Viewing the log

If you follow the steps below or you are using DataPower by APICUP the log file will be available in logtemp:///gwd-log


### Via the Cli

Log into the cli either directly via the console or ssh. Run the following commands.

```
co ; logging target gwd-log
      type file
      format text
      timestamp syslog
      size 50000
      local-file logtemp:///gwd-log
      event apic-gw-service debug
    exit
write memory
```


### Via the Web UI

1. Log into DataPower
![]("/images/2019-08-02-1.png")
2. Go to the domain with the API Connect Gateway Service

3. Go to the log target
![]("/images/2019-08-02-2.png")
4. Click Add

5. Set the following properties

* Name
* File Name - logtemp:///gwd-log
* Log Size - 50000
![]("/images/2019-08-02-3.png")
6. Click on Event Subscription
![]("/images/2019-08-02-4.png")
7. Click on Add

8. Select apic-gw-service with the debug level  (feel free to change the level if need be )

9. Press Done.

10. Press Apply
