---
layout: post
date: 2026-03-10 14:00:00
categories: DataPower
title: "Configuring TLS Client Profiles in DataPower CLI"
description: "Learn how to configure TLS client profiles in IBM DataPower using the CLI. Complete guide covering protocol versions, cipher suites, certificate validation, and best practices for secure downstream connections."
tags: [DataPower, TLS, SSL, CLI, Security, Encryption, Ciphers, Certificate]
draft: true
---

When working with DataPower, configuring TLS client profiles through the CLI provides a fast and scriptable way to manage SSL/TLS settings for downstream connections. This article demonstrates how to configure TLS client profiles using the DataPower command-line interface, including protocol versions and cipher suite selection.

<!--more-->

## What is a TLS Client Profile?

A TLS client profile in DataPower defines the SSL/TLS settings used when DataPower acts as a client connecting to downstream (backend) services. This includes:

- **TLS protocol versions** - Which versions of TLS to support (TLS 1.2, TLS 1.3, etc.)
- **Cipher suites** - The encryption algorithms to use for secure communication
- **Certificate validation** - How to verify server certificates
- **Client authentication** - Optional client certificate settings

## Basic CLI Configuration

Here's the basic command structure to configure a TLS client profile in the DataPower CLI:

```bash
top ; sw DOMAINanme ; co ; ssl-client downstreamprofile
    protocols TLSv1d2+TLSv1d3
    ciphers AES_256_GCM_SHA384
    ciphers AES_128_GCM_SHA256
    ciphers AES_128_CCM_SHA256
    ciphers AES_128_CCM_8_SHA256
exit
```

Let's break down each component:

### 1. Creating the Profile

```bash
ssl-client downstreamprofile
```

This command creates (or modifies) an SSL client profile named `downstreamprofile`. The name can be any valid identifier that describes your use case.

**Important**: You can create a TLS client profile through the WebGUI by searching for "tls client" or via CLI as shown above.

### 2. Setting Protocol Versions

```bash
protocols TLSv1d2+TLSv1d3
```

This line configures which TLS protocol versions are allowed:

- **`TLSv1d2`** - Enables TLS 1.2
- **`TLSv1d3`** - Enables TLS 1.3
- **`+`** - The plus sign means "and", allowing both protocols

**Note**: DataPower uses `d` instead of `.` in protocol version names (e.g., `TLSv1d2` instead of `TLSv1.2`).

**Common Protocol Options**:
- `TLSv1d2` - TLS 1.2 only
- `TLSv1d3` - TLS 1.3 only
- `TLSv1d2+TLSv1d3` - Both TLS 1.2 and 1.3
- `TLSv1d0+TLSv1d1+TLSv1d2` - TLS 1.0, 1.1, and 1.2 *(not recommended for production)*

### 3. Configuring Cipher Suites

```bash
ciphers AES_256_GCM_SHA384
ciphers AES_128_GCM_SHA256
ciphers AES_128_CCM_SHA256
ciphers AES_128_CCM_8_SHA256
```

Each `ciphers` line adds a cipher suite to the profile. The order matters - DataPower will prefer ciphers in the order they're listed.

**Critical Requirement**: The profile must include at least one cipher suite that matches the associated key material:
- When using RSA keys or certificates, you must specify at least one RSA cipher suite
- When using ECDSA keys or certificates, you must specify at least one ECDSA cipher suite

**Understanding the Cipher Names**:

- **`AES_256_GCM_SHA384`**
  - `AES_256` - AES encryption with 256-bit key
  - `GCM` - Galois/Counter Mode (authenticated encryption)
  - `SHA384` - SHA-384 hash algorithm

- **`AES_128_GCM_SHA256`**
  - `AES_128` - AES encryption with 128-bit key
  - `GCM` - Galois/Counter Mode
  - `SHA256` - SHA-256 hash algorithm

- **`AES_128_CCM_SHA256`**
  - `CCM` - Counter with CBC-MAC mode (authenticated encryption)

- **`AES_128_CCM_8_SHA256`**
  - `CCM_8` - CCM mode with 8-byte authentication tag

### 4. Exiting and Apply Configuration Mode

```bash
exit
```

## Best Practices

### 1. Use Strong Protocols Only

For production environments, use only TLS 1.2 and TLS 1.3:

```bash
protocols TLSv1d2+TLSv1d3
```

Avoid older protocols like TLS 1.0 and 1.1, which have known vulnerabilities.

### 2. Prioritize Strong Ciphers

List stronger ciphers first. GCM-based ciphers are generally preferred:

```bash
ciphers AES_256_GCM_SHA384 
ciphers AES_128_GCM_SHA256
```

### 3. Limit Cipher Suite Selection

Don't enable every available cipher. Use only those that meet your security requirements and are supported by your downstream services. Remember that the cipher suite order matters - the displayed order is the preferred order.

### 4. Enable Certificate Validation

Always validate server certificates in production:

```bash
validate-server-cert on
valcred trustedCAs
```

By default, server authentication is not enabled. For production environments, you should enable server validation to ensure secure connections.

### 5. Use Descriptive Names

Name your profiles descriptively to indicate their purpose:

```bash
ssl-client backend-api-profile
ssl-client payment-gateway-profile
ssl-client internal-services-profile
```

## Viewing Current Configuration

To view the current configuration of a TLS client profile:

```bash
show ssl-client downstreamprofile
```

To see all SSL client profiles:

```bash
show ssl-client
```

## Additional Resources

- [IBM DataPower Gateway Documentation](https://www.ibm.com/docs/en/datapower-gateway)
- [Creating a TLS Client Profile](https://www.ibm.com/docs/en/datapower-gateway/10.5.x?topic=profiles-creating-tls-client-profile)
- [DataPower CLI Reference](https://www.ibm.com/docs/en/datapower-gateway/10.0?topic=interface-command-line)
