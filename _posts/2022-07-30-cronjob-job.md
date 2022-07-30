---
layout: post
categories: OpenShift
date: 2022-07-30 00:14:00
title: Run CronJob immediately
---

One of my most common google strings is how to run a cronjob in k8s immediately.

`kubectl create job --from=cronjob/<CronJob Name> <JobName>`

Use the above command just change the cronjob name and the jobname
