---
layout: post
date: 2023-09-29 01:00:00
categories: APIConnect
title: "Friday Lunchtime Hack - jmeter on OCP"
---

A few years ago I was playing around with jmeter-on-ocp. [https://github.com/ChrisPhillips-cminion/jmeter-on-ocp](https://github.com/ChrisPhillips-cminion/jmeter-on-ocp). Please note this is my fork, i am unsure what is happening to the original but credit must go to https://github.com/alvarolop for the start of this.

<!--more-->

This week I had to go back into performance test to reproduce a clients issue. So I dusted off this repo.  Now the point of friday lunchtime hack is to quickly knock something together to solve a problem. It WONT be pretty.

This repo was designed to quickly be able to run a JMETER workload in three replicas on OCP. It is not clever.

To make this work clone the repo. And open the auto-install.sh.

Inside the auto-install script file you can reference the test file and on line 43.

Then you can run the auto-install script to build the container, and initiate the test.

I like to wrap this in another shell script to extract the jmeter logs using `oc logs -lapp=jmeter -n jmeter`
