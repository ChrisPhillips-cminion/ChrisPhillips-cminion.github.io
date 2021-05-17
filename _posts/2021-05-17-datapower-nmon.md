---
layout: post
categories: APIConnect
date: 2021-05-17 00:15:00
title: Loading DataPower DPMon in Nmon visualisation
---

DataPower contains a file called DPMon that stores all nmon information. This is extremely useful for determing resource constraints

<!--more-->

Once the file is extracted from Datapower `temporary:///dpmon/dpmon` it can be loaded into NMONVisualizer.

This can be downloaded from https://nmonvisualizer.github.io/nmonvisualizer/

**Before the file can be loaded in it must be manually renamed to add .nmon extension.**

![https://nmonvisualizer.github.io/nmonvisualizer/screenshots/SingleSystemReport.jpg](https://nmonvisualizer.github.io/nmonvisualizer/screenshots/SingleSystemReport.jpg)
