---
layout: post
date: 2017-07-20  00:00:00
categories: APIConnect
title: 'APIConnect Developer Portal --- Logs'
---
-<!--more-->--



Thanks to Chris Dudley for providing this information

When upgrading the developer portal additional logs can be found in
/var/log/syslog and /var/log/devportal/site\_action.log

The following command will print them to the screen while the upgrade is
taking place.

```
sudo tail -F  /var/log/devportal/site_action.log /var/log/syslog
```





By [Chris Phillips](https://medium.com/@cminion) on
[July 20, 2017](https://medium.com/p/e8a37843e30b).

[Canonical
link](https://medium.com/@cminion/apiconnect-developer-portal-logs-e8a37843e30b)

Exported from [Medium](https://medium.com) on April 6, 2019.
