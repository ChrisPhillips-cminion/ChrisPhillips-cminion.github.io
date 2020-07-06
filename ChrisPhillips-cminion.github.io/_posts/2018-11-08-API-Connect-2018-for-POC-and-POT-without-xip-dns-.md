---
layout: post
date: 2018-11-08  00:00:00
categories: APIConnect
title: 'API Connect 2018 for POC and POT without xip dns.'
---


A few months back I wrote an article on how to get a quick dns working
for working with API Connect 2018. This is another strategy that you can
do at your own risk. [www.dot.tk](http://www.dot.tk) allow you to register a free domain, that is free for 12 months. You can then use their DNS server.
<!--more-->
I recommend fully reading the T&Cs of dot.tk first.

Dot.tk off a service to register a free domain on some of the lesser
known domain endpoints. I have registered
[www.bored-prawn.cf](http://www.bored-prawn.cf) as well as cminion.cf.

Once you have registered your domain you can configure A and C NAME
records to point to the ingress for your API Connect.

This is great for two reasons,

1.  [If you move or redeploy your stack you can keep the endpoints the
    same]
2.  [It looks better then using xip.]

I recommend that you create an A or CNAME record to act as a parent.
This should point to the ingress. And then create CNAME records for each
endpoint that point to the parent.

I have no connection to dot.tk other then a free customer.





By [Chris Phillips](https://medium.com/@cminion) on
[November 8, 2018](https://medium.com/p/1271485caf1).

[Canonical
link](https://medium.com/@cminion/api-connect-2018-for-poc-and-pot-without-xip-dns-1271485caf1)

Exported from [Medium](https://medium.com) on April 6, 2019.
