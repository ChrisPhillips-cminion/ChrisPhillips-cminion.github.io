---
layout: post
date: 2020-6-10 00:01:00
categories: APIConnect
title: "Calling DataPower's Rest interface from API Connect"
author: ["lfanebost"]
draft: true
---
Lars Fanebost put together this awesome guide on calling DB2 from inside of API connect. This is taken from [https://github.com/lfanebost/api-connect-exposing-db-data-pub/](https://github.com/lfanebost/api-connect-exposing-db-data-pub/)

<!--more-->

Learn by example how to expose DB2 Database data in a interaction api with IBM API Connect (v2018 or newer). Input is userid + password. And a SQL Statement (e.g. select * from tst.persons). Data returned will be a nice JSON.

## Prerequisites

The asset has been developed and tested on API Connect version 2018. So you need a working installation of API Connect with access to Designer. Do NOT implement this asset on version 5 (v5) or even older versions of API Connect. Well, you can try, but I have never tested it so I dont know if it will work. And I have no plans for testing it on older versions.

I created a DB2 Service on IBM Cloud. From DB2 Console I created a database and a simple table for testing that it is working. Feel free to use any table of your choice. I used a table with two columns. You can actually send any SQL Statement you want as long as it is compliant with DB2s SQL syntax. You can create data, update data, delete data and select (retrieve data).


You need the service credentials for your db2 instance. See my screenshot attached: db2_service_credentials_where_to_find.png. To understand how DB2 REST APIs are working, here's the documentation: https://cloud.ibm.com/apidocs/db2-on-cloud

## Installation

Create a API in your API Designer. You can Create the API from existing OpenApi Service. Use the YAML file in this git repo.

Or

Create a API in your API Designer. I named mine DB2-GetToken-SendSQL-GetResult. Also I created a project that uses the API. I named it DB2-GetToken-SendSQL-GetResult - exactly the same as the API.

Once the API is created you will be standing in the editor. First, look at the attached file "assembly.png" to see how the Assembly will look like once the yaml file has been imported.

Copy the yaml file into your recently created API. You can do that by opening the attached YAML file and mark+copy all text in the JSON. Then open the source code for you API and simply relace it. Don't forget to hit "Save". Now you should study each policy in the API. Some adjustments are needed to be done to get it working in your own environment.


### Update the following

- The URL in the Invoke named "Get token". You need to look at your service credential and update with your URL, and add /dbapi/v4/auth/tokens at the end. For example, here is mine:
        https://dashdb-txn-flex-yp-fra02-386.services.eu-de.bluemix.net/dbapi/v4/auth/tokens

- The URL in the GatewayScript named "Send SQL". You need to look at your service credential and update with your URL, and add /dbapi/v4/sql_jobs at the end. For example, here is mine:
	var options = {
    		target: 'https://dashdb-txn-flex-yp-fra02-386.services.eu-de.bluemix.net/dbapi/v4/sql_jobs',

- The URL in the GatewayScript named "get result". You need to look at your service credential and update with your URL, and add /dbapi/v4/sql_jobs at the end. For example, here is mine:
	var options = {
    		target: 'https://dashdb-txn-flex-yp-fra02-386.services.eu-de.bluemix.net/dbapi/v4/sql_jobs/'

- The URL in the GatewayScript named "retry get result if needed". Exactly the same way as you did with "get result". This GatewayScript is the assemblys second attempt to retrive
data if DB2 returns a status="running" the first time the assembly tried to get the result. Some SQL might be "heavy" to process, and since DB2 REST APIs are Async by nature, you cannot
be guaranteed DB2 have enought time to process your SQLs in a couple of seconds (instead DB2 returns status="running") meaning that you must wait a litte and try again.... And that is why you have this GatewayScript names "retry get result if needed".

All inside the "Catch" are subject to your review and evt update. See the attached file assembly.png.

### Logging
In the GatewayScript you'll see several "console.alert". Those result in log entries in the DataPower Gateway Log that you should have open when you run the API.

## Use the asset

You can run the asset from inside the Assembly Designer editor. Click the "run" button and and republish the product. Once done, scroll down and select the "post" api operation. Scroll further down and in "uidpw" you fill in DB2 userID and password. Note that it has to be in JSON format (as in your service credentials). Here is an example with mine: {"userid":"bluadmin", "password":"OTgxM2Y45TA4ZmWk"} And below that you have to fill in your SQL Statement. As an example I used: select * from lf.post;   (dont forget the semicolon at the end).

## Next step for this asset

The asset was written using API Connect V2018. As soon as I have access to 2020.1 (or later) I will continue to update the asset and come up with whatever is needed to get it "upgraded".
