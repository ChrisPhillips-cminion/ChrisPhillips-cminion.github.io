---
layout: post
date: 2019-05-28 02:00:00
categories: API
title: 'Mix and Matching your API Flavours'
image:  '/images/2019-05-25-CUPCAKE1.JPG'
---

There are many types of APIs available, I propose to reference these as flavours. In this article I am going to talk about the three key flavours.  

* Resource APIs
* System APIs
* Consumer APIs

These APIs can work by themselves or together depending on the requirements, but not every combination is suitable for everyone. A bit like Ice Cream.

![](/images/2019-05-25-CUPCAKE1.JPG)
*Vegan BlackForrest, Mint Choc and Mocha Cupcakes made by* [Indulgent Me](https://indulgentme.co.uk/)

## What is an API?

The purpose of an API is to provide function to a system via a remote call. This remote call is usually via HTTP(s) but can be MQ any type of remote call.

## The API Flavours

An API Flavour is type of API design philosophy for how it is designed. Here we describe the three most common design philosophies. The key take away of this article is that there is more then one way to design an API.


### Resource APIs

| **Cost to Provider** | Low |
| **Complexity to Provider** | Low |
| **Complexity to Consumer** | Hard |

<span style="float:left; margin-right:5px; margin-left:5px"> <img src="/images/2019-05-25-cupcake1.png" /></span>

Resource APIs are the most common APIs. These are designed to directly interact with the object inside of the API. Each API will access a single object. This is simple to produce as it does not require implementing any additional functionality. However users who are consuming these APIs must be aware of the DataModel and how it interlinks with each object.

`e.g. if Object A depends on Object B and C the consumer must first create B and C.`

#### Pros
* Quick to implement the APIs

#### Cons
* Complex for the consumer to implement as they require knowledge of the DataModel.
* Complex Use Cases must be implemented by the Consumer
* Bigger Use Cases can require multiple Resource API Calls


### System APIs

| **Cost to Provider** | Medium |
| **Complexity to Provider** | Medium |
| **Complexity to Consumer** | Medium |

<span style="float:right; margin-right:5px; margin-left:5px"> <img src="/images/2019-05-25-cupcake2.png" /></span>

System APIs expose Use Cases based on the systems being exposed. The API Provider will implement an API that invokes one or more down stream systems depending on the Use Cases.

`e.g. API A will create Object B, C and A all in one transaction`

**Pros**
* Simpler for Consumers to consume the API
* Does not require the  consumer to have knowledge of the DataModel

**Cons**
* May not provide the Use Cases required by the consumers
* Requires bespoke development and design by the provider

### Consumer APIs

| **Cost to Provider** | High |
| **Complexity to Provider** | High |
| **Complexity to Consumer** | Low |

<span style="float:left; margin-right:5px; margin-left:5px"> <img src="/images/2019-05-25-cupcake3.png" /></span>

Consumer APIs are designed purely on the consumers Use Cases, ignoring any provider DataModel or systems. These are designed to lower the barrier of entry for the consumers and to allow for quick consumption. This could be around Use Cases provided by consumers or be determined by a Product Manager wanting to dictate how the APIS should be used.

`e.g. API A will create a new entry. The consumer does not know which down stream system are used.`

**Pros**
* Simple Consumers to consume the API
* Does not require the  consumer to have knowledge of the Provider DataModel or Systems

**Cons**
* May not be reusable
* Requires guessing at what consumers need if Use Cases are not provided.


## Mix and Matching

While i declare these are flavours of APIs I deliberately do not call them layers. Layers dictate that each one must be build on to of the previous layer. Though this can be done it is not required. The Consumer APIs could consume Service APIs, Resource APIs or go directly to the datasource.  Resource APIs would never invoke a higher level API. System APIs would directly invoke Resource APIs or the DataSource. Where as Consumer APIs could invoke anything.

## Summary

This article has gone through the three key flavours of APIs.

The table below summaries the key differences.


| Flavour  | Cost | Complexity to Produce | Complexity to Consume | Pros | Cons |
|---|---|---|---|---|---|
| Resource APIs | Cheap | Low | High | Quick to implement the APIs |  Complex for the consumer to implement as they require knowledge of the DataModel. |
 | | | | | | Complex Use Cases must be implemented by the Consumer |
 | | | | | | Bigger Use Cases can require multiple Resource API Calls |
|---|---|---|---|---|---|
| System APIs | Medium | Medium | Medium | Simpler for Consumers to consume the API | May not provide the Use Cases required by the consumers |
| | | | | Does not require the  consumer to have knowledge of the DataModel | Requires bespoke development and design by the provider |
| Consumer APIs | High | High | Low | Simple Consumers to consume the API | May not be reusable |
| | | | | Does not require the  consumer to have knowledge of the Provider DataModel or Systems | Guessing at what consumers need if Use Cases are not provided. |
| | | | | |  Guessing at what consumers need if Use Cases are not provided. |



**Please note there is not a one size fits all pattern. An understanding about how and who is using the APIs is essential for selecting the correct flavour.**

*All Cup Cakes made by [Indulgent Me](https://indulgentme.co.uk/)*
