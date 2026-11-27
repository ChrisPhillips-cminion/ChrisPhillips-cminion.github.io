---
layout: post
date: 2026-11-28 12:00:00
categories: APIConnect
title: "Retrieving audit events from API Connect"
author: ["ChrisPhillips", "IBMBob"]
description: "API Connect records every user operation — how to configure the audit settings, test the endpoint, and pull the events back out through the analytics REST route when an auditor asks for them."
tags: [APIConnect, Audit, Compliance, REST, CloudManager]
draft: true
image: /images/audit-retrieval-route.png
---

An auditor asks for six months of user activity on your API Connect cloud. The product has been recording it the whole time — getting it back out is the work. This article pulls the pieces into one workflow: the settings, the endpoint test, and the retrieval route.

<!--more-->

## What gets audited

API Connect can audit user operations on the cloud and send them to an HTTP or Syslog endpoint you configure. Since 10.0.5.3, read operations can be audited too, when the `audit_reads` setting is enabled — worth switching on if your audits require access logging, not just changes.

## Configuring the settings

The audit settings are managed from the Cloud Manager and the toolkit CLI: set the endpoint and options in the cloud settings, and upload with `apic cloud-settings:update`. The KC section "Configuring the audit settings" has the full procedure — UI edit path, endpoint fields, and the YAML syntax including `audit_reads`.

If you feed events to a SIEM, the HTTP or Syslog endpoint is the push side: events flow to your endpoint as they happen.

## Test the endpoint before you rely on it

For HTTP endpoints (not Syslog), the toolkit can verify the connection:

```bash
apic cloud-settings:audit-endpoint-test-connection
```

Run this after configuring and before your first audit window. The failure you are avoiding is discovering the endpoint was misconfigured by finding the records missing during an investigation.

## Retrieving the events

The pull side is a REST route on the analytics service:

```
GET <platform-api-hostname>/analytics/<analytics-service>/cloud/audit
```

Three things to establish for your cloud before the call is usable:

1. **The platform API hostname** — the platform API endpoint of your management subsystem.
2. **The analytics service** — the service your audit events are stored under.
3. **Authentication** — the credential and header the GET requires, and the shape of the response, including any pagination, for whatever consumes it.

If a script or SIEM integration will read the route regularly, capture the response shape once and code against it — the event data recorded in audit events is documented in the analytics sections of the KC.

## The workflow, end to end

1. Configure the audit settings and endpoint (UI or `apic cloud-settings:update`), including `audit_reads` if you need access logging.
2. Verify the endpoint with `apic cloud-settings:audit-endpoint-test-connection`.
3. Let events accumulate — pushed to your HTTP/Syslog endpoint as they happen.
4. When the auditor asks, pull history with `GET .../analytics/<analytics-service>/cloud/audit`.

## Summary

Audit logging in API Connect has a push side and a pull side: events flow to a configured HTTP or Syslog endpoint, and history is retrieved through the analytics REST route. Configure with the cloud settings, verify the endpoint with the toolkit's test-connection command, and resolve the platform API hostname, analytics service, and authentication before you need the route under pressure.

## Limitations and Notes

- The route's two parameters and its authentication are not spelled out in one place in the documentation — the values above are what to establish on your own cloud. I will update this post with a worked example once I have run it against a live system.
- The endpoint test applies to HTTP endpoints only; Syslog endpoints have no toolkit test command.
- Behaviour described against 12.1.x; check your version.
