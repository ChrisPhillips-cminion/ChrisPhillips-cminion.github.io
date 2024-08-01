---
layout: post
date: 2024-05-22 10:00:00
categories: APIConnect
title: "Setting an invoke proxy"
author: [ "ChrisPhillips","TreyWilliamson" ]
draft: true
---

Setting a downstream proxy is often a requirement when API Connect needs to make calls to the invoke downstream services on the internet.

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
			"proxy * 127.0.0.1 10999"
         ]
      }
   }
}
```
In the above sample we are overriding the proxy object in the apigw.  We have configured the proxy remote host to be 127.0.0.1 and the port to be 10999, please ensure these are updated to match the values you require.


Then put both files into a zip and you have your gateway extension. This can be loaded via the Cloud Manager into an API Gateway service.

![](/images/gwx.png)


Now if you check in the DataPower you can see the proxy is correctly configured.
