---
layout: post
date: 2018-02-16  00:00:00
categories: APIConnect
title: APIConnect Streaming Logs from the API Manager
---

APIConnect Streaming Logs from the API Manager 
==============================================

 
Recently we were debugging an infrastructure "situation" and we did not
have an external log source set up. The postmortem was failing and...


 
 
 

------------------------------------------------------------------------


 
 
### APIConnect Streaming Logs from the API Manager 

Recently we were debugging an infrastructure "situation" and we did not
have an external log source set up. The postmortem was failing and the
cmc.out was wrapping far too quickly.

I knocked together this script to allow us to stream the log files from
the API Manager to the local disk.

**THIS IS NOT RECOMMENDED TO BE USED OUTSIDE OF EXTRAORDINARY
CIRCUMSTANCES.**

<https://github.com/ChrisPhillips-cminion/APIConnect-LogTailer>

The Log Tailer simple creates one or more SSH sessions and runs the
following command.

``` 
debug tail file <filepath>
```

It then writes the file to the local disk.





By [Chris Phillips](https://medium.com/@cminion) on
[February 16, 2018](https://medium.com/p/3a040acf2cb2).

[Canonical
link](https://medium.com/@cminion/apiconnect-streaming-logs-from-the-api-manager-3a040acf2cb2)

Exported from [Medium](https://medium.com) on April 6, 2019.
