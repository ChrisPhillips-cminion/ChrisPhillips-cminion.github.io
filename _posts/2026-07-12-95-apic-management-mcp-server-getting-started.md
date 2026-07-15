---
layout: post
date: 2026-07-12 19:00:00
categories: APIConnect
title: "IBM API Connect MCP Server Part 2: API Manager and AI Tools"
description: "A guide to the Management and Management AI MCP servers in the IBM API Connect MCP Server preview — what they do, how to install them, and how to connect them to your AI client."
tags: [APIConnect, MCP, Management, Automation, AI, GatewayScript, Spectral]
draft: true
author: ["ChrisPhillips", "IBMBob"]
---

[Part 1 of this series]({% post_url 2026-07-12-95-apic-analytics-mcp-server-getting-started %}) covered the Analytics MCP server — querying API usage data from an AI client. This article covers the two remaining servers in the same GitHub repository: the **Management MCP server**, which lets you interact with and manage your API Connect provider organisation through natural language, and the **Management AI MCP server**, which brings generative AI capabilities to gateway policy authoring, spectral governance rules, and OpenAPI enhancement.

<!--more-->

## Table of Contents

1. [Repository Layout](#repository-layout)
2. [Management MCP Server](#management-mcp-server)
   - [What It Does](#what-it-does)
   - [Installation](#installation)
   - [Configuration](#configuration)
   - [Connecting Your AI Client](#connecting-your-ai-client)
   - [Available Tools](#available-tools)
3. [Management AI MCP Server](#management-ai-mcp-server)
   - [What It Does](#what-it-does-1)
   - [Installation](#installation-1)
   - [Configuration](#configuration-1)
   - [Connecting Your AI Client](#connecting-your-ai-client-1)
   - [Available Tools](#available-tools-1)
4. [Example Sessions](#example-sessions)
5. [Running Multiple Servers Together](#running-multiple-servers-together)
6. [Preview Caveats](#preview-caveats)

## Repository Layout

The [ibm-apiconnect/apic-mcp-server](https://github.com/ibm-apiconnect/apic-mcp-server) repository contains several service folders, each with its own `.tgz` and `.mcpb` files:

| Folder | Package name | What it covers |
|---|---|---|
| `analytics/` | `apic-analytics-mcp-server` | API analytics queries (covered in Part 1) |
| `management/` | `apic-management-mcp-server` | Catalog, product, API, consumer org and subscription management |
| `management-ai/` | `apic-management-ai-mcp-server` | AI-assisted gateway policy generation, spectral rule creation, OpenAPI enhancement |
| `governance/` | — | Governance tooling (separate article) |

None of these packages are published to the npm registry. All are downloaded as pre-built `.tgz` files directly from the repository.

## Management MCP Server

### What It Does

The Management MCP server exposes your API Connect provider organisation over the MCP protocol. From an AI client you can discover catalogs, list published APIs and products, inspect consumer organisations and applications, manage subscriptions, create consumer apps, and publish APIs and products — all via natural language prompts.

The IBM documentation lists the full set of operations at [API Connect Management tools documentation](https://www.ibm.com/docs/en/api-connect/software/12.1.0?topic=tools-api-connect-task).

### Installation

Download the `.tgz` directly from the management folder of the repository — it is **not** on npm:

```
https://github.com/ibm-apiconnect/apic-mcp-server/tree/main/management
```

Save the file to a stable path, for example `~/apic-mcp/apic-management-mcp-server-0.0.1.tgz`.

A `.mcpb` installer (`apic-management-mcp-server-0.0.1.mcpb`) is also available in the same folder for Claude Desktop.

### Configuration

Configuration is passed through the `env` block in your MCP client config file — the same variables as the Analytics server, and the same rule: no `--config` CLI flag, no shell environment, just the `env` block:

| Variable | Description |
|---|---|
| `PROVIDER_ORG` | Your provider organization name |
| `API_KEY` | Your API Connect API key |
| `client_id` | Client ID for your APIC instance |
| `client_secret` | Client Secret for your APIC instance |
| `APIC_PLATFORM_URL` | Your APIC platform endpoint URL |
| `APIC_MANAGEMENT_URL` | Your APIC management endpoint URL |
| `NODE_TLS_REJECT_UNAUTHORIZED` | `0` to disable certificate validation (self-signed certs), `1` to enable |
| `LOG_LEVEL` | Optional. `debug` for verbose logging |

### Connecting Your AI Client

#### IBM Bob

Use the template from [`management/mcp.bob.json`](https://github.com/ibm-apiconnect/apic-mcp-server/blob/main/management/mcp.bob.json):

```json
{
  "mcpServers": {
    "apic-management-mcp-server": {
      "command": "npx",
      "args": ["-y", "-p", "<path-to-tgz>", "apic-management-mcp-server"],
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

Copy this to `.bob/mcp.json` and replace the placeholders. Restart Bob after saving.

#### VS Code (GitHub Copilot)

Use the template from [`management/mcp.vscode.json`](https://github.com/ibm-apiconnect/apic-mcp-server/blob/main/management/mcp.vscode.json):

```json
{
  "servers": {
    "apic-management-mcp-server": {
      "command": "npx",
      "args": ["-y", "-p", "${input:tarPath}", "apic-management-mcp-server"],
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

Copy to `.vscode/mcp.json`. VS Code will prompt for each value when the server first starts.

#### Claude Desktop

Double-click `apic-management-mcp-server-0.0.1.mcpb` from the management folder. The setup wizard prompts for your credentials. Enable the extension after installation.

### Available Tools

The management server exposes three groups of operations:

**Catalog and API Manager operations**

| Operation | What it does |
|---|---|
| List catalogs | Returns all catalogs in the provider org, with pagination |
| List published APIs | Lists APIs published to a catalog (default: Sandbox) |
| List published products | Lists products published to a catalog |
| List gateways in catalog | Lists configured gateways for a catalog |

**Consumer-related operations**

| Operation | What it does |
|---|---|
| List consumer organizations | Lists consumer orgs in a catalog |
| List applications in catalog | Lists consumer apps, optionally filtered by consumer org |
| List consumer app credentials | Returns credentials for a specific consumer app |
| List subscriptions in catalog | Lists subscriptions with optional filtering by plan, consumer org, or product |
| List subscriptions in consumer app | Lists subscriptions for a specific app |
| Create consumer app | Creates a consumer application in a catalog (requires confirmation) |
| Create subscription for an API | Subscribes a consumer app to a published API's plan |
| Create subscription for a product | Subscribes a consumer app to a product's plan |

**Project-related operations**

| Operation | What it does |
|---|---|
| Create project | Creates an API Manager–managed project with optional description and tags |
| List projects | Lists all projects in the provider org with pagination |
| List files in project | Lists the files (APIs, products) inside a named project |

> **Note:** Catalog-dependent operations (list consumer orgs, list apps, create consumer app, create subscription, publish API, publish product) require the target catalog to be enabled for API Agent in the API Manager UI. The operation will fail if the catalog is not enabled.

## Management AI MCP Server

### What It Does

The Management AI MCP server is a generative AI toolbox for API practitioners. It uses foundation models to help you write DataPower gateway policy YAML, generate spectral governance rules from natural language, and enhance or correct OpenAPI specifications. The output is always reviewed YAML or JSON that you can download and apply — it does not make direct changes to your API Connect instance.

The IBM documentation is at [Management AI MCP documentation](https://www.ibm.com/docs/en/api-connect/software/12.1.0?topic=tools-management-ai-mcp).

### Installation

Download the `.tgz` from the management-ai folder — not on npm:

```
https://github.com/ibm-apiconnect/apic-mcp-server/tree/main/management-ai
```

Save to, for example, `~/apic-mcp/apic-management-ai-mcp-server-0.0.1.tgz`.

A `.mcpb` installer is available in the same folder for Claude Desktop.

### Configuration

Same environment variables as the management server — all passed through the `env` block of the client config:

| Variable | Description |
|---|---|
| `PROVIDER_ORG` | Your provider organization name |
| `API_KEY` | Your API Connect API key |
| `client_id` | Client ID |
| `client_secret` | Client Secret |
| `APIC_PLATFORM_URL` | APIC platform endpoint URL |
| `APIC_MANAGEMENT_URL` | APIC management endpoint URL |
| `NODE_TLS_REJECT_UNAUTHORIZED` | `0` or `1` |
| `LOG_LEVEL` | Optional. `debug` for verbose logging |

### Connecting Your AI Client

#### IBM Bob

From [`management-ai/mcp.bob.json`](https://github.com/ibm-apiconnect/apic-mcp-server/blob/main/management-ai/mcp.bob.json):

```json
{
  "mcpServers": {
    "apic-management-ai-mcp-server": {
      "command": "npx",
      "args": ["-y", "-p", "<path-to-tgz>", "apic-management-ai-mcp-server"],
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

#### VS Code (GitHub Copilot)

From [`management-ai/mcp.vscode.json`](https://github.com/ibm-apiconnect/apic-mcp-server/blob/main/management-ai/mcp.vscode.json):

```json
{
  "servers": {
    "apic-management-ai-mcp-server": {
      "command": "npx",
      "args": ["-y", "-p", "${input:tarPath}", "apic-management-ai-mcp-server"],
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

### Available Tools

**`ListGatewayPolicies`**

Returns the list of policies available for AI-assisted generation. Covers both the DataPower API Gateway and the DataPower Nano Gateway.

DataPower API Gateway policies available: `activity-log`, `client-security`, `extract`, `gatewayscript`.

DataPower Nano Gateway policies available: `block`, `cors`, `invoke`, `parse`, `ratelimit`, `redact`, `remove`, `set`, `validate`.

Example prompts:
```
List gateway policies for generation
What are all the datapower nano gateway policies available for generation?
```

**`GatewayPolicyGenerator`**

Generates a DataPower API Gateway or Nano Gateway assembly document in YAML format from a list of policies you specify. Optionally associates the output with an API name or project (IBM API Studio only).

Example prompts:
```
Create a datapower api gateway with the ratelimit, map and invoke gateway policies
Generate a datapower nano gateway with the invoke gateway policy for the project SampleProject
```

**`GatewayPolicyModifier`**

Takes an existing DataPower assembly YAML file (referenced with `@filename.yaml`) and adds or modifies gateway policies within it. Outputs the updated YAML.

Example prompts:
```
Add the datapower api gateway client-security and map policies to @da.yaml
Extend this datapower nano gateway document @sample-da.yaml with the invoke gateway policies for the api sample-api
```

**`SpectralRuleGenerator`**

Converts a natural language description into a spectral rule in JSON format. The generated rule can be downloaded and added to a spectral ruleset for API governance.

Write clear, single-operation descriptions for best results. Specify `jsonPath` fields when possible.

Example prompts:
```
Generate a spectral rule that ensures info.description must be at least 20 characters long
Generate a spectral rule that ensures all POST operations must have a request body defined
Generate a spectral rule that ensures info.title must not contain special characters
```

> Always validate generated spectral rules with the Spectral rule validator before deploying them to a live governance pipeline.

**`OpenAPI Enhancer`**

Enhances or corrects an OpenAPI 3.0 specification. Two modes:

- **Suggest improvements** — analyses the spec and generates recommendations for descriptions and examples
- **Correct validation errors** — identifies validation errors in the spec and generates potential corrections

Pass an OpenAPI file with `@filename.yaml`. Output is downloadable YAML or JSON.

Example prompts:
```
Augment the following openapi with enhanced descriptions and examples @openapi-sample.yaml
Correct the validation errors in the following openapi file @openapi-sample.yaml
```

**`OpenAPI Generator`** — generates an OpenAPI specification. Check the current preview package for exact parameters and prompts.

## Example Sessions

### "List all the consumer orgs subscribed to my payments product"

```
List consumer orgs in catalog production
List subscriptions in catalog production filtered by product payments:2.0.0
```

The management server returns all consumer orgs in the production catalog, then all subscriptions against the payments 2.0.0 product — useful for understanding blast radius before a deprecation.

### "Generate a rate-limit policy for my DataPower nano gateway"

```
Generate a datapower nano gateway with the ratelimit and invoke gateway policies
```

`GatewayPolicyGenerator` returns a YAML assembly document with both policies pre-configured. You can then paste this into your API assembly.

### "Write a spectral rule to enforce that every API has a contact email"

```
Generate a spectral rule that ensures info.contact.email is present and non-empty in every OpenAPI document
```

`SpectralRuleGenerator` returns a JSON spectral rule. Download it, validate it with the spectral validator, and add it to your governance ruleset.

## Running Multiple Servers Together

You can run the analytics, management, and management-ai servers simultaneously in the same client. Each server registers under a different key in the `mcpServers` (Bob / Claude) or `servers` (VS Code) block:

```json
{
  "mcpServers": {
    "apic-analytics-mcp-server": {
      "command": "npx",
      "args": ["-y", "-p", "~/apic-mcp/apic-analytics-mcp-server-0.0.1.tgz", "apic-analytics-mcp-server"],
      "env": { "...": "..." }
    },
    "apic-management-mcp-server": {
      "command": "npx",
      "args": ["-y", "-p", "~/apic-mcp/apic-management-mcp-server-0.0.1.tgz", "apic-management-mcp-server"],
      "env": { "...": "..." }
    },
    "apic-management-ai-mcp-server": {
      "command": "npx",
      "args": ["-y", "-p", "~/apic-mcp/apic-management-ai-mcp-server-0.0.1.tgz", "apic-management-ai-mcp-server"],
      "env": { "...": "..." }
    }
  }
}
```

This means a single conversation can jump between "which APIs have high error rates this week?" (analytics), "list the consumer apps subscribed to that API" (management), and "generate a tighter rate limit policy for it" (management-ai) without switching tools.

## Preview Caveats

The same caveats as Part 1 apply, plus a few specific to the AI tooling:

- **GitHub-distributed, not on npm:** Download `.tgz` files directly from the repository. No npm registry entry exists.
- **AI output requires validation:** `SpectralRuleGenerator`, `GatewayPolicyGenerator`, `GatewayPolicyModifier`, and the OpenAPI Enhancer all use foundation models. The output can contain errors or hallucinations. Validate generated spectral rules before use. Review generated YAML before deploying.
- **Catalog must be API Agent–enabled:** Consumer, subscription, publish, and list operations require the target catalog to have API Agent enabled in the API Manager UI.
- **Node.js 20–24 required:** Check the bundled `package.json` for the exact constraint.
- **No persistent process:** All servers are invoked on demand by the MCP client via `npx`.
- **Preview support posture:** Check the [GitHub repository](https://github.com/ibm-apiconnect/apic-mcp-server) for the current release state and any known issues.

## Summary

The Management and Management AI MCP servers extend the API Connect MCP Server preview beyond read-only analytics into active management and AI-assisted authoring. The management server covers the day-to-day lifecycle operations you'd normally do in the API Manager UI. The management-ai server brings generative AI to the parts of API development that are currently manual and time-consuming: writing gateway policy assemblies, authoring spectral governance rules, and improving OpenAPI specifications.

Both servers use the same installation pattern as Part 1: download the `.tgz` from GitHub, configure the `env` block in your MCP client config file, and run via `npx`. No npm registry, no `--config` flag, no background process.

See also:
- [Part 1: Analytics MCP Server]({% post_url 2026-07-12-95-apic-analytics-mcp-server-getting-started %})
- [IBM API Connect Management tools documentation](https://www.ibm.com/docs/en/api-connect/software/12.1.0?topic=tools-api-connect-task)
- [IBM API Connect Management AI MCP documentation](https://www.ibm.com/docs/en/api-connect/software/12.1.0?topic=tools-management-ai-mcp)
- [GitHub repository](https://github.com/ibm-apiconnect/apic-mcp-server)
