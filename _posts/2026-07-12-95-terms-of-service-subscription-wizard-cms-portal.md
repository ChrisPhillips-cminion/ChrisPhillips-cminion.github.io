---
layout: post
date: 2026-07-12 12:00:00
categories: APIConnect
title: "Configuring Terms of Service in the Subscription Wizard — CMS Portal"
description: "A practical guide to configuring Terms of Service acknowledgement in the API Connect CMS Portal subscription wizard workflow."
tags: [APIConnect, CMSPortal, SubscriptionWizard, TermsOfService, DeveloperExperience]
draft: true
author: ["ChrisPhillips", "IBMBob"]
---

If a developer must accept legal terms before subscribing to an API, the CMS Portal subscription wizard can be configured to enforce that step. This is useful for Terms of Service, Acceptable Use Policies, or similar legal documents that require explicit consent.

<!--more-->

## When to Use Terms of Service in Subscription Workflows

Add a ToS requirement when:

- Your API provides access to **sensitive data** (financial, health, personal)
- You have **legal or regulatory obligations** around API usage (PCI-DSS, GDPR, HIPAA)
- You need **explicit consumer consent** before providing access
- Your legal team requires an **audit trail** of who agreed to what terms and when

The ToS feature is particularly valuable in B2B API programmes where you're onboarding third-party developers who are themselves under regulatory obligations.

## How It Works in the Consumer Journey

1. Developer selects the plan and clicks **Subscribe**
2. The subscription wizard displays the **Terms of Service** page
3. The developer must scroll to the bottom (or click "I have read and agree") before the **Confirm** button activates
4. On confirmation, the subscription is created and the agreement is recorded with a timestamp and user identity

## Configuring Terms of Service in CMS Portal Admin

### Step 1: Create the Terms of Service Content

1. Log into the **CMS Portal** as an administrator
2. Navigate to **Content** → **Websites** → **Legal Pages**
3. Create a new content item of type **Legal Document** or **Terms of Service**
4. Enter your terms content — HTML is supported for formatting
5. Set a **Title** (e.g., "API Terms of Service v2.1") and a **Version identifier**
6. Save and publish

### Step 2: Register the ToS in API Connect

1. Navigate to **Manage** → **Catalog** → **Settings** → **Subscriptions**
2. Find the **Terms of Service** section
3. Click **Add Terms of Service**
4. Enter:
   - **Name**: e.g., "API General Terms v2.1"
   - **URL**: the URL of your published CMS legal page
   - **Version**: e.g., "2.1"
   - **Effective date**: when these terms come into force
5. Save

### Step 3: Associate ToS with a Plan

1. Navigate to **Manage** → **Catalog** → **Products**
2. Select your product
3. Open the plan you want to attach ToS to
4. In the plan settings, find **Terms of Service** and select your configured ToS from the dropdown
5. Save and publish the updated product

## Consumer Experience

The subscription wizard presents the ToS acknowledgement step before the subscription is confirmed. The wizard page:

- Displays the ToS document (inline or with a link to open it in a new tab)
- Requires the developer to explicitly acknowledge before proceeding
- Records the acknowledgement against their subscription

If the ToS is updated later, you can configure whether existing subscribers need to re-accept.

## Managing ToS Versions and Updates

### Strategy 1: Non-Breaking Updates (No Re-Acceptance Required)

For minor updates that don't materially change the consumer's obligations:

- Publish the updated ToS content in the CMS
- Update the version reference in API Connect
- Existing subscriptions remain valid — no re-acceptance required

### Strategy 2: Breaking Updates (Re-Acceptance Required)

For material changes that require explicit consumer re-consent:

- Publish the new ToS in the CMS
- In the product/plan settings, select **Require re-acceptance** for the updated ToS
- The next time affected developers access their subscriptions, they'll be prompted to accept the new terms
- Subscriptions remain in a "pending acceptance" state until they re-accept

```bash
# Illustrative example only — confirm the exact REST resource shape and field names
# for your API Connect version before using this in automation.
curl -X PATCH \
  "https://${MANAGEMENT_SERVER}/api/catalogs/${CATALOG_ID}/products/${PRODUCT_ID}/plans/${PLAN_ID}" \
  -H "authorization: Bearer ${TOKEN}" \
  -H "content-type: application/json" \
  -d '{
    "terms_of_service": {
      "tos_id": "tos-uuid",
      "require_reacceptance": true
    }
  }'
```

## Summary

Configuring Terms of Service in the API Connect CMS Portal subscription wizard is a straightforward but important step for any API programme with legal or compliance obligations.

Keep terms readable — legal walls of text lead developers to click "agree" without reading. Version everything. Notify subscribers proactively before enforcing re-acceptance.
