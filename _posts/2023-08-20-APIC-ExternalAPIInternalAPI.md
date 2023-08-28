---
layout: post
date: 2023-08-28 01:00:00
categories: APIConnect
title: "Protecting the routes out of the castle. Five advantages for exposing external APIs and services as internal APIs to your own developers. "
---

Protecting APIs inside of your business so external consumers can be policed is a recognised and well understood pattern. However, what about APIs from outside of your business that that are consumed by your internal developers.

<!--more-->

## Scenario

There are three development teams each using the APIs provided by the Weather Company. They consumer APIs in one of the following two ways.

![](/images/externalapi/ExternalAPIs-diagrams/Slide1.jpeg)
1.	Each team has their own credentials and pays directly to the Weather Company

![](/images/externalapi/ExternalAPIs-diagrams/Slide2.jpeg)
2.	One set of credentials is used, but no one is sure who is using what.

This article aims to show the benefit of putting an API Gateway for internal API consumers to access the WeatherCompanies APIs.

![](/images/externalapi/ExternalAPIs-diagrams/Slide3.jpeg)

## 1. Security

Looking at the diagram above you can see that each developer has their own set of credentials (1,2,3) to the API Manager, and the API Manager has its own credentials (Z) to the weather company. Credentials 1, 2 and 3 are used to authenticate and authorize with the API Manager. Credentials 1,2 and 3 could be a simple API Key or a more complex method like OIDC or oAuth, where as the Weather Company only provides a single mechanism. This creates a more flexible solution for application developers to use the system that works for them.  

![](/images/externalapi/ExternalAPIs-diagrams/Slide4.jpeg)

Secondly if the credentials are compromised for one develop, those details can be reset without impacting the other teams. If they are sharing a single set of credentials between all teams this would not be possible.

## 2. Fair Cost Recovery and Limiting

Following on from section on security,  as each Developer is using their own credentials their usage can easily be tracked through the analytics. This allows each team to be held accountable for their own consumption.

By introducing consumer level rate limiting not only can each team be tracked for exactly what they are using, they will be unable to go above the agreed limit.

Provider level rate limiting means that a maximum usage of the Weather Companies APIs can be known so there are no surprise bills.

## 3. Caching

![](/images/externalapi/ExternalAPIs-diagrams/Slide5.jpeg)

If multiple developers are utilising the same APIs, then a caching layer can be introduced in the API Gateway. This will reduce the number of calls going to WeatherCompany and so potentially reduce the cost of the api calls.

## 4. Socialisation

When a fourth developer is brought on board to solve a new technical challenge they may not be aware of the weather companies APIs and so start using a different weather service. If a Developer Portal was available, they could quickly self-discover their APIs using the Weather Company and get sample code on how to use. This would allow them to quickly get started.

## 5. Interface Change

![](/images/externalapi/ExternalAPIs-diagrams/Slide6.jpeg)

If the Weather Company introduced a new major version of an API that required an interface change this would normally require each developer to make a change to their applications consuming the APIs. What’s more the WeatherCompany may only give a specific period until the existing version will be removed.   However, if an API Gateway is available the interface change might be able to be contained within the API itself. This would mean that the developers do not need to change their code.

## Closing Summary

In this article we have shown five key reasons for putting external APIs that you depend on behind an internal API Gateway
