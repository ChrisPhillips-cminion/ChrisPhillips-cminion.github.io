---
layout: post
date: 2018-09-07  00:00:00
categories: APIConnect
title: APIConnect 2018 and Ingress in Public Clouds
---

APIConnect 2018 and Ingress in Public Clouds 
============================================

 
When installing API Connect 2018 to any pubic cloud solution the ingress
needs to be modified to allow for SSL Pass through. The purpose of...


 
 
 


 
 


 


\


 
 
### **APIConnect 2018 and Ingress in Public Clouds** 



 



 
 


 
 
When installing API Connect 2018 to any pubic cloud solution the ingress
needs to be modified to allow for SSL Pass through. The purpose of this
series is to explain how to it for each Cloud Service.

New Public Cloud offerings will be added as I use them. If you would
like to advise on other environments please comment below.




 
 


 
 
**IBM Kubernetes Services (IKS)**


 
![](https://cdn-images-1.medium.com/max/1200/1*iuNeL_y9rFDCSle0jSJkPQ.png)


 
Edit each of the API Connect ingress files for the DataPower, Portal and
Analytics

``` 
kubectl edit ing <name> 
```

In the Metadata.Annotations add the following line.

``` 
ingress.bluemix.net/ssl-services: “ssl-service=<myservice1> [ssl-secret=<service1-ssl-secret>];ssl-service=<myservice2> [ssl-secret=<service2-ssl-secret>]”
```

Please read for more information

<https://console.bluemix.net/docs/containers/cs_annotations.html#ssl-services>





By [Chris Phillips](https://medium.com/@cminion) on
[September 7, 2018](https://medium.com/p/6b0160eaf447).

[Canonical
link](https://medium.com/series/apiconnect-2018-and-ingress-in-public-clouds-6b0160eaf447)

Exported from [Medium](https://medium.com) on April 6, 2019.
