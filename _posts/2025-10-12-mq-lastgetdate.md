---
layout: post
date: 2025-10-12 08:00:00
categories: MQ
title: "MQ Get the last GET Date"
draft: true
---

On of my customers was writing a script to detect when the last message was got from an MQ QUEUE. 

<!--more-->

```
DISPLAY DISPLAY QSTATUS(<queue name>)  TYPE(HANDLE) CONNAME
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

The above shows just the connames that are connected to a queue.

The `conname` and channel name can then be put into the following runmqsc command

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

The `LSTMSGDA` and `LSTMSGTI` provide the date and time for the last GET from the queue. 

Thanks to the MQ Support team in putting this together