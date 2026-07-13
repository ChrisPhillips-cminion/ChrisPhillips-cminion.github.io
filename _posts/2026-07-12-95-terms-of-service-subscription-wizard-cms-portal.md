---
layout: post
date: 2026-07-12 12:00:00
categories: APIConnect
title: "Configuring Terms of Service in the Subscription Wizard — CMS Portal"
description: "A practical guide to configuring Terms of Service acknowledgement in the API Connect CMS Portal subscription wizard workflow."
tags: [APIConnect, CMSPortal, SubscriptionWizard, TermsOfService, DeveloperExperience]
draft: true
---

Consumer-facing API programmes often need to present legal terms — a Terms of Service (ToS), an Acceptable Use Policy, a Data Processing Agreement — before a developer can subscribe to an API. API Connect's CMS Portal supports this natively via the subscription wizard, and in v12 the configuration experience has been improved. This article covers everything you need to know about when to use ToS in subscription workflows, how to configure it in the CMS Portal admin, and how your consumers will experience the acknowledgement.

<!--more-->

## Table of Contents

1. [When to Use Terms of Service in Subscription Workflows](#when-to-use-terms-of-service-in-subscription-workflows)
2. [How It Works in the Consumer Journey](#how-it-works-in-the-consumer-journey)
3. [Configuring Terms of Service in CMS Portal Admin](#configuring-terms-of-service-in-cms-portal-admin)
4. [Attaching ToS to a Product/Plan](#attaching-tos-to-a-productplan)
5. [Consumer Experience](#consumer-experience)
6. [Managing ToS Versions and Updates](#managing-tos-versions-and-updates)
7. [Screenshot Recommendations](#screenshot-recommendations)

## When to Use Terms of Service in Subscription Workflows

You should consider adding a ToS requirement to your subscription workflow when:

- Your API provides access to **sensitive data** (financial, health, personal)
- You have specific **legal or regulatory obligations** around API usage (PCI-DSS, GDPR, HIPAA)
- Your organisation has **liability concerns** around how APIs are used
- You need **explicit consumer consent** before providing access
- Your legal team requires an **audit trail** of who agreed to what terms and when

The ToS feature is particularly valuable in B2B API programmes where you're onboarding third-party developers who are themselves under regulatory obligations.

## How It Works in the Consumer Journey

When a developer navigates to your CMS Portal and attempts to subscribe to a plan that has a ToS requirement:

1. They select the plan and click **Subscribe**
2. The subscription wizard displays the **Terms of Service** page
3. The developer must **scroll to the bottom** of the terms (or click "I have read and agree") before the **Confirm** button activates
4. Upon confirmation, the subscription is created and the agreement is recorded with a timestamp and user identity

This gives you a legally meaningful consent record.

## Configuring Terms of Service in CMS Portal Admin

### Step 1: Create the Terms of Service Content

1. Log into the **CMS Portal** as an administrator
2. Navigate to **Content** → **Websites** → **Legal Pages** (or similar, depending on your CMS version)
3. Create a new content item of type **Legal Document** or **Terms of Service**
4. Enter your terms content — you can use HTML for formatting if your CMS supports it
5. Set a **Title** (e.g., "API Terms of Service v2.1") and a **Version identifier**
6. Save and publish

### Step 2: Register the ToS in API Connect

The ToS content lives in two places: the CMS (the human-readable content) and API Connect (the configuration that enforces it). In API Connect:

1. Navigate to **Manage** → **Catalog** → **Settings** → **Subscriptions**
2. Find the **Terms of Service** section
3. Click **Add Terms of Service**
4. Enter:
   - **Name**: A descriptive name (e.g., "API General Terms v2.1")
   - **URL**: The URL of your published CMS legal page
   - **Version**: For tracking (e.g., "2.1")
   - **Effective date**: When these terms come into force
5. Save

### Step 3: Associate ToS with a Plan

1. Navigate to **Manage** → **Catalog** → **Products**
2. Select your product
3. Open the plan you want to attach ToS to
4. In the plan settings, find **Terms of Service** and select your configured ToS from the dropdown
5. Save and publish the updated product

## Consumer Experience

When a developer navigates to your portal and subscribes to a plan with ToS attached, here's what they see:

The subscription wizard should present the Terms of Service acknowledgement step before the subscription is confirmed.

The wizard page will:
- Display the ToS document (either inline or with a link to open it in a new tab)
- Require the developer to explicitly acknowledge before proceeding
- Record the acknowledgement against their subscription

If the ToS is updated later, you can choose whether existing subscribers need to re-accept — this is configured at the plan level.

## Managing ToS Versions and Updates

When your legal terms change, you have two strategies:

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
- Their subscriptions remain in a "pending acceptance" state until they re-accept

```bash
# Illustrative example only — confirm the exact REST resource shape and field names
# for your API Connect version before using this in automation.
# Update a plan to require ToS re-acceptance
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


## Best Practices

- **Keep terms readable**: Legal walls of text lead developers to click "agree" without reading. Summarise key points and link to the full text.
- **Version everything**: Always track your ToS versions. You may need this for legal disputes.
- **Use a CDN-hosted ToS**: If your CMS supports it, serve ToS from a CDN with long cache headers. This ensures the agreed text is immutable after acceptance.
- **Notify subscribers of updates**: When you update ToS, proactively notify developers via email/portal notification before enforcing re-acceptance.

## Summary

Configuring Terms of Service in the API Connect CMS Portal subscription wizard is a straightforward but important step for any API programme with legal or compliance obligations. The v12 improvements make it easier to configure and manage ToS at the plan level, with proper version tracking and re-acceptance workflows.

If you're building a consumer-facing API programme, don't skip this. The time you invest in a clear, well-presented ToS will save you significant legal headaches later.

---
*Questions about CMS Portal configuration or developer experience design? Find me on Twitter [@cminion](https://twitter.com/cminion).*
