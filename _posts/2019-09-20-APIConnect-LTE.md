---
layout: post
date: 2019-09-20 01:00:00
categories: APIConnect
title: "API Connect Local Test Environment"
draft: true
Location: "Tunis Airport, Tunisia"
---

API Connect Local Test Environment was releaed in Beta in August 2019.

The purpose of the Local Test Environment was to allow developers to build and test APIs on their laptop and not have to depend on server instance.

<!--more-->


### The Components

LTE requires the API Connect Designer and docker running localling on the Laptop. Please set the memory of docker to be atleast 6GB.

LTE requries a number of docker containers running together. *Please note it does not require Kuebrnetes*

### Installing the Local Test environment

Download the binary from PassPort Advantage or fix Central. The video below will explain how to install the LTE components.

ASCII Cinema Video


### Connecting the API Connect Designer to LTE

* Load the API Connect Designer,
* Select a directory to save the YAML files.
* Connect to a new cloud server with the following credentials
  - Server https://localhost:2000
* Login with
  - Username Shavon
  - Password 7iron-hide

You can now create an API in the designer

VIDEO

### Publishing an API to LTE

Once you have created an API you must click on the publication button in the header of hte API Designer.

SCREEN SHOT

### Testing an API

Co to a terminal window and run `apic-lte status`. This will return an output similar to the below.

```
output
```

Here you can see the target context route endpoint and the cliend ID and Secret if it is required.

You can invoke the API from any tool like API Connect Test and Monitor, Curl or Postman.

ASCI CINEMA
