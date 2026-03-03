---
layout: post
date: 2026-03-03 01:00:00
categories: APIConnect
title: "Monitoring GatewayScript Availability with DataPower REST API: Real-Time Performance Tracking"
author: ["ChrisPhillips", "TreyWilliamson"]
description: "Learn how to use the DataPower REST Management Interface to continuously monitor GatewayScript engine availability and detect performance bottlenecks in real-time."
tags: [APIConnect, DataPower, GatewayScript, Monitoring, REST API, Performance]
draft: true
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
    "Available": "8",
    "Available": "8",
    "Available": "8",
    "Available": "7",  ← One engine now in use
    "Available": "6",  ← Two engines in use
    "Available": "8",  ← Back to full availability
```

## Understanding the Response

The full JSON response from the REST API endpoint contains valuable metrics. Here's the actual output structure:

```json
{
  "GatewayScriptStatus": {
    "Available": "8",
    "InUse": "2",
    "Queued": "0",
    "Failures": "0",
    "mAdminState": "enabled",
    "MaxProcessingDuration": "0",
    "AverageProcessingDuration": "12"
  }
}
```

**Complete Example Output:**

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
    "Available": "8",
    "InUse": "2",
    "Queued": "0",
    "Failures": "0",
    "mAdminState": "enabled",
    "MaxProcessingDuration": "0",
    "AverageProcessingDuration": "12"
  }
}
```

**Key Fields:**

| Field | Description | What to Monitor |
|-------|-------------|-----------------|
| `Available` | Total engines configured | Should match CPU core count |
| `InUse` | Engines currently executing | Watch for approaching Available count |
| `Queued` | Requests waiting for engines | **RED FLAG if > 0** |
| `Failures` | GatewayScript execution errors | Should always be 0 |
| `mAdminState` | Administrative state | Should be "enabled" |
| `MaxProcessingDuration` | Maximum processing time (ms) | Track for performance spikes |
| `AverageProcessingDuration` | Average processing time (ms) | Monitor for performance trends |

## Enhanced Monitoring Script

For production monitoring, you'll want more detail. Here's an enhanced version:

```bash
#!/bin/bash

# Configuration
DATAPOWER_HOST="1.2.3.4"
DATAPOWER_PORT="5554"
DOMAIN="default"
USERNAME="admin"
PASSWORD="password"
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
    
    # Extract values using grep and sed
    AVAILABLE=$(echo "$RESPONSE" | grep -o '"Available":"[^"]*"' | sed 's/"Available":"\([^"]*\)"/\1/')
    INUSE=$(echo "$RESPONSE" | grep -o '"InUse":"[^"]*"' | sed 's/"InUse":"\([^"]*\)"/\1/')
    QUEUED=$(echo "$RESPONSE" | grep -o '"Queued":"[^"]*"' | sed 's/"Queued":"\([^"]*\)"/\1/')
    FAILURES=$(echo "$RESPONSE" | grep -o '"Failures":"[^"]*"' | sed 's/"Failures":"\([^"]*\)"/\1/')
    
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

## Integration with Monitoring Systems

### Prometheus Exporter

For Prometheus integration, you can create a simple exporter:

```python
#!/usr/bin/env python3
import requests
import time
from prometheus_client import start_http_server, Gauge

# Metrics
gw_available = Gauge('datapower_gatewayscript_available', 'Available GatewayScript engines')
gw_inuse = Gauge('datapower_gatewayscript_inuse', 'In-use GatewayScript engines')
gw_queued = Gauge('datapower_gatewayscript_queued', 'Queued GatewayScript requests')
gw_failures = Gauge('datapower_gatewayscript_failures', 'GatewayScript failures')

def collect_metrics(host, port, domain, username, password):
    url = f"https://{host}:{port}/mgmt/status/{domain}/GatewayScriptStatus"
    
    try:
        response = requests.get(url, auth=(username, password), verify=False)
        data = response.json()
        
        status = data['GatewayScriptStatus']
        gw_available.set(int(status['Available']))
        gw_inuse.set(int(status['InUse']))
        gw_queued.set(int(status['Queued']))
        gw_failures.set(int(status['Failures']))
        
    except Exception as e:
        print(f"Error collecting metrics: {e}")

if __name__ == '__main__':
    # Start Prometheus HTTP server
    start_http_server(8000)
    
    # Configuration
    DATAPOWER_HOST = "1.2.3.4"
    DATAPOWER_PORT = "5554"
    DOMAIN = "default"
    USERNAME = "admin"
    PASSWORD = "password"
    
    print("Prometheus exporter started on port 8000")
    
    while True:
        collect_metrics(DATAPOWER_HOST, DATAPOWER_PORT, DOMAIN, USERNAME, PASSWORD)
        time.sleep(15)
```

### Splunk Integration

For Splunk, you can use the REST API to feed data directly:

```bash
#!/bin/bash

SPLUNK_HEC_URL="https://splunk.example.com:8088/services/collector"
SPLUNK_TOKEN="your-hec-token"

while true; do
    RESPONSE=$(curl -k -s -u admin:password \
        "https://1.2.3.4:5554/mgmt/status/default/GatewayScriptStatus")
    
    # Send to Splunk HEC
    curl -k -X POST "${SPLUNK_HEC_URL}" \
        -H "Authorization: Splunk ${SPLUNK_TOKEN}" \
        -d "{
            \"sourcetype\": \"datapower:gatewayscript\",
            \"event\": ${RESPONSE}
        }"
    
    sleep 30
done
```

## Alerting Thresholds

Based on our [previous analysis](/apiconnect/2026/02/04/apigw-gatewayscript-concurrency.html), here are recommended alert thresholds:

| Metric | Warning | Critical | Action |
|--------|---------|----------|--------|
| Utilization | > 70% | > 85% | Review capacity planning |
| Queued Requests | > 0 | > 5 | Immediate investigation |
| Failures | > 0 | > 10 | Check GatewayScript code |
| Available Engines | < Expected | N/A | Configuration issue |

## Best Practices

1. **Poll Frequency**: 
   - Development: 5-10 seconds
   - Production: 15-30 seconds (balance between visibility and load)

2. **Authentication**:
   - Use dedicated monitoring user with read-only permissions
   - Store credentials securely (environment variables, secrets manager)
   - Never hardcode credentials in scripts

3. **Error Handling**:
   - Implement retry logic for transient failures
   - Log connection errors separately
   - Alert on monitoring script failures

4. **Data Retention**:
   - Store historical data for trend analysis
   - Keep at least 30 days for capacity planning
   - Archive older data for compliance

5. **Multiple Domains**:
   - Monitor all domains separately
   - Aggregate metrics for overall health
   - Domain-specific alerting

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
- [API Connect Performance Tuning](https://www.ibm.com/docs/en/api-connect)

---

*Have questions about monitoring DataPower or API Gateway performance? Feel free to reach out or leave a comment below.*