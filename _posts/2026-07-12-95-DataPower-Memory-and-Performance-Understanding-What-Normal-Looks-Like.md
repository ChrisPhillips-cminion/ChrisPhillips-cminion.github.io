---
layout: post
date: 2026-07-12 18:07:00
categories: [DataPower]
title: "DataPower Memory and Performance: Understanding What Normal Looks Like (Before You Open a Ticket)"
description: "A practical guide to DataPower memory and CPU performance covering normal baselines, leak detection, CPU spike analysis, and performance troubleshooting triage."
tags: [DataPower, Performance, Memory, Troubleshooting, Firmware]
draft: true
---

"50% memory usage and rising — is this normal?" is a question I get a lot, usually preceded by "We've had the appliance for six months and we've never seen it this high." The answer is almost always "it depends" — but "it depends" is not a satisfying answer when you're looking at a DataPower at 2am and trying to decide whether to open a severity-1 with IBM.

A good example of why comparing raw memory percentages between HA pair appliances is misleading: the secondary appliance showed consistently higher memory usage than the primary — same firmware version, same traffic pattern, same configuration. We had screenshots of both appliances' memory dashboards and were preparing to open a ticket about the secondary. When we looked at it properly, both appliances were within normal parameters for their firmware version and traffic load. The apparent difference was because the secondary had been running for a longer period since its last restart, while the primary had been restarted during a recent maintenance window. The baseline was simply different.

This article is about knowing what normal looks like for your specific environment, so you can tell the difference between expected growth and a genuine problem.

## 1. How DataPower Allocates Memory

DataPower's memory is divided into several regions:

- **Firmware-reserved memory:** The operating system and DataPower firmware services reserve a portion of total memory. This is not available for application use.
- **Domain memory:** Each DataPower domain has its own memory allocation. Domains process API traffic and run configurations.
- **Application buffers:** DataPower uses buffers for XML parsing, JSON processing, HTTP connection handling, and XSLT transformations. These are allocated from a shared buffer pool.
- **Compilation cache:** GatewayScript and XSLT compiled code is cached. More traffic means more compiled code in cache, which means more memory used.

**What this means for comparing HA pairs:** The raw percentage reported by `show memory` on each appliance is the percentage of installed memory in use across the whole system. Because the two appliances in an HA pair may have different uptime (and therefore different cache/buffer fill levels), their reported percentages will naturally differ even under identical traffic loads. The Abu Dhabi case demonstrated this exactly.

**Key metrics from `show memory` (DataPower CLI):**

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

The number to watch is **Available memory** trending over time — if it decreases consistently day-over-day without corresponding traffic growth, you may have a memory leak. Note that `show memory` shows system-level memory, not per-domain breakdown; per-domain stats are in the error report's `DomainStatusObject`.

## 2. Normal Memory Growth vs. Genuine Memory Leak

Memory growth in DataPower is expected in three scenarios:

**Expected growth:**
- New APIs deployed → new domain configurations loaded → more domain memory
- Traffic growth → more application buffers allocated
- Longer uptime → larger compilation cache

**Leak indicators:**
- **Available memory** (from `show memory`) decreases by more than 10% per day with no change in traffic or configuration
- A specific domain's memory allocation grows continuously without plateauing
- After restarting the domain (without restarting the appliance), memory does not return to baseline

**Diagnosing with error report:**

The DataPower error report is a directory of XML status files. Generate one with:

```bash
generate error-report
```

The relevant files for memory leak diagnosis are:

- **`DomainsMemoryStatus2.xml`** — per-domain memory tracking. Fields include `ServicesCurrent`, `ServicesOneMinute` through `ServicesOneDay`, `DocumentCaches`, `StylesheetCaches`. Watch `ServicesOneDay` growing relative to `ServicesCurrent` — sustained growth without traffic growth indicates a leak.
- **`MemoryStatus2.xml`** — system-level memory snapshot (`Usage`, `AvailableMemory`, `UsedMemory`, `TotalMemory`).
- **`DocumentCachingSummary.xml`** — per-XMLManager document cache stats (`DocCount`, `CacheSizeKiB`).
- **`StylesheetCachingSummary2.xml`** — per-XMLManager stylesheet cache stats (`CacheCount`, `CacheKBCount`).

**Example `DomainsMemoryStatus2.xml` entry:**

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

If `ServicesLifetime` is growing steadily while `ServicesCurrent` is stable and traffic is flat, you likely have a memory leak in that domain's configuration or GatewayScript code.

## 3. CPU Spikes: Three Most Common Causes

**Cause 1: Burst traffic**

A sudden increase in API traffic — a batch job starting, a traffic spike from a partner system — will cause CPU to spike as DataPower processes the incoming requests. This is expected behaviour.

**Diagnosis:** Correlate the CPU spike with request logs showing increased traffic volume. If the spike lasts exactly as long as the burst and then subsides, this is normal.

**Cause 2: Large payload processing**

Processing multi-megabyte XML or JSON payloads (common in B2B integrations, file transfer APIs) causes brief CPU spikes as DataPower parses, validates, and transforms the content. The larger the payload, the more CPU consumed.

