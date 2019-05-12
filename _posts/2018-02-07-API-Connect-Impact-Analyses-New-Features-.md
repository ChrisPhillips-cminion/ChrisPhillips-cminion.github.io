---
layout: post
date: 2018-02-07  00:00:00
categories: APIConnect
title: 'API Connect Impact Analyses --- New Features!'
---
# API Connect Impact Analyses --- New Features! 

Last year we released a useful script for analyzing API Connect. For
more information take a look
here.<https://www.ibm.com/developerworks/library/mw-1703-phillips/index.html>



![](https://cdn-images-1.medium.com/max/2560/1*wFES1nin1znbZKN-RWPNxg.png)



I have just published an update that allows you to not only look at the
down stream services, but also look at the policies or OAuth URLs.

When you first load the tool it now asks you to select one of the
following,

![](https://cdn-images-1.medium.com/max/800/1*MIJOyTAq6HpCU0OxcFc1Og.png)

Invokes and Policies provide the previous functionality

Policies instead of listing down stream services lists the name and
version of policies used in APIs. This can be used to track where custom
policies are used.

![](https://cdn-images-1.medium.com/max/800/1*3Xj3Q3Uisg1zBsOrfd5l1g.png)

Security returns the security policies or the OAuth URLs. This can be
used to assess which API is using which OAuth Provider.

![](https://cdn-images-1.medium.com/max/800/1*TFhsFblC-vY6lUObbHluQA.png)

Of course you can still reorder these parameters to provide the
information in any order with Applications, API, Products and Plans..

![](https://cdn-images-1.medium.com/max/800/1*wFES1nin1znbZKN-RWPNxg.png)

The example above shows the OAuth endpoints required for each client
application.

The code is available here
<https://github.com/ChrisPhillips-cminion/APIConnect-ImpactAnalysis>





By [Chris Phillips](https://medium.com/@cminion) on
[February 7, 2018](https://medium.com/p/b8204d824a32).

[Canonical
link](https://medium.com/@cminion/api-connect-impact-analyses-new-features-b8204d824a32)

Exported from [Medium](https://medium.com) on April 6, 2019.
