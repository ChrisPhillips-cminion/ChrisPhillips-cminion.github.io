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

The API Connect MCP Server preview lets you query API Connect analytics data from MCP-capable AI clients. If you want to ask natural-language questions about API usage from an AI client, this package is one way to do it.

<!--more-->

## What Is the MCP Server?

The API Connect MCP Server is a standalone service that implements the Model Context Protocol server interface. MCP, originally developed by Anthropic, defines a standard way for AI applications to connect to external tools and data sources.

The server is distributed as pre-built `.tgz` files (and `.mcpb` installer files for Claude Desktop) downloaded directly from the public GitHub repository — it has not been published to the npm registry. The **Analytics** service exposes your API Connect analytics data as MCP tools, letting you ask an AI assistant (Claude Desktop, VS Code Copilot, IBM Bob, or any MCP-compatible client) natural-language questions about your API programme and get answers pulled directly from live analytics data.

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

- A supported API Connect deployment with analytics data
- **Node.js 20+** up to Node.js 24 (`"node": ">=20.0.0 <25.0.0"` per `package.json`)
- npm installed
- From your API Connect instance: Provider Organisation name, API Key, Client ID, Client Secret, APIC Platform Endpoint URL, APIC Management Endpoint URL
- A compatible MCP client (Claude Desktop, VS Code, IBM Bob)

## Installation

The preview package is downloaded directly from the public GitHub repository — it is **not** on npm:

```
https://github.com/ibm-apiconnect/apic-mcp-server/tree/main/analytics
```

Save the downloaded `.tgz` to a stable path (e.g. `~/apic-mcp/apic-analytics-mcp-server-0.0.1.tgz`). The MCP client invokes it via `npx` pointing at your local `.tgz` — there is no global `npm install` step and no separate server process to start.

## Configuration

All configuration is passed through the **env block inside your MCP client config file** (e.g. `.vscode/mcp.json`, `.bob/mcp.json`, or the Claude Desktop equivalent). There is no separate config file, no `--config` CLI flag, and no environment variables set in your shell.

| Variable | Description |
|---|---|
| `PROVIDER_ORG` | Your provider organisation name |
| `API_KEY` | Your API Connect API key |
| `client_id` | Client ID for your APIC instance |
| `client_secret` | Client Secret for your APIC instance |
| `APIC_PLATFORM_URL` | Your APIC platform endpoint URL |
| `APIC_MANAGEMENT_URL` | Your APIC management endpoint URL |
| `NODE_TLS_REJECT_UNAUTHORIZED` | `0` to disable certificate validation (self-signed certs), `1` to enable |
| `LOG_LEVEL` | Optional. `debug` for verbose logging |

> **Security note:** Treat `API_KEY` and `client_secret` as passwords. Do not commit them to source control.

## Connecting Your AI Client

### Claude Desktop

1. Download `analytics/apic-analytics-mcp-server-0.0.1.mcpb` from the repository
2. Double-click the `.mcpb` file — Claude Desktop opens and starts the installation wizard
3. The wizard prompts for your APIC credentials
4. Click **Save** / **Install**
5. Confirm the extension is enabled before testing

### VS Code (GitHub Copilot)

Use the template from [`analytics/mcp.vscode.json`](https://github.com/ibm-apiconnect/apic-mcp-server/blob/main/analytics/mcp.vscode.json):

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

Copy to `.vscode/mcp.json` and fill in values. Full instructions: [VS Code MCP server setup](https://code.visualstudio.com/docs/copilot/customization/mcp-servers#_add-an-mcp-server).

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

Copy to `.bob/mcp.json`, replace placeholders, and restart Bob. Full instructions: [IBM Bob MCP server setup](https://www.ibm.com/think/tutorials/mcp-integration-ibm-bob).

## Available Analytics Tools

| Tool | What it answers |
|---|---|
| `GetAnalyticsUsage` | API call counts and error rates; spikes in API usage; popularity ranking |
| `GetAnalyticsApplication` | Which applications are driving traffic; application error rates; subscription information |
| `GetAnalyticsConsumer` | Consumer organisation activity; error rates per consumer org; traffic over time |
| `GetAnalyticsLatency` | API response times (min / max / average); fastest and slowest APIs |
| `GetAnalyticsStatus` | HTTP response status code distribution across API calls |
| `GetAnalyticsUsers` | Geographic usage (countries, timezones); user agents; client IP data |
| `GetAnalyticsAILLM` | AI / LLM token consumption; model usage patterns; consumer orgs using AI services |
| `GetAnalyticsMCP` | MCP call volumes; MCP tool popularity; consumer orgs using MCP services |

Tool names should be checked against the exact preview package you downloaded.

## Example Sessions

### "What were our top APIs by traffic last week?"

```
What were the top 5 APIs by traffic volume in the last 7 days?
```

Response:

```
Based on API Connect analytics for the last 7 days:

Top 5 APIs by call volume:
1. /forex/rates       — 2.1M calls
2. /payments/checkout — 1.8M calls
3. /accounts/balance  — 1.2M calls
4. /orders/history    — 890K calls
5. /users/profile     — 654K calls
```

### "Are there APIs with elevated error rates?"

```
Which APIs have error rates above 1% this month?
```

### "Which consumer orgs are sending the most traffic?"

```
Show me the top consumer organisations by API calls this quarter.
```

## Debug Logs

The preview package may write `INFO`-level logs to a rotating daily file:

- **macOS / Linux:** `~/apic-mcp/apic-mcp-YYYY-MM-DD.log`
- **Windows:** `%USERPROFILE%\apic-mcp\apic-mcp-YYYY-MM-DD.log`

Add `LOG_LEVEL: 'debug'` to the `env` section of your MCP client config to enable verbose logging.

## Preview Caveats

- **GitHub-distributed, not on npm:** Download the `.tgz` directly from the repository. No npm registry entry exists.
- **Node.js version constraint:** Check the `package.json` bundled with the package you downloaded for the exact constraint.
- **No persistent server process:** The package is invoked by the MCP client on demand.
- **MCP spec evolution:** Config formats and tool signatures may change between releases. Check the [GitHub repository](https://github.com/ibm-apiconnect/apic-mcp-server) for the latest version.

The key practical points: download the `.tgz` directly from GitHub (not on npm), save it to a stable local path, check the bundled `package.json` for the supported Node.js range, and configure it via the `env` block in your MCP client config file.

See also: [IBM API Connect Analytics tools documentation](https://www.ibm.com/docs/en/api-connect/software/12.1.0?topic=tools-analytics)
