---
layout: post
date: 2017-07-17  00:00:00
categories: APIConnect
title: 'Proxy and Invoke --- What is the difference in API Connect?'
---

Proxy and Invoke --- What is the difference in API Connect? 
===========================================================

 
API Connect offers both Proxy and Invoke policies. I am often asked what
hte difference. Ulas Cubuk from the IBM Pan European API Connect...


 
 
 

------------------------------------------------------------------------


 
 
### Proxy and Invoke --- What is the difference in API Connect? 

API Connect offers both Proxy and Invoke policies. I am often asked what
hte difference. Ulas Cubuk from the IBM Pan European API Connect team
provided the following description.

``` 
Proxy Policy: by default do not resolves HTTP redirects and rewrites the host name and port in the Location response header (of the 302/301 response) with the gateway’s host name and port so that all the subsequent requests are always sent to the gateway. 
In order to rewrite host name the following conditions should be true:
```

``` 
 • The host name and port in the Location header matches that of the target server.
 • The request contains a Host header.
```

``` 
Invoke Policy: attempts to resolve HTTP redirects.
```





By [Chris Phillips](https://medium.com/@cminion) on
[July 17, 2017](https://medium.com/p/13cb59e07673).

[Canonical
link](https://medium.com/@cminion/proxy-and-invoke-what-is-the-difference-in-api-connect-13cb59e07673)

Exported from [Medium](https://medium.com) on April 6, 2019.
