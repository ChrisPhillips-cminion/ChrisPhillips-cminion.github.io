---
layout: post
date: 2026-11-12 18:00:00
categories: webMethods
title: "webMethods API Gateway: Enable the Tracer and Set the Trace Timeout"
author: ["ChrisPhillips", "ChrisGilroy", "IBMBob"]
description: "How to turn on the tracer for an API in IBM webMethods API Gateway (SaaS) 11.1, read the results, and change how long the tracer stays on using tracerTimeoutSecs."
tags: [webMethods, APIGateway, Trace, Debugging, Troubleshooting]
---

An API call is failing and you cannot see why. The tracer in webMethods API Gateway shows each policy that ran, how long it took, and the request and response at every hop.


This post is based on the IBM webMethods API Gateway (SaaS) 11.1.0 documentation.

<!--more-->
## Enable the tracer

You need the **Manage APIs** privilege, and the API must be in an active state.

### Step 1: Open the API

1. Open the menu options and select **APIs**.
2. Click the API you want to trace.

### Step 2: Enable tracing

1. Click **Enable tracing**.
2. The API details page now shows a warning: `This API has tracing enabled. Tracing impacts performance and storage, hence disable tracing when it is not needed.`

### Step 3: Send a request and open the Tracer tab

1. Call the API.
2. Click the **Tracer** tab.
3. The **Trace API** page has three sections: **Runtime events**, **Policies applied** and **Event tracer details**.

Tracing works for REST, SOAP and OData APIs only.

## Read a trace

1. In **Runtime events**, click the client request you want to look at.
2. **Event tracer details** shows **General Information**, **API request and response** and **Server logs**.
3. **API request and response** has four parts:
   - The request sent by the client.
   - The response sent to the client.
   - The request sent to the native service.
   - The response sent by the native service.
4. In **Policies applied**, click a stage name to see the status and response time of that stage and its policies.
5. Click a policy name to see its configuration, its input and its output.

A **Success** status means the policy ran. It does not mean the policy's conditions matched. Click the policy to see how the conditions were applied.

A stage with no policies enforced during the call is greyed out. The Error Handling stage is the usual example.

## Set the trace timeout

The tracer switches itself off after a timeout. The default is 300 seconds (5 minutes). You control it with the `tracerTimeoutSecs` extended setting.

You need the **Manage user administration** functional privilege.

1. Open the menu options and select **Administration**.
2. Select **General > Extended settings**.
3. Click **Show and hide keys**.
4. Find `tracerTimeoutSecs` in the **Extended keys** section and enter a value in seconds.
5. Click **Save**.

The change takes effect immediately. No restart is needed.

The minimum is 1 second and the maximum is 300 seconds. You can make the tracer stop sooner. You cannot make it run longer than 5 minutes. If you need more time, click **Enable tracing** again after it stops.

> IBM's page for extended settings says not to change them unless IBM Global Support asks you to. Check with support before changing `tracerTimeoutSecs` on a production tenant.

## Things that catch people out

- **Traces appear slowly.** The tracer data is pushed as a single bulk request, so there is a minimum delay of 5 seconds before a request shows in the UI.
- **Not every request is traced.** The tracer is throttled to protect the gateway. The documentation says one request per second per node. Other requests in that window are dropped. The `throttleTracerBucketLeakRate` setting controls this.
- **Only recent traces are kept.** The last 100 requests are retained by default. `allowedTracerCount` changes this. The default is 100 and the maximum is 1000.
- **Tracing switches off when the API changes.** It is disabled on a new version of the API, after an import with Overwrite set to **All** or **Custom - API**, and after a promotion with **Overwrites assets except alias that already exist on the selected target stages**. Enable it again after each.
- **Streaming bodies are not captured.** This applies even with the tracer on.

## Limitations and Notes

- Threat protection policies and rules cannot be traced.
- Microgateway groups cannot be traced.
- Tracing can be enabled and disabled through the Service Management REST API. See the IBM documentation for the details.
- Two IBM pages describe `throttleTracerBucketLeakRate` differently. The debugging page says one request per second per node. The extended settings page says the value is in milliseconds with a default of 100. I have not tested which is right on a live tenant.

## References

- [Debugging API](https://www.ibm.com/docs/en/wams/wm-api-gateway-saas/11.1.0?topic=implementation-debugging-api)
- [Enabling tracing](https://www.ibm.com/docs/en/wams/wm-api-gateway-saas/11.1.0?topic=api-enabling-tracing)
- [Viewing trace details](https://www.ibm.com/docs/en/wams/wm-api-gateway-saas/11.1.0?topic=api-viewing-trace-details)
- [Configuring extended settings](https://www.ibm.com/docs/en/wams/wm-api-gateway-saas/11.1.0?topic=administering-configuring-extended-settings)
