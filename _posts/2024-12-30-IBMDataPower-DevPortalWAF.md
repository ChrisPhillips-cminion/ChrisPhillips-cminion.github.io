---
layout: post
date: 2024-12-30 10:00:00
categories: APIConnect
title: "Building a Reverse Proxy for the IBM Developer Portal with IBM DataPower"
author: [ "ChrisPhillips", "SimonKapadia" ]
draft: true
---

The IBM Developer Portal is essential for socialising your APIs to external consumers. In order to do this it must be assibsle outside of the Internal Network. We suggest that that a reverse proxy is deployed in the DMZ and that forwards requests to the Developer Portal inside the network, as opposed to have having the Developer Portal directly deployed to the DMZ.

IBM DataPower has facilities to provide this reverse proxy with its WAF capabilities.  This article will explain how to configure for a Physical, Linux or Virtal DataPower. This can be done with DataPower in Kubernetes but the configuration needs to be placed in a ConfigMap and that will be not be covered by these intrustions.



DIAGRAM  **Simon will draw a pretty picture**


A request will come into IBM DataPower and this will then be forwarded to the Developer Portal pods.  **DataPower is great beacuse simon will write some stuff here.**

<!--more-->

**Important Note:** The IBM Developer Portal site address must be correctly configured when the site is deployed in the Catalog. We do not support rewriting the site hostname in the reverse proxy. See [https://www.ibm.com/docs/en/api-connect/10.0.8?topic=deployment-firewall-requirements](https://www.ibm.com/docs/en/api-connect/10.0.8?topic=deployment-firewall-requirements)

## Assumptions
1. DataPower will use a different DNS server as the external request. When the DataPower resolves the IBM Developer Portal Site hostname it will be directed to the IBM Developer Portal instance inside the network.
2. The Developer Portal site address is not the default and does not use the default hostname.
3. TLS Certificates and Keys are available and the Identification Credential Object is already created.


## Configure the TLS Server Profiles
The TLS Client Profile is configured to handle the certifcates for receiving calls. In this example we will configure the minimum, but additional options can be enabled to add aditional security. This step
1. Log into Datapower
2. Go to the  domain that will contain your Web Application Firewall
3. Go to TLS Server Profile and click add
![TLS Server profile](/images/TLS-1.png)
4. Set following
  - Name - "Developer Portal WAF TLS Server Profile"
  - Select the Identification Credential Object as described in the Assumptions.

![TLS Server profile](/images/TLS-2.png)
5. Click Apply.

## Configure the TLS Client Profiles
The TLS Client Profile is configured to handle the certifcates for making downstream calls. In this example we will configure the minimum, but additional options can be enabled to add aditional security.
1. Log into Datapower
2. Go to the  domain that will contain your Web Application Firewall
3. Go to TLS Client Profile and click add
![TLS Client profile](/images/TLSC-1.png)
4. Set following
  - Name - "Developer Portal WAF TLS Client Profile"
  - Disable - "Validate server certificate"

![TLS Client profile](/images/TLSC-2.png)
5. Click Apply.

## Configure the Application Security Policy
The Application Security Policy **SIMON EXPLAIN WHAT THIS DOES PLEASE**
1. Log into Datapower
2. Go to the  domain that will contain your Web Application Firewall
3. Go to Application Security Policy and click Add
4. Set following in Main
  - Name - "Developer Portal WAF ASP"
5. Set following in Request Maps after clicking Add
  Create a new Matching Rule where the rule is of
  - Matching Type - URL
  - URL Match - *
  Click Apply to save the Web Request Map  
  Create a new Web Request Profile
  - Set Name to "Developer Portal WAF WRP"
  Click Apply to save the Web Request Profile  
6. Set following in Request Maps after clicking Add
  - Select the previously created Matching Rule.
  Create a new Web Response Profile
  - Set Name to "Developer Portal WAF WRespP"
  Click Apply to save the Web Response Profile  
7. Click Apply to save the Application Security Profile

## Configure the Web Application Firewall
The WAF handles the requests. WAFs have numerous configuration options which we will not cover here. This section will cover the basics to allow the WAF to function. If more advanced configuration is required please contact your local IBM Expert Labs team.
1. Log into Datapower
2. Go to the  domain that will contain your Web Application Firewall
3. Go to Web Application Firewall
4. New
5. Set the following in Main
  - Name - "Developer Portal WAF"
  - Remote Host - IBM Developer Portal hostname used when deploying the IBM Developert Portal site.
  - Remote Port - 443
  - TLS Type - Sever profile
  - TLS Server Profile - As confgured in previous section
  - TLS Client Profile - As confgured in previous section
  - Security Profile - As confgured in previous section
  - XML Manager  - Set to default
6. Set the following in Source Address, after clicking Add
  - Local IP Address - 0.0.0.0 (Please note this will allow connections from any interface and may not be desired)
  - Local Port - Desired Port to listen to requests from, often 443.
  - Enable TLS
  Click Apply to save the Source Address configuration
7. Click Apply at teh top of the screen to save the WAF
