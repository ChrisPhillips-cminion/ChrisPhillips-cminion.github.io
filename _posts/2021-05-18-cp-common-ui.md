---
layout: post
categories: APIConnect
date: 2021-05-18 00:15:00
title: Customising the names of the components in the CP switcher.
---

When installing IBM Cloud Packs 2021.x you get the option of having a dashboard for each namespace. This dashboard allows all CloudPaks in the same namespace to share a single pain of glass for various information.

<!--more-->

However out of the box the switcher shows the Cloud Pak name and no other identifier. This is a challenge if for example you have installed Cloud Pak for Business Automation into multiple namespaces.

![https://chrisphillips-cminion.github.io/images/menu-1.png]()
![https://nmonvisualizer.github.io/nmonvisualizer/screenshots/SingleSystemReport.jpg](https://nmonvisualizer.github.io/nmonvisualizer/screenshots/SingleSystemReport.jpg)

1. In order to customise these titles you must go into the `Platform customization` for each entry. <BR> ![https://chrisphillips-cminion.github.io/images/menu-2.png]()
2. Click on Branding
3. Set the product name. This will be displayed in the switcher. Please note at this time the name contain special characters.<BR> ![https://chrisphillips-cminion.github.io/images/menu-3.png]()


The result is that you will have a menu like
![https://chrisphillips-cminion.github.io/images/menu-4.png]()