**Diagnosis:** Use `show statistics` to check global connection counts and payload processing metrics — note this is a global view, not per-domain. Large request volumes correlating with the spike confirm payload-driven CPU usage. This is expected for large payloads but can become a problem if partners start sending payloads larger than your configured limits.

**Cause 3: First-call XSLT/GatewayScript compilation**

The first time an XSLT stylesheet or GatewayScript module is executed after a domain restart, it must be compiled. This compilation is CPU-intensive. Subsequent calls use the cached compiled version and are significantly faster.

**Diagnosis:** If CPU spikes correlate with a domain restart, an XSLT or GatewayScript deployment, or an API product publish, this is almost certainly first-call compilation. It should only happen once. If it happens repeatedly, the compilation cache may be too small.

**Collecting CPU data for IBM support cases:**

IBM support often asks for CPU screenshots — the pattern is well-established. The Abu Dhabi team attached screenshots of their HA pair CPU graphs showing sustained elevated CPU, which helped identify a genuine performance issue rather than burst traffic.

For a support case, collect:

```bash
# Firmware version (include in every support case)
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

> **Note:** `show statistics` and `show cpu` are global commands — they do not accept a `domain` parameter. Per-domain memory metrics are in the error report's `DomainsMemoryStatus2.xml`, not via a CLI `show` command.

## 4. Collecting Right Diagnostic Data for Performance Issues

Before opening a performance support case, collect:

**Object and statistics from error report:**

```bash
# Generate error report
generate error-report

# Key files to inspect in the error report directory:
# - MemoryStatus2.xml          — system memory (Usage, AvailableMemory, UsedMemory, TotalMemory)
# - DomainsMemoryStatus2.xml   — per-domain memory (ServicesOneDay, ServicesLifetime, DocumentCaches)
# - SystemUsage.xml            — CPU load (Load field, 0-100 scale)
# - DocumentCachingSummary.xml — document cache per XMLManager (DocCount, CacheSizeKiB)
# - StylesheetCachingSummary2.xml — stylesheet cache per XMLManager (CacheCount, CacheKBCount)
# - HTTPConnections.xml        — HTTP connection pool stats per XMLManager (reqTenSec through reqOneDay)
```

**Key DataPower CLI commands:**

```bash
# Memory summary (system-level: available, used, reserved, total)
show memory

# Global connection count (included in show statistics output)
show statistics

# CPU usage intervals (10s / 1m / 10m / 1h / 24h)
show cpu

# For per-domain memory and request metrics, generate an error report:
generate error-report
# Then inspect DomainsMemoryStatus2.xml for per-domain memory counters.
# Per-domain memory breakdown is not available via a single CLI show command.
```

> **Note:** `show domain-memory`, `show connections` (as a standalone command), `show cpu domain all`, and `show xml-managers` are not separate CLI commands. Use `show statistics` for global connection counts, `show cpu` for CPU intervals, and the error report files (`DomainsMemoryStatus2.xml`, `HTTPConnections.xml`) for per-domain and connection pool detail.

## 5. Performance Tuning Levers

**Document cache sizing:**

The document cache controls how many compiled stylesheets and parsed documents DataPower retains in memory. Configure it via the WebGUI under **Objects → XML Manager → [your XML manager] → Document Cache** or via the DataPower CLI in the relevant domain context. The key settings to tune are maximum number of cached entries and the TTL for cache expiry. If you observe high first-call latency but low subsequent latency, the cache size may be too small. If memory is growing without traffic growth, the TTL may be too long.

**Connection pool configuration:**

Connection pool settings (max connections, idle timeout, connection timeout) are configured per Multi-Protocol Gateway or HTTP Front Side Handler in the WebGUI or CLI. The defaults are tuned for balanced workloads. Only adjust these with specific evidence that pool exhaustion is occurring — look for `connection refused` or `connection pool full` errors in the DataPower log.

**Thread count — caveat on defaults:**

DataPower's default thread count is tuned for a balanced workload. Increasing thread counts beyond firmware-recommended values can actually decrease performance by causing excessive context switching. Do not change thread count without IBM guidance.

## 6. Triage Checklist: Five Questions Before Opening a Support Case

Answer these before you call IBM:

1. **Is the appliance still processing traffic?** If yes, is performance degraded or is it fully functional? Note exact response times before and after the issue started.
2. **What changed immediately before the issue started?** New API deployed? Firmware upgraded? Configuration change? Traffic pattern change?
3. **Is the issue on one appliance or both in an HA pair?** If only one, is it the primary or secondary? What does HA status show?
4. **Is Available memory (from `show memory`) decreasing consistently day-over-day, or has it plateaued?** Provide a graph of memory usage over at least 48 hours.
5. **What error messages appear in the DataPower logs?** Export the relevant log entries for the problem period. Never describe errors — show them.

Having these five answers ready when you call IBM support will dramatically accelerate the case resolution. Screenshots of CPU and memory graphs (as IBM support asked for in the Abu Dhabi case) are worth more than written descriptions.

