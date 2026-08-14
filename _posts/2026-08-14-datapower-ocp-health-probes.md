---
layout: post
date: 2026-08-14 10:00:00
categories: [DataPower, APIConnect]
title: "Kubernetes Health Probes: What They Actually mean to APIConenct and DataPower and How to Tune Them"
author: ["ChrisPhillips", "IBMBob"]
description: "A practical guide to DataPower liveness and readiness probes on OpenShift. Covers what each probe tests, default values set by the API Connect operator, common misconfiguration patterns, and how to tune thresholds without fighting the operator."
tags: [DataPower, OpenShift, Kubernetes, Probes, Liveness, Readiness, APIConnect, Troubleshooting]
draft: true
---

DataPower pods on OpenShift restart unexpectedly. The OCP events log says `Liveness probe failed`. Your gateway logs show no errors. The pod was healthy from DataPower's perspective, yet Kubernetes killed it.

This is one of the most disruptive — and most preventable — operational problems in an API Connect on OCP deployment.

<!--more-->

## 1. The Three Probes and What They Do

Kubernetes supports three probe types. The API Connect operator configures two of them on DataPower gateway pods:

| Probe | What happens on failure | What it tests on DataPower |
|---|---|---|
| **Liveness** | Pod is killed and restarted | Is the firmware still running and responsive? |
| **Readiness** | Pod is removed from the Service endpoints (traffic stops routing to it) | Is DataPower ready to serve API traffic? |
| **Startup** | Pod is killed if startup takes longer than the window allows | Has DataPower finished initialising? |

**The critical distinction:**

- A **liveness** failure restarts the pod. This is destructive. It terminates any in-flight transactions on that pod.
- A **readiness** failure is graceful. Traffic is drained away from the pod but the pod keeps running.

Most unnecessary DataPower restarts on OCP are caused by a **liveness probe that is too aggressive** — its timeout is too short, or its failure threshold is too low, causing it to declare the pod dead during a brief period of high load.

---

## 2. What the API Connect Operator Configures by Default

The API Connect operator injects probe configuration into the DataPower gateway pods via the `GatewayCluster` CR. As of API Connect v10/v12, the default probe configuration on the gateway pods is approximately:

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 7878
    scheme: HTTP
  initialDelaySeconds: 120
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3
  successThreshold: 1

readinessProbe:
  httpGet:
    path: /readiness
    port: 7878
    scheme: HTTP
  initialDelaySeconds: 120
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3
  successThreshold: 1
```

> **Note:** These values change between operator versions. Always verify the actual values in your cluster:
> ```bash
> oc get pod <gateway-pod> -n <namespace> -o jsonpath='{.spec.containers[0].livenessProbe}' | python3 -m json.tool
> oc get pod <gateway-pod> -n <namespace> -o jsonpath='{.spec.containers[0].readinessProbe}' | python3 -m json.tool
> ```

### What `/health` and `/readiness` actually test

Both endpoints are served by DataPower's built-in probe service on port `7878`. They are not general HTTP health checks — they query DataPower's internal state:

- **`/health` (liveness):** Returns HTTP 200 if the DataPower firmware process is alive and the probe service is responsive. It does **not** check whether APIs are loaded or whether gateway peering is healthy. It is a minimal "is the process up?" check.

- **`/readiness`:** Returns HTTP 200 only when DataPower has completed its startup sequence and is ready to serve API traffic. This includes: firmware initialisation, domain activation, and — critically — the initial synchronisation of API configuration from the API Connect Manager. Until that sync completes, `/readiness` returns non-200 and the pod stays out of rotation.

The readiness check is the reason why a pod can show `Running` in OCP but not appear `Ready` — it is waiting for API sync to complete. On a large gateway with many APIs, this can take several minutes.

---

## 3. The Most Common Misconfiguration Patterns

### Pattern 1: `timeoutSeconds` too short under load

The probe makes an HTTP request to port 7878. Under heavy load, DataPower's probe service may take longer than the default 5 seconds to respond — not because DataPower is unhealthy, but because the node CPU is saturated and all threads are busy processing API traffic.

With `failureThreshold: 3` and `periodSeconds: 10`, three consecutive timeouts over 30 seconds will trigger a pod restart. On a loaded gateway, this can happen during a traffic spike with no underlying fault.

**Symptom:** Pod restarts correlate precisely with traffic peaks. DataPower logs show no errors at the time of restart. OCP events show `Liveness probe failed: context deadline exceeded`.

**Fix:** Increase `timeoutSeconds` to 10–15 and `failureThreshold` to 5. This means the probe must fail 5 consecutive times over 50–75 seconds before a restart is triggered — enough time to distinguish a genuine failure from load-related probe latency.

### Pattern 2: `initialDelaySeconds` too short on large deployments

The default `initialDelaySeconds: 120` is sufficient for a small gateway with few APIs. A large deployment — hundreds of APIs, multiple domains, large gateway peering datasets — can take longer than 120 seconds to complete its startup sequence.

If liveness starts checking before DataPower is fully up, it will see non-200 responses, accumulate failures, and restart the pod — which starts the cycle again.

**Symptom:** Pod enters a restart loop on initial deployment or after a full cluster restart. Each restart takes slightly longer than the last as partial state is cleaned up. OCP events show liveness failures within the first 2–4 minutes of pod start.

**Fix:** Increase `initialDelaySeconds` to 180–300 for large deployments. Alternatively, configure a `startupProbe` with a generous `failureThreshold` to cover the startup window, then let liveness take over once the pod is stable.

### Pattern 3: Readiness timeout during API Manager connectivity loss

The `/readiness` endpoint depends on DataPower's ability to communicate with the API Manager for the initial sync. If the API Manager is temporarily unreachable (network blip, management pod restart), DataPower will not report ready.

This is the **correct behaviour** — an unsynchronised gateway should not receive traffic. However, if your load balancer or ingress is configured to fail-over based on readiness, a brief API Manager outage will take your gateway pods out of rotation entirely.

**This is not a bug.** Do not set an aggressive `successThreshold` or manipulate readiness probes to work around this — you will end up serving stale or empty API configurations. Instead, monitor API Manager availability independently and treat gateway readiness failures as a symptom of an upstream problem.

---

## 4. How to Override Probe Values Without Fighting the Operator

The API Connect operator manages the GatewayCluster CR and will reconcile changes made directly to pod specs. The correct way to adjust probe settings is through the `GatewayCluster` CR itself.

Check whether your operator version supports `livenessProbe` and `readinessProbe` overrides in the CR spec:

```yaml
apiVersion: gateway.apiconnect.ibm.com/v1beta1
kind: GatewayCluster
metadata:
  name: my-gateway
