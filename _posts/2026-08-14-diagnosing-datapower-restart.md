---
layout: post
date: 2026-08-14 09:00:00
categories: DataPower
title: "How to Diagnose a DataPower Restart: Reading error-report and Backtrace Files"
author: ["ChrisPhillips", "IvanH", "IBMBob"]
description: "A field guide to diagnosing why IBM DataPower restarted. Covers the error-report archive structure, how to read backtrace files, interpreting throttler reloads vs crashes, and what to send to IBM Support."
tags: [DataPower, Troubleshooting, Restart, ErrorReport, Backtrace, Support, Performance]
draft: true
---

DataPower restarted. Now what? The first instinct is to open a support ticket — but before you do, the answer is almost certainly already on the appliance. DataPower writes a detailed post-mortem every time it restarts, and knowing how to read it will either resolve the issue immediately or cut hours off your support case.

<!--more-->

## 1. First: Know Which Type of Restart Occurred

Not all restarts are equal. Before reading any file, identify which category you are dealing with:

| Restart type | What it means | Where to confirm |
|---|---|---|
| **Throttler Reload** | Memory fell below the Throttle At or Terminate At threshold. Deliberate, controlled restart. | `system.log` — look for `throttler-reload` |
| **Firmware crash (panic)** | An unhandled internal error caused the firmware to abort. | `error-report` backtrace files |
| **Manual restart** | Operator ran `shutdown restart` or restarted the pod/container. | `system.log` — look for `system shutdown initiated` |
| **OCP pod eviction** | Kubernetes killed the pod due to node pressure or OOM. | OCP event log, not DataPower logs |
| **Domain restart** | A single application domain restarted, not the full firmware. | `system.log` in the affected domain |

A Throttler Reload is not a crash — it is a deliberate protective action. Do not treat it like a firmware panic. The diagnostic approach differs.

---

## 2. Generating the Error Report

If the appliance is still running, generate the error report immediately — before any further restarts wash the state:

```bash
# From the CLI (top-level, not inside a domain)
top
generate error-report
```

The report is written to `temporary:///error-report-<timestamp>.zip` and also to `logtemp:///error-report-<timestamp>.zip`. Download it from the WebGUI under **Administration → Main → Error Report** or via the REST Management Interface:

```bash
curl -k -u admin:password \
  https://<datapower-host>:5554/mgmt/filestore/temporary/ \
  | grep error-report
```

> **Note:** On a containerised DataPower (OCP/Kubernetes), the `error-report` is written inside the pod's ephemeral filesystem. Retrieve it before the pod restarts again, or configure a persistent log target to ship it externally.

---

## 3. Error Report Archive Structure

The `.zip` contains many files. For restart diagnosis, focus on these:

```
error-report-<timestamp>.zip
├── system.log                  ← Start here — the timeline of events
├── backtrace.txt               ← Present only on a firmware crash/panic
├── backtrace-<n>.txt           ← Additional threads at time of crash
├── MemoryStatus2.xml           ← System memory at time of report
├── SystemUsage.xml             ← CPU load at time of report
├── ErrorReportSummary.xml      ← High-level summary, useful for quick triage
├── GatewayPeeringStatus.xml    ← Peering state at time of restart
└── <domain>/
    └── log                     ← Per-domain log (look here for domain-level events)
```

---

## 4. Reading system.log

`system.log` is your timeline. Open it and search backwards from the end for the restart event. Key patterns:

```
# Throttler Reload
0x8100003d ... throttler-reload
mgmt(notice): ... System firmware reload due to memory threshold

# Controlled shutdown (manual or OCP signal)
mgmt(notice): System shutdown initiated

# Firmware panic (will be followed by backtrace files)
mgmt(error): Firmware panic: <reason>
mgmt(error): Generating crash report
```

Once you find the restart line, scroll up 60–120 seconds to see what was happening immediately before. Look for:

- Repeated `connection refused` or `connection pool full` — traffic overload
- `document-cache full` or `stylesheet-cache full` — cache exhaustion driving memory growth
- `GatewayScript runtime failure` — a runaway GatewayScript consuming memory/CPU
- `gateway-peering` errors — peering instability preceding a restart

---

## 5. Reading a Backtrace File

Backtrace files are only present after a firmware panic (unhandled error). They are not present after a Throttler Reload.

A backtrace looks like this:

