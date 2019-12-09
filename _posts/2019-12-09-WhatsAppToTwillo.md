---
layout: post
date: 2019-12-9 00:02:00
categories: APIConnect
title: "Chatbot with Twilio via API Connect "
draft: true
---

Chatbots have been a current fashionable project to work on right now. An API Gateway is critical to help take the load off the main business application as well as providing a way to implement multiple Chatbot intermediaries without rewriting the business logic.

![chatbot1.png](/images/chatbot1.png)

<!--more-->


In this example we will make a request  to WhatsApp. Twilio will forward that onto the API Gateway. The API Gateway will validate the HMAC Signature sent by Twilio and then simply return the the body back to Whats App.. Instead this map can be preceded with  an invoke to reach a downstream service.

The downstream service will execute the business logic required and send a response to the API Gateway. The API Gateway would wrap this response with the Map Policy  into the format required for Twilio.

This guide assumes that the user can configure Twilio with the basic settings. In Twilio you specify the API Gateway Endpoint.

Though this guide talks about Twilio the same flow can be used for  other ChatBot providers meaning you can implement your business logic agnostic to  the consuming body.



![chatbot2.png](/images/chatbot2.png)


The first gateway script is responsible validating the HMAC form Twilio. Information on the validation can be found here.  [https://www.twilio.com/docs/usage/security#test-the-validity-of-your-webhook-signature](https://www.twilio.com/docs/usage/security#test-the-validity-of-your-webhook-signature)

```javascript
//############# These are the params that need updating
var params="https://123/123/123/123" //URL that the request is coming in on.
var key ='123123' //Auth Token from Twilio
//######

var crypto = require('crypto');

var hmac = crypto.createHmac('hmac-sha1', new Buffer(key) );
var dataList = new String(context.get('request.body')).split("&")
dataList.sort()
dataList.forEach(function(e) {
    console.error(e)
    if (e.startsWith('Body=')) {
        e = e.replace(/\+/g," ")
    }
    params=params+e.replace(/=/g,"")//.replace("%3A%2B",":+")
})
    // console.error(params)
var result = hmac.update(Buffer.from(decodeURIComponent(params), 'utf-8')).digest('base64');
if (result != context.get("message.headers.X-Twilio-Signature")) {
    console.error("HMAC Error "+decodeURIComponent(params))
    context.set("message.body", "HMAC Error "+decodeURIComponent(params))
    throw new Error("CheckSumError")
}
```

The second gateway script is used to turn the requested payload into a javascript object.

The invoke to downstream systems will take place in the switch.

```javascript
var d = context.get('request.body')
var dataList = new String(d).split("&")
dataList.sort()
var params = {}
dataList.forEach(function(e) {
    var entry = e.split("=")
    if (entry[0] == 'Body') {
        entry[1] = entry[1].replace(/\+/g,' ')
    }
    params[entry[0]]=decodeURIComponent(entry[1])
})
console.error(params)
context.set('message.body',params)
```

The Switch is used to determine which operations need to be routed down stream.


The complete example is available below.
```yaml
swagger: '2.0'
info:
  title: WhatsAppBot
  x-ibm-name: whatsappbot
  version: '2'
schemes:
  - https
basePath: /whatsappbotv2
securityDefinitions:
  clientIdHeader:
    type: apiKey
    in: header
    name: X-IBM-Client-Id
x-ibm-configuration:
  cors:
    enabled: true
  gateway: datapower-api-gateway
  type: rest
  phase: realized
  enforced: true
  testable: true
  assembly:
    execute:
      - gatewayscript:
          version: 2.0.0
          title: CheckSum Validation
          source: >-
            var
            params="123123123123123"
            //URL that the request is coming in on.

            var key ='123123123123' //Auth Token from Twilio

            var hmac = require('crypto').createHmac('hmac-sha1', new Buffer(key)
            );

            var dataList = new String(context.get('request.body')).split("&")

            dataList.sort()

            dataList.forEach(function(e) {
                console.error(e)
                if (e.startsWith('Body=')) {
                    e = e.replace(/\+/g," ")
                }
                params=params+e.replace(/=/g,"")
            })

            var result = hmac.update(Buffer.from(decodeURIComponent(params),
            'utf-8')).digest('base64');

            if (result != context.get("message.headers.X-Twilio-Signature")) {
                console.error("HMAC Error "+decodeURIComponent(params))
                context.set("message.body", "HMAC Error "+decodeURIComponent(params))
                throw new Error("CheckSumError")
            }
      - gatewayscript:
          version: 2.0.0
          title: Parse Data
          source: |-
            var d = context.get('request.body')
            var dataList = new String(d).split("&")
            dataList.sort()
            var params = {}
            dataList.forEach(function(e) {
                var entry = e.split("=")
                if (entry[0] == 'Body') {
                    entry[1] = entry[1].replace(/\+/g,' ')
                }
                params[entry[0]]=decodeURIComponent(entry[1])
            })
            console.error(params)
            context.set('message.body',params)
      - parse:
          version: 2.0.0
          title: parse
          parse-settings-reference:
            default: apic-default-parsesettings
      - switch:
          version: 2.0.0
          title: switch
          case:
            - condition: ($string(message.body.SmsStatus) = 'received')
              execute:
                - map:
                    version: 2.0.0
                    title: map
                    inputs:
                      input:
                        schema:
                          $ref: '#/definitions/hmacWhatsApp'
                        variable: message.body
                        content: application/json
                    outputs:
                      output:
                        schema:
                          $ref: '#/definitions/TwiML'
                        variable: message.body
                        content: application/xml
                    actions:
                      - set: output.Response.Message
                        from: input.Body
            - otherwise: []
    catch:
      - default:
          - set-variable:
              version: 2.0.0
              title: set-variable
              actions:
                - set: message.status.code
                  value: '400'
                  type: any
                - set: message.status.reason
                  value: HMAC Checksum Failed
                  type: any
  activity-log:
    success-content: payload
    error-content: header
    enabled: true
  buffering: true
  application-authentication:
    certificate: false
definitions:
  Twiml-Response:
    type: object
    additionalProperties: false
    properties:
      Message:
        type: string
  TwiML:
    type: object
    additionalProperties: false
    properties:
      Response:
        $ref: '#/definitions/Twiml-Response'
        properties: {}
  hmacWhatsApp:
    type: object
    additionalProperties: true
    properties:
      AccountSid:
        type: string
        example: AC6d968b21fc1e27103ab66c1d25c49f58
      ApiVersion:
        type: string
        example: '2010-04-01'
      Body:
        type: string
      From:
        type: string
        example: whatsapp%3A%2B44774728791
      MessageSid:
        type: string
        example: SM6f708e26e46b2d4d64e4dcada9e5a0b6
      NumMedia:
        type: string
        example: '0'
      NumSegments:
        type: string
        example: '1'
      SmsMessageSid:
        type: string
        example: SM6f708e26e46b2d4d64e4dcada9e5a0b6
      SmsSid:
        type: string
        example: SM6f708e26e46b2d4d64e4dcada9e5a0b6
      SmsStatus:
        type: string
        example: received
      To:
        type: string
        example: whatsapp%3A%2B447747868792
paths:
  /:
    put:
      responses:
        '200':
          description: success
          schema:
            type: string
      consumes: []
      produces: []
    post:
      responses:
        '200':
          description: success
          schema:
            type: string
      consumes: []
      produces: []
    options:
      responses:
        '200':
          description: success
          schema:
            type: string
      consumes: []
      produces: []
```
