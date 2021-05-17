---
layout: post
categories: APIConnect
date: 2021-05-17 00:15:00
title: Loading DataPower DPMon in Nmon NMONVisualizer
---

DataPower contains a file called DPmon that stores nmon information. This is extremely useful for investigating resource constraints

<!--more-->

Once the file is extracted from DataPower `temporary:///dpmon/dpmon` it can be loaded into NMONVisualizer.

This can be downloaded from https://nmonvisualizer.github.io/nmonvisualizer/

**Before the file can be loaded in it must be manually renamed to add .nmon extension.**

![https://nmonvisualizer.github.io/nmonvisualizer/screenshots/SingleSystemReport.jpg](https://nmonvisualizer.github.io/nmonvisualizer/screenshots/SingleSystemReport.jpg)
(image above taken from NMONVisualizer website)
