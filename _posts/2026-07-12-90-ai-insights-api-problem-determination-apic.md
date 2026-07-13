---
layout: post
date: 2026-07-12 10:00:00
categories: APIConnect
title: "Simplify API Problem Determination with AI Insights and Enriched Analytics in API Connect v12.1.1"
description: "Learn how AI Insights and enriched analytics data in API Connect v12.1.1 transform raw API events into structured operational insights for faster problem determination."
tags: [APIConnect, APIConnectv12, AIInsights, ProblemDetermination, Troubleshooting]
draft: true
---

When an API starts behaving unexpectedly — errors spike, latency climbs, or a consumer reports a problem — you enter problem determination mode. Traditionally, this means pulling logs from multiple places, correlating timestamps, checking backend health, and working backward from symptoms. It's time-consuming and requires deep familiarity with your API ecosystem. API Connect v12.1.1 introduces **AI-powered problem determination** via AI Insights, designed to dramatically accelerate this process.

Importantly, it's not just the AI-generated insight that helps — v12.1.1 may also surface richer event context alongside each event than was available in earlier reporting views. Depending on the report and deployment, this can give operators more raw material to work with before they even review the AI-generated summary.

In this article, I'll walk you through how AI Insights analyses individual API events, how it transforms raw event data into structured operational insights, and how the enriched event data in v12.1.1 gives you more to work with during problem determination.

<!--more-->

## Table of Contents

1. [The Problem Determination Challenge](#the-problem-determination-challenge)
2. [How AI Insights Analyses API Events](#how-ai-insights-analyses-api-events)
3. [From Raw Events to Structured Insights](#from-raw-events-to-structured-insights)
4. [The Investigation Workflow](#the-investigation-workflow)
5. [Example: Investigating an Error Spike](#example-investigating-an-error-spike)
6. [Limitations and Notes](#limitations-and-notes)

## The Problem Determination Challenge

API problem determination typically involves some combination of:


- **Gateway logs**: Backend response times, protocol-level errors
- **Analytics events**: Who called what when, Request counts, error rates per API/plan/application
- **Backend telemetry**: Your own service health metrics
- **Consumer reports**: Often vague — "your API is slow" or "it's not working"

Correlating across all these sources takes time and expertise. Even when you have good tooling, the mental overhead of switching between contexts and building a timeline is significant.

AI Insights in v12.1.1 acts as a first-pass investigator. It ingests the same event data available in API Connect and synthesises a structured narrative: what changed, when, what else was happening at the same time, and what the likely cause is.

## How AI Insights Analyses API Events

When you open the AI Insights panel for a specific API event or set of filtered events, the feature may perform several types of analysis on the filtered analytics data:

### Baseline Comparison
It compares current metrics against historical baselines for the same API, plan, and application. If error rates normally sit at 0.1% and suddenly jump to 5%, it flags that deviation immediately.

### Temporal Correlation
It looks for correlated events across dimensions. For example, if your latency spiked at the same time a specific backend service returned errors, AI Insights surfaces that correlation rather than making you discover it manually.

### Anomaly Classification
It classifies anomalies into categories: backend latency regression, authentication/authorisation issues, rate limit violations, schema validation failures, upstream timeouts, and more. Each classification comes with a confidence score.

### Root Cause Signalling
Based on the event fingerprint, AI Insights attempts to identify the most likely root cause category — not a guaranteed diagnosis, but a strongly informed hypothesis that can direct your investigation.

## From Raw Events to Structured Insights

Here's an illustrative example of how raw event data might be summarised into an AI insight. Imagine your API gateway logs this sequence of events for the `/orders` endpoint:

```
2026-07-12 08:14:23.441 [gateway] HTTP 500 — POST /orders 
  backend_latency=4521ms upstream_timeout
2026-07-12 08:14:25.112 [gateway] HTTP 500 — POST /orders 
  backend_latency=4301ms upstream_timeout
2026-07-12 08:14:27.003 [gateway] HTTP 504 — POST /orders 
  gateway_timeout
```

Raw, this is a sequence of error codes. An AI-generated summary might express it like this:

```
🔴 [CRITICAL] Upstream Service Degradation Detected — /orders

A pattern of backend timeouts has been detected on the /orders endpoint:
- 8 timeout errors (HTTP 500/504) in the past 12 minutes
- Average backend response time: 4,380ms (vs. baseline of 230ms)
- All failures are from POST /orders operations
- Correlated event: Backend /order-service health endpoint returned 
  HTTP 503 at 08:14 UTC

Likely root cause: Upstream order service is overloaded or unreachable.
Recommended actions:
  1. Check order-service pod/container health in your backend cluster
  2. Review recent deployments to order-service
  3. Consider temporary rate limiting on /orders to protect the backend
```

## The Investigation Workflow

Here's how I'd use AI Insights in a real problem determination session:

### Step 1: Consumer Reports an Issue
"Hi, our application is getting errors on the `/payments` endpoint since this morning."

### Step 2: Open AI Insights for `/payments`
Rather than starting from raw logs, I open the API Analytics report for `/payments` with a time range covering "today". Depending on the report, v12.1.1 may expose more event detail than earlier versions, which can make the initial investigation faster. Then I look at the AI Insights panel on top of that.

### Step 3: Read the AI Insight
The AI Insights panel might show something like:
```
⚠️ [WARNING] Validation Error Spike on /payments
POST requests to /payments with content-type application/json 
have returned 400 errors at 3.2x the normal rate since 2026-07-12 06:00 UTC.
Error body analysis: "card_number: must be a 16-digit string" — 
this suggests a schema validation change was published.
```

### Step 4: Validate and Confirm
I check the API definition — yes, a schema update was published at 06:00 UTC. I notify the API consumer that they'll need to update their payload format.

This whole investigation took under 2 minutes instead of 20.

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
