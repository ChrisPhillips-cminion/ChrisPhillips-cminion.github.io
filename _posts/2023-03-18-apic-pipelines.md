---
layout: post
date: 2023-03-18 00:01:00
categories: APIConnect
title: "OpenShift Pipeline - Publish APIC"
draft: true
---

I have been asked almost daily for the last few weeks what is my preferred CIDC took or process.  My answer is always the same, given APIC has a rest interface the best tool is the one the team know.

<!--more-->

However this is not often seen as an acceptable answer. So I decided to dive back into OCP Pipelines. I set myself two hours to see what I could put together. This is by no means perfect but will meet the initial needs.  

**Requirements**
1. OpenShift Environment - I did this with OCP 4.10
2. OpenShift Pipelines Operator installed

![https://chrisphillips-cminion.github.io//images/ocppipelines.png](https://chrisphillips-cminion.github.io/images/ocppipelines.png)

**My Task**

I have placed my task on github here [https://gist.github.com/ChrisPhillips-cminion/830ac19b20e6985a31e9e6ce7e13eceb](https://gist.github.com/ChrisPhillips-cminion/830ac19b20e6985a31e9e6ce7e13eceb)

Save the gist to a local file and load it with

`oc apply -f ./apic-publish-task.yaml`

This must be loaded into the namespace that will host the pipeline.

**Create the Pipeline**

![https://chrisphillips-cminion.github.io/images/pipeline.png](https://chrisphillips-cminion.github.io/images/pipeline.png)

I wont repeat a thousand other articles on how to create a pipeline, but I will provide a sample here.
[https://gist.github.com/ChrisPhillips-cminion/830ac19b20e6985a31e9e6ce7e13eceb](https://gist.github.com/ChrisPhillips-cminion/830ac19b20e6985a31e9e6ce7e13eceb)

This simple pipeline will extract from git and then publish the products listed.
