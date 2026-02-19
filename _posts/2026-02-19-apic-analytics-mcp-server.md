---
layout: post
date: 2026-02-19 00:00:00
categories: APIConnect
title: "API Connect Analytics MCP Server: AI-Powered API Management (Preview)"
author: ["ChrisPhillips"]
description: "Explore the new API Connect MCP server that brings AI capabilities to API management through the Model Context Protocol, enabling intelligent interactions with your API Connect environment."
tags: [APIConnect, MCP, AI, Analytics, Automation, Preview]
draft: true
---

IBM API Connect now has an MCP (Model Context Protocol) server that enables AI assistants to interact directly with your API Connect environment. This preview release brings intelligent automation to API management, allowing you to query analytics, manage APIs, and troubleshoot issues using natural language.

<!--more-->

## What is the API Connect MCP Server?

The [API Connect MCP Server](https://github.com/ibm-apiconnect/apic-mcp-server) is an implementation of Anthropic's Model Context Protocol that provides AI assistants (like Claude) with direct access to your API Connect Provider Organization. Through this server, AI can:

- Query API analytics and usage data
- List and inspect provider organizations, catalogs, and spaces
- Retrieve product and API definitions
- Analyze consumer organizations and subscriptions
- Access detailed API analytics with time-series data

**Important:** This is a **preview release** and should be evaluated in non-production environments before broader deployment.

---

## Why MCP for API Connect?

Traditional API management requires navigating through multiple UI screens, running CLI commands, or writing custom scripts to gather information. The MCP server changes this by:

1. **Natural Language Queries** - Ask questions in plain English instead of learning complex CLI syntax
2. **Contextual Understanding** - AI maintains context across multiple queries for deeper analysis
3. **Automated Workflows** - Chain multiple operations together intelligently
4. **Rapid Troubleshooting** - Get instant insights without manual data correlation

---

## Architecture Overview

The MCP server acts as a bridge between AI assistants and the API Connect REST API:

```
┌─────────────┐         ┌──────────────┐         ┌─────────────────┐
│             │  MCP    │              │  REST   │                 │
│ AI Assistant│◄───────►│  MCP Server  │◄───────►│  API Connect   │
│  (Claude)   │Protocol │              │  API    │  Provider Org   │
│             │         │              │         │                 │
└─────────────┘         └──────────────┘         └─────────────────┘
```

**Screenshot Placeholder:** *Architecture diagram showing the flow from AI assistant through MCP server to API Connect*

---

## Installation and Setup

### Prerequisites

- Node.js 18 or higher
- Access to an API Connect Provider Organization
- API Connect credentials (username/password or API key)
- An MCP-compatible AI assistant (e.g., Claude Desktop)

### Installation Steps

**1. Install the MCP Server:**

```bash
npm install -g @ibm-apiconnect/apic-mcp-server
```

**2. Configure Your AI Assistant:**

Add the server configuration to your AI assistant's MCP settings. For Claude Desktop, edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "apiconnect-provider": {
      "command": "apic-mcp-server",
      "env": {
        "APIC_MANAGER_URL": "https://your-apim-host.com",
        "APIC_USERNAME": "your-username",
        "APIC_PASSWORD": "your-password",
        "APIC_REALM": "provider/default-idp-2"
      }
    }
  }
}
```

**Screenshot Placeholder:** *Configuration file showing MCP server setup in Claude Desktop*

**3. Restart Your AI Assistant:**

After configuration, restart your AI assistant to load the MCP server.

**Screenshot Placeholder:** *Claude Desktop showing successful MCP server connection*

---

## Available Tools and Capabilities

The MCP server provides 15 specialized tools for interacting with API Connect:

### Organization Management

**`list_provider_orgs`** - List all provider organizations
```json
{
  "limit": 100,
  "offset": 0
}
```

**`get_provider_org`** - Get details of a specific provider organization
```json
{
  "org_name": "my-provider-org"
}
```

**Screenshot Placeholder:** *AI assistant listing provider organizations with details*

---

### Catalog and Space Management

**`list_catalogs`** - List all catalogs in a provider organization
```json
{
  "org_name": "my-provider-org",
  "limit": 50
}
```

**`get_catalog`** - Get details of a specific catalog
```json
{
  "org_name": "my-provider-org",
  "catalog_name": "sandbox"
}
```

**`list_spaces`** - List all spaces in a catalog
```json
{
  "org_name": "my-provider-org",
  "catalog_name": "production",
  "limit": 50
}
```

**Screenshot Placeholder:** *AI assistant showing catalog hierarchy with spaces*

---

### Product and API Management

**`list_products`** - List all products in a catalog or space
```json
{
  "org_name": "my-provider-org",
  "catalog_name": "production",
  "space_name": "retail-apis"
}
```

**`get_product`** - Get details of a specific product
```json
{
  "org_name": "my-provider-org",
  "catalog_name": "production",
  "product_name": "banking-apis:1.0.0"
}
```

**`publish_product`** - Publish a product to a catalog or space
```json
{
  "org_name": "my-provider-org",
  "catalog_name": "production",
  "product_name": "payment-apis:2.0.0",
  "space_name": "payments"
}
```

**Screenshot Placeholder:** *AI assistant publishing a product with confirmation*

---

### API Discovery

**`list_apis`** - List all APIs in a catalog
```json
{
  "org_name": "my-provider-org",
  "catalog_name": "production",
  "limit": 100
}
```

**`get_api`** - Get details of a specific API
```json
{
  "org_name": "my-provider-org",
  "catalog_name": "production",
  "api_name": "customer-api:1.0.0"
}
```

**Screenshot Placeholder:** *AI assistant displaying API definition with endpoints*

---

### Consumer Organization Management

**`list_consumer_orgs`** - List consumer organizations in a catalog
```json
{
  "org_name": "my-provider-org",
  "catalog_name": "production",
  "limit": 100
}
```

**Screenshot Placeholder:** *AI assistant showing consumer organizations and their subscriptions*

---

### Analytics and Monitoring

The MCP server provides powerful analytics capabilities:

**`get_analytics`** - Get analytics data for APIs in a catalog
```json
{
  "org_name": "my-provider-org",
  "catalog_name": "production",
  "start_time": "2026-02-01T00:00:00Z",
  "end_time": "2026-02-19T23:59:59Z",
  "api_name": "customer-api:1.0.0"
}
```

**`get_api_analytics`** - Get detailed analytics for a specific API
```json
{
  "org_name": "my-provider-org",
  "catalog_name": "production",
  "api_name": "customer-api:1.0.0",
  "start_time": "2026-02-01T00:00:00Z",
  "end_time": "2026-02-19T23:59:59Z",
  "time_unit": "day"
}
```

**`get_analytics_summary`** - Get summary analytics including total calls, errors, and response times
```json
{
  "org_name": "my-provider-org",
  "catalog_name": "production",
  "start_time": "2026-02-01T00:00:00Z",
  "end_time": "2026-02-19T23:59:59Z"
}
```

**Screenshot Placeholder:** *AI assistant displaying analytics summary with call counts and error rates*

---

### Advanced Analytics Views

**`get_analytics_by_product`** - Get analytics data grouped by product
```json
{
  "org_name": "my-provider-org",
  "catalog_name": "production",
  "start_time": "2026-02-01T00:00:00Z",
  "end_time": "2026-02-19T23:59:59Z"
}
```

**`get_analytics_by_plan`** - Get analytics data grouped by subscription plan
```json
{
  "org_name": "my-provider-org",
  "catalog_name": "production",
  "start_time": "2026-02-01T00:00:00Z",
  "end_time": "2026-02-19T23:59:59Z"
}
```

**`get_analytics_by_app`** - Get analytics data grouped by consumer application
```json
{
  "org_name": "my-provider-org",
  "catalog_name": "production",
  "start_time": "2026-02-01T00:00:00Z",
  "end_time": "2026-02-19T23:59:59Z"
}
```

**Screenshot Placeholder:** *AI assistant showing analytics breakdown by application*

---

### Direct API Access

**`query_endpoint`** - Query any API Connect endpoint directly (for debugging and exploration)
```json
{
  "endpoint": "/orgs/my-org/draft-apis",
  "method": "GET"
}
```

This tool is particularly useful for:
- Exploring undocumented endpoints
- Debugging API responses
- Testing new API Connect features
- Custom integrations

**Screenshot Placeholder:** *AI assistant executing a direct API query and showing raw response*

---

## Real-World Use Cases

### 1. Rapid Troubleshooting

**Scenario:** An API is experiencing high error rates.

**Traditional Approach:**
1. Log into API Manager
2. Navigate to Analytics
3. Select the catalog and API
4. Configure time range
5. Export data
6. Analyze in spreadsheet

**With MCP Server:**
```
User: "Show me error rates for the customer-api in production over the last 7 days"

