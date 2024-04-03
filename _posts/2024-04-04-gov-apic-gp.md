---
layout: post
date: 2024-04-04 09:00:00
categories: APIConnect
title: "Suggested Governance Rules"
draft: true
---

I have been challenged by API Connects Product Management to come up with some sensible governance rules. I expect this article to grow from time to time as new ideas are formed.

![](/images/api-gp.png)

<!--more-->
The ruleset in this github gist I hope will grow over time. The initial one has two rules.

### Rule 1
Check to see if any of the GatewayScript uses the `require('apim')`.
When using the native DataPower gateway it is recommended to not use the `apim` module.

### Rule 2
Check that the policies have had their title changed from the default value. This does not work for User Defined Policies.

[https://gist.github.com/ChrisPhillips-cminion/fc200d73ecc4c1232a164df474bc41b6](https://gist.github.com/ChrisPhillips-cminion/fc200d73ecc4c1232a164df474bc41b6)


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
