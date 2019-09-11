---
layout: post
date: 2019-09-11 01:00:00
categories: APIConnect
title: "Datapower webgui ssl server profile gives 'certificate unknown' error"
author: ["JPSchiller"]
---
This is error message is a common issue when using DataPower with the web mgmt interface enabled
```
[0x8120002f][ssl][error] ssl-server(webgui-ssl): SSL library error: error:14094416:SSL
    routines:ssl3_read_bytes:sslv3 alert certificate unknown
[0x8120002f][ssl][error] ssl-server(webgui-ssl): SSL library error: error:140940E5:SSL
    routines:ssl3_read_bytes:ssl handshake failure
```

<!--more-->
This is caused by the web browser is sending the "certificate unknown" error because it does not recognise the DataPower certificate as a well known CA certificate.  DataPower then repeats the error from the browser in its logs.


The solution for this is documented in a tech note here. [https://www.ibm.com/support/pages/datapower-webgui-ssl-server-profile-gives-certificate-unknown-error](https://www.ibm.com/support/pages/datapower-webgui-ssl-server-profile-gives-certificate-unknown-error)
