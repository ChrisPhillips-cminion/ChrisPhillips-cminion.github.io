---
layout: post
date: 2019-05-19 02:00:00
categories: Networking
title: 'ARGH NETWORKS !!! - A Question'
---

*This is an blog post on what i am currently stuck on. This is posted partially to get my thoughts in order and to help anyone else hitting the same issue feel like they are not alone*

I know nothing about networking, I muddled through the University module many many years ago. The embarrassing  things is networking is my family trade. My Dad worked on System X the first digital telephone exchange, my brother lectures and researches in the subject... My sister did something back in the day before retraining as a midwife. (My other sister was sensible and stayed out of tech. )


I am frequently hitting issues with customers and waiting for the networking teams to get stuff configured. I did not understand and so I went to ebay and bought a cheap Dell PowerConnect 7024.  I intended to split each room in my house into its own subnet, why you may ask... well I am not sure i can answer that. Early on my brother told me I needed to use the ASUS router for its NAT and DMZ facility so my network diagram is similar to below.

![](/images/2019-05-19-network.png)

I have a static route in my ASUS router that forwards all traffic to 192.168.2.0 to 192.168.1.71.

The workstation 192.168.2.5 can ping google.comm, 8.8.8.8 and  192.168.2.3. However we cannot establish and SSL connection to the internet. (I have not tried locally)

My laptop on 192.168.1.100 that connects directly to the ASUS wifi point can nmap 192.186.2.5 and 192.186.2.2 but not 192.168.2.3. However it cannot ssh into 192.168.2.5 with  a timeout error. The other nodes on that the CISCO unmanaged switch do not seem to have IPs. Or at least I can only see 192.168.2.5 from my laptop.
