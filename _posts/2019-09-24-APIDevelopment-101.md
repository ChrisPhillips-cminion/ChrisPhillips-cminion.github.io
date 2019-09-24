---
layout: post
date: 2019-09-23 06:00:00
categories: APIConnect
title: "Developing APIs - 101 - Proxy a Rest Service"
Location: "Paris, France"
draft: true
---

 Part of One of the API Development Series.  In this part we will show screenshot by screenshot how to create a very basic API.

<!--more-->

**Requirements**

-   API Connect Manager or the API Designer with the API Connect Local Test Environment up and running.  
-   Access to the internet from your DataPower or API Connect Local Test Environment

-   Sample URLs (If the first URL is no longer available please use the second)
    -   <http://apic-test-app.eu-gb.mybluemix.net/api/balance?id=1001>  (Created by Ben Cornwell)
    -   <https://httpbin.org/anything?id=100>

### Steps

1.  Goto the API Drafts by clicking on this button after logging into the API Manager.  
    ![](/images/2019-09-24-APIDevelopment-101-1.png){:height="400px" }

2.  Click on Add -> API
    ![](/images/2019-09-24-APIDevelopment-101-2.png){:height="400px" }{:height="200px" }

3.  Click on Next
    ![](/images/2019-09-24-APIDevelopment-101-3.png){:height="400px" }{:height="400px" }

4.  Set the following parameters
    <BR>![](/images/2019-09-24-APIDevelopment-101-4.png){:height="400px" }{:height="400px" }
  <br>**Title** Get Balance
  <br>**Description** This API returns the Balance for a given account id
  <br>**Target Service URL**  http://apic-test-app.eu-gb.mybluemix.net/api/balance?id=1001

5.  Click on Next

6.  We are going to start with the default security options. Click on Next
    ![](/images/2019-09-24-APIDevelopment-101-5.png){:height="400px"}

7.  Click on Edit API
    ![](/images/2019-09-24-APIDevelopment-101-6.png){:height="400px"}

8.  The API is now created and we need to publish it.
  <br>a. If you are in the API Designer Press this button ![](/images/publishButton.png){:height="100px"}
  <br>   b. If you are in the API Manager Web Interface
      <br>   i. Goto Assembly.
      <br>   ii. Click on the Play button
      <br>   iii. Click Activate API

9.  Testing the API
    <br>a. If you are in the API Designer, follow the instructions on this page to Test the API. <https://chrisphillips-cminion.github.io/apiconnect/2019/09/21/APIConnect-LTE.html>
  <br>b. If you are in the API Manager Web Interface
      <br>i. Scroll Down and click on to Invoke

10. You will see a response similar to

```json
{"balance":998155}
```
