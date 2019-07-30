---
title: 'API Connect: Test Your APIs Better with Latency Injection'
layout: post
date:   2017-07-10 00:00:00
categories: APIConnect
---


This was originally posted on IBM APIConnects's
Blog. --- <http://developer.ibm.com/apiconnect/2017/05/24/test-apis-better-latency-injection/>

We recently wrote and shared a user defined policy called [API
Mocka](https://developer.ibm.com/apiconnect/2017/05/11/mocking-backend-services-gateway-policies/) to help you simulate responses directly from the API
Connect Assembly. API Mocka is a quick and easy way for application
developers to leverage the API Assembly for simulating the testing of
APIs without calling downstream systems. Today we're sharing an
additional user defined policy, Latency Injector, to enhance your API
testing experience.

When you are mocking up an API for testing an application it needs to be
as realistic as possible. API Mocka allows you to simulate responses,
the Set Variable policy allows you to simulate headers but until now,
there wasn't an available policy to simulate the latency of a backend
system. Meet API Connect Latency Injector.

![](https://cdn-images-1.medium.com/max/800/0*mzcB4e1_-ybqSLCQ.png)

The API Connect Latency Injector is a User Defined Policy that simply
increases the time taken to respond. If your backend system takes 300ms
to respond, simply add 300ms to the policy. Do you need to simulate your
backend systems over a much slower connection? Increase the latency as
required.

![](https://cdn-images-1.medium.com/max/800/0*-HmokCEYkW-ixdV_.png)

The API Connect Latency Injection Policy is available on GitHub at
<https://github.com/ChrisPhillips-cminion/APIConnect-Policy-LatencyInjector/>

[Taken from
http://developer.ibm.com/apiconnect/2017/05/24/test-apis-better-latency-injection/](http://developer.ibm.com/apiconnect/2017/05/24/test-apis-better-latency-injection/)





By [Chris Phillips](https://medium.com/@cminion) on
[July 10, 2017](https://medium.com/p/601d02685d2b).

[Canonical
link](https://medium.com/@cminion/api-connect-test-your-apis-better-with-latency-injection-601d02685d2b)

Exported from [Medium](https://medium.com) on April 6, 2019.
