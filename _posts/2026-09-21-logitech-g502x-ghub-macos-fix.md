---
layout: post
date: 2026-09-21 09:00:00
categories: Tools
title: "Logitech G Hub Not Working on macOS — The Fix"
author: ["ChrisPhillips"]
tags: [Logitech, macOS, G502X, GHub]
---

After installing [Logitech G Hub](https://www.logitechg.com/en-gb/innovation/g-hub.html) for the [G502X](https://www.amazon.co.uk/dp/B07W7LW3VV?th=1&linkCode=ll2&tag=chrisphilli03-21&linkId=ce9be1868d29ba9f4c06345b54b0734e&ref_=as_li_ss_tl), nothing worked. Weeks of frustration until [a Reddit thread had the answer](https://www.reddit.com/r/LogitechG/comments/113ls7a/logitech_g502_macos_ventura_device_inactive/).

![Logitech G Hub Privacy settings on macOS](/images/2026-09-21-logitech-ghub.jpg)

<!--more-->

Go to **Settings → Privacy & Security → Input Monitoring** and make sure **Logitech G Hub Agent** is enabled.

Then go to **Accessibility** in the same section and make sure both **G Hub** and **G Hub Agent** are on.

That's it. Mouse and keyboard work and I can change the DPI settings. No idea why Logitech doesn't auto-enable these permissions on install.