```
Thread 1 (Thread 0x7f... (LWP 12345)):
#0  0x00007f... in dp_internal_function ()
#1  0x00007f... in dp_xml_parse ()
#2  0x00007f... in dp_assembly_execute ()
#3  0x00007f... in dp_transaction_process ()
...

Thread 2 (Thread 0x7f... (LWP 12346)):
#0  0x00007f... in pthread_cond_wait ()
...
```

**What to look for:**

- **Thread 1** is almost always the thread that triggered the panic. The top of its stack (frame `#0`, `#1`, `#2`) identifies the subsystem that was executing.
- Common subsystem indicators:

| Stack frame contains | Likely area |
|---|---|
| `dp_xml_parse`, `dp_xslt` | XML/XSLT processing — large or malformed payload |
| `dp_gatewayscript`, `dp_js_engine` | GatewayScript execution — script error or OOM |
| `dp_ssl`, `dp_tls` | TLS handshake — cipher/cert issue causing abort |
| `dp_gateway_peering` | Peering subsystem — network or state corruption |
| `dp_mgmt`, `dp_config` | Management plane — configuration load failure |

- **Do not try to decode the memory addresses** — they are ASLR-randomised and meaningless without the firmware symbol table. IBM Support has the symbol tables. Send the full backtrace.

> **The most useful thing you can do with a backtrace is send it to IBM Support along with:**
> 1. The full `error-report.zip`
> 2. The exact firmware version (`show version` output)
> 3. The timestamp of the crash and your timezone
> 4. What was happening on the appliance at the time (traffic spike, deployment, config change)

---

## 6. Diagnosing a Throttler Reload (No Backtrace)

A Throttler Reload leaves no backtrace. Diagnose it through memory data:

**Step 1 — Confirm it was a Throttler Reload:**

```bash
# In system.log, search for:
throttler-reload
# or
memory threshold
```

**Step 2 — Establish the memory trend before the reload:**

Open `MemoryStatus2.xml` from the error report. The `AvailableMemory` field shows the state at time of report. Compare against any previously collected `show memory` snapshots or monitoring data to establish the trend.

**Step 3 — Identify the memory consumer:**

Run these commands on the recovered appliance to understand what is using memory:

```bash
top; co; show memory
top; co; show statistics
```

Then open `DomainsMemoryStatus2.xml` from the error report — the `ServicesLifetime` counter per domain indicates which domain has processed the most data. The largest consumers are the most likely candidates, though per-domain figures will not pinpoint a genuine leak (see the [memory post](/2026/07/24/95-DataPower-Memory-and-Performance-Understanding-What-Normal-Looks-Like) for detail on why).

**Step 4 — Check the throttle thresholds:**

Navigate to **WebGUI → Administration → Device → Memory Management** and note the configured thresholds. If Available memory is consistently hovering near the Throttle At threshold, the thresholds need adjusting or the appliance is genuinely under-resourced.

---

## 7. What to Send IBM Support

A support case opened with the right data upfront resolves significantly faster. For a restart:

| Item | How to get it |
|---|---|
| Full `error-report.zip` | `generate error-report` from CLI, then download |
| `show version` output | From CLI — include firmware build number |
| `show system` output | System identity, uptime, serial |
| Timeline of events | What changed in the 30 minutes before the restart |
| `system.log` excerpt | 200 lines either side of the restart event |
| Backtrace files | Already inside the error-report.zip — confirm they are present |
| Memory trend graph | 48-hour graph from your monitoring tool if available |

Do not paraphrase the logs in the case description. Attach the files. Support engineers read log files faster than case descriptions and it eliminates ambiguity.

---

## 8. Quick Triage Checklist

```
□ Was there a backtrace?
  YES → Firmware panic → open support case with error-report + show version
  NO  → Continue below

□ Does system.log show "throttler-reload"?
  YES → Memory-triggered restart → check MemoryStatus2.xml trend + thresholds
  NO  → Check for "shutdown initiated" → manual or OCP-driven restart

□ Is this repeating on a schedule?
  YES → Likely correlated with a batch job, cert rotation, or scheduled task → check cron/automation

□ Did it affect only one node in an HA pair?
  YES → Hardware or network issue on that node more likely → check OCP node events

□ Can you reproduce it?
  YES → Capture error-report immediately after next occurrence
```
