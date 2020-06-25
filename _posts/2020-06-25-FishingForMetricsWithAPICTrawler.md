---
layout: post
date: 2020-6-25 01:12:00
categories: APIConnect
title: "API Connect - Fishing you Pod metrics into Prometheus with APIConnect Trawler "
---
![Trawler Logo ](https://github.com/IBM/apiconnect-trawler/raw/main/docs/trawler.png)

Trawler is a metrics exporter for IBM API Connect, allowing Kuberentes metrics to be sent to Prometheus.


<!--more-->

The API Connect Managed Offering Operations team needed a way to get  metrics into prometheus for API Connect 2018.

This is not an uncommon request from customers either so I wanted to acknowledge it here.


API Connect Trawler is designed to run within the same Kubernetes cluster as API Connect, such that it can scrape metrics from the installed components and make them available. The metrics gathering in Trawler is separated into separate nets for the different types of metrics to expose so you can select which ones to enable for a particular environment.

It requires a service account with read access to list pods and services in the namespace(s) the API Connect components are deployed in.

For more information please take a look at [https://github.com/IBM/apiconnect-trawler](https://github.com/IBM/apiconnect-trawler)

Thanks to [Ricky](https://www.linkedin.com/in/rickymoorhouse/) and his team for allowing me to post this here.
