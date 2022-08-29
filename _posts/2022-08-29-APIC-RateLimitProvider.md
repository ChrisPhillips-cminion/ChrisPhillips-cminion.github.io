---
layout: post
categories: APIConnect
date: 2022-08-29 00:14:00
title: Rate Limiting an API that does not take a Consumer ID as a parameter.
---

Applying a rate limit to an API is essential to protecting downstream systems. Usually this is done OOTB with plans in API Connect. However if the API does not require a Client ID to be passed in this system will not work. Luckily API Connect provides a facility to rate limit directly on the canvas.

<!--more-->

## APIC Flow


![https://chrisphillips-cminion.github.io/images/flow.png](https://chrisphillips-cminion.github.io/images/flow.png)

The rate limit policy uses a rate limit object in DataPower to count the number of calls being made.  This can be configured to return a 429 or 504 to the API consumer depending on the need.

![https://chrisphillips-cminion.github.io/images/policy.png](https://chrisphillips-cminion.github.io/images/policy.png)




## Sample DataPower Config for creating the Rate Limit

The below will create a rate limit of ten per second. Each API must have its own API Connect rate limit object otherwise the APIs will share the same ratelimit count. This should be applied via a gw extension if DataPower is running in Kubernetes/OCP. Otherwise it can be applied immediately to the objects in your DataPower appliance.

```
sw apiconnect;co;
  apigw apiconnect;
    assembly-rate-limit apiratelimit 10 1 second on off on on off off na 1 ;
  exit;
exit
```

##Sample API
<button class="collapsible" id="html1">Click to reveal </button>

<div class="content" id="html1data" markdown="1">

```yaml
swagger: '2.0'
info:
  version: 1.0.0
  x-ibm-name: no-security-rate-limitng
  title: NoSecurity
basePath: /nosecurity
x-ibm-configuration:
  properties:
    target-url:
      value: https://httpbin.org/200
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
      - invoke:
          title: invoke
          version: 2.0.0
          verb: keep
          target-url: http://httpbin.org/status/200
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
                - name: apiratelimit
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


**Useful links**
* https://www.ibm.com/docs/en/datapower-gateway/10.0.x?topic=processing-api-rate-limit-action
* https://www.ibm.com/docs/en/api-connect/10.0.x?topic=connect-understanding-rate-limits-apis-plans
* https://www.ibm.com/docs/en/api-connect/10.0.x?topic=policies-rate-limit
