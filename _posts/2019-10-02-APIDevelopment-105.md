---
layout: post
date: 2019-10-02 06:00:00
categories: APIConnect
title: "Developing APIs - 105 - Avoiding losing Plans and Subscriptions"
Location: "Paris, France"
draft: true
author: ["NickCawood"]
---

Avoiding losing Plans and Subscriptions of Published APIs when Updating an API: Staging a Product

<!--more-->

*Steps*

1.	In the Developer Portal view the Subscription to the Product containing the API via the App
<br>![](/images/2019-10-03-105-1.png)

2.	Goto API Manager and login, and go to the Provider Organization containing the API

3.	Goto Develop
<br>![](/images/2019-10-03-105-2.png)

4.	Edit the API and save it as v2 (or overwrite v1 of the API)
<br>![](/images/2019-10-03-105-3.png)

5.	Click on the “3 dots” next to v2 of the API
<br>![](/images/2019-10-03-105-4.png)

6.	Click Stage, then select New Product, name it and click Next (the same Product name can be used, by setting a new version, if preferred)
<br>![](/images/2019-10-03-105-5.png)

7.	Select the Catalog and click Stage
<br>![](/images/2019-10-03-105-6.png)<br>The above process is covered in Knowledge Center here:<br><BR>[https://www.ibm.com/support/knowledgecenter/SSMNED_2018/com.ibm.apic.toolkit.doc/task_deploy_api_offline.html](https://www.ibm.com/support/knowledgecenter/SSMNED_2018/com.ibm.apic.toolkit.doc/task_deploy_api_offline.html)<BR><BR>And the Product Lifecyle here:<BR><BR>[https://www.ibm.com/support/knowledgecenter/SSMNED_2018/com.ibm.apic.apionprem.doc/capim_product_lifecycle.html](https://www.ibm.com/support/knowledgecenter/SSMNED_2018/com.ibm.apic.apionprem.doc/capim_product_lifecycle.html)

8.	Goto Manage and select the Catalog
<br>![](/images/2019-10-03-105-7.png)<BR>The new Product “New Product” is set to “staged”

9.	Goto the “3 dots” next to the already published Product
<br>![](/images/2019-10-03-105-8.png)

10.	Select Replace
<br>![](/images/2019-10-03-105-9.png)

11.	Select the “New Product” Product and click Next

12.	Choose the “Plans” (and associated Subscriptions) to migrate
<br>![](/images/2019-10-03-105-10.png)

13.	Click Replace
<br>![](/images/2019-10-03-105-11.png)<BR>The new Product “New Product” is now published and all the Plans / Subscriptions from the old Product are migrated to the new product

14.	 In the Developer Portal view the Subscription to the Product containing the API via the App
<br>![](/images/2019-10-03-105-12.png)

**Knowledge Center links for Replace (and Supersede):**
* [https://www.ibm.com/support/knowledgecenter/SSMNED_2018/com.ibm.apic.apionprem.doc/task_replacing_a_product.html](https://www.ibm.com/support/knowledgecenter/SSMNED_2018/com.ibm.apic.apionprem.doc/task_replacing_a_product.html)

* [https://www.ibm.com/support/knowledgecenter/SSMNED_2018/com.ibm.apic.apionprem.doc/task_superseding_a_product.html
](https://www.ibm.com/support/knowledgecenter/SSMNED_2018/com.ibm.apic.apionprem.doc/task_superseding_a_product.html)