spec:
  # ... other fields ...
  livenessProbe:
    timeoutSeconds: 15
    failureThreshold: 5
    initialDelaySeconds: 180
  readinessProbe:
    timeoutSeconds: 15
    failureThreshold: 5
    initialDelaySeconds: 180
```

> **Check your operator documentation** for the exact field names and which versions support probe overrides. In earlier operator versions, probe configuration is not exposed at the CR level and requires a support case to request adjusted defaults via a patch.

After applying changes, verify the updated values were picked up on the running pods:

```bash
oc get pod <gateway-pod> -n <namespace> -o jsonpath='{.spec.containers[0].livenessProbe}'
```

---

## 5. Diagnosing a Probe-Triggered Restart

When you suspect probe misconfiguration is causing restarts, work through this sequence:

**Step 1 — Confirm the restart cause:**

```bash
# Check restart count and last termination reason
oc describe pod <gateway-pod> -n <namespace> | grep -A 10 "Last State\|Liveness\|Readiness"
```

Look for `Reason: Error` with `Exit Code: 137` (SIGKILL — Kubernetes killed it) and `Liveness probe failed` in the Events section.

**Step 2 — Correlate with the traffic timeline:**

```bash
# Check gateway pod restart times against your monitoring
oc get events -n <namespace> --sort-by='.lastTimestamp' | grep -i "liveness\|readiness\|killing\|restart"
```

If restarts align with known traffic spikes, probe timeout is likely the cause.

**Step 3 — Check the probe endpoint directly:**

While the pod is running, exec into it and hit the probe endpoint yourself to see the baseline response time:

```bash
oc exec -ti <gateway-pod> -n <namespace> -- curl -w "\nTime: %{time_total}s\n" -o /dev/null -s http://localhost:7878/health
oc exec -ti <gateway-pod> -n <namespace> -- curl -w "\nTime: %{time_total}s\n" -o /dev/null -s http://localhost:7878/readiness
```

Under no load, these should respond in under 1 second. If they are already taking 3–4 seconds at baseline, the probe service itself is under pressure and the timeout needs significant headroom.

**Step 4 — Review DataPower logs at the time of restart:**

```bash
oc logs <gateway-pod> -n <namespace> --previous | tail -100
```

If DataPower logs show no errors immediately before the pod termination, the restart was externally triggered (probe) rather than a DataPower fault.

---

## 6. Summary: Recommended Probe Values

These are starting points. Adjust based on your deployment size and observed startup times.

| Setting | Default | Small deployment | Large deployment (many APIs / high traffic) |
|---|---|---|---|
| `initialDelaySeconds` | 120 | 120 | 240–300 |
| `periodSeconds` | 10 | 10 | 10 |
| `timeoutSeconds` | 5 | 10 | 15 |
| `failureThreshold` (liveness) | 3 | 3 | 5 |
| `failureThreshold` (readiness) | 3 | 3 | 5 |

The most impactful changes are `timeoutSeconds` and `failureThreshold` on the liveness probe. Increasing these gives DataPower enough slack to survive a traffic spike without being unnecessarily killed.

---

## Related posts

- [API Connect Health Check Endpoints](/apiconnect/2023/10/11/APICMonitoring.html) — monitoring the API Manager and gateway readiness endpoint
- [Readiness when restarting API GW Pods](/apiconnect/2022/11/30/DataPower-Restart-APIFGWQ.html) — behaviour during rolling restarts and quorum
- [Validating the Gateway Peering status](/apiconnect/2021/04/22/dp-gwp-status.html) — checking peering health from inside a pod
