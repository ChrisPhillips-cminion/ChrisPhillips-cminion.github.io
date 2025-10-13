---
layout: post
date: 2025-10-12 08:00:00
categories: MQ
title: "MQ Get the last GET and PUT Datetime"
author: ["AlameluNagarajan","ChrisPhillips"]
draft: true
---

On of my customers was writing a script to detect when the last message was got from an MQ QUEUE. 

<!--more-->

```
DISPLAY DISPLAY QSTATUS(<queue name>)  TYPE(HANDLE)  LGETTIME LGETDATE LPUTTIME LPUTDATE CONNAME
```

The above runmqsc command  returns something similar to

```
DISPLAY QSTATUS(SOURCE.Q) TYPE(HANDLE) CONNAME
AMQ8450I: Display queue status details.
   QUEUE(SOURCE.Q)                         TYPE(HANDLE)
   LGETDATE(2025-10-10)                    LGETTIME(14.57.31)
   LPUTDATE(2025-10-10)                    LPUTTIME(14.57.01) 
   CONNAME(10.131.1.20)                
AMQ8450I: Display queue status details.
   QUEUE(SOURCE.Q)                         TYPE(HANDLE)
   LGETDATE(2025-10-10)                    LGETTIME(14.59.21)
   LPUTDATE(2025-10-10)                    LPUTTIME(14.37.10) 
   CONNAME(10.129.3.151)  
```

*In order for the LGETTIME LGETDATE LPUTTIME LPUTDATE you must have MONQ enabled for the QUEUE.*

The above shows you the date and time of the last GET and PUT. When there are no MQPUT and no MQGET the last PUT and last GET time will not help. In these scenarios we recommend monitoring LSTMSGTI as well.

The `conname` and channel name can  be put into the following runmqsc command. Please note that in the example above the CONNAME is an IP Address this is determined on how the QMGR is configured.

```
DISPLAY CHSTATUS(<channel name>) CONNAME(<conname>) LSTMSGDA LSTMSGTI
```

This returns the following.

```
DISPLAY CHSTATUS(TEST.CHAN) CONNAME(10.131.1.23) LSTMSGDA LSTMSGTI
AMQ8417I: Display Channel Status details.
   CHANNEL(TEST.CHAN)                      CHLTYPE(SVRCONN)
   CONNAME(10.131.1.23)                    CURRENT
   LSTMSGDA(2025-10-10)                    LSTMSGTI(14.57.01)
   STATUS(RUNNING)                         SUBSTATE(RECEIVE)
```

The `LSTMSGDA` and `LSTMSGTI` provide the date and time when the last MQI call was handled.

Thanks to the MQ Support team in putting this together