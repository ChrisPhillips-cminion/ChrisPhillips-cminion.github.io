---
layout: post
date: 2019-07-15 01:00:00
categories: APIConnect
title: "WebSockets Part 3 - Socialising with API Connect"
---


#This article has been replaced with

DataPower provides the facility to proxy WebSocket connections. This article is part **three** of a three part guide consisting of

* *Part 1* - How to create a WebSocket Proxy in DataPower
* *Part 2* - How you can use API Connect to secure your implementation
* **~~Part 3 - How to socialise it via the Developer Portal giving your consumers the easiest~~**
* _Part 3.1_  - How to socialise it via the Developer Portal giving your consumers the easiest way to use your websocket
<!--more-->

*DataPower is used to protect and proxy http connections. As a WebSocket is an upgraded HTTP Connection it allows DataPower to offer similar protection and proxying facilities. When a WebSocket connection is established with DataPower before the connection is upgraded it applies the MultiProtocol Gateway Policies. This means that additional logic can be applied to validate the request. In this series of articles we are going to be using API Connect for this.*


In the previous parts we created a WebSocket proxy and secured it with an API Connect API.  In this article we will create an unenforced api that will contain the details for the WebSocket. The purpose of this is to advertise and provide the documentation for using the WebSocket along side your other APIs.  This API needs to be in the same product as the API built in part 2 in order to create the correct subscription.

This API is an unenforced API as explained in [https://chrisphillips-cminion.github.io/api/2019/06/07/ManagingApisNotRunningInApIC.html](https://chrisphillips-cminion.github.io/api/2019/06/07/ManagingApisNotRunningInApIC.html)




<button class="collapsible" id="yaml">Click here for the sample.</button>

<div class="content" id="yamldata" markdown="1">

```yaml

swagger: '2.0'
info:
  title: WebSocketDemo
  x-ibm-name: websocketdemo
  version: 1.0.0
  description: 'This is a WebSocket endpoint, please enter instructions for using it here.'
host: websocketendpoint.com
schemes:
  - http
  - https
  - ws
  - wss
basePath: /
x-ibm-configuration:
  type: rest
  phase: realized
  enforced: false
  testable: false
  application-authentication:
    certificate: false
  cors:
    enabled: false
paths:
  /:
    get:
      responses:
        '200':
          description: OK
          schema:
            type: string
      consumes: []
      produces: []

```

</div>
The key parts of this api are listed blow.

|---|---|---|
| | Value | Description |
|---|---|---|
| Host |  | Hostname of the websocket endpoint |
| Testable | false | This stops the test tool being displayed in the Developer Portal, this is because the test tool in the developer portal  is not set up to test websockets. |
| Enforced | false |  This enabled the API to just be logically presented in the Developer Portal |
| description |  |  Instructions how to use the WebSocket endpoint.|
|---|---|---|


Save the API and add it to the product that contains the API built in part 2.
