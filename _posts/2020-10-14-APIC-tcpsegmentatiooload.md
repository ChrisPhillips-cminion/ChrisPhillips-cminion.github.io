---
layout: post
date: 2020-10-14 00:13:00
categories: APIConnect
title: "UI intermittently fails to load Large Product lists, Application List, Consumer Org lists  or  Analytics"
---

With some advanced and unusual network configurations (that I do not understand) API  Connect has intermittent issues with OVAs. The impact of this situation is that the UI appears to hang or fail to load analytics, product list or application lists.
<!--more-->

Under the covers this is because a REST API call from the UI to the other pods is hanging when large payloads need to be returned.

In order to fix this we recommend setting `tcp-segmentation-offload` to  off. It is on by default.

**I am not a network engineer** but `tcp-segmentation-offload` when turned on for the majority of configurations will improve  performance by allowing the NIC Driver to segment the traffic. If it is disabled the segmentation is done by the CPU and so this may have a negative impact on performance across all aspects.

<!-- Thanks to the two gentlemen ..... for assisting with this. -->