AI: [Automatically queries analytics, analyzes data, and presents insights]
"The customer-api has a 12% error rate, primarily 500 errors. 
Peak errors occur between 2-4 PM daily. Top error: 'Backend timeout'."
```

**Screenshot Placeholder:** *AI assistant conversation showing error analysis*

---

### 2. Capacity Planning

**Scenario:** Planning for increased API traffic.

**Query:**
```
User: "Compare API call volumes across all products in production 
for the last 30 days. Which APIs are growing fastest?"

AI: [Analyzes trends across all products]
"Payment APIs show 45% growth, Customer APIs 23% growth. 
Payment APIs will need capacity increase within 2 months at current rate."
```

**Screenshot Placeholder:** *AI assistant showing growth trends and predictions*

---

### 3. Consumer Insights

**Scenario:** Understanding API consumer behavior.

**Query:**
```
User: "Which consumer applications are using the most API calls 
in the retail catalog this month?"

AI: [Retrieves and analyzes consumer data]
"Top 3 consumers:
1. Mobile App (45% of calls)
2. Web Portal (32% of calls)
3. Partner Integration (18% of calls)
Mobile App primarily uses Product Search API."
```

**Screenshot Placeholder:** *AI assistant displaying consumer usage breakdown*

---

### 4. Compliance Reporting

**Scenario:** Generate SLA compliance reports.

**Query:**
```
User: "Generate an SLA report for all APIs in production. 
Show which APIs met the 99.9% uptime target last month."

