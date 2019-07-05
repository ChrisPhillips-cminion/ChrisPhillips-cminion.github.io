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

In Part 2 we will go through how API Connect can be used to provide Authentication and Authorization for the websocket connection using the API Connect Security Definitions.

### Prerequisites
* WebSocket Proxy from Part 1
* WebSocket Client and Server application (The sample I use is here  [](https://github.com/ChrisPhillips-cminion/PlayingWithWebSockets) )
* API Connect 2018 Instance

The API works similarly to an Authorisation URL. The API must be secured with the same security that you want to have to secure the Web Socket. When the Web Socket is establishing the connection to the DataPower, DataPower sends a request to this API with the credentials and the API responds with 200, 400, 401 or 500

### 1. Create the API

To simplify this  guide I have provided a sample API below.

To Import this into API Connect 2018.
1. Login to API Connect
2. Go to Drafts
3. New API.
4. Select Import.
5. Create a new Product

### 2. Publish the API
1. Login to API Connect
2. Go to Drafts
3. Click on the hotdog menu and publish

### 3. Subscribe to the API
1. Login to API Connect
2. Go to Catalogs
3. Select the Catalog you published to
4.  Select Consumer Organization
5. Click add
6. Select Applications
7. Subscribe

### 6. Call the API From DataPower
1. Log into DataPower
2. Go to the Multi-Protocol Gateways
3. Select the WebSocket MPG
4. Go to policies

### Test
