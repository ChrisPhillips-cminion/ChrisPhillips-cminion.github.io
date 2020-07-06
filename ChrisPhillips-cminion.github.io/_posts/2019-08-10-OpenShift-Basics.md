---
layout: post
date: 2019-08-10 03:00:00
categories: OpenShift
title: "OpenShift Basics - Living Post"
draft: true
---

Though I am fairly experienced at Kubernetes I am new to OpenShift. The purpose of this post is to keep track of all the little hits and tips i pick up. In short if I have to google how to do something I will add it to this list.  Some of these will appear very very obvious.

### Creating a project in OpenShift

1. Ensure you are logged in as the correct user
2. `oc create namespace  <project name>` or `kubectl create namespace  <project name>`
3. `oc projects` to check the project as created
4. `oc project <project name>` to switch the scope to that project`
