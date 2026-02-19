---
layout: post
date: 2025-06-03 09:00:00
categories: APIConnect
title: "Accessing OpenAPI Extensions in the API Runtime."
author: ["ChrisPhillips"]
description: "Learn how to access and utilize OpenAPI extensions (x-* fields) in IBM API Connect runtime for custom metadata, routing logic, and enhanced API functionality."
tags: [APIConnect, OpenAPI, API Design, Extensions, API Gateway, Best Practices]
---

API Connect has the ability to load and attacked Open API Extensions. Here we show how to access the content from the extension in the API Runtime. 

For more information on OpenAPI Extensions  please review [https://swagger.io/docs/specification/v3_0/openapi-extensions/](https://swagger.io/docs/specification/v3_0/openapi-extensions/)

To add an extension document in API Connect the following links can be used.
* [https://www.ibm.com/docs/en/api-connect/10.0.x_cd?topic=definitions-adding-openapi-extension-api](https://www.ibm.com/docs/en/api-connect/10.0.x_cd?topic=definitions-adding-openapi-extension-api)
* [https://www.ibm.com/docs/en/SSMNED_v10cd/com.ibm.apic.toolkit.doc/ref_CLI_exten_commands.html](https://www.ibm.com/docs/en/SSMNED_v10cd/com.ibm.apic.toolkit.doc/ref_CLI_exten_commands.html)
* [https://www.ibm.com/docs/en/api-connect/10.0.x_cd?topic=cli-referring-extension-in-api-definition](https://www.ibm.com/docs/en/api-connect/10.0.x_cd?topic=cli-referring-extension-in-api-definition)


<!--more-->

The Open API Extension can be accessed in a GatewayScript policy by retrieving the swagger document.

```
  if (context.swagger) {
    context.swagger.readAsJSON(function(error, swaggerDoc) {
      if (error) {
        context.set('message.body',error)
      }
      else {
        extensionContent = swaggerDoc["x-banking"]      
      }     
    });
  } 
```

The above the sample will set the variable `extensionContent` to the content of the OpenAPI extension `x-banking`. 