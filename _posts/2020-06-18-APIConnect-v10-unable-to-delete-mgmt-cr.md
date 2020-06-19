---
layout: post
date: 2020-6-16 00:01:00
categories: APIConnect
title: "API Connect v10 - unable to delete mangement cr"
author: ["LukeRaus","ChrisPhillips"]
---

When deploying API Connect it is possible that the postgres does not start due to user error. (Most commonly due to invalid image registry url).


<!--more-->
`kubctl delele mgmt -n <namespaec> <mgmt-name> ` should delete the cr but this just hangs. In order to remove the CR you must run the following command.


```
kubectl patch mgmt <mgmt-name>  -n <namespaec> -p '{"metadata":{"finalizers": []}}' --type=merge
```

Then you can delete the mgmt cr with `kubctl delele mgmt -n <namespaec> <mgmt-name> `
