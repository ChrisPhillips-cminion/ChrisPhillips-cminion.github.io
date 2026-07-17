---
layout: post
date: 2026-07-12 18:07:00
categories: [DataPower]
title: "DataPower Memory and Performance: Understanding What Normal Looks Like (Before You Open a Ticket)"
description: "A practical guide to DataPower memory and CPU performance covering normal baselines, leak detection, CPU spike analysis, and performance troubleshooting triage."
tags: [DataPower, Performance, Memory, Troubleshooting, Firmware]
draft: true
author: ["ChrisPhillips", "IBMBob"]
---

Rising memory on a DataPower appliance is not automatically a problem — but knowing whether it is requires understanding what the numbers actually mean.

![CPU Sample graph](/images/cpu.png)


<!--more-->

Comparing raw memory percentages between HA pair appliances is misleading. Two appliances with identical firmware and configuration can show different memory usage simply because one has been running longer or has a warmer cache.

## 1. How DataPower Allocates Memory

DataPower divides memory into several regions:

- **Firmware-reserved:** The OS and DataPower firmware services reserve a fixed portion. It is not available for application use.
- **Domain memory:** Each domain has its own chunk. Domains process API traffic and hold configurations.
- **Application buffers:** Used for XML parsing, JSON processing, HTTP connection handling, and XSLT transformations. Allocated from a shared buffer pool.
- **Compilation cache:** GatewayScript and XSLT compiled code is cached in memory. More traffic means more compiled code, which means more memory used.

The `show memory` output from the CLI:

```
DataPower# show memory

Memory usage:      62%
Installed memory:  8388608 KB
Available memory:  3145728 KB
Used memory:       5242880 KB
Reserved memory:   1048576 KB
Total memory:      7340032 KB
Requested memory:  4915200 KB
Hold memory:       131072 KB
```

Watch **Available memory** trending over time. If it decreases consistently day-over-day without corresponding traffic growth, that is a memory leak. Note that `show memory` is system-level — per-domain breakdown is in the error report's `DomainStatusObject`.

## 2. Normal Memory Growth vs. Genuine Memory Leak

Expected growth happens in three scenarios:

- New APIs deployed → new domain configurations loaded → more domain memory
- Traffic growth → more application buffers allocated
- Longer uptime → larger compilation cache

Leak indicators:

- **Available memory** drops by more than 10% per day with no change in traffic or configuration
- A specific domain's memory allocation grows continuously without plateauing
- After restarting the domain (not the appliance), memory does not return to baseline

**Diagnosing with an error report:**

Generate one with:

```bash
generate error-report
```

Relevant files for memory leak diagnosis:

- **`DomainsMemoryStatus2.xml`** — per-domain memory. Watch `ServicesOneDay` growing relative to `ServicesCurrent` with flat traffic — that is a leak.
- **`MemoryStatus2.xml`** — system-level snapshot (`Usage`, `AvailableMemory`, `UsedMemory`, `TotalMemory`).
- **`DocumentCachingSummary.xml`** — per-XMLManager document cache (`DocCount`, `CacheSizeKiB`).
- **`StylesheetCachingSummary2.xml`** — per-XMLManager stylesheet cache (`CacheCount`, `CacheKBCount`).

Example `DomainsMemoryStatus2.xml` entry:

```xml
<DomainsMemoryStatus2>
  <Domain>apiconnect</Domain>
  <ServicesCurrent>0</ServicesCurrent>
  <ServicesOneMinute>0</ServicesOneMinute>
  <ServicesFiveMinutes>0</ServicesFiveMinutes>
  <ServicesTenMinutes>0</ServicesTenMinutes>
  <ServicesOneHour>0</ServicesOneHour>
  <ServicesTwelveHours>0</ServicesTwelveHours>
  <ServicesOneDay>0</ServicesOneDay>
  <ServicesLifetime>0</ServicesLifetime>
  <DocumentCaches>0</DocumentCaches>
  <StylesheetCaches>0</StylesheetCaches>
</DomainsMemoryStatus2>
```

If `ServicesLifetime` is growing steadily while `ServicesCurrent` is stable and traffic is flat, you have a memory leak in that domain's configuration or GatewayScript code.

