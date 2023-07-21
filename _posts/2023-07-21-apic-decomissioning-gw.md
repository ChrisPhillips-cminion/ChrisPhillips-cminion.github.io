---
layout: post
date: 2023-07-21 01:00:00
categories: APIConnect
title: "API Connect decommissioning a gateway service"
---


In API Connect you can have multiple gateway services. I have written about how to add one before but not how to decommission on that is no longer needed.

<!--more-->

## Step 1 - Remove the APIs from the Gateway Service
This can be done using the script [https://chrisphillips-cminion.github.io/apiconnect/2022/07/16/APIC-Gateway-Service-replace.html](APIC Gateway Service Replace)

## Step 2 - Remove the Gateway Service from the Catalogs or Spaces
* Log into the API manager
* Go to each Catalog or Space
* Go to Settings then Gateway services
* Click Edit
* Untick the Gateway Service to be decommissioned.
* Press Save

## Step 3 - Remove the Gateway Service from the cloud manager consoles
* Log into the Cloud manager
* Go to topology
* Delete the Gateway Service to be decommissioned.
