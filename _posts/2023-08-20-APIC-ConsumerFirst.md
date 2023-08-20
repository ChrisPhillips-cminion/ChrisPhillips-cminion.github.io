---
layout: post
date: 2023-08-19 01:00:00
categories: APIConnect
title: "API Consumers, the **only** API Success Criteria"
draft: true
---

API Consumers are what dictate the value to an API Estate. This document goes through the key values of an API and how focusing on the consumer allows an API to be successful.

<!--more-->


*"If a tree falls in a forest and no one is around to hear it, does it make a sound?”* - Physics by Charles Riborg Mann and George Ransom Twiss 1920

*“The objects of sense exist only when they are perceived”* - George Berkeley 1710


The two quotes above have always made me think hard about what I do. Somethings we do to be seen; other things we do not want to be noticed. This flows nicely into value and success that influence Business Impact. What is the Business Impact vs the Cost of a Change. If we get this right, we are successful. if we get this wrong, we are not. If a change is very expensive but has no visibility, is it successful?  If a change saves money but produces a negative impact on the business, is it successful?

In this article I will go through the changing way that API value is being determined by business. The questions being asked is no longer “how many APIs are we exposing?”, but “How many of our APIs are being used?” or even “what value are we gaining from our APIs?”.

When an API is published, it is created to achieve an objective. The most common objective is as follows:

**To provide access to data or a function to someone outside of the immediate team.**

To achieve the objective, we need to ask ourselves this import question.

If an API is published and no one is told, does it have value?

The first question to answer is “What do we mean by value?”. It is often difficult to directly quantify the value of an API. Please Note: this is an individual API not the entire estate. In my perspective these are the key factors to weigh when determining value.

Measuring Impact:
1.	Number of transactions
2.	Number of users registered to the use the API

Measuring Cost:
3.	Engineering time to build
4.	Engineering time to support




The first two points (number of transactions and number of users registered) are obvious; the more people using an API, then the greater the value. This value could be demonstrated via direct business links or name recognition.  If an API is not used, or has no users registered (or showing intention of future use) there is (probably?) no value.  This information can be gathered from Analytics data of the API Platform. The value that is provided here needs to be compared to the cost of the final two points.

The time it takes to build an API is an obvious metric. If it takes three person years to build an API, the costs are significantly larger than if it takes one person day to build a similar API.

The final point is the hidden and forgotten costs, the support cost. Often these costs are the larger then any other part. If an API has a problem this needs to be addressed – via support, and resolution. Additionally, and often overlooked is support to new users learning how to use the API. In talking to many API Estate owners >50% of their development effort time is spent supporting consumers to onboard, debug, or teach.

To increase an API’s Value, we therefore need to do some or all the following.

1.	Increase number of transactions
2.	Increase number of users registered to the use the API
3.	Reduce engineering time to build
4.	Reduce engineering time to support

The easiest way to improve all these criteria is use a Developer Portal. The Developer portal is correctly seen as a socialisation point of APIs. The Developer Portal when used correctly will unlock many facilities to assist with consumer consumption. This must be considered for both internal and external consumers.

A developer portal firstly increases visibility of the APIs. **An API that is discoverable is easier to grow organically.** If an API is not discoverable, then this growth is far more difficult to achieve, as new users must be made aware by alternative more costly means. Though word of mouth can be used, its unpredictable and hard to guarantee its sucess.


A simple API will be used more than a complex API, if the complexity is not required. **All APIs must be designed with a simple purpose.** This also means the effort to build the simple API is greatly reduced and the API is less intimidating to new users. If a user’s first view of an API contains one hundred optional parameters, they will be put off. **If only the five most common parameters are exposed, the API becomes friendlier to consume.**  More advanced use cases can be added as the need arises.

The time it takes to support an API should be as near to zero as possible. Onboarding users to a developer portal can be self-service, or by invitation. **APIs must be well documented**. This includes the following.
* Descriptions
* Definitions
* Parameter Descriptions
* Examples.
* Code Samples

With the above in place a user can quickly get started using any API. Where as previous a consumer may be put off by complexity, they can now have enough information to instantly get started.  This means it takes less time and effort to consume the API. Providing a more friendly and self-affirming experience for the consumer.

Many customers tell me they do not need a developer portal. Or it is not a priority they are been measured on. This is always a surprise to me, for the following reasons above.

In summary this article has shown that all the keyways for deriving value from an API, are dependent on the consumer’s experience. Building APIs to meet the needs of the consumers both functionally (Purpose) and non-functionally (Documentation, Complexity) is key to the success of the API and so the API Estate.  
