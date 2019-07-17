---
layout: post
date: 2019-07-17 01:00:00
categories: APIConnect
title: "WebSockets Part 3.1  - Socialising with API Connect - a Better Way"
image: "/images/2019-7-16-websocket-pt3.1.2.png"
---

DataPower provides the facility to proxy WebSocket connections. This article is part **three** of a three part guide consisting of

* *Part 1* - How to create a WebSocket Proxy in DataPower
* *Part 2* - How you can use API Connect to secure your implementation
* ~~Part 3 - How to socialise it via the Developer Portal~~
* **_Part 3.1_  - How to socialise it via the Developer Portal giving your consumers the easiest way to use your websocket**

*DataPower is used to protect and proxy http connections. As a WebSocket is an upgraded HTTP Connection it allows DataPower to offer similar protection and proxying facilities. When a WebSocket connection is established with DataPower before the connection is upgraded it applies the MultiProtocol Gateway Policies. This means that additional logic can be applied to validate the request. In this series of articles we are going to be using API Connect for this.*

This article replaces part 3. The key difference between part 3 and part 3.1 is that, in this article we will only have one API in the product.

The purpose of this API is to describe how we can socialise the WebSocket Service through API Connect. In order to make the on boarding as simple as possible we will take the security API that was built in part 2 and modify it so that it appears to be the endpoint for WebSocket. This means when a consumer subscribes to the API they will be able to use their Client ID and Client Secret for the WebSocket connection. In addition the same API will contain the connection details for the WebSocket.

In order to achieve this we need to enable Vanity Endpoints for the API. The Vanity Endpoints allow the host value set in the API to override the advertised endpoint in the portal.

### Enable Vanity Endpoints in a catalog
1. Log into API Manager
2. Go to the required catalog
3. Go to preferences
<br>
![](/images/2019-7-16-websocket-pt3.1.1.png)
<br>
4. Click on API Endpoints
5. Click on Edit
6. Click on Display Vanity Endpoint
7. Click on API priority
<br>
![](/images/2019-7-16-websocket-pt3.1.2.png)
<br>

### Changes to the swagger file
Taking the API Swagger  from Part 2

<button class="collapsible" id="yaml">Click here for the sample.</button>

<div class="content" id="yamldata" markdown="1">

```yaml
swagger: '2.0'
info:
  title: WebSocket
  x-ibm-name: WebSocket
  version: 1.0.0
  description: This is a Web Socket Service. You need to use a WebSocket client to use invoke. Other instructions also go on here.
schemes:
  - https
host: websocketendpoint.com
basePath: /WebSocket
security:
  - clientID: []
securityDefinitions:
  clientID:
    type: apiKey
    in: header
    name: X-IBM-Client-Id
x-ibm-configuration:
  cors:
    enabled: true
  gateway: datapower-gateway
  type: rest
  phase: realized
  enforced: true
  testable: false
  assembly:
    execute:
      - set-variable:
          version: 1.0.0
          title: set-variable
          actions:
            - set: message.body
              value: SUCCESS
    catch: []
  properties:
    target-url:
      value: 'http://example.com/operation-name'
      description: The URL of the target service
      encoded: false
  application-authentication:
    certificate: false
paths:
  /:
    get:
      responses:
        '200':
          description: ok
          schema:
            type: string
      consumes: []
      produces: []
```
</div>


|---|---|---|
| | Value | Description |
|---|---|---|
| Host |  | Hostname of the websocket endpoint |
| Testable | false | This stops the test tool being displayed in the Developer Portal, this is because the test tool in the developer portal  is not set up to test websockets. |
| description |  |  Instructions how to use the WebSocket endpoint.|
|---|---|---|