AI: [Analyzes availability and performance data]
"SLA Report - January 2026:
✓ Customer API: 99.95% uptime
✓ Product API: 99.92% uptime
✗ Payment API: 99.87% uptime (missed target)
Payment API had 3 outage incidents totaling 56 minutes."
```

**Screenshot Placeholder:** *AI assistant showing SLA compliance report*

---

## Security Considerations

### Authentication

The MCP server supports multiple authentication methods:

1. **Username/Password** - Basic authentication with API Manager credentials
2. **API Key** - Token-based authentication for automated workflows
3. **Realm Selection** - Support for different identity providers

### Best Practices

**1. Use Dedicated Service Accounts:**
Create a dedicated user account for the MCP server with appropriate permissions:
```json
{
  "APIC_USERNAME": "mcp-service-account",
  "APIC_PASSWORD": "secure-password"
}
```

**2. Limit Permissions:**
Grant only the necessary permissions:
- Read-only access for analytics queries
- Specific catalog access for product management
- Avoid admin-level permissions unless required

**3. Secure Credential Storage:**
- Never commit credentials to version control
- Use environment variables or secure vaults
- Rotate credentials regularly

**4. Network Security:**
- Use HTTPS for all API Connect connections
- Consider VPN or private networks for production access
- Monitor MCP server access logs

**5. Audit Trail:**
All MCP server actions are logged in API Connect audit logs for compliance and security monitoring.

---

## Performance Considerations

### Response Times

The MCP server adds minimal overhead:
- Simple queries: < 500ms
- Analytics queries: 1-5 seconds (depending on data volume)
- Complex aggregations: 5-15 seconds

### Rate Limiting

Be aware of API Connect rate limits:
- Default: 100 requests per minute per user
- Analytics queries count as multiple requests
- Consider caching for frequently accessed data

### Optimization Tips

**1. Use Time Ranges Wisely:**
```json
{
  "start_time": "2026-02-18T00:00:00Z",
  "end_time": "2026-02-19T00:00:00Z"
}
```
Shorter time ranges return faster results.

**2. Leverage Pagination:**
```json
{
  "limit": 50,
  "offset": 0
}
```
Request smaller batches for large datasets.

**3. Cache Results:**
For static data (API definitions, product info), cache results locally to reduce API calls.

---

## Limitations and Known Issues

As a preview release, be aware of these limitations:

### Current Limitations

1. **Read-Only Analytics** - Cannot modify analytics data or configurations
2. **No Real-Time Streaming** - Analytics data has a delay (typically 1-5 minutes)
3. **Limited Bulk Operations** - Some operations require multiple API calls
4. **No Gateway Configuration** - Cannot modify DataPower gateway settings

### Known Issues

1. **Large Dataset Performance** - Very large analytics queries (>1M records) may timeout
2. **Concurrent Requests** - Multiple simultaneous queries may hit rate limits
3. **Error Handling** - Some error messages could be more descriptive

### Roadmap

Future enhancements planned:
- Real-time analytics streaming
- Bulk product publishing
- Gateway configuration management
- Enhanced error diagnostics
- Performance optimizations

---

## Troubleshooting

### Common Issues

**Issue: "Connection refused"**
```
Error: ECONNREFUSED connecting to API Connect
```

**Solution:**
- Verify `APIC_MANAGER_URL` is correct
- Check network connectivity
- Ensure API Connect is accessible from your machine

---

**Issue: "Authentication failed"**
```
Error: 401 Unauthorized
```

**Solution:**
- Verify username and password
- Check realm configuration
- Ensure account is not locked
- Verify account has necessary permissions

---

**Issue: "No data returned"**
```
Analytics query returns empty results
```

**Solution:**
- Verify time range includes data
- Check catalog and API names are correct
- Ensure analytics are enabled for the catalog
- Confirm API has received traffic in the time range

---

**Issue: "Rate limit exceeded"**
```
Error: 429 Too Many Requests
```

**Solution:**
- Reduce query frequency
- Implement request throttling
- Use pagination for large datasets
- Consider caching results

---

## Getting Started: Example Workflow

Here's a complete workflow to get started:

**1. Install and Configure:**
```bash
npm install -g @ibm-apiconnect/apic-mcp-server
```

**2. Set Up Environment:**
```json
{
  "mcpServers": {
    "apiconnect-provider": {
      "command": "apic-mcp-server",
      "env": {
        "APIC_MANAGER_URL": "https://apim.example.com",
        "APIC_USERNAME": "admin",
        "APIC_PASSWORD": "password",
        "APIC_REALM": "provider/default-idp-2"
      }
    }
  }
}
```

**3. Test Connection:**
```
User: "List all provider organizations"
AI: [Returns list of organizations]
```

**Screenshot Placeholder:** *Complete workflow from installation to first query*

**4. Explore Your Environment:**
```
User: "Show me all catalogs in my-org and their API counts"
AI: [Analyzes and presents catalog overview]
```

**5. Run Analytics:**
```
User: "What were the top 5 most-called APIs yesterday?"
AI: [Queries analytics and ranks APIs by call volume]
```

---

## Best Practices for AI-Assisted API Management

### 1. Start with Exploration

Begin with simple queries to understand your environment:
- "List all catalogs"
- "Show me products in production"
- "What APIs are deployed?"

### 2. Build Context Gradually

AI assistants maintain conversation context. Build on previous queries:
```
User: "Show me the customer-api"
AI: [Displays API details]

