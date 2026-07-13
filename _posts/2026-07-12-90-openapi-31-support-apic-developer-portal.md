---
layout: post
date: 2026-07-12 16:00:00
categories: APIConnect
title: "OpenAPI 3.1 Support in IBM API Connect Developer Portal"
description: "A practical guide to creating, publishing, and managing APIs with OpenAPI 3.1 in the IBM API Connect Developer Portal."
tags: [APIConnect, OpenAPI, DeveloperPortal, APIStandards]
draft: true
---

OpenAPI 3.1 support is useful if you want newer JSON Schema behaviour and want the same definition to flow through API Connect and the Developer Portal. This article covers what changed from 3.0, how to create and publish 3.1 APIs, and what to test carefully.

<!--more-->

## Table of Contents

1. [OpenAPI 3.1 — What Changed from 3.0?](#openapi-31--what-changed-from-30)
2. [OpenAPI 3.1 Support in API Connect v12](#openapi-31-support-in-api-connect-v12)
3. [Creating OpenAPI 3.1 APIs in the Developer Portal](#creating-openapi-31-apis-in-the-developer-portal)
4. [Publishing OpenAPI 3.1 APIs](#publishing-openapi-31-apis)
5. [Developer Portal Rendering of OpenAPI 3.1](#developer-portal-rendering-of-openapi-31)
6. [Limitations and Caveats](#limitations-and-caveats)
7. [Migration from OpenAPI 3.0 to 3.1](#migration-from-openapi-30-to-31)

## OpenAPI 3.1 — What Changed from 3.0?

The most significant changes in OpenAPI 3.1 relative to 3.0 are:

### 1. `type: null` Removed — JSON Schema is Now Fully Supported

In OpenAPI 3.0, the type system was a simplified subset of JSON Schema. You could specify `type: string` but not all JSON Schema keywords. OpenAPI 3.1 aligns with JSON Schema 2020-12, meaning you can use the full vocabulary of JSON Schema within `schema` objects.

```yaml
# OpenAPI 3.0 — limited type keywords
components:
  schemas:
    User:
      type: object
      properties:
        age:
          type: integer
          minimum: 0
          maximum: 150

# OpenAPI 3.1 — full JSON Schema support
components:
  schemas:
    User:
      type: object
      properties:
        age:
          # Full JSON Schema keywords available
          type: number
          multipleOf: 0.5
          minimum: 0
          maximum: 150
          examples: [18, 21.5, 65]
```

### 2. Schema Composition with `allOf`, `oneOf`, `anyOf`

OpenAPI 3.1 makes `allOf`, `oneOf`, and `anyOf` more powerful by allowing them to reference schemas that would have been invalid in 3.0.

### 3. `items` is Now Optional for `type: array`

In 3.0, `type: array` required an `items` schema. In 3.1, you can omit it (making it a tuple-like array).

### 4. `format: binary` Changes

The `format: binary` for `type: string` has different semantics in 3.1 — it's now explicitly for byte streams rather than a vague "binary".

### 5. Security Scheme Changes

`http` security schemes now support the `BearerToken` format explicitly, and OAuth 2.0 flows are more precisely defined.

## OpenAPI 3.1 Support in API Connect v12

API Connect v12.1.1 supports OpenAPI 3.1 throughout:

- **API Designer**: Create and edit OpenAPI 3.1 definitions using the visual designer or YAML/JSON editor
- **API Manager**: Validate, manage, and publish OpenAPI 3.1 APIs
- **Developer Portal**: Render OpenAPI 3.1 documentation
- **Gateway**: The DataPower and API Gateways process OpenAPI 3.1 requests the same as 3.0 — the schema differences don't affect runtime processing
- **Analytics**: All analytics features work with OpenAPI 3.1 APIs

## Creating OpenAPI 3.1 APIs in the Developer Portal

### Using the API Designer

1. Log into **API Manager**
2. Navigate to **APIs** → **Add** → **New API**
3. In the API creation wizard, select **OpenAPI 3.1** as the version
4. Give your API a title and version
5. Click **Create API**

The designer opens with a blank OpenAPI 3.1 scaffold:

```yaml
openapi: 3.1.0
info:
  title: My API
  version: 1.0.0
  description: |
    My API description
servers:
  - url: https://api.example.com
paths: {}
```

### Writing OpenAPI 3.1 by Hand

If you're writing your OpenAPI definition by hand, here's a more complete example:

```yaml
openapi: 3.1.0
info:
  title: Payments API
  version: 1.0.0
  description: |
    A payments API demonstrating OpenAPI 3.1 features
  contact:
    name: API Support
    email: api-support@example.com
servers:
  - url: https://api.example.com/v1
paths:
  /payments:
    post:
      operationId: createPayment
      summary: Create a payment
      description: Create a new payment
      tags:
        - Payments
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PaymentRequest'
            example:
              amount: 99.99
              currency: GBP
              reference: INV-2026-001
      responses:
        '201':
          description: Payment created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaymentResponse'
        '400':
          description: Validation error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
components:
  schemas:
    PaymentRequest:
      type: object
      required:
        - amount
        - currency
      properties:
        amount:
          type: number
          multipleOf: 0.01
          minimum: 0.01
          description: Amount in the smallest currency unit
        currency:
          type: string
          pattern: '^[A-Z]{3}$'
          description: ISO 4217 currency code
        reference:
          type: string
          maxLength: 255
        metadata:
          type: object
          additionalProperties:
            type: string
    PaymentResponse:
      type: object
      properties:
        payment_id:
          type: string
          format: uuid
        status:
          type: string
          enum: [pending, confirmed, failed]
        created_at:
          type: string
          format: date-time
    Error:
      type: object
      properties:
        code:
          type: string
        message:
          type: string
        details:
          type: array
          items:
            type: object
            properties:
              field:
                type: string
              reason:
                type: string
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
security:
  - BearerAuth: []
```

## Publishing OpenAPI 3.1 APIs

Publishing an OpenAPI 3.1 API works the same as 3.0:

1. Complete your API definition (paths, schemas, security)
2. Add a **Product** to bundle the API
3. Publish the product to your catalog
4. The Developer Portal automatically picks up the 3.1 API and renders the documentation

### Validation on Publish

API Connect validates your OpenAPI 3.1 definition on publish. If there are structural issues (e.g., invalid JSON Schema), you'll see validation errors before the API is accepted:

```bash
# You can also validate locally before publishing
apic api:validate ./my-api.yaml
```

## Developer Portal Rendering of OpenAPI 3.1

The Developer Portal renders OpenAPI 3.1 documentation with an interactive interface identical to 3.0 from the developer's perspective — they see the interactive documentation, can try out endpoints (if enabled), and download the OpenAPI definition.

From the developer's perspective, the rendered documentation experience should look broadly similar to OpenAPI 3.0, with the portal presenting the schema, operations, and examples interactively.

### Automatic `examples` Rendering

One notable improvement in 3.1 is the `examples` keyword on parameter and property objects (previously `example` — singular — in 3.0). Multiple examples are rendered in the portal, giving API consumers more context about what values look like:

```yaml
# OpenAPI 3.1 multiple examples
components:
  schemas:
    Country:
      type: string
      examples:
        - GB
        - US
        - DE
        - FR
```

## Limitations and Caveats

### 1. API Connect-Specific Extensions Still Use 3.0 Patterns

Some `x-` extensions specific to API Connect (e.g., `x-ibm-configuration`) still follow the 3.0 structure. When mixing 3.1 with API Connect extensions, test thoroughly.

### 2. GatewayScript and JSON Schema

If you're relying on custom GatewayScript policies to validate request bodies against OpenAPI 3.1 schemas, test those policies carefully. OpenAPI 3.1 aligns with newer JSON Schema semantics, so custom validation logic may need adjustment even when the core API definition imports cleanly.

### 3. Not All Tools Support 3.1 Fully Yet

Some API testing tools (e.g., Postman, some older versions) may not fully parse OpenAPI 3.1 definitions. Ensure your API consumers are using current tooling.

### 4. `type` is No Longer Optional

In 3.0, `type` was required on all schema objects. In 3.1, it's still good practice to include it, but schemas without `type` now have different semantics (they act as "any type" matchers). Be explicit with `type` to avoid surprises.

## Migration from OpenAPI 3.0 to 3.1

If you have existing OpenAPI 3.0 APIs and want to migrate to 3.1:

1. **Update the version string**: Change `openapi: 3.0.3` to `openapi: 3.1.0` at the top of the file
2. **Review schema type changes**: If you used `type: integer`, `type: number` now has different semantics for `multipleOf` — test your schemas
3. **Test validation**: Re-run all your validation rules and test cases
4. **Update tooling**: Ensure all team members use tooling that supports 3.1
5. **Check API Connect extensions**: Review any `x-ibm-*` extensions for any changes needed for 3.1 compatibility

```bash
# Automated migration check (IBM's linting tool)
apic lint my-api.yaml --openapi-version 3.1
```

## Summary

OpenAPI 3.1 support in API Connect v12 is solid and production-ready. The main practical benefit for most API teams is the ability to use full JSON Schema for richer request/response validation descriptions. The Developer Portal renders 3.1 APIs correctly, and the gateway processes them without issues.

If you're starting a new API today, use OpenAPI 3.1. If you're maintaining existing 3.0 APIs, plan a migration — the ecosystem is moving in that direction, and 3.1's JSON Schema alignment will pay dividends in the long run.
