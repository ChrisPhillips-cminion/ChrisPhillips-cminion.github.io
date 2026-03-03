---
layout: post
date: 2026-03-03 01:00:00
categories: APIConnect
title: "Monitoring GatewayScript Availability with DataPower REST API: Real-Time Performance Tracking"
author: ["ChrisPhillips", "TreyWilliamson"]
description: "Learn how to use the DataPower REST Management Interface to continuously monitor GatewayScript engine availability and detect performance bottlenecks in real-time."
tags: [APIConnect, DataPower, GatewayScript, Monitoring, REST API, Performance]
---

In our [previous article on GatewayScript concurrency](/apiconnect/2026/02/04/apigw-gatewayscript-concurrency.html), we explored how to understand and optimize GatewayScript engine performance. But how do you monitor these engines in real-time without constantly logging into the DataPower CLI?

The answer: DataPower's REST Management Interface. This powerful API allows you to programmatically query GatewayScript status and build automated monitoring solutions.

<!--more-->

## Why Monitor GatewayScript Availability?

As we discussed in our [GatewayScript bottlenecks guide](/apiconnect/2026/02/04/apigw-gatewayscript-concurrency.html), understanding engine availability is critical for:

- **Detecting bottlenecks** before they impact users
- **Capacity planning** based on actual usage patterns
- **Performance trending** over time
- **Alerting** when engines are saturated
- **Troubleshooting** performance issues in production

The CLI command `show gatewayscript-status` is great for ad-hoc checks, but for continuous monitoring, you need automation.

## The DataPower REST Management Interface

DataPower provides a comprehensive REST API for management operations. The endpoint we're interested in is:

```
GET https://<datapower-host>:5554/mgmt/status/<domain>/GatewayScriptStatus
```

This endpoint returns the same information as the CLI `show gatewayscript-status` command, but in JSON format that's perfect for automation.

## Quick Start: Monitoring Script

Here's a simple bash one-liner to continuously monitor GatewayScript availability:

```bash
while true; do 
  curl -k -u admin:password -X GET \
    https://1.2.3.4:5554/mgmt/status/default/GatewayScriptStatus 2>&1 | \
    grep Available; 
  echo; 
done
```

**What This Does:**
- Continuously polls the GatewayScript status endpoint
- Extracts the "Available" field showing engine availability
- Displays results in real-time
- Runs indefinitely until stopped (Ctrl+C)

**Sample Output:**
```
    "Available": 8,
    "Available": 8,
    "Available": 8,
    "Available": 8, 
```

## Understanding the Response

The full JSON response from the REST API endpoint contains valuable metrics. Here's the actual output structure:

```bash
$ curl -k -u admin:password -X GET https://1.2.3.4:5554/mgmt/status/default/GatewayScriptStatus
{
  "_links": {
    "self": {
      "href": "/mgmt/status/default/GatewayScriptStatus"
    },
    "doc": {
      "href": "/mgmt/docs/status/GatewayScriptStatus"
    }
  },
  "GatewayScriptStatus": {
    "Available": 8,
    "InUse": 0,
    "QueuedWork": 0,
    "Failed": 0
  }
}
```

**Note:** The values are returned as integers (not strings), making them easy to parse and compare in monitoring scripts.

**Key Fields:**

| Field | Description | What to Monitor |
|-------|-------------|-----------------|
| `Available` | Total engines configured (integer) | Should match CPU core count unless on a physical appliance |
| `InUse` | Engines currently executing (integer) | Watch for approaching Available count |
| `QueuedWork` | Requests waiting for engines (integer) | **RED FLAG if > 0** |
| `Failed` | GatewayScript execution errors (integer) | Should always be 0 |

## Enhanced Monitoring Script

For production monitoring, you'll want more detail. Here's an enhanced version:

```bash
#!/bin/bash

# Configuration
DATAPOWER_HOST="9.37.230.250"
DATAPOWER_PORT="5554"
DOMAIN="default"
USERNAME="admin"
PASSWORD="Level2was"
POLL_INTERVAL=5  # seconds

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo "Monitoring GatewayScript Status on ${DATAPOWER_HOST}:${DATAPOWER_PORT}"
echo "Domain: ${DOMAIN}"
echo "Poll Interval: ${POLL_INTERVAL}s"
echo "Press Ctrl+C to stop"
echo "----------------------------------------"

while true; do
    # Get current timestamp
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    
    # Query the REST API
    RESPONSE=$(curl -k -s -u ${USERNAME}:${PASSWORD} \
        -X GET \
        "https://${DATAPOWER_HOST}:${DATAPOWER_PORT}/mgmt/status/${DOMAIN}/GatewayScriptStatus")
    
    # Extract values using grep and sed (values are integers, not strings)
    AVAILABLE=$(echo "$RESPONSE" | grep -o '"Available" : [0-9]*' | sed 's/"Available" : //')
    INUSE=$(echo "$RESPONSE" | grep -o '"InUse" : [0-9]*' | sed 's/"InUse" : //')
    QUEUED=$(echo "$RESPONSE" | grep -o '"QueuedWork" : [0-9]*' | sed 's/"QueuedWork" : //')
    FAILURES=$(echo "$RESPONSE" | grep -o '"Failed" : [0-9]*' | sed 's/"Failed" : //')
    

    # Calculate utilization percentage
    if [ -n "$AVAILABLE" ] && [ "$AVAILABLE" -gt 0 ]; then
        UTILIZATION=$((INUSE * 100 / AVAILABLE))
    else
        UTILIZATION=0
    fi
    
    # Determine status color
    if [ "$QUEUED" -gt 0 ]; then
        STATUS_COLOR=$RED
        STATUS="CRITICAL"
    elif [ "$UTILIZATION" -ge 80 ]; then
        STATUS_COLOR=$YELLOW
        STATUS="WARNING"
    else
        STATUS_COLOR=$GREEN
        STATUS="OK"
    fi
    
    # Display status
    echo -e "${TIMESTAMP} | ${STATUS_COLOR}${STATUS}${NC} | Available: ${AVAILABLE} | In-Use: ${INUSE} (${UTILIZATION}%) | Queued: ${QUEUED} | Failures: ${FAILURES}"
    
    # Alert on critical conditions
    if [ "$QUEUED" -gt 0 ]; then
        echo -e "${RED}⚠️  ALERT: ${QUEUED} requests queued - engines saturated!${NC}"
    fi
    
    if [ "$FAILURES" -gt 0 ]; then
        echo -e "${RED}⚠️  ALERT: ${FAILURES} GatewayScript failures detected!${NC}"
    fi
    
    sleep $POLL_INTERVAL
done
```

**Sample Output:**
```
Monitoring GatewayScript Status on 1.2.3.4:5554
Domain: default
Poll Interval: 5s
Press Ctrl+C to stop
----------------------------------------
2026-03-03 14:30:00 | OK | Available: 8 | In-Use: 2 (25%) | Queued: 0 | Failures: 0
2026-03-03 14:30:05 | OK | Available: 8 | In-Use: 3 (37%) | Queued: 0 | Failures: 0
2026-03-03 14:30:10 | WARNING | Available: 8 | In-Use: 7 (87%) | Queued: 0 | Failures: 0
2026-03-03 14:30:15 | CRITICAL | Available: 8 | In-Use: 8 (100%) | Queued: 5 | Failures: 0
⚠️  ALERT: 5 requests queued - engines saturated!
```



## Troubleshooting

### Connection Refused

```bash
curl: (7) Failed to connect to 1.2.3.4 port 5554: Connection refused
```

**Solutions:**
- Verify REST Management Interface is enabled
- Check firewall rules
- Confirm port 5554 is correct (default for REST interface)

### Authentication Failed

```bash
curl: (22) The requested URL returned error: 401 Unauthorized
```

**Solutions:**
- Verify username and password
- Check user has appropriate permissions
- Ensure user is not locked out

### Empty Response

**Solutions:**
- Verify domain name is correct
- Check GatewayScript is enabled in the domain
- Confirm API Gateway service is running

## Conclusion

Monitoring GatewayScript availability through the DataPower REST API provides:

- **Real-time visibility** into engine utilization
- **Automated alerting** for capacity issues
- **Historical data** for trend analysis
- **Integration** with enterprise monitoring tools

Combined with the capacity planning formulas from our [previous article](/apiconnect/2026/02/04/apigw-gatewayscript-concurrency.html), you now have a complete toolkit for managing GatewayScript performance in production environments.

## Additional Resources

- [DataPower REST Management Interface Documentation](https://www.ibm.com/docs/en/datapower-gateway)
- [GatewayScript Concurrency Guide](/apiconnect/2026/02/04/apigw-gatewayscript-concurrency.html)


---
