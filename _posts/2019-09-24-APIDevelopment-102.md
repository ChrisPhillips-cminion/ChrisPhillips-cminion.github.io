---
layout: post
date: 2019-09-24 06:00:00
categories: APIConnect
title: "Developing APIs - 102 - Adding Parameters"
Location: "Paris, France"
draft: true
---
Part of One of the API Development Series. In this part we will show how to specify parameters for an API call. This builds on from the artefact and knowledge created in [part 1.](/apiconnect/2019/09/23/APIDevelopment-101.html)

<!--more-->

1. Go to the API that was created in part 1.

2. Go to the Design View
<br>![](/images/2019-09-24-APIDevelopment-102-1.png){:height="100px" }

3. Click on Paths
<br>![](/images/2019-09-24-APIDevelopment-102-2.png){:height="400px" }

4. Click on `/`
<br>![](/images/2019-09-24-APIDevelopment-102-3.png){:height="200px" }

5. Click on GET
<br>![](/images/2019-09-24-APIDevelopment-102-4.png){:height="200px" }

6. Fill in the parameters
<br>**Summary** - Operations Returns the account balance for a given Account ID
<br>**Tags** - balance
<br>**Description** - To consume this API you must pass on the account id

6. Click on Add Parameters
<br>![](/images/2019-09-24-APIDevelopment-102-5.png){:height="100px" }

7. Fill in the parameters
**Name** - uid
**Located In** - query
**Type** - String
**Description** - The Account ID to be queried
<br>![](/images/2019-09-24-APIDevelopment-102-6.png){:height="100px" }

8. Press Save  

9. Click on Properties
<br>![](/images/2019-09-24-APIDevelopment-102-7.png){:height="400px" }

10. Click on the Hot Dog Menu next to target url and select edit
<br>![](/images/2019-09-24-APIDevelopment-102-8.png){:height="100px" }


11. The query parameter must be removed and replaced with the variable we defined in the parameter in step 7.  Change default value to `http://apic-test-app.eu-gb.mybluemix.net/api/balance?id={uid}`

12. Press Save

13. Republish and test the API as we detailed in [part 1.](/apiconnect/2019/09/23/APIDevelopment-101.html). If you are using the API Designer ensure you add the paremeter `?uid=1001` or `?uid=1002` at the end of the url you are invoking. If you are using the API Manager you will need specify the parameter in the test form.
