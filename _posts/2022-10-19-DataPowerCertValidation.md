---
layout: post
date: 2022-10-19 00:01:00
categories: DataPower
title: "Global disabling of Certificate Expiry validation"
author: [  "RGeorgeInness", "ChrisPhillips" ]
---

Recently a customer has asked how to disable certificate expiry validtion. In short they wanted to be able to still use certificates if they had reached end of life. Though this is not something I would recommend I wanted to share the steps.

<!--more-->

Log into the Datapower CLI and run the following commands in the default domain.

```
config
crypto
cert-monitor
disable-expired-certs off
exit
exit
write mem
```

This can also be done via the UI