User: "What's its error rate this week?"
AI: [Queries analytics for that specific API]

User: "Compare that to last week"
AI: [Performs comparative analysis]
```

### 3. Use Natural Language

Don't worry about exact syntax:
- ✓ "Which APIs are slowest?"
- ✓ "Show me errors in production"
- ✓ "What's the most popular product?"

### 4. Combine Multiple Queries

Ask complex questions that require multiple operations:
```
User: "Find all APIs with error rates above 5% in the last 24 hours, 
then show me their backend response times"
```

### 5. Request Visualizations

Ask the AI to format data for clarity:
- "Show that as a table"
- "Create a summary report"
- "Compare these side by side"

---

## Integration with Existing Workflows

### CI/CD Integration

Use the MCP server in automated workflows:

```yaml
# Example: Pre-deployment validation
- name: Validate API Health
  run: |
    # AI assistant checks current API health
    # Blocks deployment if error rates are high
```

### Monitoring and Alerting

Combine with monitoring tools:
```
# Scheduled query: Check API health every hour
# Alert if error rates exceed threshold
```

### Documentation Generation

Use AI to generate documentation:
```
User: "Generate API documentation for all products in production"
AI: [Creates comprehensive documentation with examples]
```

---

## Comparison with Traditional Tools

| Task | Traditional Approach | With MCP Server |
|------|---------------------|-----------------|
| Check API error rate | Navigate UI → Select catalog → Choose API → Set time range → View analytics | "What's the error rate for customer-api today?" |
| Find slow APIs | Export analytics → Import to spreadsheet → Sort by response time | "Which APIs have response times over 2 seconds?" |
| Compare products | Multiple UI screens → Manual data collection → Spreadsheet analysis | "Compare call volumes across all products this month" |
| Troubleshoot issue | Check logs → Review analytics → Correlate data → Identify pattern | "Why is payment-api failing? Show me errors and patterns" |
| Generate report | Export data → Format in document → Add charts → Manual analysis | "Generate an SLA report for all production APIs" |

**Screenshot Placeholder:** *Side-by-side comparison showing traditional UI vs AI assistant*

---

## Community and Support

### Resources

- **GitHub Repository:** [ibm-apiconnect/apic-mcp-server](https://github.com/ibm-apiconnect/apic-mcp-server)
- **Issues and Feature Requests:** [GitHub Issues](https://github.com/ibm-apiconnect/apic-mcp-server/issues)
- **API Connect Documentation:** [IBM Documentation](https://www.ibm.com/docs/en/api-connect)

### Contributing

This is an open-source project. Contributions are welcome:
- Report bugs and issues
- Suggest new features
- Submit pull requests
- Share use cases and examples

### Getting Help

1. Check the [GitHub README](https://github.com/ibm-apiconnect/apic-mcp-server)
2. Search existing [GitHub Issues](https://github.com/ibm-apiconnect/apic-mcp-server/issues)
3. Open a new issue with detailed information
4. Join the API Connect community discussions

---

## Conclusion

The API Connect MCP Server represents a significant step forward in API management automation. By enabling AI assistants to interact directly with your API Connect environment, it transforms how you:

- **Query and analyze** API analytics
- **Troubleshoot issues** with natural language
- **Generate reports** automatically
- **Monitor performance** proactively
- **Manage APIs** more efficiently

**Key Takeaways:**

1. **Preview Release** - Evaluate in non-production environments first
2. **Natural Language** - Interact with API Connect using plain English
3. **Comprehensive Tools** - 15 specialized tools for complete API management
4. **Security First** - Follow best practices for credential management
5. **Active Development** - Regular updates and improvements planned

As this is a preview release, we encourage you to:
- Test in development environments
- Provide feedback on GitHub
- Share your use cases
- Report issues and suggestions

The future of API management is conversational, intelligent, and automated. The API Connect MCP Server is your gateway to that future.

---

## Additional Resources

- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [API Connect REST API Reference](https://www.ibm.com/docs/en/api-connect/software/10.0.8_lts?topic=reference-rest-api)
- [API Connect Analytics Overview](https://www.ibm.com/docs/en/api-connect/software/10.0.8_lts?topic=analytics-overview)
- [Claude Desktop MCP Configuration](https://docs.anthropic.com/claude/docs/model-context-protocol)

---

**Note:** This is a preview release. Features and capabilities are subject to change. Always test thoroughly in non-production environments before deploying to production.