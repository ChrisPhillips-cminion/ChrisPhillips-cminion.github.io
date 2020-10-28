---
layout: post
date: 2020-10-26 00:14:00
categories: APIConnect
title: "Applying API Governance Part 4 –  API 'Governance as Code' for a Decentralized world"
draft: true
---

Things ‘Everybody Knows’ about governance:
* Governance is important.
* Governance provides controls.
* Governance enforces consistency.
* Governance appears to reduce the velocity of development.
* Governance does not provide value but it does reduce unplanned expense.

<!--more-->

This is part four of a series on how to apply governance for API Connect.  Governance is sometimes considered a taboo topic because when people imagine governance, they see red tape that stifles progress. If governance is designed properly it can provide a single approach for all parts of the project with minimal impact on the development rate.

When I break down applying Governance for an API or Service factory I focus on three areas


* Ownership  - Who ones and controls the API at a certain point in the development process
* Certification - Which gates have the API been through, where autonomously or by a human
* Standards - Consistent Naming and structure

Governance is not just done at the start of the process of developing an API but comes into every stage.

This article will go through how each one of these areas can be addressed in an automated process to minimize the overhead.  

The term "as Code"  has a number of different definitions. For this  article we are following the definition that where possible we treat the rules as code. We commit the rules to our code repository and run them as part of the build pipeline (see build pipeline article [https://chrisphillips-cminion.github.io/apiconnect/2020/09/18/pipelines.html](https://chrisphillips-cminion.github.io/apiconnect/2020/09/18/pipelines.html) ).  

The recommendations in this article will be to validate OpenAPI specifications files with custom linting rules. An example on how to produce these can be found [https://chrisphillips-cminion.github.io/apiconnect/2020/09/28/apicgov3-linting.html](https://chrisphillips-cminion.github.io/apiconnect/2020/09/28/apicgov3-linting.html)


## Ownership
Ownership is split into two key areas. the owners and control.

The body owning the API will be a team that may change during its journey to production.  During the journey the API will go through multiple environments and if there is a problem in that environment (Design, Dev, Test or Prod) the owning body is responsible for investigating and if a change is required sending the API back to development or Design. The same team may own the API from design to production. The current ownership of the API must clearly be identifiable from the specification so problems can be reported if not caught via an automated process.

In order to ensure ownership is clearly represented custom linting rules must be added to the specification validation to verify the owner of the current state is documented. The current state must also be accurately listed.

e.g.
```YAML
x-governance:
  ownership:
    dev: Claims
    test: Claims
    preprod: Claims-Operations
    production: Claims-Operations
  state: test
```

Ensuring that only the owning team can publish, update or delete the API in each environment is critical. Human error is a common reason for APIs accidentally being changed and removed.  In API Connect I recommended that a shared catalog is split into multiple spaces, which each owning team have access to just their space. For more details please read [https://chrisphillips-cminion.github.io/apiconnect/2020/08/26/APIGov2.html](https://chrisphillips-cminion.github.io/apiconnect/2020/08/26/APIGov2.html). When publishing the API the pipeline deployment script must select target space based on the content of the API. This will ensure the API it is published to the space with the correct permissions.

## Certification
Certification comes in many different names. By certification we mean the validation that an API has completed a set of checks and can move along the journey to production. It is not uncommon for multiple checks to be required prior to going live in production.

Certifications can be either a human validation or a series of autonomous tests. I would expect to see both in an API Factory. The certification are there to provide a statement showing that the API has met the required checkpoints. The exact details of the failure and testing criteria must not be included as it will be stored in a centralized test system. Each certification must be given one of the following levels.

|Level| Description|
|-----|-----|
| Awaiting |  The certification process has not yet completed |
| Error |  The certification process threw errors that need to be addressed |
| Warning |  The certification process threw warnings but the API can continue |
| Certified  |  The certification passed with no errors or warnings. |


The certification would be stated in the swagger file.  If multiple certifications are required, only the current certification must be listed. The full list of certifications may optionally be included.

e.g.
```YAML
x-governance:
  certification:
    design: Warning
    dev: Certified
    system-test: Certified
    performance: Error
    production: Awaiting
```

The table below shows what sort of checks that could be done at each stage.

| stage | What Certification means |
|-----|-----|
| design | The design includes descriptions and follow naming conventions |
| dev | Examples includes valid data and  naming standards are followed |
| system-test | Test have passed  |
| performance  | Performance test have run and results are within the predicted needs  |
| production  | Operations team accepts the other certifications and the API is ready for it to go into production  |



The example above shows how I see the majority of clients arrange their approvals in a waterfall like way. Certifications must match to the approvals gates not to environments. In the example below is an example where the approval gates don't align with environments.

```YAML
x-governance:
  certification:
    design: Warning
    performance-short: Certified
    performance-long: warning
    pentest: warning
    operations-review: Awaiting
```

The table below shows what sort of checks that could be done at each stage.

| stage | What Certification means |
|-----|-----|
| design | The design includes descriptions and follow naming conventions |
| performance-short | Performance test have run and results are within the predicted needs |
| performance-long |  Performance test of over 24 hours have run and results are within the predicted needs |
| pentest  | Pen Testing is complete and all concerns have been addressed  |
| operations-review  | Operations team accepts the other certifications and the API is ready for it to go into production |




Each environment must have a set of criteria for which certifications are required in order to deploy an API into that environment. e.g. Unable to deploy into system-test until the dev certification is in the certified or warning state. This must be enforced using a linting tool to validate that the certifications are of the correct level prior to deployment.

## Standards
Naming standards are important to ensure that a common language are used over all of the APIs and solutions. If there is not a strict naming and style convention it makes each API a new language to learn.  These philosophy has been true for many years however it is hard to enforce programmatically and is a time consuming manual process.

Where possible linting rules should be included to ensure that the common styles, such as camelCase or snake_case are used consistently. In addition more complex rules can be produced to validate if paths contain blacklisted words, or creation of new definitions where existing ones would be best.

Content standards cover the metadata fields that must be included. Some examples of content standards are each Description and ex   ample must be populated. Descriptions and examples must verified to exist. Examples must then be validated against the schema in the API to ensure it was updated as the schema is extended.  Descriptions can be run against tools such as Watson Natural Language Understanding to ensure the emotion level and keywords are as expected for the API and meet a predefined criteria.  This will help set a consistent message and style to the consuming users.

This article has covered multiple strategies for API governance as code. Many of these strategies are already being incorporated today in organizations around the world.
