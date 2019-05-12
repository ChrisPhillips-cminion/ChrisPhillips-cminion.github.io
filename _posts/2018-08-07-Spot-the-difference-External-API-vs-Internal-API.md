---
layout: post
date: 2018-08-07  00:00:00
categories: APIConnect
title: 'Spot the difference: External API vs Internal API'
---
# Spot the difference: External API vs Internal API

So in response to my previous blog post
(<https://medium.com/@cminion/no-really-what-is-the-difference-between-a-web-service-and-an-api-and-why-do-i-need-to-care-a6f5c4ead61f>)
I have had a few people bring up that Services are being rebranded
Internal APIs.

I dislike the term External API or Internal APIs. So lets start with
some definitions

**Definitions**

External API --- An API that is exposed outside for the business

Internal API --- An API that is exposed inside the business

I am going to break this article down into two sections Non Functional
and Functional differences.

**Non Functional Requirements**

Every API has its own set of Non Functional Requirements (NFR) depending
on the need. The non functional requirements I will cover here are,
performance (Including Scalability and throttling), Availability,
Security and Maintainability.

Performance is about ensuring that the API can meet the desired number
of results without an outage. Scalability and Throttling are used to
expand and control the demand. An External API is often built with no
clear understanding of what the external demand, even if the demand is
guessed things can go viral. When building an Internal API you can
predict the initial usage and so plan accordingly. However you cannot
easily predict how many systems are going to be using it 6+ months time.
Therefore both Internal and External APIs must be designed to withstand
a non determined amount of requests or risk outages. This same
philosophy is true for availability.

One question to consider*, how many projects have you worked on where
the volumetrics were provided and turned out to be correct?*

Security all APIs MUST be secured. This is a personal mantra, whether
this is OAuth, OIDC, Basic Auth or just a client ID in addition to a non
compromised version of TLS (SSL). A Client ID is essential to track
usage of APIs. If API usage is not tracked the business is unable to
measure success or any PKI for each individual APIs. TLS is mandatory to
ensure that transmissions are not captured or recorded. If your inner
network is compromised then it is easy to sniff out passwords without
encryption on the wire. The NSA was accused of doing this to google in
2013
(<https://www.zdnet.com/article/google-the-nsa-and-the-need-for-locking-down-datacenter-traffic/>
). The fallacy that SSL impacts performance needs to be stopped given
todays computing power.
(<https://www.imperialviolet.org/2010/06/25/overclocking-ssl.html>). All
APIs that need to have a limited access role must be secured. In 2015
security intelligence wrote an article saying that 55% of breaches were
occurred by Malicious Insiders or Inadvertent Actors. This number is
expected to increase. If you would not trust the API on the Internet we
should assume there are Malicious people inside the network to reduce
the risk.
(<https://securityintelligence.com/the-threat-is-coming-from-inside-the-network/>)

![](https://cdn-images-1.medium.com/max/800/1*juvvRPjzqa59pzygO9Mslg.png)

Image taken from
<https://securityintelligence.com/the-threat-is-coming-from-inside-the-network/>

Every API needs to be maintained both inside and outside of the
business. I hope this is common sense.

**Functional**

The functional requirements for an API should be based on the need of
the API not the channel. APIs should be designed to be channel agnostic.
So they can be quickly reused in different parts of the business when
and where they are required. If we design APIs to be channel agnostic
there is no cost to adapt them when they are needed for additional
channels.

**Conclusion**

The only difference between the External and Internal APIs is the
channel. However the channel should not be the deciding the factor for
any key design points as these often change with the success or failure
of ideas.

I am not the only person to say this, Jeff Bezos brought this up in his
mandate in 2012.
http://[apievangelist.com/2012/01/12/the-secret-to-amazons-success-internal-apis/](http://apievangelist.com/2012/01/12/the-secret-to-amazons-success-internal-apis/)





By [Chris Phillips](https://medium.com/@cminion) on
[August 7, 2018](https://medium.com/p/fdcf3ad8816f).

[Canonical
link](https://medium.com/@cminion/spot-the-difference-external-api-vs-internal-api-fdcf3ad8816f)

Exported from [Medium](https://medium.com) on April 6, 2019.
