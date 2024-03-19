---
layout: post
date: 2023-03-07 09:00:00
categories: APIConnect
title: "API Connect - Harnessing the Canary "
---

Canary deployments are a way to roll out changes to a service in a controlled manner, by gradually introducing the changes to a small group of users before rolling them out to the entire user base. API Connect can provide the functionality to different versions of a downstream service using a simple piece of gateway script.

<!--more-->
Here's how it works:

1. A new version of the service with the changes you want to deploy is created.
2. Deploy the new version of the service. The intention is to allow a smaller proportion of the traffic to be routed to this service.
3. You then monitor the performance of the new version of the service in the canary group, to see if there are any issues or problems.
4. If the new version of the service is performing well in the canary group, you gradually roll it out to a larger proportion of traffic.
5. You continue to monitor the performance of the new version of the service in the rollout group, and if it's still performing well, you roll it out to the entire user base.
6. If there are any issues or problems with the new version of the service, you can quickly roll back to the previous version, minimising the impact on your users.

Here's an example of how this might work in a real-world scenario:

Let's say you're a company that offers an online shopping service, and you want to deploy a new version of your website with some new features. You create a canary group of 10% of your users, and deploy the new version of the website to them. You monitor the performance of the new version, and see that it's performing well. You then gradually roll it out to a rollout group of 20% of your users, and continue to monitor its performance. If everything looks good, you roll it out to the entire user base.

The benefits of canary deployments include:

* Reduced risk: By gradually rolling out changes to a small group of users before rolling them out to the entire user base, you can minimise the risk of introducing bugs or other issues that could impact your users.
* Faster feedback: By monitoring the performance of the new version of the service in the canary group, you can get feedback on its performance more quickly, and make any necessary adjustments before rolling it out

This can be achieved in API Connect with some custom GatewayScript.

This sample will use two policies and invoke and some gateway script.


## Image
![image](/images/CanaryAPIC.png)


## Sample gateway script
```javascript
//Object where each attribute key is they weight and each value is the url that would be routed to,.
let map = {
    10 : "https://httpbin.org/ip",
    20 : "https://httpbin.org/status/418"
}

let total = 30;

const number = Math.floor(Math.random() * total) + 1;
let count = 0;
Object.keys(map).forEach((key) => {
    let keyInt = parseInt(key);
    if (count <= number && number <= (count+keyInt)) {
        context.set('targeturl',map[key])
        console.error('Debug message for Canary - ',map[key])
    }
    count = (count+keyInt);
})
```

When the gateway script is called it will generate a number between 0 and the total weighting. This is then used to select an appropriate URL and sets it to the context variable called `targeturl`.

In the invoke policy  set the `target-url` parameter to  `$(targeturl)`

## Full API Yaml

```
swagger: '2.0'
info:
  version: 1.0.0
  title: Canary Test
  x-ibm-name: canary-test
basePath: /canary-test
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
          title: gatewayscript
          source: |-
            let map = {
                10 : "https://httpbin.org/ip",
                20 : "https://httpbin.org/status/418"
            }
            let total = 30;

            const number = Math.floor(Math.random() * total) + 1;
            let count = 0;
            Object.keys(map).forEach((key) => {
                let keyInt = parseInt(key);
                if (count <= number && number <= (count+keyInt)) {
                    context.set('targeturl',map[key])
                    console.error('Debug message for Canary - ',map[key]);
                }
                count = (count+keyInt);
            })
      - invoke:
          title: invoke
          version: 2.0.0
          verb: keep
          target-url: $(targeturl)
          follow-redirects: false
          timeout: 60
          parameter-control:
            type: allowlist
            values: []
          header-control:
            type: blocklist
            values: []
          inject-proxy-headers: true
          persistent-connection: true
          chunked-uploads: true
    catch: []
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
schemes:
  - https
```

Here is a sample of the log file from when the api was executed three times
```
20240319T143318.611Z [apiconnect][0x8580005c][gatewayscript-user][error] apigw(apiconnect): tid(26192)[request][172.30.104.134] gtid(a1ab7cdb65f9a22e00006650): Debug message for Canary -  'https://httpbin.org/status/418'
20240319T143319.430Z [apiconnect][0x88c00313][mgmt][notice] : tid(656): Successfully retrieved the data for probe ID '2712370395-Landlord-apiconnect-small-gw-0-e9638d7d-3d97-4007-9c00-db7caba186db'.
20240319T143406.644Z [apiconnect][0x8580005c][gatewayscript-user][error] apigw(apiconnect): tid(26464)[request][172.30.104.134] gtid(a1ab7cdb65f9a25e00006760): Debug message for Canary -  'https://httpbin.org/ip'
20240319T143406.644Z [apiconnect][0x8580005c][gatewayscript-user][error] apigw(apiconnect): tid(26464)[request][172.30.104.134] gtid(a1ab7cdb65f9a25e00006760): Debug message for Canary -  'https://httpbin.org/status/418'
20240319T143407.979Z [apiconnect][0x88c00313][mgmt][notice] : tid(656): Successfully retrieved the data for probe ID '2712370395-Landlord-apiconnect-small-gw-0-b4e872cd-b126-4351-82a7-db7caba1288b'.
```


Video
