---
layout: post
date: 2022-10-19 00:01:00
categories: DataPower
title: "Global disabling of Certificate Expiry validation"
author: [ "ChrisPhillips", "RGeorgeInness" ]
draft: true
---

Recently a customer has asked how to disable certificate expiry validtion. In short they wanted to be able to still use certificates if they had reached end of life. Though this is nothing I would recommend

**UPDATED 2022** - *Since this article was originally published three years ago datapower has added a requirement that each domain should have the same name therefore to achieve the first design you must split your datapower with tenants.*
<!--more-->
