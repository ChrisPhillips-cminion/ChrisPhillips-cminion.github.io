---
layout: post
date: 2026-01-31 01:00:00
categories: APIConnect
title: "Mastering GatewayScript BottleNecks: Performance Optimization for IBM API Gateway"
author: ["ChrisPhillips", "IvanH"]
draft: true
---

When designing high-performance API solutions with IBM API Gateway, understanding the relationship between GatewayScript engines, CPU cores, and concurrent execution is crucial for optimal performance. This comprehensive guide explores these relationships and provides battle-tested recommendations for handling high-concurrency scenarios in production environments.

<!--more-->

## Understanding GatewayScript Engine Architecture

IBM API Gateway uses GatewayScript engines to execute custom logic within API policies. The number of concurrent GatewayScript executions your gateway can handle depends on three key factors:

1. **Number of GatewayScript Engines**: The pool of available engines for executing scripts
2. **CPU Cores Assigned**: The processing power available to the gateway
3. **Script Complexity**: The computational intensity of your GatewayScript logic

## How Engines, CPU Cores, and Concurrency Work Together

### GatewayScript Engines: The Execution Workers

Each GatewayScript engine can execute one script at a time. If you have 10 engines configured, you can theoretically execute 10 GatewayScript operations concurrently. When all engines are busy, additional requests requiring GatewayScript execution will queue, waiting for an engine to become available.

### CPU Cores: The Processing Foundation

The number of CPU cores assigned to your API Gateway determines the overall number of GatewayScript engines. While GatewayScript engines handle the execution, they still require CPU resources to run. The relationship is always 1:1.

## Understanding Concurrent Execution Limits

The maximum number of concurrent GatewayScript executions is limited by:

```
Max Concurrent GatewayScript = Number of Available Engines
```

## Calculating Total Gateway Concurrency

Understanding the total number of transactions "live" in the gateway at any point in time is crucial for capacity planning. Gateway concurrency can be calculated using the fundamental relationship between throughput and latency:

```
Total Concurrency = Throughput (TPS) × Latency (seconds)
```

### Using HTTP Status Data to Calculate Concurrency

You can estimate total gateway concurrency using data from the `show http` status provider:

**Example Calculation:**

From the HTTP status output:
- **Throughput**: 100 transactions per second (TPS)
- **Mean Transaction Time**: 50 milliseconds

```
Total Concurrency = 100 TPS × 0.050 seconds = 5 concurrent transactions
```

**Note:** Ensure dimensional consistency - convert milliseconds to seconds before multiplying.

### Understanding the Two Types of Concurrency

It's critical to distinguish between:

1. **Total Gateway Concurrency**: All transactions actively being processed by the gateway
   - Calculated from: `TPS × Latency (from show http)`
   - Represents the complete workload across all gateway components

2. **GatewayScript Engine Concurrency**: Only transactions executing GatewayScript code
   - Obtained directly from: `show gatewayscript-status` (In-use run times)
   - Represents the subset of transactions using GatewayScript engines

**Example Scenario:**

```
Total Gateway Concurrency:     50 transactions (from TPS × latency)
GatewayScript Concurrency:     8 transactions (from gatewayscript-status)
```

This indicates that while 50 transactions are in-flight through the gateway, only 8 are currently executing GatewayScript code. The remaining 42 are in other processing stages (routing, transformation, backend calls, etc.).

### Practical Application

Use these metrics together to:
- **Identify bottlenecks**: If GatewayScript concurrency approaches engine count while total concurrency is low, GatewayScript is the bottleneck
- **Capacity planning**: Calculate required engines based on expected TPS and GatewayScript execution time
- **Performance optimization**: If total concurrency is high but GatewayScript concurrency is low, focus optimization elsewhere

**Formula for Required GatewayScript Engines:**

```
Required Engines = Expected TPS × GatewayScript Execution Time (seconds)
```

Example: If you expect 200 TPS and GatewayScript takes 25ms per transaction:
```
Required Engines = 200 × 0.025 = 5 engines minimum
```

Add 20-30% buffer for peak loads and failover scenarios.


## Best Practices for High-Concurrency Scenarios

### 1. Strategic GatewayScript Usage

For high-concurrency APIs, consider whether GatewayScript is necessary:

**When to use GatewayScript:**
- Complex data transformations
- Complex logic when there are no XSLT skills available. XSLT does not have the limitation of engines

**When to avoid GatewayScript:**
- Simple header manipulation (use Set Variable policy)
- Simple data transformations where the mapping policy will suffice
- Basic routing decisions (use Switch policy)
- Where XSLT skills are available.


### 2. Gateway Isolation for High-Traffic APIs

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


### 3. Continuous Monitoring and Performance Tuning

Key metrics to monitor:
- **Engine Utilization**: Number of threads of drouter utilised is usually in ratio to the number of engines utilised
- **Response Time**: Latency introduced by GatewayScript execution
- **CPU Usage**: Overall gateway CPU consumption



### Checking GatewayScript Engine Status

You can monitor GatewayScript engine status using the DataPower CLI command:

**GatewayScript Engine status**

```
top;co;show gatewayscript-status
```

*Sample Output:*

```
Global mode

Available run times: 1 
   In-use run times: 0 
        Queued work: 0 
   Runtime failures: 0 
```

**CPU Utlisation**
```
top;co;show cpu
```

*Sample Output:*

```
Global mode

                      10 s       1 min      10 min        1 hr       1 day
cpu usage (%):           10           5           0           0           0
```


**HTTP Transactions per second and latency for a given domain**

```
'top;co;switch <domain containing service(s) of interest>;show http'
```

*Sample Output*

```
HTTP transactions/second:

 Service type Service name 10 s 1 min 10 min 1 hr 1 day 
 ------------ ------------ ---- ----- ------ ---- ----- 
 apiGateway   apiconnect   10   10     0      0    0     

HTTP mean transaction times (msec):

 Service    Proxy      10 s 1 min 10 min 1 hr 1 day 
 ---------- ---------- ---- ----- ------ ---- ----- 
 apiGateway apiconnect 1    1     1      0    0   
 ```



**Tuning Guidelines:**  
- If CPU usage > 80% consistently: Scale horizontally or vertically
- If GwS engine availability < 1 consistently: Scale horizontally or vertically.
- If "Engines Queued" is consistently > 0: Scale horizontally or vertically.
- If latency is high for the gatewayscript policies check the number of CPU threads being used by drouter
- Monitor "Engines In Use" vs "Engines Configured" to understand utilization patterns
- Enable ExtLatency logging to a dedicated LogTarget

## Key Takeaways

Understanding the relationship between GatewayScript engines, CPU cores, and concurrency is essential for building high-performance API solutions. Key takeaways:

1. **Engine count determines concurrent execution capacit0y**
2. **CPU cores provide the processing power for engines**
3. **The ratio is one CPU Core to one Enginer**
4. **For high concurrency, consider dedicated gateway services**
5. **Use GatewayScript only when necessary**
6. **Monitor, measure, and tune based on actual workload**

By following these guidelines and recommendations, you can design API Gateway deployments that efficiently handle high-concurrency workloads while maintaining optimal performance and resource utilization.

---

*Have questions about API Gateway performance tuning? Feel free to reach out or leave a comment below.*