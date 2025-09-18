---
layout: post
date: 2025-09-18 09:00:00
categories: APIConnect
title: "Enabling the DotDot feature"
---

DataPower has a number of features that can be enabled with API Connect with Gateway extensions. One of these is the DotDot feature that `Allow requests that contain .. in the URL.` 
To look at other features that can be enabled take a look here - [https://www.ibm.com/docs/en/datapower-gateway/10.5.x?topic=commands-allowed-features](https://www.ibm.com/docs/en/datapower-gateway/10.5.x?topic=commands-allowed-features)

<!--more-->

## Create the Gateway Extension

To enable the DotDot feature you need to create a cfg file that extends the FrontSideHandler (FSH) in datapower. If you look at the `allowed-features` line in the sample below you can see `DotDot` is concatinated to the end of the string with a `+` as a seperator/

```
top
co
source-https apiconnect_https_9443
  allowed-features HTTP-1.0+HTTP-1.1+HTTP-2.0+POST+GET+PUT+PATCH+HEAD+OPTIONS+TRACE+DELETE+CustomMethods+QueryString+FragmentIdentifiers+DotDot
exit
```

This needs to be zipped with a command like

```
zip dotdot-fsh.zip dotdot.cfg
```

Then a manifest is required like below

manifest.json
```
{
   "extension":{
      "files":[
         {
            "filename":"dotdot-fsh.zip",
            "deploy":"immediate",
            "type":"extension"
         }
      ]
   }
}
```

Then a zip of both the manifest and the fsh zip must be created

```
zip dotdot.zip manifest.json dotdot-fsh.zip
```

## Load the Gateway Extension
Login to API Connect Cloud Manager Admin, go to topology, select the gateway and click on configure gateway extension.


![](/images/otel1.png)

Click on Add and upload the zip file created in step above and press save

![](/images/otel2.png)

![](/images/otel3.png)

Wait a few minutes for the extension to apply

Once gateway extension is applied you can see that the FSH is updated to include the DotDot feature. 
