---
layout: post
categories: APIConnect
date: 2025-03-7 00:14:00
title: Circuit Breaker in API Connect
author: ["ChrisPhillips"]
description: "Implementing the circuit breaker pattern in IBM API Connect for resilient API architectures. Includes configuration examples, best practices, and failure handling strategies."
tags: [APIConnect, Circuit Breaker, Resilience, API Design, Fault Tolerance, Microservices, Best Practices]
---

*This is an update to a previous article. The changes are the samples and examples.*

A Circuit breaker pattern is becoming a common pattern for remote calls today. The purpose of the circuit breaker is to detect when a series of errors are returned and block traffic for a time period, thus giving the backend system time to recover.



<!--more-->

## APIC Flow

In API Connect there is no out of the box Circuit Breaker pattern but we can build a system that can do a similar function.

![https://chrisphillips-cminion.github.io/images/flow.png](https://chrisphillips-cminion.github.io/images/flow.png)

This assembly flow is made up of four policies, three ratelimits and an invoke.  The first ratelimit policy will increment (consume) the counter by one, this exists so we can terminate the request if the rate limit is reached prior to the invoke being made. The second ratelimit policy is used to reduce (replenish) the same counter so we don't impact the counter prior to errors being returned. The invoke is used to call  the downstream system and is configured to stop the flow when an error is returned.  The ratelimit policy in the catch block  will only be reached if the invoke is unsuccessful, it then increases (Consume) the rate limit counter by one.

![https://chrisphillips-cminion.github.io/images/policy.png](https://chrisphillips-cminion.github.io/images/policy.png)


The criteria for the rate limit must be defined in DataPower. I recommend this is set to an apigw object via a GW extension.

## Sample DataPower Config for creating the Rate Limit

The below will create a rate limit of ten per second.

```
sw apiconnect;co;
  apigw apiconnect;
    assembly-rate-limit errorcount 10 1 second on off on on off off na 1 ;
  exit;
exit
```
**UPDATE 31/8/2022 **
Thomas Burke correctly suggested that developers may prefer to detect the failure by using a switch case to look at the response code from the invoke rather then throwing an error. This is an excellent idea and so I wanted to highlight it here.

**UPDATE 7/3/2022 **
Charles Coble has recommended that we highlight the code to use in a gateway extension to create this object.
```
{
   "apigw":{
      "_global":{
         "override":[
            "assembly-rate-limit errorcount 10 1 second on off on on off off na 1"
         ]
      }
   }
}
```


## Sample API
<button class="collapsible" id="html1">Click to reveal </button>

<div class="content" id="html1data" markdown="1">

```yaml
swagger: '2.0'
info:
  version: 1.0.0
  title: ErrorLimitting
  x-ibm-name: errorlimitting
basePath: /errorlimitting
x-ibm-configuration:
  properties:
    target-url:
      value: https://httpbin.org/422
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
      - ratelimit:
          version: 2.2.0
          title: ratelimit
          source: gateway-named
          rate-limit:
            - name: errorcount
              operation: consume
          description: as
      - ratelimit:
          version: 2.2.0
          title: ratelimit
          source: gateway-named
          rate-limit:
            - name: errorcount
              operation: replenish
      - invoke:
          title: invoke
          version: 2.0.0
          verb: keep
          target-url: http://httpbin.org/status/422
          follow-redirects: false
          timeout: 60
          parameter-control:
            type: blocklist
            values: []
          header-control:
            type: blocklist
            values: []
          inject-proxy-headers: true
          persistent-connection: true
    finally: []
    catch:
      - errors:
          - ConnectionError
          - PropertyError
          - JavaScriptError
          - SOAPError
          - OperationError
          - BadRequestError
          - RuntimeError
        execute:
          - ratelimit:
              version: 2.2.0
              title: ratelimit
              source: gateway-named
              rate-limit:
                - name: errorcount
                  operation: consume
  activity-log:
    enabled: true
    success-content: activity
    error-content: payload
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
security: []
schemes:
  - https

```

</div>

## Sample GW Extension

A sample gateway extension can be found [https://chrisphillips-cminion.github.io/images/override_apigw.zip](https://chrisphillips-cminion.github.io/images/override_apigw.zip).
Thanks to Charles Coble for providing.



**Useful links**
* https://www.ibm.com/docs/en/datapower-gateway/10.0.x?topic=processing-api-rate-limit-action
* https://www.ibm.com/docs/en/api-connect/10.0.x?topic=connect-understanding-rate-limits-apis-plans
* https://www.ibm.com/docs/en/api-connect/10.0.x?topic=policies-rate-limit
* https://www.ibm.com/docs/en/api-connect/10.0.1.x?topic=environment-extending-gateway-server-behavior
