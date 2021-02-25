---
layout: post
categories: APIConnect
date: 2021-02-25 00:14:00
title: API Connect Reserve Instance - configure IAM
draft: true
---

More and more people are signing up to IBM API Connect Reserve Instance. IBM API Connect Reserve Instance allows you to have all the benefits of API Connect while IBM Manages the invite so you can just bring your developers and publish APIs. Also you can bring in additional Gateway Services from a different location or from your Data Center to be managed by API Connect in RI.

One of the common questions I am asked is how do we configure complex  user topologies to allow only subsets of users to each role.
<!--more-->

*Thanks to [https://www.linkedin.com/in/rickymoorhouse/](Ricky Moorhouse) for his help and support putting this together*

In IAM you need to configure two things

* A role - collection of permissions
* Access Group  - collection of users

You then apply the role to the access group and specify which RI provider org is for.

### Create a role
To create a role, login into [https://cloud.ibm.com/iam/roles](https://cloud.ibm.com/iam/roles)

![/images/2021-02-25-iam1.JPG](/images/2021-02-25-iam1.JPG)

Click on Create

* Enter a Name, ID and Description
* Select `API Connect` from the service.
* Select the permissions you wish to assgin to the role.   

![/images/2021-02-25-iam2.JPG](/images/2021-02-25-iam2.JPG)

Today the only granularity we allow is the role level, not individual permissions.

Click on Create

### Create an Access Group
To create a group, login into  [https://cloud.ibm.com/iam/groups](https://cloud.ibm.com/iam/groups)

Click on create

* Enter a name and Description and press create
* Click on Add Users to add users to the group
![/images/2021-02-25-iam3.JPG](/images/2021-02-25-iam3.JPG)

### Bind a role an Access Group for specific  API Connect Provide Org
To create a group, login into  [https://cloud.ibm.com/iam/groups](https://cloud.ibm.com/iam/groups)

* Click on the group you want to associate with a role
* Click on `Access policies`
* Click on `Assign access`

The roles you have created will appear under `Custom access` at the bottom of the list
![/images/  2021-02-25-iam4.JPG](/images/2021-02-25-iam4.JPG)

To select which Provider Org to apply this to,  click on `Service based on attributes` and click on  `Service Instance` then from the drop down select the Provider Org you want this to be applied to.

Click on `Add`
