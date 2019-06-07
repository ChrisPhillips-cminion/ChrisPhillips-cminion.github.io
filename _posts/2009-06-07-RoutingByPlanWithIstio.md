---
layout: post
date: 2009-06-07 09:00:00
categories: APIConnect
title: 'Using API Connect to allow Istio to route by plan - [Draft]'
image:  '/images/2019-06-07-title.png'
---


*Written by Chris Phillips and Claudio Tag*

API Connect allows an Application to subscribe to one plan for a product. This is traditionally used to determine which rate limit they are allowed to subscribe to. A couple of years ago I wrote an article on how to use this for plan variable to route to specific endpoints.  Istio provides the facility to route to different endpoints depending on header variables. This article shows how you can take the plan from a context variable and set it to a header to be picked up by Istio.

## What is istio?


``` Tag to write ```

## Writing the API and Product Logic
In order for this to work the keyword that Istio will look for will be the name as the name of the plan. Please note this is not the title.



### Product Sample

In the example below `plan1` will be picked up and sent to istio.

```
plan1:
  rate-limits:
    default:
      value: 100/1minute
  title: PLAN 1
  description: First Plan
  approval: false
```

Complete sample available at the end of the document

### API Sample

The API Logic is extract the plan value from the context variable, set it as a header and invoke the proxy. The core logic from the yaml is below.


```
- set-variable:
    version: 1.0.0
    title: set-variable
    actions:
      - value: $(plan.name)
        set: message.headers.X-PLAN
- proxy:
    title: proxy
    version: 1.0.0
    verb: GET
    target-url: $(target-url)/theInfo
```

And a screenshoot from the UI.

![](/images/2019-06-07-assembly.png)

The complete sample is available at the end of this article.


## Istio configuration
``` Tag to write```


## Links
* Links to github where samples are stored
* Links to learn more about Istio


## Samples
### Product Sample

```

info:
  name: istoRoutingSample-product
  title: istoRoutingSample product
  version: 1.0.0
gateways:
  - datapower-gateway
plans:
  default-plan:
    rate-limits:
      default:
        value: 100/1hour
    title: Default Plan
    description: Default Plan
    approval: false
  plan1:
    rate-limits:
      default:
        value: 100/1minute
    title: PLAN 1
    description: First Plan
    approval: false
  plan2:
    title: PLAN 2
    description: Everything Else Plan
    approval: false
    rate-limits:
      default:
        value: 3/1minute
        hard-limit: true
    burst-limits: {}
apis:
  istoRoutingSample1.0.0:
    $ref: istoRoutingSample_1.0.0.yaml
visibility:
  view:
    type: public
    orgs: []
    enabled: true
  subscribe:
    type: authenticated
    orgs: []
    enabled: true
product: 1.0.0

```
### API Sample

```
swagger: '2.0'
info:
  title: istoRoutingSample
  x-ibm-name: istoRoutingSample
  version: 1.0.0
schemes:
  - http
  - https
basePath: /IstoRoutingSample/v2
security:
  - clientID: []
securityDefinitions:
  clientID:
    type: apiKey
    in: header
    name: X-IBM-Client-Id
x-ibm-configuration:
  properties:
    target-url:
      value: 'https://ISTIOTargetHost0/simpleinfoapp/v1'
      description: URL of the proxy policy
      encoded: false
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
            - value: $(plan.name)
              set: message.headers.X-PLAN
      - proxy:
          title: proxy
          version: 1.0.0
          verb: GET
          target-url: $(target-url)/theInfo
    catch:
      - errors: []
        execute: []
  application-authentication:
    certificate: false
definitions:
  env data model:
    type: object
    properties:
      inputVar:
        type: string
      targetEndPoint:
        type: string
      soapReqDest:
        type: string
paths:
  /theInfo:
    get:
      operationId: gettheInfo
      responses:
        '200':
          description: The operation was successful.
          schema:
            $ref: '#/definitions/env data model'
      produces:
        - application/json
      description: Retrieve theInfo
      parameters:
        - name: varName
          in: query
          type: string
          description: Name of the backend service
```
