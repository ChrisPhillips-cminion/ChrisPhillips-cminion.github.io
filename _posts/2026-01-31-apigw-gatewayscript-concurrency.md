---
layout: post
date: 2026-01-31 01:00:00
categories: APIConnect
title: "Mastering GatewayScript Bottlenecks: Performance Optimization for IBM API Gateway"
author: ["ChrisPhillips", "IvanH"]
description: "A comprehensive guide to understanding GatewayScript engines, CPU cores, and concurrency in IBM API Gateway. Learn how to calculate capacity, identify bottlenecks, and optimize for high-performance API deployments."
tags: [APIConnect, DataPower, GatewayScript, Performance, Optimization, Concurrency]
draft: true
---

Your API Gateway is slow under load. GatewayScript engines are maxed out. Requests are queuing. Sound familiar?

Understanding the relationship between GatewayScript engines, CPU cores, and concurrent execution is crucial for building high-performance API solutions. This guide cuts through the complexity with battle-tested formulas and real-world recommendations for handling high-concurrency scenarios.

<!--more-->

## Key Takeaways

Understanding the relationship between GatewayScript engines, CPU cores, and concurrency is essential for building high-performance API solutions:

1. **Engine count determines concurrent execution capacity** (1 core = 1 engine = 1 concurrent execution)
2. **CPU cores provide the processing power for engines**
3. **The ratio is always 1:1** (one CPU core to one engine)
4. **For high concurrency, consider dedicated gateway services**
5. **Use GatewayScript strategically** - only when necessary
6. **Monitor, measure, and tune based on actual workload**

---

## 1. The Fundamentals: Engines, Cores, and Concurrency

### 1.1 The Simple Truth

IBM API Gateway uses GatewayScript engines to execute custom logic. Here's what you need to know:

```
1 CPU Core = 1 GatewayScript Engine = 1 Concurrent Execution
```

If you have 8 CPU cores assigned to your gateway, you get 8 GatewayScript engines, which means 8 concurrent GatewayScript executions maximum.

When All Engines Are Busy, they wait for an engine to become available. This is your bottleneck.

### 1.2 The Two Types of Concurrency (Don't Confuse Them!)

**1. Total Gateway Concurrency**
- ALL transactions actively being processed
- Includes routing, transformation, backend calls, GatewayScript, everything
- Formula: `TPS × Total Latency`

**2. GatewayScript Engine Concurrency**
- ONLY transactions executing GatewayScript code
- This is what hits your engine limit
- Check with: `show gatewayscript-status` (In-use run times)

**Example:**
```
Total Gateway Concurrency:     50 transactions
GatewayScript Concurrency:      8 transactions
```

Translation: 50 requests are in-flight, but only 8 are using GatewayScript engines. The other 42 are doing other things (backend calls, routing, etc.).

If GatewayScript concurrency approaches your engine count while total concurrency is low, GatewayScript is your bottleneck. Time to optimize or scale.

## 2. Capacity Planning: How Many Engines Do You Need?

### 2.1 The Formula

```
Required Engines = Expected TPS × GatewayScript Execution Time (seconds)
```

**Example:**

You expect 200 TPS and your GatewayScript takes 25ms per transaction:

```
Required Engines = 200 × 0.025 = 5 engines minimum
```

**Add a Buffer:**

Always add 20-30% for peak loads and failover:
```
Production Engines = 5 × 1.25 = 6-7 engines (round up to 7)
```

### 2.2 Calculating Current Concurrency

Use data from `show http` to understand your current load:

**Example:**
- Throughput: 100 TPS
- Mean Transaction Time: 50ms

```
Total Concurrency = 100 TPS × 0.050 seconds = 5 concurrent transactions
```

**Important:** Convert milliseconds to seconds before multiplying!

**Where to Get the Data:**
- Latency: `show http` or ExtLatency logs
- GatewayScript execution time: Include any synchronous backend calls made within GatewayScript


## 3. Monitoring: Know Your Numbers

Before you can optimize, you need to measure. Here are the key commands:

### 3.1 Check GatewayScript Engine Status

```bash
top; co; show gatewayscript-status
```

**What to Look For:**

```
Available run times: 8    ← Total engines configured
   In-use run times: 7    ← Currently executing (this is your concurrency!)
        Queued work: 15   ← Requests waiting (RED FLAG!)
   Runtime failures: 0    ← Errors in GatewayScript execution
```

