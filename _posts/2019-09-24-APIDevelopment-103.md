---
layout: post
date: 2019-09-24 06:00:00
categories: APIConnect
title: "Developing APIs - 103 - Debugging an API"
Location: "Paris, France"
draft: true
---
Part of Three of the API Development Series. In this part we will show how to add debug messages and how to retrieve them in the DataPower Logs.
<!--more-->

<button class="collapsible" id="fulloutput">Sample Yaml for the new DataPower API Gateway</button>

<div class="content" id="fulloutputdata" markdown="1">
```yaml
swagger: '2.0'
info:
  version: 1.0.0
  title: DebugSample
  x-ibm-name: debug-sample
  description: 'Sample API to show how to write messages to the DataPower log '
basePath: /debug-sample
x-ibm-configuration:
  properties:
    target-url:
      value: 'http://apic-test-app.eu-gb.mybluemix.net/api/balance?id={uid}'
      description: URL of the proxy policy
      encoded: false
  cors:
    enabled: true
  gateway: datapower-api-gateway
  type: rest
  phase: realized
  enforced: true
  testable: true
  assembly:
    execute:
      - parse:
          version: 2.0.0
          title: parse
          parse-settings-reference:
            default: apic-default-parsesettings
      - gatewayscript:
          version: 2.0.0
          title: gatewayscript
          source: console.error(context.get("message.body"))
      - map:
          version: 2.0.0
          title: map
          inputs:
            input:
              schema:
                $ref: '#/definitions/request'
              variable: message.body
              content: application/json
          outputs:
            output:
              schema:
                $ref: '#/definitions/second'
              variable: message.body
              content: application/json
          actions:
            - set: output.p3
              from: input.p1
            - set: output.p4
              from: input.p2
      - gatewayscript:
          version: 2.0.0
          title: gatewayscript
          source: console.error(context.get("message.body"))
      - invoke:
          version: 2.0.0
          title: invoke
          header-control:
            type: blacklist
            values: []
          parameter-control:
            type: whitelist
            values: []
          timeout: 60
          verb: GET
          cache-response: protocol
          cache-ttl: 900
          stop-on-error: []
          target-url: 'http://apic-test-app.eu-gb.mybluemix.net/api/balance?id=1001'
      - parse:
          version: 2.0.0
          title: parse
          parse-settings-reference:
            default: apic-default-parsesettings
      - gatewayscript:
          version: 2.0.0
          title: gatewayscript
          source: console.error(context.get("message.body"))
      - map:
          version: 2.0.0
          title: map
          inputs:
            input:
              schema:
                $ref: '#/definitions/responseFromInvoke'
              variable: message.body
              content: application/json
          outputs:
            output:
              schema:
                $ref: '#/definitions/third'
              variable: message.body
              content: application/json
          actions:
            - set: output.p1
              from: input.balance
      - gatewayscript:
          version: 2.0.0
          title: gatewayscript
          source: console.error(context.get("message.body"))
  catalogs: {}
  application-authentication:
    certificate: false
paths:
  /:
    get:
      responses:
        '200':
          description: success
          schema:
            type: string
      consumes: []
      produces: []
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
    delete:
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
    head:
      responses:
        '200':
          description: success
          schema:
            type: string
      consumes: []
      produces: []
    patch:
      responses:
        '200':
          description: success
          schema:
            type: string
      consumes: []
      produces: []
securityDefinitions:
  clientID:
    type: apiKey
    in: header
    name: X-IBM-Client-Id
security:
  - clientID: []
schemes:
  - https
definitions:
  request:
    type: object
    additionalProperties: false
    properties:
      p1:
        type: string
      p2:
        type: string
  third:
    type: object
    additionalProperties: false
    properties:
      p1:
        type: integer
  responseFromInvoke:
    type: object
    additionalProperties: false
    properties:
      balance:
        type: integer
  second:
    type: object
    additionalProperties: false
    properties:
      p3:
        type: string
      p4:
        type: string
```
</div>

*Sample Request*
```
curl -k https://<DP endpoint>/<org>/<catalog>/debug-sample?id=123  -H "x-ibm-client-id: <client id>" -v -d '{"p1":"asddsd","p2":"123"}' -H "Content-Type:application/json" -v
```
e.g.
```
curl -k https://localhost:9444/localtest/sandbox/debug-sample?id=123  -H "x-ibm-client-id: d0db0196fee3c3751ad3514978a3795c" -v -d '{"p1":"asddsd","p2":"123"}' -H "Content-Type:application/json" -v
```
### Accessing the DataPower Log


The Sample YAML above shows how to log messages to the DataPower log from within an API. In order to see the DataPower log you must have access to it.

If you are using LTE then this is possible by running  `docker logs  apic-lte-datapower-api-gateway`.

If you are not running LTE  then you must have access to a DataPower WebUI, the Kubernetes infrastructure that DataPower is running in or [LogEar](https://chrisphillips-cminion.github.io/kubernetes/2019/07/23/LogEar.html)

### Gateway Script Code
The easiest way to log the message to the DataPower console is with the following gateway script.

*DataPower-API-Gateway*
```javascript
console.error("Point of Flow")
console.error(context.get("message.body"))
console.error(context.get("message.headers"))
```
*DataPower-Gateway*
```javascript
console.error("Point of Flow")
console.error(apim.getvariable("message.body"))
console.error(apim.getvariable("message.headers"))
```

The `message` value is the default variable name. If an invoke, parse or validate is configured to save its response in a different variable,  use that variable name instead of `message`.

Though I have used `error` in the sample above this can be modified for any of the DataPower standard verbs. However by default the `error` messages appear in the DataPower logs and do not require additional logging to be enabled.

Before putting the API into production the `error` verbs should be replaced with the appropriate logging level.

### Logging the initial Payload  (DataPower API Gateway Only)

At the start of an API or after an invoke in the new DataPower API Gateway the payload is a buffer. The easiest way to turn the buffer into a XML or JSON object is using the Parse Policy.
