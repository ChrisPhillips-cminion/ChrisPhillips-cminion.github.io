---
layout: post
date: 2018-03-09  00:00:00
categories: APIConnect
title: 'API Connect MQ Invoke v2.'
---
<!--more-->



![](https://cdn-images-1.medium.com/max/2560/1*7Gh8_izqdIsi5knXr7p1Vw.png)



I have finally managed to sit down and spend sometime with this
artifact. I was asked to produce a Lab at Think 2018 with Natasha
(<https://www.linkedin.com/in/natasha-kirkup-1896b360/>) to shows off
the MQ Invoke Policy for API Connect.

The policy can be downloaded from here. Github Link :
<https://github.com/charlottehutchinson/APIConnect-Policy-MQInvoke>

This is based off the work I did with Charlotte (\@C\_Hutchinson1) and
Jack (<https://www.linkedin.com/in/jack-dunleavy-784baa109/>).

Original Article :
<https://www.ibm.com/developerworks/library/mw-1611-hutchinson-trs/index.html>

The only significant change is that we added support to set some RFH2
headers from the Policy Setting page it self. See the image below.

![](https://cdn-images-1.medium.com/max/600/1*OPa8j3tl5LyiLnJSjNEw5w.png)

While making these changes we discovered a major bug. It worked fine for
XML but not JSON. I am unsure how this missed our original testing, and
quite frankly I found this very embarrassing. The issue we had was JSONX
was being returned not JSON. After a lot of work with the help of Andrew
White (<https://www.linkedin.com/in/andrew-white-007b7624/>) we managed
to add some logic to handle this translation. I will write this up in a
separate blog post shortly.





By [Chris Phillips](https://medium.com/@cminion) on
[March 9, 2018](https://medium.com/p/c45104984935).

[Canonical
link](https://medium.com/@cminion/api-connect-mq-invoke-v2-c45104984935)

Exported from [Medium](https://medium.com) on April 6, 2019.
