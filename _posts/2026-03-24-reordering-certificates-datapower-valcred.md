---
layout: post
date: 2026-03-24 01:00:00
categories: DataPower
title: "Reordering Certificates in DataPower Validation Credentials: A Step-by-Step Guide to Managing Certificate Order in ValCred Truststores"
author: ["ChrisPhillips"]
description: "Complete guide to reordering certificates in IBM DataPower Validation Credentials (ValCred) truststores. Learn how to modify certificate order through config files, restart domains, and verify changes for proper SSL/TLS certificate chain validation."
tags: [DataPower, SSL, TLS, Certificates, ValCred, Truststore, Configuration, Security, Certificate Management]
draft: true
---

When working with IBM DataPower Gateway, you may need to reorder certificates within a Validation Credentials (ValCred) truststore. The order of certificates can be important for certificate chain validation and SSL/TLS handshake processing. This guide walks you through the process of reordering certificates in a DataPower valcred.

<!--more-->

## 1. What is a Validation Credentials (ValCred)?

In DataPower, a **Validation Credentials** object (commonly referred to as "valcred") is a type of truststore that contains trusted certificates used for validating SSL/TLS connections. The full name in the WebGUI is "Truststore (validation credentials)" and it's found under **Objects / Crypto configuration**.

## 2. Why Reorder Certificates?

Certificate order in a truststore can affect:
- Certificate chain validation behavior
- SSL/TLS handshake performance
- Which certificate is presented first during validation
- Troubleshooting certificate-related issues

## 3. Prerequisites

Before you begin, ensure you have:
- Access to DataPower WebGUI with administrative privileges
- Access to the domain's file manager
- A maintenance window (reordering requires a domain restart)
- Backup of your current configuration

## 4. Step-by-Step Process

### 4.1. View Current Certificate Order in WebGUI

1. Log into the DataPower WebGUI
2. Navigate to **Objects / Crypto configuration**
3. Search for or select **Truststore (validation credentials)**

![Searching for Truststore](/images/2026-03-24-valcred-search.png)
*Figure 1: Searching for Truststore (validation credentials) in the WebGUI*

![Truststore List](/images/2026-03-24-truststore-list.png)
*Figure 2: List of available truststore objects*

4. Click on your valcred object (e.g., "test")
5. In the **Certificates** section, note the current order of certificates

![ValCred Certificate List in WebGUI](/images/2026-03-24-valcred-webgui-before.png)
*Figure 3: Current certificate order in the valcred WebGUI*

**Example current order:**
```
gwd_ca
gwd_cert
peering_ca
tls-server-profile-default_idcred_cert
```

### 4.2. Locate and Edit the Configuration File

1. In the DataPower WebGUI, navigate to **Administration / Main**
2. Select **File management** from the left menu
3. Browse to the **config:** directory
4. Locate your domain's configuration file (e.g., `mydomain.cfg`)

![File Management](/images/2026-03-24-file-management.png)
*Figure 4: Navigating to the config directory in File Management*

5. Click on the configuration file to open it for editing
6. Search for your valcred object name (e.g., search for `valcred "test"`)

You'll find a configuration block similar to this:

```
valcred "test"
  certificate gwd_ca
  certificate gwd_cert
  certificate peering_ca
  certificate tls-server-profile-default_idcred_cert
  cert-validation-mode legacy
  use-crl
  no require-crl
  crldp ignore
  initial-policy-set "2.5.29.32.0"
  no explicit-policy
  check-dates
exit
```

![Config File Before](/images/2026-03-24-valcred-config-before.png)
*Figure 5: Original certificate order in the configuration file*

### 4.3. Reorder the Certificates

1. In the configuration file, reorder the `certificate` lines to your desired sequence
2. For example, to move `tls-server-profile-default_idcred_cert` to the top:

**New order:**
```
valcred "test"
  certificate tls-server-profile-default_idcred_cert
  certificate gwd_ca
  certificate gwd_cert
  certificate peering_ca
  cert-validation-mode legacy
  use-crl
  no require-crl
  crldp ignore
  initial-policy-set "2.5.29.32.0"
  no explicit-policy
  check-dates
exit
```

![Config File After](/images/2026-03-24-valcred-config-after.png)
*Figure 6: Reordered certificate configuration*

3. Save the configuration file

### 4.4. Restart the Domain

**Important:** Restarting the domain will cause a brief service interruption. Ensure this is performed during a maintenance window.

1. In the DataPower WebGUI, navigate to the domain control panel
2. Select your domain from the domain dropdown or domain status page
3. Click the **Restart** action for the domain
4. Wait for the domain to complete the restart process
5. Verify the domain is back online and operational

### 4.5. Verify the New Certificate Order

1. Return to **Objects / Crypto configuration**
2. Navigate to **Truststore (validation credentials)**
3. Open your valcred object
4. Verify the certificates now appear in the new order

![ValCred After Reorder](/images/2026-03-24-valcred-webgui-after.png)
*Figure 7: Verified new certificate order in the WebGUI*

**Expected new order:**
```
tls-server-profile-default_idcred_cert
gwd_ca
gwd_cert
peering_ca
```

## 5. Important Considerations

### 5.1. Timing and Impact
- **Always perform this operation during a maintenance window**
- Domain restart will cause a brief service interruption
- Active connections will be terminated during the restart
- Plan for connection re-establishment after restart

### 5.2. Best Practices
- Document the original certificate order before making changes
- Test the new certificate order in a non-production environment first
- Verify SSL/TLS connections work correctly after reordering
- Keep a backup of the configuration file before editing

### 5.3. Troubleshooting

If certificates don't appear in the expected order after restart:
1. Verify the configuration file was saved correctly
2. Check for syntax errors in the valcred configuration block
3. Review domain logs for any configuration errors during restart
4. Ensure the domain restart completed successfully

## 6. Alternative: Using CLI

You can also perform this operation using the DataPower CLI:

```bash
# Enter configuration mode
configure terminal

# Enter the domain
domain [domain-name]

# Modify the valcred
valcred "test"
  # Remove all certificates first
  no certificate gwd_ca
  no certificate gwd_cert
  no certificate peering_ca
  no certificate tls-server-profile-default_idcred_cert
  
  # Add them back in the desired order
  certificate tls-server-profile-default_idcred_cert
  certificate gwd_ca
  certificate gwd_cert
  certificate peering_ca
exit

# Save configuration
write memory

# Restart domain
restart domain [domain-name]
```

## 7. Conclusion

Reordering certificates in a DataPower valcred is a straightforward process that involves editing the domain configuration file and restarting the domain. While the process is simple, it's important to plan for the service interruption and verify the changes take effect correctly.

Remember to always:
- Perform changes during maintenance windows
- Document your changes
- Test in non-production environments first
- Verify SSL/TLS functionality after changes

## 8. Related Resources

**Useful Links:**
* [IBM DataPower Gateway Documentation](https://www.ibm.com/docs/en/datapower-gateway)
* [DataPower Crypto Configuration](https://www.ibm.com/docs/en/datapower-gateway/10.0.x?topic=configuration-crypto)
* [SSL/TLS Certificate Management in DataPower](https://www.ibm.com/docs/en/datapower-gateway/10.0.x?topic=certificates-managing)

