---
layout: post
categories: HomeLab
date: 2022-09-07 00:14:00
title: Setting Payload limits to protect your apis in API Connect
draft: true
---

One of the questions I’m often asked is how I pick up things like OCP so quickly. The answer is simple I run an OCP Stack at home for personal projects.  The original objective was to run this long term, so I understood the challenges of running an OCP cluster for a long period. In reality it gets reinstalled every three months after a “learning” event. Aka I broke something testing an idea out.

This post is a flex and will be one of a few about what I run at home.

PHOTO

<!--more-->

So how do I make this happen.  First of all you need an ebay account and a spend limit.

## Main Virtualization Box

For the last two years I have run a Dell PowerEdge R620 that had 150GB of memory. Last week this developed a fault on one of the memory channels (its very old kit) and it was replaced with an R720. I moved my RAID Contorler,  CPUs and Memory and added more memory. So I now have a 40 thread, 330GB of memory, 6TB Raid 6 server.  

The rough costs after the initial R620 purchase are
•	R720 Chassis
•	CPU £20 each
•	16 x 600gb in 2 RAID 6 configurations
•	Memory 24x16GB sticks

I was looking at an Dell PowerEdge R730 but that is DDR4 and I was not in a position to replace my DDr3 with DD4 yet.

Thanks to the people at Datatekuk for dealing with my weird requests and providing me a great deal on the R720 Chassis. This is **not** a sponsored post, but they deserve calling out. [https://www.ebay.co.uk/usr/datatekuk?mkevt=1&mkpid=0&emsid=e11051.m44.l1181&mkcid=26&ch=osgood&euid=e490a28c78df406e89a6d00c9649dea5&bu=43133661369&osub=-1%7E1&crd=20221014001215&segname=11051&ul_noapp=true](Datatekuk)


This VM box runs ESX 7 (license form ebay). On this box I have a run for
-	VCenter to simplify installing OCP
-	Windows Server (180 day trial still) – mainly for active directory
-	Bind 9 – (about to be replaced with Windows DNS )
-	PI Hole
-	HomeBridge (Home Kit)
-	DryDock (OCP Bastion vm)
-	OCP 4.10 Master
-	OCP 4.10 Worker x 3
-	WildCard – LetsEncrypt generating vm
-	Airlock – DMZ VM
-	Unifi Management Software – (Now decommissioned)

## NAS

I have a separate Custom Build NAS with a RAID 0 Disk. Atom CPU with 8GB Memory. This is running TrueNas and has nothing special going on. This is where I back up everything to. As I do not have an offsite backup yet this hardware hasn’t changed for five years.  I have been intending to increase the memory for a few years.

## Network
I run a UnifI network. For those that are not aware of Unifi it is the prosumer drug where you keep talking yourself out of setting up a 10GB network. I have some 2GB LAG connections on my main trunk the rest is GB.
*	UDM pro
*	US-8
*	US-8150 W
*	US Nano HD
*	US AP Lite
*	US-16
*	Uni Flex  x2

Image

## Other.

I have a couple of Raspberry Pi’s
1.	Home Dashboard client
2.	Octo Print3d for my 3d printer

The future projects for this are as follows
*	Increase Network Ports in my NAS so it can do 2GB LACP
*	Increase Memory in NAS
* Three UPS
  - My Desktop
  - Switch in Loft
  - Daughters Computer
*	Install 3rd Wifi Point
*	Move to 10GB network,
  - Buy an Unifi Aggregation switch
  - complete my fibre roll out
  - Unifi Pro switches (when I win the lottery)
*	Buy an F5 (They are only £50 for an old one ) Load Balancer so I can understand why there is such an issue with configuring them.
