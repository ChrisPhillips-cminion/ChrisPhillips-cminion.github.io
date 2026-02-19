---
layout: post
date: 2025-01-14 09:00:00
categories: APIConnect
title: "API Authorization when using Third Party oAuth Providers in APIC"
author: [ "ChrisPhillips", "SimonKapadia" ]
description: "Configure OAuth third-party provider authorization in IBM API Connect for secure API access delegation and federated identity management."
tags: [APIConnect, OAuth, Security, Authorization, Third Party, Identity Management, API Security]
---

API Connect has the facility to use third party oAuth providers. This means that you can use nearly any oAuth security provider to secure APIs providing it can be reached by the API Gateway.

This is great for Authentication however for Authorization this leads to a number of options that need to be considered.

Definitions
•	Authentication - is validating the user is who they say they are
•	Authorization – is validating they have permissions to do what they are requesting


<!--more-->

## Using Scopes from the oAuth Provider for Authorization
One of the easiest ways to do authorization is to use the scope configured on the oAuth Provider. Each API when it has an OAuth provider specified must also include which scopes are required for it to be called. When the user requests an oAuth token they request which scopes are needed, then the token is passed to the API and the scopes are validated.  In this example we are not passing in an additional client identifier.

*Pros*
•	All Authorization is done at the oAuth Provider
*Cons*
•	Requires careful scope creation
•	Consumers cannot manage their own subscriptions in API Connect
- Subscriptions, Applications and Consumer Orgs will not be used
•	Consumers cannot reset their client secret.
•	Analytics will not capture the consumer information

## Using APIC for Authorization
If you want to make use of some of the best features of API Connect we need to pass in a client ID so that APIConnect can identify the consumer. This can be used in conjunction for the scope on the oAuth provider or not allowing for all APIs to be contained within more broad scopes.

This solution provides all the benefits of an external oAuth provider while allowing API Connect to handle the authorization all while using a single client id.
The challenge with this solution is that the Client ID must be the same in the oAuth Provider and API Connect. If you would like the consumers to be able reset credentials through the developer portal the developer portal can push these changes (with custom code) to the third party oAuth Provider. If you would like the Client ID to be owned by the oAuth then the ClientID must be automatically federated to API Connect.

*Pros*
•	Consumers can manage their own subscriptions
•	Consumers may be able to create and update their own client credentials
•	Analytics data will be linked to a consumer organization and application

*Cons*
•	Requires the federation of Client Ids between the oAuth provider or API Connect
