---
layout: post
date: 2026-11-28 09:00:00
categories: APIConnect
title: "Writing a gateway extension for API Connect"
author: ["ChrisPhillips", "IBMBob"]
description: "A gateway extension is the supported way to set DataPower gateway behaviour the API Connect UI doesn't expose. The manifest, the gwd_extension override file, the twelve object types you can override, packaging, and the upload and apply workflow — with links to four worked examples."
tags: [APIConnect, DataPower, GatewayExtension, gwd_extension, CLI]
draft: true
image: /images/gateway-extension-manifest.png
---

Some gateway behaviour just isn't exposed in the API Connect UI — rate limit objects, invoke proxies, TLS client settings, cipher priority order. The supported way to set it is a gateway extension. I have written four of them for this blog; this article puts the whole workflow in one place.

<!--more-->

## What a gateway extension is

A zip file with a `manifest.json` at the root, plus implementation files. What goes in the implementation files depends on your gateway type:

- **DataPower API Gateway** — a `gwd_extension` JSON file carrying override commands.
- **v5-compatible DataPower Gateway** — DataPower exported configuration, with the extension XML saved to `local:///ext/extensions.xml` inside the exported config zip.

## The manifest

The manifest tells API Connect what the zip contains. The two sections that matter:

- **`properties`** — deployment behaviour: `deploy-policy-emulator`, `deploy-policies`, and `defer-all-override`.
- **`files`** — one entry per file: `filename`, `type` (seven are supported), `deploy` set to `immediate` or `deferred`, and the `catalog` the file applies to.

The full property tables are in the KC under "Gateway extensions manifest" — worth keeping open while you write your first one.

## The gwd_extension override file

For the API Gateway, the override file maps object types to scopes to commands:

```json
{ "apigw": { "_global": { "override": [
  "assembly-rate-limit ratelimit-reject-ALL 10000 5 second on on on off off off \"\" \"1\""
] } } }
```

The scopes, coarsest to finest: `_global`, `_organization`, `_catalog`, `_product`, `_instance`. An `@exclusive` flag marks a scope as taking precedence, and entries apply in granularity order.

The override entries are DataPower gateway CLI commands — the same commands you would run on the gateway object directly. Some examples that appear in the manifest reference: `document-size 4194304`, `ldap-port 636`, `ssl-client ldap-ssl-client`, `apic-access-token-ttl 86400`, `scopes-allowed cmcscope1`. The full command vocabulary lives in the DataPower documentation, so budget time there when you need a setting the examples don't show.

## The object types you can override

| Object type | What it governs |
|---|---|
| `apigw` | the API Gateway object itself — rate limits via `assembly-rate-limit` |
| `parse-settings` | message parse behaviour, e.g. `document-size` |
| `tls-client` | TLS client settings |
| `registry` | user registries, including LDAP (`ldap-port`, `ssl-client`) |
| `oauth-provider` | OAuth provider — token lifetimes and scopes |
| `front-side-handler` | front-side handler settings |
| `api-collection` | API collections |
| `api-plan` | API plans |
| `api-definition` | API definitions |
| `assembly` | assembly behaviour |
| `analytics-endpoint` | analytics endpoints |
| `config-sequence` | configuration sequencing |

Each object type has a reference page in the KC under the manifest documentation, with its override keys, scopes, and an example.

## Packaging

Zip the manifest and implementation files with `manifest.json` at the root. If you modify a file inside an existing extension zip by hand, update the hash attribute in its `export.xml` — that is part of the DataPower export format, and the gateway will reject or misapply a package whose checksum no longer matches. The clean path is re-exporting from DataPower.

On v5-compatible gateways, mind the restrictions: the `webapi` prefix is reserved, and `local:///isp/*` and `local:///gwapi/*` are immutable. IBM keeps sample extensions in the `dp-extensions` repository on GitHub — good starting points.

## Upload and apply

In the Cloud Manager UI: Topology → options → Configure gateway extension. Or with the toolkit:

```bash
apic login
apic gateway-extensions:create
```

Applying is a restart of the `apic-gw-service`: on Kubernetes, delete the pod; on DataPower, take the object out of the load-balancing group and disable/enable it. Manifest entries marked `deferred` take effect at this restart — so treat the restart as your change window, and test the extension on a non-production gateway service first.

## Worked examples

Every one of these is a `gwd_extension` override file plus a manifest:

- [Setting an invoke proxy]({% link _posts/2024-08-01-setting-invoke-proxy.md %})
- [Creating a rate limit object]({% link _posts/2024-08-07-creating-a-rate-limit.md %}) — the `assembly-rate-limit` example above, in full
- [Circuit breaker in API Connect]({% link _posts/2025-03-7-APIC-CircuitBreaker2025.md %})
- [Setting SSL cipher priority order]({% link _posts/2026-02-19-setting-ssl-cipher-priority.md %})

For v2018 the mechanism was entirely different — configmaps and `apicup`: [the old approach]({% link _posts/2021-02-26-APIC2018-gwextension.md %}).

## Summary

A gateway extension is a zip: `manifest.json` at the root, plus a `gwd_extension` JSON file (API Gateway) or DataPower exported config (v5-compatible). Overrides are DataPower CLI commands scoped from `_global` down to `_instance`, across twelve object types. Upload via the Cloud Manager or `apic gateway-extensions:create`, and apply by restarting the gateway service — which is when deferred entries activate, so plan the window.

## Limitations and Notes

- The full manifest property tables and per-object reference pages are in the KC gateway extensions sections; this article is the workflow around them, not a replacement.
- Override commands are DataPower gateway CLI commands — the DataPower documentation owns the complete vocabulary and arguments per command.
- Extensions take effect at gateway service restart. Validate on a non-production gateway service before the production window.
