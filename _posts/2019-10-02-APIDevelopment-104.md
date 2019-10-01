---
layout: post
date: 2019-10-02 06:00:00
categories: APIConnect
title: "Developing APIs on API Connect - 104 - Adding Definitions"
Location: "Paris, France"
---
Part of Four of the API Development Series. In this part we will show how to create simple definitions in API Connect and use teh Mapping Policy to map between them.
<!--more-->


### Introduction
Start by creating a new API liked we did in [part 1](/apiconnect/2019/09/27/APIDevelopment-101.html) only with this endpoint. `http://apic-test-app.eu-gb.mybluemix.net/api/payment`

The sample below can be used,

<button class="collapsible" id="fulloutput">Sample Yaml for the new DataPower API Gateway</button>

<div class="content" id="fulloutputdata" markdown="1">
```yaml
swagger: '2.0'
info:
  version: 1.0.0
  title: paymoney
  x-ibm-name: paymoney
basePath: /paymoney
x-ibm-configuration:
  properties:
    target-url:
      value: 'http://apic-test-app.eu-gb.mybluemix.net/api/payment'
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
      - proxy:
          title: proxy
          version: 1.0.0
          verb: keep
          target-url: $(target-url)
  application-authentication:
    certificate: false
paths:
  /:
    post:
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

```
</div>

This Service takes in a payload in the format.
```json
{
  "toId":"1001",
  "fromId":"1002",
  "amount":100
}
```

We will modify the API to accept the following payload
```json
{
  "FromAccountNo":"1001",
  "TargetAccountNo":"1002",
  "Amount":100
}
```
### Steps
1. Go to the Design View
<br>![](/images/2019-09-24-APIDevelopment-102-1.png){:height="100px" }

2. Go to Definitions
<br>![](/images/2019-10-02-APIDevelopment-140-1.png){:height="300px" }

3. Click on Add

4. Enter the following parameters
<br>![](/images/2019-10-02-APIDevelopment-140-3.png){:height="300px" }
<br>*Name* : IntialRequest
<br>*Description* : This is the payload schema for the data passed into  the API

5. Press Add
<br>![](/images/2019-10-02-APIDevelopment-140-4.png){:height="200px" }
6. Enter the following details
<br>*Property Name* : FromAccountNo
<br>*Property Type* : String
<br>*Property Example* : 1001
<br>*Property Description* : The account number to take the money from.


7. Press Add

8. Enter the following details
<br>*Property Name* : ToAccountNo
<br>*Property Type* : String
<br>*Property Example* : 1002
<br>*Property Description* : The account number to put the money from.


9. Press Add

10. Enter the following details
<br>*Property Name* : Amount
<br>*Property Type* : float
<br>*Property Example* : 100
<br>*Property Description* : The amount of money to move


11. Press Save

12. Now we will create the definition for the Service Request.
<br>Click on Add

13. Enter the following parameters
<br>![](/images/2019-10-02-APIDevelopment-140-4.png){:height="100px" }
<br>*Name* : ServiceRequest
<br>*Description* : This is the payload schema for the data passed into the Downstream Service

14. Press Add

15. Enter the following details
<br>*Property Name* : fromId
<br>*Property Type* : String
<br>*Property Example* : 1001
<br>*Property Description* : The account number to take the money from.


16. Press Add

17. Enter the following details
<br>*Property Name* : toId
<br>*Property Type* : String
<br>*Property Example* : 1002
<br>*Property Description* : The account number to put the money.


18. Press Add

19. Enter the following details
<br>*Property Name* : Amount
<br>*Property Type* : Number
<br>*Property Example* : 100
<br>*Property Description* : The amount of money to move

11. Press Save

12. Go to Path
<br>![](/images/2019-10-02-APIDevelopment-140-5.png){:height="100px" }

13. Click on `/`

14. Click on `Post`

15. Click on Add in the Parameters Section
<br>![](/images/2019-10-02-APIDevelopment-140-6.png){:height="100px"

16. Enter the following details
<br>*Required* : True
<br>*Name* : Request  
<br>*Located in* ; body
<br>*Type* : IntialRequest
<br>*Descrioption* : JSON Payload container details on the acounts to move money from and two, and the quantity.

17. Press Save

18. Goto Assembly
<br>![](/images/2019-10-02-APIDevelopment-140-7.png){:height="100px"}

19. Drag a Parse Policy onto the start of the flow. The parse policy is required to turn the input message from a buffer into an Object.
<br>![](/images/2019-10-02-APIDevelopment-140-8.png){:height="200px"}

20. Drag a Validate policy and place it after the Parse policy. We want to validate the payload prior to invoking the DownSteam service.
<br>![](/images/2019-10-02-APIDevelopment-140-9.png){:height="200px"}

21. Click on the Validate policy and select the following
<br>![](/images/2019-10-02-APIDevelopment-140-10.png){:height="300px"}

22. Drag a Map Policy after the validate and before the Invoke and configure it like below.
<br>![](/images/2019-10-02-APIDevelopment-140-11.png){:height="200px"}

23. Set the Input to the following
<br>![](/images/2019-10-02-APIDevelopment-140-12.png){:height="300px"}

24. Set the Output to teh following
<br>![](/images/2019-10-02-APIDevelopment-140-13.png){:height="300px"}

25. Link up the parameters,
<br>![](/images/2019-10-02-APIDevelopment-140-15.png){:height="300px"}

26. Save and Publish the API,

27. Invoke it as described in [part 1](/apiconnect/2019/09/28/APIDevelopment-101.html)
