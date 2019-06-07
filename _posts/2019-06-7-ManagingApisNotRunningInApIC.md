---
layout: post
date: 2019-06-7 08:00:00
categories: API
title: 'Managing and Socialising APIs running outside of API Connect.'
image:  '/images/2019-06-06-sh1.png'
---

There are many places today to run your APIs. zOS Connect and Akamai are two such examples. Though I recommend that DataPower runs all APIs, if different API Gateways are available then you may want to socialise all of your APIs throught a single shop window. However these APIs still need to be managed and socialised.

API Connect has a lesser known feature that allows you to manage and expose on portal APIs running on other platforms. This is where the enforced option comes in.  Please note that athentication, authorization and other policies will not be enforced through API Gateway as DataPower is not being used.

You would still use the same swagger spec but set the host variable to point to the external API Gateway and set the enforced option to false.. A sample is below.

```swagger: '2.0'
info:
  title: HTTPBin Example
  x-ibm-name: httpbin-example
  version: 1.0.0
host: httpbin.org
schemes:
  - https
basePath: /
x-ibm-configuration:
  cors:
    enabled: true
  type: rest
  phase: realized
  enforced: false
  testable: true
  application-authentication:
    certificate: false
paths:
  /ip:
    get:
      responses:
        '200':
          description: success
          schema:
            type: string
      consumes: []
      produces: []
```



In the Portal it will appear like the following.


[](/images/2019-06-06-sh1.png)
[](/images/2019-06-06-sh2.png)


For a demo on how to do this please take a look at the following developer portal article. [https://developer.ibm.com/APIconnect/2019/05/20/consolidated-and-unified-catalog-with-API-connect/]
