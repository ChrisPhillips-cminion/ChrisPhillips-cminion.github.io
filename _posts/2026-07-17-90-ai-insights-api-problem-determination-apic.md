---
layout: post
date: 2026-07-17 10:00:00
categories: APIConnect
title: "Simplify API Problem Determination with AI Insights and Enriched Analytics in API Connect v12.1.1"
author: ["ChrisPhillips", "IBMBob"]
---

When an API starts failing or slowing down, problem determination usually means checking several data sources and trying to build a timeline from them. API Connect v12.1.1 uses AI Insights to make that initial investigation easier.

Depending on the report and deployment, v12.1.1 may also expose more event detail than earlier reporting views. That gives the operator more context to work with before reviewing the AI-generated summary.

This article covers how AI Insights can be used during problem determination and how the extra event context can help.

<!--more-->

## The Problem

When something goes wrong with an API, you're typically pulling from several sources at once:

- **Gateway logs**: backend response times, protocol-level errors
- **Analytics events**: who called what, when, at what rate
- **Backend telemetry**: your own service health metrics
- **Consumer reports**: usually vague — "it's slow" or "it's not working"

Correlating those sources takes time. Even with good tooling, the context-switching overhead is significant.

AI Insights acts as a first-pass investigator. It ingests the event data available in API Connect and synthesises a structured narrative: what changed, when, what else was happening at the same time, and what the likely cause is.

## How AI Insights Analyses Events

When you open the AI Insights panel for a set of filtered events, it runs several types of analysis:

**Baseline comparison** — compares current metrics against historical baselines for the same API, plan, and application. A jump from 0.1% to 5% error rate gets flagged immediately.

**Temporal correlation** — looks for correlated events across dimensions. If latency spiked at the same time a specific backend returned errors, it surfaces that correlation rather than making you discover it manually.

**Anomaly classification** — classifies anomalies into categories: backend latency regression, auth/authorisation issues, rate limit violations, schema validation failures, upstream timeouts. Each classification includes a confidence score.

**Root cause signalling** — attempts to identify the most likely root cause category. Not a guaranteed diagnosis — a strongly informed hypothesis that directs the investigation.

## From Raw Events to Structured Insight

Here's what the raw gateway log for a failing `/orders` endpoint might look like:

```
2026-07-12 08:14:23.441 [gateway] HTTP 500 — POST /orders
  backend_latency=4521ms upstream_timeout
2026-07-12 08:14:25.112 [gateway] HTTP 500 — POST /orders
  backend_latency=4301ms upstream_timeout
2026-07-12 08:14:27.003 [gateway] HTTP 504 — POST /orders
  gateway_timeout
```

The same data expressed as an AI-generated summary:

```
🔴 [CRITICAL] Upstream Service Degradation Detected — /orders

8 timeout errors (HTTP 500/504) in the past 12 minutes.
Average backend response time: 4,380ms (vs. baseline of 230ms).
All failures are POST /orders operations.
Correlated event: Backend /order-service health endpoint returned
HTTP 503 at 08:14 UTC.

Likely root cause: Upstream order service is overloaded or unreachable.
Recommended:
  1. Check order-service pod/container health in your backend cluster
  2. Review recent deployments to order-service
  3. Consider temporary rate limiting on /orders to protect the backend
```

## An Investigation Walkthrough

A consumer reports: "Our application is getting errors on the `/payments` endpoint since this morning."

1. Open API Analytics for `/payments`, time range: today.
2. Open the AI Insights panel. It shows:
   ```
   ⚠️ [WARNING] Validation Error Spike on /payments
   POST requests with content-type application/json have returned 400 errors
   at 3.2x the normal rate since 2026-07-12 06:00 UTC.
   Error body: "card_number: must be a 16-digit string" —
   suggests a schema validation change was published.
   ```
3. Check the API definition — a schema update was published at 06:00 UTC.
4. Notify the consumer: they need to update their payload format.

Under 2 minutes instead of 20.

## Example: Investigating an Error Spike

Let's walk through a more complete example:

1. **Alert fires**: PagerDuty wakes you at 03:00 — error rate above threshold on production.
2. **Open API Manager → Analytics → API Health**: You see an error spike on several endpoints.
3. **Open AI Insights panel**: It immediately shows:
   - Primary insight: "Backend database connection pool exhaustion detected"
   - Supporting detail: "Error pattern matches known 'connection timeout' signature"
   - Recommended action: "Check database max_connections and active connection count"
4. **Confirm**: You check your PostgreSQL instance — sure enough, connections are maxed.
5. **Remediate**: You kill idle connections and temporarily increase the pool limit.
6. **Compare outcome to insight**: After the incident, compare the actual resolution with the suggested cause to judge how useful the insight was.

## Limitations and Notes

- **AI Insights augments, not replaces, your expertise**. Always validate insights against your actual systems before taking action.
- **Requires v12.1.1.0** — this feature is not backported to earlier v12 versions.
- **Baselines need time to establish** — AI Insights is most powerful after your APIs have been running for at least 1-2 weeks.
- **Not a real-time incident management tool** — for PagerDuty-class alerting, configure the Alerts feature in API Manager separately. AI Insights is for interactive investigation.
- **Environment-specific requirements**: Exact availability and runtime dependencies may vary by deployment model. Check the IBM documentation for your specific environment.

## Summary

API Connect v12.1.1 improves problem determination on two fronts. First, the analytics experience may expose richer event context than earlier views, giving operators more raw material to investigate with even without any AI involvement. Second, **AI Insights** can help synthesise that data into a structured narrative: what changed, when, what else was happening, and what the likely cause may be.

Together these two improvements take the tedious work out of the initial investigation phase — correlating events, surfacing anomalies, and pointing you toward likely causes — so you spend your time fixing problems rather than hunting for them.

If you're on v12.1.1, take it for a spin next time something goes wrong. You might find your mean time to resolution drops noticeably.
