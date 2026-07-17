---
layout: post
date: 2026-07-15 09:00:00
categories: APIConnect
title: "AI Insights for Analytics Reports in IBM API Connect v12.1.1"
description: "Discover how AI Insights transforms raw API analytics data into actionable intelligence within the API Connect reporting experience."
tags: [APIConnect, APIConnectv12, Analytics, AIInsights, Reporting]
author: ["ChrisPhillips", "IBMBob"]
---

API Connect analytics reports show a lot of data, but the harder part is understanding what it means. AI Insights is intended to help with that by turning report data into short explanations and recommendations.

This article covers what AI Insights is, where it appears in reporting, and the kind of output it can provide.

<!--more-->

## What is AI Insights?

AI Insights is embedded in the API Connect v12.1.1 analytics reporting framework. Instead of presenting raw event counts and charts for you to interpret, it analyses your API traffic patterns, error distributions, latency trends, and subscription behaviour, then generates natural-language summaries and recommended actions.

## How It Works in the Reporting Experience

When you open any analytics report in API Connect v12.1.1 — API Usage, Application Activity, Plan Performance — an **AI Insights** panel appears at the top of the report view. It generates on demand based on the current filter context: time range, API, plan, application.

The panel analyses:
- Historical baseline metrics for the same API/plan/application
- Cross-dimensional correlations (error spikes against specific time windows or backend latencies)
- Historical behaviour visible in the analytics dataset

Results appear as a scrolling list of insight cards, each with a plain-language title, a severity indicator (Info, Warning, Critical), a brief explanation, and a recommended action where applicable.

## Practical Examples

Here are examples of the kind of insight AI Insights can generate:

### Elevated Error Rate

```
⚠️ [WARNING] Elevated 5xx Error Rate on /payments/refund
Detected: 5xx errors increased by 340% compared to the 7-day baseline
(from avg 0.3% to 13.2%) starting 2026-07-10 14:00 UTC.
Likely cause: Backend service latency spike detected on the same timeline.
Recommended: Check backend /payments service health and recent deployments.
```

### Unusual Application Traffic

```
ℹ️ [INFO] Traffic Spike for Application "mobile-banking-app"
Detected: Outbound call volume exceeded 2x its typical daily peak
at 2026-07-11 09:15 UTC. Coincides with a referrer pattern shift.
Consider: Reviewing rate limit configuration for this plan.
```

### Orphaned Subscriptions

```
ℹ️ [INFO] Plan "/standard" subscriptions have migrated
23% of applications on the /standard plan have not called any API
operation in 14+ days. These subscriptions may be orphaned.
Recommended: Review subscription health as part of your quarterly API review.
```

### Latency Regression

```
🔴 [CRITICAL] P99 Latency Regression on /forex/rates
P99 latency increased from ~120ms to ~2.1s over the past 48 hours — a 17x degradation.
Affected: 1,240 requests in the past hour.
Recommended: Investigate backend service changes, database query performance,
or network path changes immediately.
```

## Accessing AI Insights

1. Log into **API Manager**
2. Navigate to **Analytics** → **[Select Report Type]**
3. Apply your filters (time range, API, plan, application)
4. The **AI Insights** panel appears at the top of the report

## Requirements

- **Minimum version**: API Connect v12.1.1.0 (GA June 2026). Not available in earlier v12 releases.
- **Analytics data required**: Needs at least 7 days of traffic to establish baselines — won't generate insights on a new installation.
- **Not real-time alerting**: Insights are generated when you open a report, not pushed proactively. For real-time alerting, use the Alerts configuration in API Manager.
- **Deployment-specific**: Exact availability and runtime dependencies vary by deployment model and entitlement. Check IBM documentation for your environment before relying on the feature.
- **Interpretive, not deterministic**: Always validate against your actual systems before acting on a recommendation.

---
*Next: "Simplify API Problem Determination with AI Insights" — using AI Insights during a live incident investigation.*
