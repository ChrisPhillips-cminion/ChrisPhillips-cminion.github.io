---
layout: post
date: 2026-01-30 09:00:00
categories: APIConnect
title: "Secure Your APIs: Seamless HashiCorp Vault Integration with IBM API Connect Custom Policy"
author: ["ChrisPhillips"]
draft: true
description: "Build a reusable custom policy that seamlessly integrates HashiCorp Vault with IBM API Connect, transforming complex authentication and secret retrieval into a single, elegant policy call"
tags: [API Connect, HashiCorp Vault, Security, Custom Policy, Secrets Management, DevOps, API Security]
---

Stop hardcoding secrets in your APIs! Learn how to build a reusable custom policy that seamlessly integrates HashiCorp Vault with IBM API Connect, transforming complex authentication and secret retrieval into a single, elegant policy call.


<!--more-->

**License Notice:** This policy is provided under the MIT License and is offered "AS IS" without warranty of any kind. See the [full license](#license) at the end of this post.


## The Challenge

When building APIs that need to access external systems, you often need to retrieve API keys, passwords, or other secrets. Hardcoding these in your API definitions is a security risk. HashiCorp Vault provides a secure way to store and access secrets, but integrating it requires multiple steps:

1. Authenticate with Vault using userpass authentication
2. Extract the authentication token from the response
3. Use the token to retrieve the secret
4. Parse and extract the secret data

Implementing this in every API leads to code duplication and maintenance overhead. A custom policy solves this by encapsulating the entire Vault integration workflow into a single, reusable component.

## The Solution: vault-retrieve Custom Policy

I've created a custom policy called `vault-retrieve` that handles the complete Vault integration workflow.

## Benefits

1. **Reusability**: Write the Vault integration once, use it in multiple APIs
2. **Maintainability**: Update the policy in one place to fix bugs or add features
3. **Security**: Credentials are retrieved at runtime, never hardcoded
4. **Simplicity**: Dramatically reduces API assembly complexity with a single policy call
5. **Flexibility**: All parameters are configurable per API

### Features

- **Userpass Authentication**: Authenticates with Vault using username and password
- **Automatic Token Management**: Extracts and uses the authentication token automatically
- **Configurable Parameters**: All Vault settings are configurable via policy properties
- **Flexible Output**: Stores retrieved secrets in a configurable context variable
- **Error Handling**: Includes proper parsing and error handling throughout the flow

### Policy Properties

The policy accepts the following configurable properties. You can customize the default values in the policy YAML file to match your environment, reducing the need to specify them in every API:

| Property | Description | Required | Default (Customizable) |
|----------|-------------|----------|------------------------|
| `vault-addr` | The URL of your HashiCorp Vault server | Yes | Set your Vault URL |
| `vault-namespace` | The Vault namespace to use | Yes | `admin` (or your namespace) |
| `secret-path` | Path to the secret in Vault (e.g., `secret/data/apic`) | Yes | Set your default path |
| `username` | Vault username for authentication | Yes | Can use `$(request.parameters.username)` |
| `password` | Vault password for authentication | Yes | Can use `$(request.parameters.password)` |
| `output-variable` | Context variable name to store the retrieved secret | Yes | `vault.secret` |

**Tip:** Edit the `default` values in the policy's `properties` section to match your environment. This way, you only need to override values that differ from your defaults when using the policy in APIs.

## Using the Policy in Your APIs

Once deployed, using the policy in your APIs is straightforward:

```yaml
x-ibm-configuration:
  assembly:
    execute:
      # Use the custom vault-retrieve policy
      - vault-retrieve:
          version: 1.0.2
          title: retrieve-vault-secret
          vault-addr: https://vault.example.com:8200
          vault-namespace: admin
          secret-path: secret/data/apic
          username: myuser
          password: mypassword
          output-variable: vault.secret
      
      # Access the retrieved secret
      - set-variable:
          version: 2.0.0
          title: use-secret
          actions:
            - set: message.body
              value: '{"apikey":"$(vault.secret.apikey)"}'
              type: string
```

You can also use dynamic values from request parameters:

```yaml
- vault-retrieve:
    version: 1.0.2
    vault-addr: https://vault.example.com:8200
    vault-namespace: admin
    secret-path: secret/data/apic
    username: $(request.parameters.username)
    password: $(request.parameters.password)
    output-variable: vault.secret
```

## Deployment

A deployment script is provided to help package and upload the policy to API Connect. The script:

- Creates a zip file containing the policy YAML
- Automatically detects your configured gateway service
- Handles both creating new policies and updating existing ones
- Validates configuration before attempting deployment

To use the script, update the configuration variables at the top of `build-and-upload.sh` with your environment details (provider org, catalog, and API Manager server), then run:

```bash
cd vault-retrieve-policy
./build-and-upload.sh
```

The script will guide you through the deployment process and provide clear feedback on success or any errors encountered.

## Screenshots

[Screenshot: Policy properties in API Manager UI]

[Screenshot: Using the policy in an API assembly]

[Screenshot: Successful secret retrieval in test tool]

## Key Learnings

### 1. Policy Property References

Custom policy properties must be referenced using `$(local.parameter.property-name)`, not `$(property-name)` or `{property-name}`.

### 2. Parse Policy Input vs Output

- **Input**: Use variable name WITHOUT `.body` (e.g., `vault-login-response`)
- **Output Access**: Use parsed variable WITH `.body` (e.g., `$(parsed-login.body.auth.client_token)`)

### 3. Dynamic Variable Names

The `set-variable` policy cannot use dynamic variable names. Use GatewayScript when you need to set a variable whose name is determined at runtime.

### 4. Gateway Service Names

When deploying policies, use the actual configured gateway service name from your catalog (e.g., `api-gateway-service`), not generic names like `datapower-api-gateway`.

## Technical Implementation

The policy implements a 7-step workflow:

### Step 1: Prepare Login Request

Sets the required headers and message body for Vault authentication:

```yaml
- set-variable:
    version: 2.0.0
    title: set-login-variables
    actions:
      - set: message.headers.X-Vault-Namespace
        value: $(local.parameter.vault-namespace)
        type: string
      - set: message.headers.Content-Type
        value: application/json
        type: string
      - set: message.body
        value: '{"password":"$(local.parameter.password)"}'
        type: string
```

**Key Point**: Policy properties are accessed using `$(local.parameter.property-name)` syntax.

### Step 2: Authenticate with Vault

Invokes the Vault userpass login endpoint:

```yaml
- invoke:
    version: 2.0.0
    title: vault-login
    verb: POST
    target-url: $(local.parameter.vault-addr)/v1/auth/userpass/login/$(local.parameter.username)
    backend-type: json
    output: vault-login-response
```

### Step 3: Parse Login Response

Parses the authentication response to extract the token:

```yaml
- parse:
    version: 2.0.0
    title: parse-login-response
    input: vault-login-response
    output: parsed-login
```

**Important**: When using the `parse` policy, the `input` parameter should reference the variable name WITHOUT `.body`. However, when accessing the parsed data later, you MUST include `.body` in the reference.

### Step 4: Extract Token and Set Headers

Extracts the authentication token and prepares headers for secret retrieval:

```yaml
- set-variable:
    version: 2.0.0
    title: set-secret-headers
    actions:
      - set: vault.token
        value: $(parsed-login.auth.client_token)
        type: string
      - set: message.headers.X-Vault-Token
        value: $(parsed-login.body.auth.client_token)
        type: string
      - set: message.headers.X-Vault-Namespace
        value: $(local.parameter.vault-namespace)
        type: string
```

### Step 5: Retrieve Secret

Invokes the Vault secret endpoint using the authentication token:

```yaml
- invoke:
    version: 2.0.0
    title: retrieve-secret
    verb: GET
    target-url: $(local.parameter.vault-addr)/v1/$(local.parameter.secret-path)
    backend-type: json
    output: vault-secret-response
```

### Step 6: Parse Secret Response

Parses the secret response:

```yaml
- parse:
    version: 2.0.0
    title: parse-secret-response
    input: vault-secret-response
    output: parsed-secret
```

### Step 7: Store Secret in Output Variable

Uses GatewayScript to dynamically store the secret in the configured output variable:

```yaml
- gatewayscript:
    version: 2.0.0
    title: store-secret
    source: |
      // Get the parsed secret data
      var secretData = context.get('parsed-secret.body.data.data');
      
      // Get the output variable name from policy properties
      var outputVar = context.get('local.parameter.output-variable');
      
      // Store the secret in the specified output variable
      context.set(outputVar, secretData);
```

**Why GatewayScript?** The `set-variable` policy cannot use a dynamic variable name. GatewayScript allows us to read the output variable name from the policy properties and set it dynamically.

## Conclusion

Custom policies are a powerful way to encapsulate complex workflows in API Connect. This Vault integration policy demonstrates how to:

- Create a reusable custom policy with configurable properties
- Handle multi-step authentication and data retrieval workflows
- Use GatewayScript for dynamic variable manipulation
- Deploy and update policies using the APIC CLI

The complete policy code and deployment scripts are available in my GitHub repository.

## License

This custom policy is provided under the MIT License:

```
MIT License

Copyright (c) 2026 Chris Phillips

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Resources

- [IBM API Connect Documentation - Custom Policies](https://www.ibm.com/docs/en/api-connect/)
- [HashiCorp Vault API Documentation](https://developer.hashicorp.com/vault/api-docs)
- [Policy Source Code](https://github.com/chrisphillips-cminion/apic-vault-policy)

---

*Have you integrated Vault with API Connect? Share your experiences in the comments below!*