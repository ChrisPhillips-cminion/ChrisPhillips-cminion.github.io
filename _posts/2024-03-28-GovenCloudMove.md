---
layout: post
date: 2024-03-28 09:00:00
categories: me
title: "Migrating to the APIC SaaS from on prem - Part 1 validating your APIs"
draft: true
---

When migrating to APIC on SaaS it is important to first validate that your APIs are able to work on SaaS prior to attempting the move.

API Connect SaaS on AWS is a multi-tenant solution in its basic form. This means the API Gateways are shared between different tenants. If you are using an Advanced plan then you have a dedicated API Gateway.  

![](/images/api-lint-saas.png)
<!--more-->

Those APIs that are run on the basic plan or free trial cannot use GatewayScript or XSLT policies. In addition, v5 compatible APIs will not run on APIC SaaS on AWS.

In API Connect 10.0.7.0 release we provide a linting tool to run a series of spectral rulesets against draft APIs.

I have created the following ruleset that contains two rules.
1. A rule to report an error if the API is written for the v5 compatible gateway.
2. A rule to report if GatewayScript or XSLT policies are used.


<button class="collapsible" id="html">Click here for the ruleset.</button>

<div class="content" id="htmldata" markdown="1">
```yaml
type: ruleset
ruleset_type: custom
api_version: 2.0.0
id: 0989806d-a11c-4f69-b568-86bfd636165d
name: saas-validation
title: SaaS Validation
description: This rule set will determine if the API is suitable for moving to
  the APIC SaaS.
ruleset_version: 1.0.0
ruleset_state: draft
rule_urls:
  - https://small-mgmt-compliance-service.apic2.svc:3077/governance/orgs/80d916dc-dad1-41fb-b019-f7890c136bad/rulesets/1.0.0-saas-validation/rules/b761f160-6380-4bf3-b727-76f6e594077a
  - https://small-mgmt-compliance-service.apic2.svc:3077/governance/orgs/80d916dc-dad1-41fb-b019-f7890c136bad/rulesets/1.0.0-saas-validation/rules/255a1995-88c4-46da-8fff-5ae0be32fb84
created_at: 2024-03-28 14:24:15.026+00
updated_at: 2024-03-28T14:38:53.000Z
url: https://small-mgmt-compliance-service.apic2.svc:3077/governance/orgs/80d916dc-dad1-41fb-b019-f7890c136bad/rulesets/0989806d-a11c-4f69-b568-86bfd636165d
rules:
  - api_version: 2.0.0
    id: b761f160-6380-4bf3-b727-76f6e594077a
    name: api-uses-gateway-script-or-xslt-which-is-not-allowed-in-non-advanced-saas
    version: 1.0.0
    title: API Uses Gateway Script or XSLT which is not allowed in non Advanced SaaS
    description: On non Advanced SaaS Gatewayscript and XSLT is not allowed
    message: XSLT or Gatewayscript policy is detected
    given:
      - $.x-ibm-configuration.assembly.execute[*].gatewayscript
      - $.x-ibm-configuration.assembly.execute[*].xslt
      - $.x-ibm-configuration.assembly.execute[*].*.case[*].execute[*].gatewayscript
      - $.x-ibm-configuration.assembly.execute[*].*.case[*].execute[*].case[*].execute[*].gatewayscript
      - $.x-ibm-configuration.assembly.execute[*].*.case[*].execute[*].case[*].execute[*].case[*].execute[*].gatewayscript
      - $.x-ibm-configuration.assembly.execute[*].*.case[*].execute[*].xslt
      - $.x-ibm-configuration.assembly.execute[*].*.case[*].execute[*].case[*].execute[*].xslt
      - $.x-ibm-configuration.assembly.execute[*].*.case[*].execute[*].case[*].execute[*].case[*].execute[*].xslt
    severity: error
    created_at: 2024-03-28T14:25:38.000Z
    updated_at: 2024-03-28T14:38:53.000Z
    url: https://small-mgmt-compliance-service.apic2.svc:3077/governance/orgs/80d916dc-dad1-41fb-b019-f7890c136bad/rulesets/1.0.0-saas-validation/rules/b761f160-6380-4bf3-b727-76f6e594077a
    then:
      - field: title
        function: falsy
  - api_version: 2.0.0
    id: 255a1995-88c4-46da-8fff-5ae0be32fb84
    name: is-the-api-configured-to-run-on-datapower-api-gateway
    version: 1.0.0
    title: Is the API Configured to run on   datapower-api-gateway
    description: When moving to APIC Connect SaaS all of the apis must be of type
      datapower-api-gateway
    message: API is not of type DataPower-API-Gateway
    given:
      - $.x-ibm-configuration
    severity: error
    created_at: 2024-03-28T14:24:15.000Z
    updated_at: 2024-03-28T14:38:53.000Z
    url: https://small-mgmt-compliance-service.apic2.svc:3077/governance/orgs/80d916dc-dad1-41fb-b019-f7890c136bad/rulesets/1.0.0-saas-validation/rules/255a1995-88c4-46da-8fff-5ae0be32fb84
    then:
      - field: gateway
        function: pattern
        functionOptions:
          match: datapower-api-gateway
```
</div>

## Enabling the API Governance feature in 10.0.7.0
The ruleset can be loaded into API Connect 10.0.7.0 or later once the API Governance function is enabled, this is described here [https://chrisphillips-cminion.github.io/apiconnect/2023/06/22/APIGov-2.html](https://chrisphillips-cminion.github.io/apiconnect/2023/06/22/APIGov-2.html)

## Loading the rule set.
In the the **Provider Organization**
1. Go to Resources in a Provider Organization
2. Go to API governance
3. Add->Import

## Running the validator
In the the **Provider Organization**
1. Go to Resources in a Provider Organization
2. Go to API governance
3. Click on Validate
4. Select the rule sets  and click next
5. Select the APIs to validate and click next.
6. The scorecard is shown for the APIs you selected.
