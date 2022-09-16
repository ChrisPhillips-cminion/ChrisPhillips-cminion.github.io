---
layout: post
categories: apiconnectz
date: 2022-09-07 00:14:00
title: Setting Payload limits to protect your apis in API Connect
draft: true
---

In API Connect a parsing policy can be used to protect your apis to ensure that large files are not malicious or accidentally clogging up system, by default the max size is 4MB.  However clients frequently want to support files larger then the default size,  this is not something I recommend (I will make a future post about).

This post will show the steps to increase or decrease the document size limit.

<!--more-->

Firstly, the document size limit is only applied when an API uses the parse policy. To apply the 4MB limit simply add the parse policy to the start of your API.

Now to customise the limit the parse-setting option must be modified on each DataPower. I recommend that this is via a gateway extension or added to an existing gateway extension.


The DataPower object looks like the below

```
parse-settings: apic-default-parsesettings [up]
-----------------------
 admin-state enabled
 document-type detect
 document-size 4194304 bytes
 nesting-depth 512
 width 4096
 name-length 256 bytes
 value-length 8192 bytes
 unique-prefixes 1024
 unique-namespaces 1024
 unique-names 1024
 number-length 128 bytes
```

To change the document size you must modify the document-size attribute. Please not the object does not exist until after the Gateway is registered with the API Manager.


The commands in data power are as follows to set the max size to 512kb

```
sw apiconnect
config
parse-settings apic-default-parsesettings
document-size 524288
exit
exit
```

I would recommend the following commands are added to a gateway extension if this is running with DataPower in a container.
```
top; co
parse-settings apic-default-parsesettings
document-size 524288
```
