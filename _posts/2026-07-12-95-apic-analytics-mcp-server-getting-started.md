---
layout: post
date: 2026-07-12 18:00:00
categories: APIConnect
title: "Getting Started with the IBM API Connect MCP Server (Preview)"
description: "How to install, configure, and use the IBM API Connect Analytics MCP Server to query analytics data programmatically from AI tools and agents."
tags: [APIConnect, MCP, Analytics, Automation, AI]
draft: true
author: ["ChrisPhillips", "IBMBob"]
---

The API Connect MCP Server preview is a way to query API Connect analytics data from MCP-capable clients. If you want to ask natural-language questions about API usage from an AI client, this package is one way to do it.

This article covers what the MCP server is, how to install it, how to connect it to a client, and what analytics tools it exposes.

<!--more-->

## Table of Contents

1. [What Is the MCP Server?](#what-is-the-mcp-server)
2. [Architecture Overview](#architecture-overview)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Connecting Your AI Client](#connecting-your-ai-client)
7. [Available Analytics Tools](#available-analytics-tools)
8. [Example Sessions](#example-sessions)
9. [Debug Logs](#debug-logs)
10. [Preview Caveats](#preview-caveats)

## What Is the MCP Server?

The API Connect MCP Server is a standalone service that implements the Model Context Protocol server interface. MCP, originally developed by Anthropic, defines a standard way for AI applications to connect to external tools and data sources. When an MCP server is running, AI assistants that support MCP can discover its tools and call them as part of a conversation.

The server is distributed as a set of pre-built `.tgz` files (and `.mcpb` installer files for Claude Desktop) downloaded directly from the public GitHub repository — it has not been published to the npm registry. Each `.tgz` covers a different capability area. The **Analytics** service — the focus of this article — exposes your API Connect analytics data as MCP tools. The repository also contains Management and other service packages.

This means you can ask an AI assistant (Claude Desktop, VS Code Copilot, IBM Bob, or any MCP-compatible AI tool) natural language questions about your API programme and get structured answers pulled directly from live API Connect analytics data.

## Architecture Overview

```
┌─────────────────────────┐
│  AI Assistant (Client)  │  Claude Desktop / VS Code / IBM Bob
└────────────┬────────────┘
             │ stdio (MCP protocol)
┌────────────▼────────────┐
│  apic-analytics-        │  ← This is what you install (tgz / mcpb)
│  mcp-server (Node.js)   │
└────────────┬────────────┘
             │ HTTPS REST API
┌────────────▼────────────┐
│  API Connect            │
│  Platform + Management  │
│  Endpoints              │
└─────────────────────────┘
```

The server is invoked via `npx` by the MCP client — you do not run it as a persistent background service.

## Prerequisites

Before installing, ensure you have:

1. **A supported API Connect deployment** with analytics data available to the MCP package you intend to use
2. **Node.js 20+** up to Node.js 24 (`"node": ">=20.0.0 <25.0.0"` per `package.json`)
3. **npm** installed
4. The following values from your API Connect instance:
   - **Provider Organization** name
   - **API Key**
   - **Client ID** configured on your instance
   - **Client Secret** configured on your instance
   - **APIC Platform Endpoint** URL
   - **APIC Management Endpoint** URL
5. A compatible MCP client such as Claude Desktop, VS Code, or IBM Bob

> **Note:** The post originally stated Node.js 18+. The actual `package.json` in the published package requires **Node.js 20–24**.

## Installation

The preview package is downloaded directly from the public GitHub repository — it is **not** published to the npm registry. Download the current analytics `.tgz` from:

```
https://github.com/ibm-apiconnect/apic-mcp-server/tree/main/analytics
```

The exact filename and version may change between preview releases. Save the downloaded `.tgz` to a stable path on your machine (e.g. `~/apic-mcp/apic-analytics-mcp-server-0.0.1.tgz`).

The MCP client invokes it via `npx` pointing at your local `.tgz` path — there is no global `npm install` step and no separate server process to start.

## Configuration

All configuration is passed through the **env block inside your MCP client config file** (e.g. `.vscode/mcp.json`, `.bob/mcp.json`, or the Claude Desktop equivalent). There is no separate config file, no `--config` CLI flag, and no environment variables you set in your shell — the MCP client reads the `env` block from its own config and injects them when it launches the server process. The variables it expects are:

| Variable | Description |
|---|---|
| `PROVIDER_ORG` | Your provider organization name |
| `API_KEY` | Your API Connect API key |
| `client_id` | Client ID for your APIC instance |
| `client_secret` | Client Secret for your APIC instance |
| `APIC_PLATFORM_URL` | Your APIC platform endpoint URL |
| `APIC_MANAGEMENT_URL` | Your APIC management endpoint URL |
| `NODE_TLS_REJECT_UNAUTHORIZED` | Set to `0` to disable certificate validation (for self-signed certs), `1` to enable |
| `LOG_LEVEL` | Optional. Set to `debug` for verbose logging (default: `info`) |

> **Security note:** Treat `API_KEY` and `client_secret` as passwords. Do not commit them to source control. MCP client config files support secret prompting — use that mechanism rather than hardcoding values.

## Connecting Your AI Client

The repository includes examples for several MCP clients. In all cases you provide the path to the downloaded `.tgz` file.

### Claude Desktop

If the release includes a `.mcpb` installer file, Claude Desktop can use it to simplify setup:

1. Download `analytics/apic-analytics-mcp-server-0.0.1.mcpb` from the repository
2. **Double-click** the `.mcpb` file — Claude Desktop opens and starts the installation wizard
3. The wizard prompts for your APIC credentials (see Prerequisites above)
4. Click **Save** / **Install**
5. Confirm the extension is enabled after installation before testing it

### VS Code (GitHub Copilot)

Use the template from the repository at [`analytics/mcp.vscode.json`](https://github.com/ibm-apiconnect/apic-mcp-server/blob/main/analytics/mcp.vscode.json):

```json
{
  "servers": {
    "apic-analytics-mcp-server": {
      "command": "npx",
      "args": ["-y", "-p", "${input:tarPath}", "apic-analytics-mcp-server"],
      "env": {
        "PROVIDER_ORG": "${input:pOrg}",
        "API_KEY": "${input:api-key}",
        "client_id": "${input:cID}",
        "client_secret": "${input:cSecret}",
        "APIC_PLATFORM_URL": "${input:platformUrl}",
        "APIC_MANAGEMENT_URL": "${input:managementUrl}",
        "NODE_TLS_REJECT_UNAUTHORIZED": "${input:validateCertificates}"
      }
    }
  }
}
```

Copy this to your workspace `.vscode/mcp.json` and fill in values, or use VS Code's `inputs` prompting to have it ask for credentials interactively. Full instructions: [VS Code MCP server setup](https://code.visualstudio.com/docs/copilot/customization/mcp-servers#_add-an-mcp-server).

### IBM Bob

Use the template from [`analytics/mcp.bob.json`](https://github.com/ibm-apiconnect/apic-mcp-server/blob/main/analytics/mcp.bob.json):

```json
{
  "mcpServers": {
    "apic-analytics-mcp-server": {
      "command": "npx",
      "args": ["-y", "-p", "<path-to-tgz>", "apic-analytics-mcp-server"],
      "env": {
        "NODE_TLS_REJECT_UNAUTHORIZED": "1",
        "PROVIDER_ORG": "<your-provider-organization-name>",
        "API_KEY": "<your-api-key>",
        "client_id": "<your-client-id>",
        "client_secret": "<your-client-secret>",
        "APIC_PLATFORM_URL": "<your-apic-platform-url>",
        "APIC_MANAGEMENT_URL": "<your-apic-management-url>"
      }
    }
  }
}
```

Copy this to `.bob/mcp.json` in your workspace and replace the placeholder values. Restart Bob after saving. Full instructions: [IBM Bob MCP server setup](https://www.ibm.com/think/tutorials/mcp-integration-ibm-bob).

## Available Analytics Tools

The analytics MCP server exposes analytics-focused tools such as the following (tool names should be checked against the exact preview package you downloaded):

| Tool | What it answers |
|---|---|
| `GetAnalyticsUsage` | API call counts and error rates; spikes in API usage; popularity ranking |
| `GetAnalyticsApplication` | Which applications are driving traffic; application error rates; subscription information |
| `GetAnalyticsConsumer` | Consumer organization activity; error rates per consumer org; traffic over time |
| `GetAnalyticsLatency` | API response times (min / max / average); fastest and slowest APIs; time-to-error |
| `GetAnalyticsStatus` | HTTP response status code distribution across API calls |
| `GetAnalyticsUsers` | Geographic usage (countries, timezones); user agents; client IP data |
| `GetAnalyticsAILLM` | AI / LLM token consumption; model usage patterns; consumer orgs using AI services |
| `GetAnalyticsMCP` | MCP call volumes; MCP tool popularity; consumer orgs using MCP services |

Query interpretation and default date handling depend on the MCP client and package version. Check the package documentation or try a few basic queries in your client to confirm the current behaviour.

Some preview builds may also include governance, scan, or OpenAPI-related tools, but those are beyond the scope of this article.

## Example Sessions

### Example 1: "What were our top APIs by traffic last week?"

```
What were the top 5 APIs by traffic volume in the last 7 days?
```

A client could use an analytics usage tool to retrieve and rank API call counts, returning a summary like:

```
Based on API Connect analytics for the last 7 days:

Top 5 APIs by call volume:
1. /forex/rates       — 2.1M calls
2. /payments/checkout — 1.8M calls
3. /accounts/balance  — 1.2M calls
4. /orders/history    — 890K calls
5. /users/profile     — 654K calls
```

### Example 2: "Are there APIs with elevated error rates?"

```
Which APIs have error rates above 1% this month?
```

The client can call one or more analytics tools and return a summary of APIs exceeding the threshold.

### Example 3: "Which consumer orgs are sending the most traffic?"

```
Show me the top consumer organizations by API calls this quarter.
```

The client can call a consumer-oriented analytics tool and return a ranked list with call counts per consumer org.

## Debug Logs

When running, the preview package may write `INFO`-level logs to a rotating daily file such as:

- **macOS / Linux:** `~/apic-mcp/apic-mcp-YYYY-MM-DD.log`
- **Windows:** `%USERPROFILE%\apic-mcp\apic-mcp-YYYY-MM-DD.log`

Retention and log-level behaviour may vary by package version. If supported by your build, add `LOG_LEVEL: 'debug'` to the `env` section of your MCP client config to enable more verbose logging.

## Preview Caveats

As this is a **preview (v0.0.1)** release, be aware of the following:

- **GitHub-distributed, not on npm:** Download the `.tgz` directly from the repository. You point `npx` at that local file — there is no npm registry entry and no global install.
- **Node.js version constraint:** Check the `package.json` bundled with the package you downloaded and use that as the source of truth.
- **Authentication model:** Confirm the required credentials for your target package and deployment before rollout.
- **No persistent server process:** The package is invoked by the MCP client on demand rather than run as a long-lived background service.
- **Preview support posture:** Check IBM release notes or repository guidance for the current support expectations of the preview.
- **MCP spec evolution:** As MCP evolves, config formats and tool signatures may change between releases. Check the [GitHub repository](https://github.com/ibm-apiconnect/apic-mcp-server) for the latest version.

## Summary

The IBM API Connect MCP Server preview is a promising way to query analytics data from MCP-capable clients. The analytics tools map well to real-world questions about API usage, consumer behaviour, latency, and error rates. If you're building AI-powered operations workflows, it's worth evaluating with the exact preview package and client combination you intend to support.

The key practical points: download the `.tgz` directly from GitHub (it is not on npm), save it to a stable local path, check the bundled `package.json` for the supported Node.js range, and configure it via the `env` block in your MCP client config file (`.vscode/mcp.json`, `.bob/mcp.json`, Claude Desktop config, etc.) using the template provided with the release.

See also: [IBM API Connect Analytics tools documentation](https://www.ibm.com/docs/en/api-connect/software/12.1.0?topic=tools-analytics)
