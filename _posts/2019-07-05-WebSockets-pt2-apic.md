---
layout: post
date: 2019-07-05 01:00:00
categories: IBMCloud
title: "WebSockets Part 2 - Securing with API Connect"
draft: true
---

DataPower provides the facility to proxy WebSocket connections. This article is part **two** of a three part guide consisting of

* *Part 1* - How to create a WebSocket Proxy in DataPower
* **Part 2 - How you can use API Connect to secure your implementation**
* *Part 3* - How to socialise it via the Developer Portal giving your consumers the easiest

*DataPower is used to protect and proxy http connections. As a WebSocket is an upgraded HTTP Connection it allows DataPower to offer similar protection and proxying facilities. When a WebSocket connection is established with DataPower before the connection is upgraded it applies the MultiProtocol Gateway Policies. This means that additional logic can be applied to validate the request. In this series of articles we are going to be using API Connect for this.*
