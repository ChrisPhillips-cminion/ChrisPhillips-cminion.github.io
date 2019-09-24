---
layout: post
date: 2019-09-23 06:00:00
categories: APIConnect
title: "Developing APIs - 102 - Adding Parameters"
Location: "Paris, France"
draft: true
---
Part of One of the API Development Series. In this part we will show how to specify parameters for an API call. This builds on from the artefact and knowledge created in (part 1.)[/apiconnect/2019/09/23/APIDevelopment-101.html]

<!--more-->

1. Go to the API that was created in part 1.

2. Go to the Design View

3. Click on Paths

4. Click on `/`

5. Click on GET

6. Fill in the parameters
**Summary** - Operations Returns the account balance for a given Account ID
**Tags** - balance
**Description** - To consume this API you must pass on the account id

6. Click on Add Parameters

7. Fill in the parameters
**Name** - uid
**Located In** - query
**Type** - String
**Description** - The Account ID to be queried

8. Press Save  

9. Click on Properties

10. Click on the Hot Dog Menu next to target url and select edit

11. The query parameter must be removed and replaced with the variable we defined in the parameter in step 7.  Change default value to `http://apic-test-app.eu-gb.mybluemix.net/api/balance?id={uid}`

12. Press Save


13. Test the API as we detailed in (Part 1.)[/apiconnect/2019/09/23/APIDevelopment-101.html]
