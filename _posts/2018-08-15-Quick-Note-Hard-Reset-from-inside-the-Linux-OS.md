---
layout: post
date: 2018-08-15  00:00:00
categories: APIConnect
title: 'Quick Note --- Hard Reset from inside the Linux OS'
---

# Quick Note --- Hard Reset from inside the Linux OS

I have been using CEPH a lot recently that has an annoying habit of
knackering disks. To fix this is simple, you do a hard reset and
everything is fine. However in this modern cloud world I do not have
access (or want it) to my vcenter, and the guy in charge is a different
time zone and equally busy.

So from a quick google I cam across this


**Hard reset on linux command line.**

Linux is not Windows XP and if reboot fail you usually still connect by
SSH and do something. This commands will
show...*www.linux-geex.com](https://www.linux-geex.com/hard-reset-on-linux-command-line/ "https://www.linux-geex.com/hard-reset-on-linux-command-line/")[](https://www.linux-geex.com/hard-reset-on-linux-command-line/)


These instructions say a hard reset can be done by doing the following

> *echo 1 \> /proc/sys/kernel/sysrq*
> *echo b \> /proc/sysrq-trigger*

And they work like a charm.

Thanks to [Pedro M. S.
Oliveira](https://www.linux-geex.com/author/x_pedro_x/ "Posts by Pedro M. S. Oliveira") for their post from 8 years ago!





By [Chris Phillips](https://medium.com/@cminion) on
[August 15, 2018](https://medium.com/p/38a39812848b).

[Canonical
link](https://medium.com/@cminion/quick-note-hard-reset-from-inside-the-linux-os-38a39812848b)

Exported from [Medium](https://medium.com) on April 6, 2019.
