---
layout: post
categories: APIConnect
date: 2021-02-25 00:14:00
title: API Connect 2018 - Gateway Extension
---

Anyone on API Connect 2018 I recommend you move to v10. But if you are unable to and need to apply some configuration to DataPower you can apply configs like below.

<!--more-->

*Thanks to John Bellessa for his help*


1. Create you datapower config and put it into a text file. In this example we will call this datapower.cfg
2. Create a configmap `kubectl create configmap custom-dp-config --from-file=datapower.cfg`
3. Create an extra values file. In this example we will call this dp-extravaluesfile.yaml
```
datapower:  
    customDatapowerConfig: "custom-dp-config"

```
4. run  `apicup subsys set <gwy> extra-values-file dp-extravaluesfile.yaml`
5. run `apicup subsys install gwy`

**THIS IS ONLY FOR APICONNECT V2018 not V10**
