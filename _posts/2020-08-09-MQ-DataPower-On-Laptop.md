---
layout: post
date: 2020-8-9 00:13:00
categories: Integration
title: "DataPower and MQ in Docker on your laptop"
---

A question I am regularly asked is how do I make DataPower and MQ run on my laptop together,  This guide gives you a step by step guide to get the basics up and running. **This is a skunkworks environment only**
<!--more-->


This guides assumes you already have docker installed
1. Download the MQ image
`docker pull ibmcom/mq`

2. Download DataPower
`docker pull ibmcom/datapower`


```
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
ibmcom/mq           latest              3545f67ca057        3 weeks ago         941MB
ibmcom/datapower    latest              47fea93fc319        2 months ago        1.48GB
```

3. start an MQ instance
```
docker run \
  --env LICENSE=accept \
  --env MQ_QMGR_NAME=QM1 \
  --publish 1414:1414 \
  --publish 9443:9443 \
  --detach \
  ibmcom/mq
```
*Taken from [https://github.com/ibm-messaging/mq-container/blob/master/docs/usage.md](https://github.com/ibm-messaging/mq-container/blob/master/docs/usage.md)*

3.b. start a datapower instance

```
docker run -it \
  -d \
  -v $PWD/config:/drouter/config \
  -v $PWD/local:/drouter/local \
  -e DATAPOWER_ACCEPT_LICENSE=true \
  -e DATAPOWER_INTERACTIVE=true \
  -e DATAPOWER_WORKER_THREADS=4 \
  -p 9090:9090 \
  ibmcom/datapower
```
*Taken from [https://hub.docker.com/r/ibmcom/datapower/](https://hub.docker.com/r/ibmcom/datapower/)*

4. Get the IP Address of hte MQ QMGR Container

`docker inspect <MQ Conteiner ID>`

Look for NetworkSettings.Networks.bridge.IPAddress

Make a note of this value

5. Disable Security on MQ * **NOT RECOMMEND OUTSIDE OF A SKUNKWORKS** *

Attack to the MQ container

`docker exec -ti <MQ Conteiner ID> bash`

Press enter twice

Run `runmqsc QM1` where QM1 is the name of the QMGR you set in the first step.

Paste in the following text
```
ALTER QMGR CHLAUTH(DISABLED) CONNAUTH('')  
ALTER CHANNEL(SYSTEM.DEF.SVRCONN) CHLTYPE(SVRCONN) MCAUSER('mqm')
REFRESH SECURITY
END
```
exit the mq container with
`exit`
6. Start the datapower admin console

`docker attach -ti <container id>`

e.g.
`docker attach -ti 314e3c45dcf9`

6.b. login with admin / admin

6.c. Run this command to enable the admin interface `co ; web-mgmt; admin-state enabled ; exit ;exit`

7. In a web brewswer go to https://127.0.0.1:9090 - *note HTTPS not HTTP*

7.b. login with admin / admin

8. create a new application domain.
*In datapower the appliance can be logically split (and physically on physical appliance) by domain. It is recommend that nothing other then  configuration is done in the default domain*

8.b. Search for `application domain` in the search box on the top left, then click on either of the Application Domain entries in the response

8.c. Click add
8.d. Give it a name and press Apply

9. Switch Domain - In the top right click on domain and select your new Domain
9.b. Click `Save changes and switch domains`


10. Search for MQ Queue Manager, click on the result and click on add.

11. Fill in the form
  Host - should be the IP you recorded earlier in 4
  Queue Manager Name - QM1 or as  you had set in 3

11.b. Press Apply


Congrats you have a DataPower and  MQ working on yourlaptop together.  This is only suitable for a skunkworks no more then that.
