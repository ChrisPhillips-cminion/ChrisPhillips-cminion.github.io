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

[Part 1]({% post_url 2026-07-12-95-apic-analytics-mcp-server-getting-started %}) covered the Analytics MCP server — querying API usage data from an AI client. This article covers the two remaining servers in the same GitHub repository: the **Management MCP server**, which lets you interact with and manage your API Connect provider organisation through natural language, and the **Management AI MCP server**, which brings generative AI capabilities to gateway policy authoring, spectral governance rules, and OpenAPI enhancement.

<!--more-->

## Repository Layout

The [ibm-apiconnect/apic-mcp-server](https://github.com/ibm-apiconnect/apic-mcp-server) repository contains several service folders, each with its own `.tgz` and `.mcpb` files:

| Folder | Package name | What it covers |
|---|---|---|
| `analytics/` | `apic-analytics-mcp-server` | API analytics queries (covered in Part 1) |
| `management/` | `apic-management-mcp-server` | Catalog, product, API, consumer org and subscription management |
| `management-ai/` | `apic-management-ai-mcp-server` | AI-assisted gateway policy generation, spectral rule creation, OpenAPI enhancement |

None of these packages are published to the npm registry. All are downloaded as pre-built `.tgz` files directly from the repository.

## Management MCP Server

### What It Does

The Management MCP server exposes your API Connect provider organisation over the MCP protocol. From an AI client you can discover catalogs, list published APIs and products, inspect consumer organisations and applications, manage subscriptions, create consumer apps, and publish APIs and products — all via natural language prompts.

IBM documentation: [API Connect Management tools documentation](https://www.ibm.com/docs/en/api-connect/software/12.1.0?topic=tools-api-connect-task).

### Installation

Download the `.tgz` directly from the management folder — it is **not** on npm:

```
https://github.com/ibm-apiconnect/apic-mcp-server/tree/main/management
```

Save to a stable path, e.g. `~/apic-mcp/apic-management-mcp-server-0.0.1.tgz`. A `.mcpb` installer is also available for Claude Desktop.

### Configuration

Same environment variables as the Analytics server, all passed through the `env` block:

| Variable | Description |
|---|---|
| `PROVIDER_ORG` | Your provider organisation name |
| `API_KEY` | Your API Connect API key |
| `client_id` | Client ID |
| `client_secret` | Client Secret |
| `APIC_PLATFORM_URL` | APIC platform endpoint URL |
| `APIC_MANAGEMENT_URL` | APIC management endpoint URL |
| `NODE_TLS_REJECT_UNAUTHORIZED` | `0` to disable certificate validation, `1` to enable |
| `LOG_LEVEL` | Optional. `debug` for verbose logging |

### Connecting Your AI Client

#### IBM Bob

From [`management/mcp.bob.json`](https://github.com/ibm-apiconnect/apic-mcp-server/blob/main/management/mcp.bob.json):

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

Copy to `.bob/mcp.json` and replace the placeholders. Restart Bob after saving.

#### VS Code (GitHub Copilot)

From [`management/mcp.vscode.json`](https://github.com/ibm-apiconnect/apic-mcp-server/blob/main/management/mcp.vscode.json):

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

Copy to `.vscode/mcp.json`. VS Code prompts for each value when the server first starts.

#### Claude Desktop

Double-click `apic-management-mcp-server-0.0.1.mcpb` from the management folder. The setup wizard prompts for your credentials. Enable the extension after installation.

### Available Tools

**Catalog and API Manager operations**

| Operation | What it does |
|---|---|
| List catalogs | Returns all catalogs in the provider org |
| List published APIs | Lists APIs published to a catalog |
| List published products | Lists products published to a catalog |
| List gateways in catalog | Lists configured gateways for a catalog |

**Consumer-related operations**

| Operation | What it does |
|---|---|
| List consumer organisations | Lists consumer orgs in a catalog |
| List applications in catalog | Lists consumer apps, optionally filtered by consumer org |
| List consumer app credentials | Returns credentials for a specific consumer app |
| List subscriptions in catalog | Lists subscriptions with optional filtering |
| Create consumer app | Creates a consumer application in a catalog (requires confirmation) |
| Create subscription for an API | Subscribes a consumer app to a published API's plan |
| Create subscription for a product | Subscribes a consumer app to a product's plan |

**Project-related operations**

| Operation | What it does |
|---|---|
| Create project | Creates an API Manager–managed project |
| List projects | Lists all projects in the provider org |
| List files in project | Lists the files (APIs, products) inside a named project |

> **Note:** Catalog-dependent operations require the target catalog to be enabled for API Agent in the API Manager UI. Operations will fail if the catalog is not enabled.

## Management AI MCP Server

### What It Does

The Management AI MCP server uses foundation models to help you write DataPower gateway policy YAML, generate spectral governance rules from natural language, and enhance or correct OpenAPI specifications. The output is always reviewed YAML or JSON that you download and apply — it does not make direct changes to your API Connect instance.

IBM documentation: [Management AI MCP documentation](https://www.ibm.com/docs/en/api-connect/software/12.1.0?topic=tools-management-ai-mcp).

### Installation

Download the `.tgz` from the management-ai folder — not on npm:

```
https://github.com/ibm-apiconnect/apic-mcp-server/tree/main/management-ai
```

### Configuration

Same environment variables as the management server, passed through the `env` block.

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

**`ListGatewayPolicies`** — returns the list of policies available for AI-assisted generation.

DataPower API Gateway policies: `activity-log`, `client-security`, `extract`, `gatewayscript`.

DataPower Nano Gateway policies: `block`, `cors`, `invoke`, `parse`, `ratelimit`, `redact`, `remove`, `set`, `validate`.

**`GatewayPolicyGenerator`** — generates a DataPower API Gateway or Nano Gateway assembly document in YAML from a list of policies you specify.

```
Create a datapower api gateway with the ratelimit, map and invoke gateway policies
Generate a datapower nano gateway with the invoke gateway policy for the project SampleProject
```

**`GatewayPolicyModifier`** — takes an existing DataPower assembly YAML file and adds or modifies gateway policies. Reference the file with `@filename.yaml`.

```
Add the datapower api gateway client-security and map policies to @da.yaml
```

**`SpectralRuleGenerator`** — converts a natural language description into a spectral rule in JSON format.

```
Generate a spectral rule that ensures info.description must be at least 20 characters long
Generate a spectral rule that ensures all POST operations must have a request body defined
```

> Always validate generated spectral rules with the Spectral rule validator before deploying them to a live governance pipeline.

**`OpenAPI Enhancer`** — enhances or corrects an OpenAPI 3.0 specification. Two modes: suggest improvements, or correct validation errors. Pass an OpenAPI file with `@filename.yaml`.

```
Augment the following openapi with enhanced descriptions and examples @openapi-sample.yaml
Correct the validation errors in the following openapi file @openapi-sample.yaml
```

## Example Sessions

### "List all the consumer orgs subscribed to my payments product"

```
List consumer orgs in catalog production
List subscriptions in catalog production filtered by product payments:2.0.0
```

Useful for understanding blast radius before a deprecation.

### "Generate a rate-limit policy for my DataPower nano gateway"

```
Generate a datapower nano gateway with the ratelimit and invoke gateway policies
```

`GatewayPolicyGenerator` returns a YAML assembly document with both policies pre-configured.

### "Write a spectral rule to enforce that every API has a contact email"

```
Generate a spectral rule that ensures info.contact.email is present and non-empty in every OpenAPI document
```

Download the JSON, validate it with the spectral validator, and add it to your governance ruleset.

## Running Multiple Servers Together

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

A single conversation can jump between "which APIs have high error rates this week?" (analytics), "list the consumer apps subscribed to that API" (management), and "generate a tighter rate limit policy for it" (management-ai).

## Preview Caveats

- **GitHub-distributed, not on npm:** Download `.tgz` files directly from the repository.
- **AI output requires validation:** `SpectralRuleGenerator`, `GatewayPolicyGenerator`, `GatewayPolicyModifier`, and the OpenAPI Enhancer all use foundation models. The output can contain errors. Validate generated spectral rules before use. Review generated YAML before deploying.
- **Catalog must be API Agent–enabled:** Consumer, subscription, publish, and list operations require the target catalog to have API Agent enabled.
- **Node.js 20–24 required:** Check the bundled `package.json` for the exact constraint.
- **No persistent process:** All servers are invoked on demand by the MCP client via `npx`.

See also:
- [Part 1: Analytics MCP Server]({% post_url 2026-07-12-95-apic-analytics-mcp-server-getting-started %})
- [IBM API Connect Management tools documentation](https://www.ibm.com/docs/en/api-connect/software/12.1.0?topic=tools-api-connect-task)
- [GitHub repository](https://github.com/ibm-apiconnect/apic-mcp-server)
