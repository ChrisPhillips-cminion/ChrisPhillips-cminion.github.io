---
layout: post
date: 2025-10-13 08:00:00
categories: MQ
title: "MQ Get the last GET and PUT Datetime"
author: ["AlameluNagarajan","ChrisPhillips"]
---

On of my customers was writing a script to detect when the last message was got from an MQ QUEUE. 

<!--more-->

```
DISPLAY DISPLAY QSTATUS(<queue name>)  TYPE(QUEUE)  LGETTIME LGETDATE LPUTTIME LPUTDATE 
```

The above runmqsc command  returns something similar to

```
DISPLAY QSTATUS(SOURCE.Q) TYPE(QUEUE)  
AMQ8450I: Display queue status details.
   QUEUE(SOURCE.Q)                         TYPE(QUEUE)
   CURDEPTH(0)                             LGETDATE(2025-10-10)
   LGETTIME(14.57.31)                      LPUTDATE(2025-10-10)
   LPUTTIME(14.57.01)             
```
*In order for the `LGETTIME` `LGETDATE` `LPUTTIME` `LPUTDATE` you must have `MONQ` enabled for the QUEUE.*

The above shows you the date and time of the last GET and PUT. Some times, last put and get times alone might not help, in these scenarios we recommend monitoring `LSTMSGTI` as well.

To get  `LSTMSGTI` first we need to extract the `CONNAME` with the following command.
```
DISPLAY DISPLAY QSTATUS(<queue name>)  TYPE(HANDLE)  CONNAME
```


The above runmqsc command  returns something similar to

```
DISPLAY QSTATUS(SOURCE.Q) TYPE(HANDLE) CONNAME
AMQ8450I: Display queue status details.
   QUEUE(SOURCE.Q)                         TYPE(HANDLE)
   CONNAME(10.131.1.20)                
AMQ8450I: Display queue status details.
   QUEUE(SOURCE.Q)                         TYPE(HANDLE)
   CONNAME(10.129.3.151)  
```


The `CONNAME` and channel name can  be put into the following runmqsc command. Please note that in the example above the `CONNAME` is an IP Address this is determined on how the QMGR is configured.

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

*In order for the `LSTMSGDA` and `LSTMSGTI` to be available  `MONCHL` must be enabled*

The `LSTMSGDA` and `LSTMSGTI` provide the date and time when the last MQI call was handled.

To identify if messages are not retrieved from the queue, if there is difference between `LGETTIME` and `LPUTTIME` and if `LPUTTIME` is recent and `LGETTIME` is very older, this indicates there are no getters.
 
However if two client applications are serving a single queue, if one of the application is able to get the message, then `LGETTIME` and `LPUTTIME` could be latest. In such cases `LSTMSGTI` will help to determine which one of the application is not able to pick the message.
