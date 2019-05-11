---
layout: post
date: 2018-11-05  00:00:00
categories: APIConnect
title: 'QuickNote : Network not working on ubuntu cosmic'
---

QuickNote : Network not working on ubuntu cosmic 
================================================

 
I installed ubuntu cosmic and upgraded so everything was on the latest
package in the ubuntu repos.


 
 
 

------------------------------------------------------------------------


 
 
### QuickNote : Network not working on ubuntu cosmic 

I installed ubuntu cosmic and upgraded so everything was on the latest
package in the ubuntu repos.

I rebooted and then the onboard network card failed to get an IP. Now
this is not a guide on how to debug it, but just how i fixed it.

This is not my first rodeo and so I have a USB wifi card sitting in my
box of cables just for these occasions. Once I plugged it in decided to
try the original kernel. A quick reboot later everything was working
fine. So it was a problem with the 4.18.11 kernel.

So I looked at how to patch to 4.19.1 to see if this fixed the problem
and I came across UKUU from this link
(<https://www.omgubuntu.co.uk/2017/02/ukuu-easy-way-to-install-mainline-kernel-ubuntu>)

This awesome app gives me a standalone interface for controlling which
kernels i have installed and installing the latest. I used the app to
install 4.19.1 did a reboot and everything worked fine.





By [Chris Phillips](https://medium.com/@cminion) on
[November 5, 2018](https://medium.com/p/2dd51d745800).

[Canonical
link](https://medium.com/@cminion/quicknote-network-not-working-on-ubuntu-cosmic-2dd51d745800)

Exported from [Medium](https://medium.com) on April 6, 2019.
