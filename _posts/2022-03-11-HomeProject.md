---
layout: post
categories: Home
date: 2022-03-11 00:14:00
title: Home Project - Starter for ten
draft: true
---


I have always believed that you need to play to learn.  In order to take my sample and explanations to the next level I am going to be basing some articles around some home projects.

<!--more-->

My current personal project is a home dashboard.



This primarily comes from me forgetting to take the bins out. *In the UK you need to take your bins to the curb once a week for them to be emptied*.

I am gluing data from a number of sources together to show on this dashboard. Some information will be events, other data will be requested through traditional API calls.  

I am running OCP 4.8 LTS on a 24 core, 48 thread server. This runs a number of home projects not just my dashboard. It exposes the dashboard via HTTPs endpoint. A raspberry pi running dietpi in kiosk mode then connects to a monitor running in my hall.  [https://dietpi.com/](https://dietpi.com/)

The dashboard is powered by smashing, a ruby based dash boarding app. [https://smashing.github.io/](https://smashing.github.io/)

Running in OCP I have CP4I CD Stream deployed with IBM Event Streams as a cluster scope deployment. I will be using the same IBM Event Streams for future projects.

## VMWare and Physical Topology
<!-- <div class="mermaid">
GraphDiagram
    Monitor
    Pi - DietOS
      Dashboard->OCP Master+Infra
    WorkHorse
      OCP Master+Infra
      OCP Worker1
      OCP Worker2
      OCP Worker3
      Bind9
      PiHole
      HomeBridge
      Instana
      Other VMs
      Block Storage
      FileStorage
    NAS
      NFS Storage
    Smart Lights
    Smart DoorBell
    Smart Thermostat
    Bindicator
    ClassCharts
 </div> -->

## OCP Topology
each box represents a namespace in OCP
<div class="mermaid">
GraphDiagram
  as
</div>


  CP4I
  Eventstreams
  BackUp
    Job-Rsnapshot-Hourly
    Job-Rsnapshot-Daily
    Job-Rsnapshot-Weekly
    Job-Rsnapshot-Monthly
  Dashboard
    dashboard
    Lights
    alerts
    food
  Ocp-backup
  Dashboard
  ACE