**Red Flags:**
- **Queued work > 0**: Engines are maxed out, requests are waiting
- **In-use approaching Available**: You're hitting capacity
- **Runtime failures > 0**: GatewayScript errors need investigation

### 3.2 Check CPU Utilization

```bash
top; co; show cpu
```

**Sample Output:**

```
                  10 s    1 min   10 min    1 hr    1 day
cpu usage (%):      85       80       75      70       65
```

**Guidelines:**
- **< 70%**: Healthy
- **70-80%**: Monitor closely
- **> 80%**: Time to scale

### 3.3 Check HTTP Transactions and Latency

```bash
top; co; switch <domain>; show http
```

**Sample Output:**

```
HTTP transactions/second:
 Service type  Service name  10 s  1 min  10 min
 apiGateway    apiconnect    200   195    180

HTTP mean transaction times (msec):
 Service     Proxy       10 s  1 min  10 min
 apiGateway  apiconnect   45    48     50
```

**Calculate Total Concurrency:**
```
Total Concurrency = 200 TPS × 0.045s = 9 concurrent transactions
```

### 3.4 Putting It All Together: Diagnosing Bottlenecks

Run all three commands and analyze the results together:

**Example Health Check:**

```
Command: show cpu
Result:  CPU Usage = 85%                    ← High, approaching limit

Command: show http
Result:  TPS = 200, Latency = 45ms
Calc:    Total Concurrency = 9 transactions ← Overall gateway load

Command: show gatewayscript-status
Result:  Available Engines = 8              ← Maximum capacity
         In-use Engines = 8                 ← All engines busy!
         Queued Work = 12                   ← Requests waiting (RED FLAG!)
```

**Diagnosis:**

GatewayScript is the bottleneck. All 8 engines are in use, 12 requests are queuing, and CPU is at 85%. The gateway can handle 9 total concurrent transactions, but GatewayScript can only handle 8 concurrent executions.

**Solutions (in order of preference):**

1. **Optimize GatewayScript code** - Reduce execution time
2. **Replace with non-engine policies** - XSLT, Set Variable, or Switch policies where possible
3. **Scale vertically** - Add more CPU cores  
4. **Scale horizontally** - Add more gateway instances

## 4. Best Practices for High-Concurrency Scenarios

### 4.1 Use GatewayScript Strategically

**When to Use GatewayScript:**
- Complex data transformations that can't be done with Map policy
- Complex business logic (when XSLT skills aren't available)
- Dynamic routing based on complex conditions

**When to Avoid GatewayScript:**
- Simple header manipulation → Use Set Variable policy
- Simple data transformations → Use Map policy
- Basic routing decisions → Use Switch policy
- Any scenario where XSLT can do the job (XSLT has no engine limit)

**Why This Matters:**

Every GatewayScript execution consumes an engine. If you can accomplish the same thing with a policy that doesn't use engines, you free up capacity for operations that truly need GatewayScript.

### 4.2 Isolate High-Traffic APIs

For APIs with extremely high concurrency requirements, consider deploying dedicated gateway instances:

**Benefits:**
- Isolated resource pools prevent contention
- Independent scaling based on specific API needs
- Failure isolation - issues in one gateway don't affect others
- Optimized configuration per workload type

**Architecture Example:**
```
┌─────────────────────────────────────┐
│   Load Balancer                     │
└─────────────────────────────────────┘
           │
           ├──────────────┬──────────────┐
           │              │              │
    ┌──────▼─────┐ ┌─────▼──────┐ ┌────▼──────┐
    │ Gateway A  │ │ Gateway B  │ │ Gateway C │
    │ (High      │ │ (Standard  │ │ (Low      │
    │ Concurrency│ │ APIs)      │ │ Volume)   │
    │ APIs)      │ │            │ │           │
    │ 16 cores   │ │ 8 cores    │ │ 4 cores   │
    │ 16 engines │ │ 8 engines  │ │ 4 engines │
    └────────────┘ └────────────┘ └───────────┘
```


### 4.3 Other Suggestions
- Enable ExtLatency logging to a dedicated LogTarget for detailed timing
- Monitor drouter thread usage (correlates with engine usage)
- Set up alerts for queued work > 0
- Review GatewayScript code for optimization opportunities

By following these guidelines and recommendations, you can design API Gateway deployments that efficiently handle high-concurrency workloads while maintaining optimal performance and resource utilization.

---

*Have questions about API Gateway performance tuning? Feel free to reach out or leave a comment below.*