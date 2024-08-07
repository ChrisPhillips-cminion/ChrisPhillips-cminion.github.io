---
layout: post
date: 2024-08-7 10:00:00
categories: APIConnect
title: "Setting an invoke proxy"
author: [ "ChrisPhillips","AmitKumarSingh" ]
---

When using the **rate limit policy on the Assembly** you need to first create a rate limit in datpower in the API Gateway object. This must be done via a GatewayExtension to stop the policy being removed when a publish request is done from API Connect.

This article will show you to create the rate limit objects in DataPower using a gateway extension.

We will create a rate limit called `chrisblog-ratelimit` that can be referenced from a rate limit policy.
<!--more-->

This requires a gateway extension to configure, regardless on the form factor of your API Gateway.  This guide requires DataPower 10.5.0.8 or later.

A Gateway extension is made up of a manifest, and the files needed for the config work. In this case it is a single gwd_extension json file.

**sample manifest**
manifest.json
```json
{
	"extension": {
		"files": [
			{
				"filename": "gwd.proxy.json",
				"type": "gwd_extension"
			}
		]
	}
}
```

The sample manifest simply references the other file that we need in this sample. If you are doing anthing more complex then you may need to add additional properties here. It is recommended that you build on the existing one if you are already using one.

**sample gwd-extension**
gwd.proxy.json
```json
{
   "apigw":{
      "_global":{
         "override":[
					 "assembly-rate-limit chrisblog-ratelimit 10 1 second on off on on off off na 1"
         ]
      }
   }
}
```

This will create a rate limit with the following parameters

| Name | Rate | Interval |Unit | Enable hard limit | Cache only | Is Client | Use API Name | Use Application ID | Use Client ID | Dynamic Value | Weight expression | Actions |
| test | 10 | 1 | minute | on | off | on | on | off | off | na | 1 |


Then put both files into a zip and you have your gateway extension. This can be loaded via the Cloud Manager into an API Gateway service.

![](/images/gwx.png)


Now if you create an api with a rate limit polic set the source to 'gateway-name' and the Rate limit name to 'chrisblog-ratelimit'
