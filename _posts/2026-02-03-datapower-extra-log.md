---
layout: post
categories: APIConnect
date: 2026-02-03 00:14:00
title: "Essential DataPower Logging when using API Connect: 5 Critical Log Types for Production Monitoring"
author: ["ChrisPhillips"]
description: "A practical guide to the five most important logging configurations for IBM DataPower in production environments, including system usage, API synchronization, and performance monitoring."
tags: [DataPower, Logging, Monitoring, APIConnect, Performance, Troubleshooting]
draft: true
---

When configuring IBM DataPower for production, proper logging is essential for troubleshooting, performance monitoring, and capacity planning. This guide covers five critical logging types that every DataPower deployment should have enabled.

<!--more-->

## 1. Why These Logs Matter

In production environments, you need visibility into:
- System resource utilization
- API synchronization between API Manager and DataPower
- Transaction latency and performance
- Detailed system metrics for capacity planning

These five log types provide comprehensive coverage without overwhelming your logging infrastructure.

## 2. Quick Reference: The 5 Essential Logs

| Log Type | Purpose | When to Use | Collection Method | Storage Impact |
|----------|---------|-------------|-------------------|----------------|
| [**System Usage Table**](#3-system-usage-table) | Real-time resource monitoring | Continuous monitoring | REST/SOMA API query | Low |
| [**Gateway Director (GWD)**](#4-gateway-director-gwd-logs) | API sync communication | Troubleshooting sync issues | Log target: `apic-gw-service debug` | Low |
| [**Collection Log**](#5-collection-log) | DataPower object creation | Troubleshooting config issues | Log targets: `cli debug` and `mgmt info` | Low |
| [**dpMon**](#6-dpmon-datapower-monitoring) | Detailed system metrics | Capacity planning & deep analysis | File collection every 2 hours | High  |
| [**ExtLatency**](#7-extlatency-extended-latency) | Transaction latency breakdown | Performance troubleshooting | Log target: `extlatency info` | Medium-High |

---

## 3. System Usage Table

**What It Does:**
Provides real-time visibility into DataPower's current workload and resource utilization.

**Key Metrics to Collect:**
- **Load Percentage** - Overall system load
- **CPU Percentage** - CPU utilization
- **Worklist** - Number of tasks awaiting scheduling
- **File Count** - Open file handles

**How to Access:**
Available via REST or SOMA interface. Query this table periodically (every 30-60 seconds) to track system health.

**Why It Matters:**
When your gateway starts queuing requests or experiencing performance issues, the System Usage Table shows you exactly what's happening at the system level.

**Example REST Query:**
```bash
curl -k -u admin:password \
  https://datapower-host:5554/mgmt/status/default/SystemUsageTable
```

## 4. Gateway Director (GWD) Logs

**What It Does:**
Captures communication between API Manager and DataPower, showing API synchronization activity.

**Configuration:**

Create a log target with the following subscription:
```
event apic-gw-service debug
```

**Kubernetes Best Practice:**
In containerized environments, send this to the default log in the default domain so Kubernetes can collect it as part of pod logs:

```bash
kubectl logs <datapower-pod-name> -n <namespace>
```

**Why It Matters:**
When APIs aren't syncing properly or you're seeing unexpected behavior after publishing, GWD logs show you exactly what's happening during the synchronization process.

**What to Look For:**
- API publish/unpublish events
- Synchronization errors
- Communication failures between API Manager and gateway

**Note:** This is enabled by default in container deployments.

## 5. Collection Log

**What It Does:**
Tracks the creation and modification of DataPower objects during API synchronization.

**Configuration:**

Create a log target with these subscriptions:
```
event cli debug
event mgmt info
```

**Kubernetes Best Practice:**
Send to the default log in the default domain for pod log collection.

**Why It Matters:**
Shows you the actual DataPower configuration changes being made when APIs are published. Essential for troubleshooting configuration issues.

**What to Look For:**
- Object creation/deletion events
- Configuration changes
- Errors during object creation
- Policy assembly modifications

**Use Case:**
When an API publishes successfully in API Manager but doesn't work in the gateway, Collection logs show you if the DataPower objects were created correctly.

## 6. dpMon (DataPower Monitoring)

**What It Does:**
Generates nmon-format snapshot files containing detailed system metrics.

**Default Configuration:**
- **Snapshot Duration:** 900 seconds (15 minutes) per file
- **Rotation:** 9 files
- **Total Coverage:** ~2.25 hours of detailed metrics

**Collection Strategy:**

For debugging or capacity analysis, copy files every 2 hours:

```bash
# Kubernetes environment
kubectl cp <namespace>/<pod-name>:temporary/dpmon/dpmon_*.nmon ./dpmon-files/

# Direct DataPower access
scp admin@datapower-host:temporary/dpmon/dpmon_*.nmon ./dpmon-files/
```

**Why It Matters:**
dpMon provides the most detailed system metrics available, including:
- CPU usage per core
- Memory utilization
- Disk I/O
- Network statistics
- Process-level details

**Analysis:**
Use nmon analyzer tools to visualize the data and identify performance patterns, bottlenecks, and capacity issues.

**Storage Consideration:**
These files are large. Only collect them during active debugging or capacity analysis periods, not continuously in production.

## 7. ExtLatency (Extended Latency)

**What It Does:**
Provides detailed latency breakdown for every transaction, showing exactly where time is spent.

**Configuration:**

Create a log target with these subscriptions:
```
event extlatency info
event memory-report debug
```

**Why Include Memory Report:**
Memory issues often correlate with performance problems. Having both latency and memory data together helps identify root causes faster.

**Kubernetes Best Practice:**
Send to the default log in the default domain for pod log collection.

**What You Get:**

ExtLatency logs show time spent in each processing stage:
- Request parsing
- Policy execution
- Backend calls
- Response processing
- Total transaction time

**Example Log Entry:**
```
[extlatency][info] tid(12345) gtid(67890) org(myorg) api(myapi) 
  total=145ms parse=2ms policy=15ms backend=120ms response=8ms
```

**Why It Matters:**
When users report slow APIs, ExtLatency tells you exactly where the time is going. Is it your backend? Policy execution? Network latency?

**Use Case:**
- Performance troubleshooting
- SLA monitoring
- Capacity planning
- Identifying slow backends

## 8.  Create Log Targets

For each log type (except System Usage Table and dpMon), create a log target:

**Via CLI:**
```
configure terminal
logging target <target-name>
  type file
  format text
  timestamp zulu
  size 100
  local-file logtemp:///<filename>
  event <subscription>
exit
```

**Via WebGUI:**
1. Navigate to Objects → Logging → Log Target
2. Click "Add"
3. Configure target with appropriate event subscriptions



## 9. Log Rotation and Retention

**Best Practices:**

| Log Type | Rotation | Retention | Storage Impact |
|----------|----------|-----------|----------------|
| GWD | 10 MB or daily | 7 days | Low |
| Collection | 10 MB or daily | 7 days | Low |
| ExtLatency | 50 MB or daily | 3 days | Medium-High |
| dpMon | Automatic (9 files) | Copy every 2 hours | High  |
| System Usage | N/A (API query) | Store in monitoring system | Low |

**Storage Calculation:**

For a busy gateway processing 1000 TPS:
- ExtLatency: ~500 MB/day
- GWD + Collection: ~100 MB/day
- dpMon: ~50 MB/hour 

Plan storage accordingly, especially for ExtLatency in high-traffic environments.

## 10. Monitoring and Alerting

**Key Metrics to Alert On:**

From **System Usage Table:**
- CPU > 80% for 5 minutes
- Worklist > 100 consistently
- Load percentage > 90%

From **ExtLatency:**
- Average latency > SLA threshold
- Backend latency > expected baseline
- Sudden latency spikes

From **GWD/Collection Logs:**
- Synchronization failures
- Object creation errors
- Communication timeouts

## 11. Troubleshooting Common Issues

### 11.1. High CPU with Low Throughput

**Check:**
1. System Usage Table - Look at worklist
2. ExtLatency - Identify slow transactions
3. dpMon - Analyze CPU usage patterns

**Common Causes:**
- GatewayScript bottlenecks
- Inefficient policies
- Memory pressure causing swapping

### 11.2. API Sync Failures

**Check:**
1. GWD logs - Communication errors
2. Collection logs - Object creation failures

**Common Causes:**
- Network connectivity issues
- Certificate problems
- Insufficient permissions

### 11.3. Intermittent Slowness

**Check:**
1. ExtLatency - Identify timing patterns
2. dpMon - Correlate with system metrics
3. System Usage Table - Look for resource spikes

**Common Causes:**
- Backend performance issues
- Garbage collection pauses
- Network congestion

## 12. Best Practices Summary

1. **Enable all five log types** in production environments
2. **Use Kubernetes pod logs** for containerized deployments
3. **Set up automated collection** for System Usage Table
4. **Configure appropriate retention** based on your storage capacity and requirements
5. **Monitor key metrics** and set up alerts
6. **Correlate logs** when troubleshooting - use multiple log types together

## 13. Conclusion

These five logging configurations provide comprehensive visibility into your DataPower environment without overwhelming your logging infrastructure. By implementing them properly, you'll have the data you need to:

- Troubleshoot issues quickly
- Monitor performance proactively
- Plan capacity accurately
- Meet SLA requirements

Start with these five, tune retention based on your needs, and you'll have a solid foundation for DataPower observability.

---

*Questions about DataPower logging? Drop a comment below or reach out directly.*
