---
layout: post
date: 2026-07-12 15:00:00
categories: APIConnect
title: "Visualizing API Evolution with the Usage Evolution Report in API Connect v12.1.1"
description: "How to use the Usage Evolution Report in API Connect v12.1.1 to track your API portfolio over time and make data-driven decisions."
tags: [APIConnect, APIConnectv12, Analytics, UsageEvolution, APIProgram]
draft: true
author: ["ChrisPhillips", "IBMBob"]
---

If you want to see how API usage changes over time, a point-in-time report is not enough. The **Usage Evolution Report** in API Connect v12.1.1 is intended to show how usage and other metrics move across reporting periods.

This article covers what the report shows, how to access it, and how to use it.

<!--more-->

## Table of Contents

1. [What Is the Usage Evolution Report?](#what-is-the-usage-evolution-report)
2. [Accessing the Report](#accessing-the-report)
3. [Metrics Tracked Across Time Periods](#metrics-tracked-across-time-periods)
4. [Reading the Report: What You're Looking At](#reading-the-report-what-youre-looking-at)
5. [Practical Use Cases](#practical-use-cases)
6. [Using Evolution Data for API Portfolio Decisions](#using-evolution-data-for-api-portfolio-decisions)
7. [Exporting and Integrating Evolution Data](#exporting-and-integrating-evolution-data)

## What Is the Usage Evolution Report?

The Usage Evolution Report is a time-series analytics view in API Connect v12.1.1 that shows how your API programme metrics have changed across defined time periods. Unlike point-in-time reports that show current state, the Evolution Report shows **trends** — the direction and magnitude of change across APIs, products, plans, applications, and consumer organisations.

Think of it as a "before and after" report for your API programme: where were you 3 months ago, where are you today, and what does that trajectory suggest you should do next.

## Accessing the Report

1. Log into **API Manager**
2. Navigate to **Analytics** → **Usage Evolution**
3. Select your **time comparison**: you can compare:
   - **Week over week** (current week vs. previous week)
   - **Month over month** (current month vs. previous month)
   - **Quarter over quarter**
   - **Custom date range** (e.g., last 90 days vs. prior 90 days)
4. Select the **scope**: All APIs, specific API, specific product, specific plan, or specific consumer org
5. The report generates with trend visualisations for each tracked dimension

The report view should show the selected metrics as trends over the chosen comparison window.

## Metrics Tracked Across Time Periods

The Usage Evolution Report tracks changes across five core dimensions:

### 1. APIs

| Metric | Description |
|---|---|
| Total APIs published | Count of unique API definitions with at least one call in the period |
| New APIs | APIs with first call in the current period (newly active) |
| Deprecated/retired APIs | APIs with no calls in the current period that had calls in the prior period |
| API versions | Count of unique API:version combinations |

### 2. Products

| Metric | Description |
|---|---|
| Total products | Products with at least one subscription |
| New products | Products with first subscription in the current period |
| Products with subscriptions | Products that have at least one active subscription |
| Subscription count | Total subscription instances |

### 3. Applications

| Metric | Description |
|---|---|
| Total applications | Applications with at least one API call in the period |
| New applications | Applications making their first API call in the current period |
| Active applications | Applications with calls in both periods (retained) |
| Churned applications | Applications active in prior period with no calls in current period |

### 4. Plans

| Metric | Description |
|---|---|
| Subscriptions by plan | Count of subscriptions broken down by plan |
| Traffic by plan | Total API calls broken down by plan |
| Top plans by growth | Plans ranked by change in traffic volume |

### 5. Consumer Organisations

| Metric | Description |
|---|---|
| Total consumer orgs | Consumer orgs with at least one active subscription |
| New consumer orgs | Org onboarding in the current period |
| Org retention rate | Percentage of orgs active in both periods |
| Top orgs by traffic | Consumer orgs ranked by total API calls |

## Reading the Report: What You're Looking At

The Usage Evolution Report presents data in two main visualisations:

### The Trend Chart

A multi-line chart showing absolute values of selected metrics over time. Each line represents a dimension (APIs, applications, traffic) and you can toggle which to display.

### The Comparison Table

A structured table showing the actual numbers for each metric across the two comparison periods, with:

- **Prior period value**
- **Current period value**
- **Change (absolute)**
- **Change (percentage)**
- **Trend indicator** (↑ growth, ↓ decline, → stable)

Example:

| Metric | Prior (Q1 2026) | Current (Q2 2026) | Change | % Change |
|---|---|---|---|---|
| Total APIs | 47 | 52 | +5 | +10.6% ↑ |
| Active applications | 183 | 201 | +18 | +9.8% ↑ |
| Total traffic (calls) | 12.4M | 15.1M | +2.7M | +21.8% ↑ |
| Consumer orgs | 34 | 38 | +4 | +11.8% ↑ |
| Products with subscriptions | 28 | 29 | +1 | +3.6% ↑ |

## Practical Use Cases

### Use Case 1: Identifying APIs in Decline

You can use the Usage Evolution Report to identify APIs that are showing declining usage — useful for deprecation planning.

Filter the report to show **APIs by traffic volume change** and look for APIs with consistent negative trends over multiple periods. An API that has declined 30%+ over two consecutive quarters is a strong candidate for a deprecation conversation with consumers.

### Use Case 2: Measuring the Impact of a New Product Launch

Compare the two periods surrounding a new product launch to measure:
- New subscriptions on the new product
- New applications calling the new product's APIs
- Whether existing applications are also migrating to the new product

### Use Case 3: Consumer Org Retention Analysis

Compare the consumer org churn rate period over period. A rising churn rate is an early warning sign — it may indicate:
- Poor developer experience
- API quality issues
- Competitor activity

### Use Case 4: Quarterly Business Reviews

Generate the Usage Evolution Report before every QBR (Quarterly Business Review). It gives leadership an instant read on the health and trajectory of the API programme without requiring manual data gathering.

## Using Evolution Data for API Portfolio Decisions

The Usage Evolution Report is most valuable when you use the trends to drive action. Here are some decision patterns:

### API Deprecation Trigger

```
IF: API traffic declined >50% over 2 consecutive quarters
AND: No subscriptions created in the last quarter
THEN: Initiate deprecation review with 6-month sunset notice
```

### Capacity Planning Trigger

```
IF: Traffic growth rate exceeded 30% in a single quarter
AND: No capacity changes were made in the same period
THEN: Review backend capacity and gateway sizing
```

### Consumer Engagement Trigger

```
IF: New consumer org rate declined for 2 consecutive quarters
AND: Application churn rate increased
THEN: Investigate portal experience and onboarding friction
```

## Exporting and Integrating Evolution Data

For deeper analysis, export the data to CSV or pull it programmatically.

### Via the UI (CSV Export)

The Usage Evolution Report has a **Download CSV** button in the top-right of the report view. This is the recommended path for ad-hoc exports and one-off data pulls into spreadsheets or BI tools.

### Via the apic CLI (Analytics Query)

There is no dedicated `analytics:usage-evolution` CLI command. The `apic` CLI's analytics support is via `apic analytics:create`, which submits a query object to the analytics service. To automate periodic exports, create a query file targeting the metrics you need and run it on a schedule:

```bash
# Submit an analytics query via CLI
# analytics-query.yaml contains your query definition (time range, dimensions, filters)
apic analytics:create \
  --server ${MANAGEMENT_SERVER} \
  --org ${PROVIDER_ORG} \
  --catalog ${CATALOG} \
  --scope catalog \
  --analytics-service ${ANALYTICS_SERVICE_NAME} \
  analytics-query.yaml
```

The query file format and available field names are documented in the IBM API Connect REST API reference — the CLI wraps the same analytics query endpoint used by the UI. Consult the [IBM API Connect documentation](https://www.ibm.com/docs/en/api-connect/software/12.1.1) for the analytics query schema for your version.

### Scheduled Export Pattern

For recurring exports (e.g., a monthly QBR data pull), wrap the `apic analytics:create` call in a cron job or CI pipeline step. Store credentials in your secrets manager and output the result to a file or pipe it to your data warehouse ingestion tooling.

## Summary

The Usage Evolution Report in API Connect v12.1.1 gives you the longitudinal view your API programme needs. Whether you're managing deprecation, planning capacity, reporting to leadership, or understanding consumer behaviour, tracking the evolution of your API portfolio over time transforms raw analytics into strategic intelligence.

Make it a habit to review the Usage Evolution Report at the start of each quarter — you'll spot trends earlier and make better API portfolio decisions as a result.

