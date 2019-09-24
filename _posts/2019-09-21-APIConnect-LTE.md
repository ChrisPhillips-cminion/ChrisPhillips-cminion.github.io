---
layout: post
date: 2019-09-21 02:00:00
categories: APIConnect
title: "API Connect Local Test Environment"
draft: true
Location: "Tunis Airport, Tunisia"
---

API Connect Local Test Environment was releaed in beta in August 2019.

The purpose of the Local Test Environment is to allow developers to build and test APIs on their laptops without depending on a server instance.

<!--more-->


### The Components

LTE requires the API Connect Designer and Docker running locally on the laptop. Set the memory of docker to be at least 6GB.

LTE requries a number of docker containers running together. *Please note it does not require Kubernetes*

### Installing the Local Test environment

Download the binary from IBM Passport Advantage or IBM Fix Central. The video below will explain how to install the LTE components.


[![asciicast](https://asciinema.org/a/267155
.svg)](https://asciinema.org/a/267155
)


### Connecting the API Connect Designer to LTE

* Load the API Connect Designer
* Select a directory to save the YAML files
* Connect to a new cloud server with the following credentials
  - Server https://localhost:2000
* Log in with
  - Username Shavon
  - Password 7iron-hide

You can now create an API in the designer

### Publishing an API to LTE

Once you have created an API click on the publication button in the header of the API Designer.


![](images/publishButton.png)



### Testing an API

Go to a terminal window and run `apic-lte status`. This will return similar to the output below.

```bash
>>$ apic-lte status

Container                       Status
---------                       ------
apic-lte-apim                   Up 4 days
apic-lte-datapower-gateway      Not Running
apic-lte-datapower-api-gateway  Up 4 days
apic-lte-db                     Up 4 days
apic-lte-juhu                   Up 4 days
apic-lte-lur                    Up 4 days

- Platform API url: https://localhost:2000
- Admin user: username=admin, password=7iron-hide
- 'localtest' org owner: username=shavon, password=7iron-hide
- 'localtest' org sandbox test app credentials client id: 5012407a4dfc0552d2808f86110c969d , client secret: 4801972213b8b28ebb4b7d7c3fcaaff9
- Datapower API Gateway API base url: https://localhost:9444/localtest/sandbox/
```

Here you can see the target context route of the endpoint, and the client ID and Secret if required.

You can invoke the API from any HTTP test tool, such as API Connect Test and Monitor, curl or Postman.


[![asciicast](https://asciinema.org/a/270133
.svg)](https://asciinema.org/a/270133
)
