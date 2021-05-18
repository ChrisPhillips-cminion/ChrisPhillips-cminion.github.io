---
layout: post
categories: APIConnect
date: 2021-05-17 00:15:00
title: Loading DataPower DPMon in Nmon NMONVisualizer
---

When installing IBM Cloud Packs 2021.x you get the option of having a dashboard for each namespace. This dashboard allows all cloudpaks in the same namespace to share a single pain of glass for various information.

<!--more-->

However out of the box the switcher shows the Cloud Pak name and no other identifier. This is a challenge if for example you have installed Cloud Pak for Business Automation into multiple namespaces.

![/images/menu-1.png]

1. In order to customise these titles you must go into the `Platform customization` for each entry. <BR>![/images/menu-2.png]
2. Then click on Branding
3. Then set the product name. This will be displayed in the switcher. Please note at this time the name contain special characters.<BR>![/images/menu-3.png]


The result is that you will have a menu like
![/images/menu-4.png]
