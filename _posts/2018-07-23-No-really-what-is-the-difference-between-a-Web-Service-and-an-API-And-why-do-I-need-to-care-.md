---
layout: post
date: 2018-07-23  00:00:00
categories: APIConnect
title: |
    No really, what is the difference between a Web Service and an API?
---
### and why do I need to care?

Recently at a Business Partner summit I was asked this question. I have
tried to come up with the right answer to this question many times, here
is my two cents.



![](https://cdn-images-1.medium.com/max/2560/1*m-5Xs2OMZltGDd1KBjiefg.png)



A Web Service and an API are different perspectives on the same idea.
Both are used for exposing an interface to access a function or data.
Both have the same set of criteria for Non Functional Requirements
(Though the NFRs depend on the planned Use Cases).

The only difference is the motivation or reason for the interface.

**API interfaces are designed around how consumers will use them.**

**Web Service interfaces are designed around the data being exposed.**







------------------------------------------------------------------------




So what does this mean?

**A simple example**: A Web Service will expose all data attributes. An
API will only expose the data attributes that a consumer can use.

**A more complex example**: An API exposes a balance status facility.
This needs to call three web services, Security, Pending Transactions
and Statement. The Pending Transactions and Statement services have many
attributes that must not be made available to the API Consumers.







------------------------------------------------------------------------




On to the final question, "Why do i need to care?"

As we discuss above the person who designs the interface will have one
of two motivations, either to expose data or to consume function. If
this is not clearly defined up front the interface maybe too restricted
or too open. Using the right terminology helps to reduce the risk.

*APIs are not just for fashion, they are for a purpose*

**As ever I welcome debate and comments, please comment below with your
opinion!**





By [Chris Phillips](https://medium.com/@cminion) on
[July 23, 2018](https://medium.com/p/a6f5c4ead61f).

[Canonical
link](https://medium.com/@cminion/no-really-what-is-the-difference-between-a-web-service-and-an-api-and-why-do-i-need-to-care-a6f5c4ead61f)

Exported from [Medium](https://medium.com) on April 6, 2019.
