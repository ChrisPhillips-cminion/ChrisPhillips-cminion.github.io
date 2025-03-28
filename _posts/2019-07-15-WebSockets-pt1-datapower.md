---
layout: post
date: 2019-07-15 01:00:00
categories: APIConnect
title: "WebSockets Part 1 - How to create a WebSocket Proxy in DataPower"
---

DataPower provides the facility to proxy WebSocket connections. This article is part one of a three part guide consisting of

* **Part 1 - How to create a WebSocket Proxy in DataPower**
* *Part 2* - How you can use API Connect to secure your implementation
* ~~Part 3 - How to socialise it via the Developer Portal giving your consumers the easiest~~
* _Part 3.1_  - How to socialise it via the Developer Portal giving your consumers the easiest way to use your websocket
<!--more-->

DataPower is used to protect and proxy http connections. As a WebSocket is an upgraded HTTP Connection it allows DataPower to offer similar protection and proxying facilities. When a WebSocket connection is established with DataPower, it applies the Multi-Protocol Gateway policies before the connection is upgraded. This means that additional logic can be applied to validate the request. In this series of articles we are going to be using API Connect for this.

*Note: if you are doing this on the same DataPower as API Connect I recommend this is run in its own dedicated domain. This solution should not be used in a Multi-Protocol Gateway that was created for the purpose of exposing APIs.*

### Prerequisites

* DataPower running the latest 2018.4.x firmware
* A dedicated application domain (not needed but it helps)
* A WebSocket server application
* A WebSocket client application

### Step by Step how to configure
1. Log into the Application Domain of the DataPower

![](/images/2019-07-04-WebSocketspt1-1.png)

2. Create a new Multi-Protocol Gateway

* Click on Multi-Protocol Gateway

![](/images/2019-07-04-WebSocketspt1-2.png)

* Click on add

![](/images/2019-07-04-WebSocketspt1-3.png)

* Set the `Multi-Protocol Gateway Name`
* Set the `Summary`
* Set the `Multi-Protocol Gateway Policy` to default
* Set the `Default Backside url`
  * Note that this should use http/https not wss/ws
  * Publicly available sites do not always upgrade requests on http or https.
  * If you do not have a WebSocket server application available use my one available here https://github.com/ChrisPhillips-cminion/PlayingWithWebSockets
* Set the `Response and Request Type` to `non-xml` 

![](/images/2019-07-04-WebSocketspt1-4.png)

3. Create a Front Side Handler

![](/images/2019-07-04-WebSocketspt1-5.png)

* Click on the + to the right of the Front Side Protocol
* Select HTTP Handler
  * HTTPs can be used but we will not cover configuring SSL in this article
![](/images/2019-07-04-WebSocketspt1-6.png)
* Set the `Name`
* Set the `Port`
* Select Get in `Allowed methods and versions`
* Set the `Allow WebSocket Upgrade` to on
* Set the `WebSocket Idle Timeout`
  * This value dictates how long an idle connection is open before it is terminated.
* Press Apply

4. Create an SSL Client Profile

![](/images/2019-07-04-WebSocketspt1-7.png)
* In the Multi-Protocol Gateway editor set the  SSL Client Type to Client Profile
* Click on the + to the right of the SSL Client Profile
  * For the sake of this demo we will configure without security in mind
![](/images/2019-07-04-WebSocketspt1-8.png)
* Set the `Name`
* Set `Validate server certificate` to off
  * This is not recommend for systems that are not prototypes


5. Press Apply.

### Testing

In order to test this you will need a WebSocket client and WebSocket server. I have a simple sample available here [https://github.com/ChrisPhillips-cminion/PlayingWithWebSockets](https://github.com/ChrisPhillips-cminion/PlayingWithWebSockets). The DataPower should be configured to point to the server NodeJS application. In your WebSocket Client set the url to be ws://\<DataPower Host\>:\<Port set in step 3\>
