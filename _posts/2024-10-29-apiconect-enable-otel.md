---
layout: post
date: 2024-10-29 10:00:00
categories: APIConnect
title: "API Connect and OpenTelemetry"
author: ["ChrisPhillips", "AmitKumarSingh" ]
draft: true
---

This article will explain how to enable Open Telemetry on API Connect 10.0.8.0 with DataPower 10.6.0.1. In order to apply these settings today, a GW extension must be used. This article will explain the steps to build the gateway extension.

Thanks to Zach Groseclose and Ben Stern for assisting with this.

For an introduction to OpenTelemetry please refer to a previous article on OpenTelemetry for AppConnect [https://chrisphillips-cminion.github.io/ace/2024/04/22/ACE-Otel.html](https://chrisphillips-cminion.github.io/ace/2024/04/22/ACE-Otel.html)

<!--more-->

## Create the config
Take the config below, update parameters as required and save as otel.cfg

**Change the HOSTNAME and PORT in the config below to match your OTel Agent (e.g. Instana)**
*The default ports for OpenTelemetry are 4317 (grpc) or 4318(http)*

```
%if% available "otel-exporter"
otel-exporter "otel-exp"
  type http
  hostname otel-collector.cp4i.svc.cluster.local
  traces-path "/v1/traces"
  metrics-path "/v1/metrics"
  logs-path "/v1/logs"
  port 4318
  http-content-type binary
  timeout 10
  processor batch
  max-queue-size 2048
  max-export-size 512
  export-delay-interval 5000
exit
%endif%
%if% available "otel-sampler"
otel-sampler "otel-samp"
  parent-based
  type always-on
exit
%endif%
%if% available "otel"
otel "api-otel"
  exporter otel-exp
  sampler otel-samp
exit
%endif%
apigw "apiconnect"
  otel api-otel
exit
```

## Create the GW extension

Place this manifest.json in the same directory as the otel.cfg.

**If you are already using a GW extension this must be merged with your existing one**

```json
{
	"extension": {
		"files": [
			{
				"filename": "otelgwextension.zip",
				"deploy":"immediate",
				"type": "extension"
			}
		]
	}
}
```

Run these commands in a shell session in the same directory as the manifest.json and otel.cfg this will build the required gateway extension zip file.
**Please note the filenames must match**

```sh
date=$(date +%s)
zip otelgwextension-$date.zip otel.cfg
zip otel-ext-$date.zip manifest.json otelgwextension-$date.zip
```


## Load the Gateway Extension
Login to API Connect Cloud Manager Admin, go to topology, select the gateway and click on configure gateway extension.


![](/images/otel1.png)

Click on Add and upload the zip file created in step above and press save

![](/images/otel2.png)

![](/images/otel3.png)

Wait a few minutes for the extension to apply

Once gateway extension is applied, we can see the corresponding Open Telemetry configuration on the API Gateway Object in DataPower

## Testing

Once the configuration is applied DataPower will send trace information to the Otel Collector (e.g. Instana) even when a health/readiness check is run.  In containers this is every few seconds.