## 3. CPU Spikes: Three Most Common Causes

**Cause 1: Burst traffic**

A sudden increase in API calls — a batch job starting, a partner system spiking — will drive CPU up as DataPower processes the requests. Correlate the spike with request logs showing increased traffic volume. If it subsides when the burst ends, it is normal.

**Cause 2: Large payload processing**

Multi-megabyte XML or JSON payloads (common in B2B and file transfer APIs) cause brief CPU spikes during parsing, validation, and transformation. Use `show statistics` to check global connection counts and correlate with the spike. This is expected for large payloads, but becomes a problem if partners start sending payloads above your configured limits.

**Cause 3: First-call XSLT/GatewayScript compilation**

The first call after a domain restart or a new deployment compiles XSLT stylesheets and GatewayScript modules. Compilation is CPU-intensive. Subsequent calls use the cached version and are significantly faster. If the spike happens once and does not recur, this is the cause. If it happens repeatedly, the compilation cache is too small.

**Collecting CPU data for a support case:**

```bash
# Firmware version — include in every support case
show version

# System identity, serial number, uptime
show system

# Global statistics (CPU over 10s/1m/10m/1h/24h, connection counts,
# memory, stylesheet compilation times) — requires statistics collection enabled
show statistics

# CPU usage intervals (10s / 1m / 10m / 1h / 24h)
show cpu

# Current memory usage (system-level)
show memory
```

> **Note:** `show statistics` and `show cpu` are global commands — they do not accept a `domain` parameter. Per-domain memory metrics are in the error report's `DomainsMemoryStatus2.xml`.

## 4. What to Collect Before Opening a Performance Support Case

```bash
# Generate error report
generate error-report

# Key files to inspect:
# - MemoryStatus2.xml              — system memory (Usage, AvailableMemory, UsedMemory, TotalMemory)
# - DomainsMemoryStatus2.xml       — per-domain memory (ServicesOneDay, ServicesLifetime, DocumentCaches)
# - SystemUsage.xml                — CPU load (Load field, 0–100 scale)
# - DocumentCachingSummary.xml     — document cache per XMLManager (DocCount, CacheSizeKiB)
# - StylesheetCachingSummary2.xml  — stylesheet cache per XMLManager (CacheCount, CacheKBCount)
# - HTTPConnections.xml            — HTTP connection pool stats (reqTenSec through reqOneDay)
```

```bash
show memory
show statistics
show cpu
generate error-report
# Then inspect DomainsMemoryStatus2.xml for per-domain memory counters.
```

> **Note:** `show domain-memory`, `show connections`, `show cpu domain all`, and `show xml-managers` are not valid standalone CLI commands. Use `show statistics` for global connection counts, `show cpu` for CPU intervals, and the error report for per-domain detail.

## 5. Performance Tuning Levers

**Document cache sizing:**

Configure via **Objects → XML Manager → [your XML manager] → Document Cache** in the WebGUI, or via the CLI in the relevant domain context. Tune the maximum number of cached entries and the TTL. High first-call latency with low subsequent latency means the cache is too small. Memory growing without traffic growth means the TTL is too long.

**Connection pool configuration:**

Set per Multi-Protocol Gateway or HTTP Front Side Handler. The defaults are tuned for balanced workloads. Only change them if you have evidence of pool exhaustion — look for `connection refused` or `connection pool full` errors in the DataPower log.

**Thread count:**

Do not change thread count without IBM guidance. Increasing beyond firmware-recommended values can decrease performance through excessive context switching.

## 6. Five Questions Before You Call IBM

1. Is the appliance still processing traffic? If yes, are response times degraded or is it fully functional? Get the exact numbers before and after.
2. What changed immediately before the issue started? New API, firmware upgrade, configuration change, traffic pattern change?
3. Is the issue on one appliance or both in the HA pair? If one, is it primary or secondary? What does HA status show?
4. Is Available memory decreasing consistently day-over-day, or has it plateaued? Provide a graph over at least 48 hours.
5. What error messages appear in the DataPower logs? Export the relevant entries. Never describe errors — show them.

Screenshots of CPU and memory graphs are worth more than written descriptions.
