---
layout: post
date: 2023-01-31 00:01:00
categories: API Connect
title: "Error: CALL recursive depth too deep"
draft: true
---

One of the reasons my blog doesn't have so many updates is that I don't often find new problems.

<!--more-->

This week I am visiting a client and they showed me this error message. After much investigation (talking to half the engineering team) we confirmed this was due to a max depth limit in APIC.

In API Connect v10 there is a max number of policies allowed in an API. This is to stop an overly complex API from a malicious actor locking up a datapower.

The error message has the an error like below


```
{
  "httpCode": "500",
  "httpMessage":"Internal Server Error",
  "moreInformation":"CALL recursive depth too deep"
}
```

Out of the box we support 128 policies to be invoked in a single API Call. This can be increased by setting the `var://service/max-call-depth` vairable to 2048.


To override the service variables set the following code in a gatewayscript of the api

```
var sm = require ('service-metadata');
sm.setVar("var://service/max-call-depth",2048);
```
