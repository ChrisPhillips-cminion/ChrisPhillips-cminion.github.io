---
layout: post
date: 2019-07-15 01:00:00
categories: APIConnect
title: "WebSockets Part 2 - Securing with API Connect"
draft: true
---

DataPower provides the facility to proxy WebSocket connections. This article is part **two** of a three part guide consisting of

* _Part 1_ - How to create a WebSocket Proxy in DataPower
* **Part 2 - How you can use API Connect to secure your implementation**
* _Part 3_ - How to socialise it via the Developer Portal giving your consumers the best onboarding experience (Delayed)

_DataPower is used to protect and proxy http connections. As a WebSocket is an upgraded HTTP Connection it allows DataPower to offer similar protection and proxying facilities. When a WebSocket connection is established with DataPower before the connection is upgraded it applies the MultiProtocol Gateway Policies. This means that additional logic can be applied to validate the request. In this series of articles we are going to be using API Connect for this._

In Part 2 we will go through how API Connect can be used to provide Authentication and Authorization for the WebSocket connection using the API Connect Security Definitions. When the WebSocket connection is made to DataPower, DataPower can run additional policies on the request. In this article we route to API Connect to validate the user can be Authenticated and Authorized.

### Prerequisites

-   WebSocket Proxy from Part 1
-   WebSocket Client and Server application (The sample I use is here  [](https://github.com/ChrisPhillips-cminion/PlayingWithWebSockets) )
-   API Connect 2018 Instance

The API works similarly to an Authorisation URL. The API must be secured with the same security that you want to have to secure the Web Socket. When the Web Socket is establishing the connection to the DataPower, DataPower sends a request to this API with the credentials and the API responds with 200, 400, 401 or 500

### 1. Create and Publish the API

This guide assumes you have experience creating and using APIs in API Connect 2018. There is a sample provided below that can be used as a starting point.  This should be published to a catalog and the URl for the API should be recorded for future parts of this guide.

<button class="collapsible" id="yaml">Click here for the sample.</button>

<div class="content" id="yamldata" markdown="1">

```yaml
swagger: '2.0'
info:
  title: WebSocketAA
  x-ibm-name: WebSocketaa
  version: 1.0.0
  description: Used To Authenticate and Authorize WebSocket calls
schemes:
  - https
basePath: /WebSocketaa
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
  testable: true
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

If you are using the sample a subscription is required, this is enforced by passing in a client id. You may choose to extend this so that a secret and/or Token or other Third Party security system. If that is case you need  to ensure in the gateway script below we pass in the correct details to the API.

### 2. Call the API From DataPower

We now need to modify the DataPower Policy so that it invokes the API when the initial connection is made.  When the connection is attempted prior to the upgrade DataPower will invoke the API with the required security details.

The sample below extracts the headers from the initial connection and proxies them on to the API call. If you have changed or extend the security requirements from the sample this will need updating.

If the API returns to DataPower a 200 then the connection continues and is upgraded. If 200 is not responded then a 500 is thrown. This is sample code that should be adapted to handle error scenarios as you need.

<button class="collapsible" id="js">Click here for the sample.</button>

<div class="content" id="jsdata" markdown="1">

```javascript
var urlopen = require('urlopen');
var requestheader = require('header-metadata');
var myheaders = requestheader.current.headers;



var urlopen = require('urlopen');

var options = {
            target: 'HTTP://APIENDPOINT/',
            method: 'get',
           headers: requestheader.current.headers,
       contentType: 'text/plain',
           timeout: 60
};

urlopen.open(options, function(error, response) {
  if (error) {
    // an error occurred during the request sending or response header parsing
    session.output.write("urlopen error: "+JSON.stringify(error));
  } else {
    // get the response status code
    var responseStatusCode = response.statusCode;
    var responseReasonPhrase = response.reasonPhrase;
    console.log("Response status code: " + responseStatusCode);
    console.log("Response reason phrase: " + responseReasonPhrase);
    // reading response data
    response.readAsBuffer(function(error, responseData){
      if (error){
        throw error ;
      } else {
        session.output.write(responseData) ;
      }
    });
  }
});
```

</div>

Please save the sample code to a file on your local file system. Before putting this sample into production you will need to configure error handling to your requirements.

### 2.1 Uploading the Sample Code

Uploading the Script

1.  Log into DataPower
    ![](/images/2019-07-04-WebSocketspt1-1.png)
2.  Upload the GatewayScript

-   Click on File System storage
    ![](/images/2019-07-08-1.png)
-   Click on Actions to the right of local (feel free to use any path as long as you select the right file in 2.2)
    ![](/images/2019-07-08-2.png)
-   Click on Upload files.
    ![](/images/2019-07-08-3.png)
-   Select the file containing the source above and upload it.

### 2.2 Creating the Policy

1.  Click on Control Panel on the top left

![](/images/2019-07-08-0.png)
2\. Go to the Multi-Protocol Gateways
![](/images/2019-07-04-WebSocketspt1-2.png)
3\. Select the WebSocket MPG that was created in part 1
4\. Click on the plus by Multi-Protocol Gateway Policy so we can create a new policy.
![](/images/2019-07-08-4.png)
5\. Give the policy a name and press Apply Policy
6\. Create a new rule and change the rule direction to be `Client to Server`
![](/images/2019-07-08-5.png)
7\. Drag a GatewayScript icon ![](/images/2019-07-08-gw.png) from the panel to the line after the match icon ![](/images/2019-07-08-m.png).
![](/images/2019-07-08-6.png)
8\. Double click on the gateway script policy
9\. Select the location of the GatewayScript file and press done
![](/images/2019-07-08-8.png)
10\. Press Apply Policy and Close Window
11\. Press Apply

### Test

To test this you need to ensure that the headers are set when creating the WebSocket connection. To use my sample implementation with the sample API set the `x-ibm-client-id` to the client id from step 1.

```javascript
const connection = new WebSocket(url, {
  headers: {
    "x-ibm-client-id": "ID"
  }
})
```

My very basic WebSocket sample is available [here](https://github.com/ChrisPhillips-cminion/PlayingWithWebSockets)
