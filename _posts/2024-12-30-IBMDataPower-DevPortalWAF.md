---
layout: post
date: 2024-12-30 10:00:00
categories: APIConnect
title: "Building a Reverse Proxy for the IBM Developer Portal with IBM DataPower"
author: [ "ChrisPhillips", "SimonKapadia" ]
draft: true
---

The IBM Developer Portal is essential for socialising your APIs to external consumers. In order to do this it must be accessible outside of your Internal Network. It is not good practice to deploy the Developer Portal directly in your DMZ and grant users direct access. The De-Militarised Zone (DMZ) is designed to be a hostile, barren place for attackers; software deployed there should have minimal function, deployed on a hardened platform, and be designed for DMZ deployment. With this in mind, we suggest that that a reverse proxy should be deployed in your DMZ, which forwards requests to the Developer Portal, and the Developer Portal should in turn be deployed in a separate secure zone designed for servers (not directly on your internal lan!). One option for a reverse proxy implementation would be to use IBM DataPower, which has facilities to provide a reverse proxy within its WAF capabilities. This article will explain how to configure a WAF as a Reverse Proxy for the Developer Portal on a Physical, Linux-based or Virtual DataPower. This can also be done with DataPower in Kubernetes but the configuration needs to be placed in a ConfigMap and that will be not be covered by these instructions.

**IMPORTANT NOTE:** Any reverse proxy placed in front of the Developer Portal must be completely transparent to the Developer Portal. We do not support any modification of the portal URL, port, hostname or path in the reverse proxy, as per the documentation. See [https://www.ibm.com/docs/en/api-connect/10.0.8?topic=deployment-firewall-requirements](https://www.ibm.com/docs/en/api-connect/10.0.8?topic=deployment-firewall-requirements)

**DataPower is great because simon will write some stuff here.**
There are many reasons why you may choose to implement your reverse proxy in DataPower. Link to some docs and stuff.

DIAGRAM  **Simon will draw a pretty picture**

A request will come into IBM DataPower and this will then be forwarded to the Developer Portal pods.  

<!--more-->

**Important Note:** The IBM Developer Portal site address must be correctly configured when the site is deployed in the Catalog. As mentioned above, we do not support rewriting the site hostname in the reverse proxy, so the site address configured in the Portal must exactly match (be identical to) the address entered in the browser. What this means is that you cannot have an "internal Portal URL" and an "external Portal URL" for the Portal instance. There is one Portal URL and it is the same everywhere. In practice, for this to work, DataPower has to resolve the site hostname to the IP of the actual Portal server, but clients must resolve the hostname to the external IP being served by DataPower.

Here's how to set it up:

## Assumptions
1. DataPower will use a different DNS server as the external request. When the DataPower resolves the IBM Developer Portal Site hostname it will be directed to the IBM Developer Portal instance inside the network.
2. The Developer Portal site address is not the default and does not use the default hostname.
3. TLS Certificates and Keys are available and the Identification Credential Object is already created.

## Configure the TLS Server Profiles
The TLS Client Profile is configured to handle the certificates for receiving calls. In this example we will configure the minimum, but additional options can be enabled to add additional security. This step
1. Log into DataPower
2. Go to the  domain that will contain your Web Application Firewall
3. Go to TLS Server Profile and click add
![TLS Server profile](/images/TLS-1.png)
4. Set the following
  - Name - "Developer Portal WAF TLS Server Profile"
  - Select the Identification Credential Object (already created, as described in the Assumptions).
![TLS Server profile](/images/TLS-2.png)
5. Click Apply.

## Configure the TLS Client Profiles
The TLS Client Profile is configured to handle the certificates for making downstream calls. In this example we will configure the minimum, but additional options can be enabled to add additional security.
1. Log into DataPower
2. Go to the  domain that will contain your Web Application Firewall
3. Go to TLS Client Profile and click add
![TLS Client profile](/images/TLSC-1.png)
4. Set the following
  - Name - "Developer Portal WAF TLS Client Profile"
  - Disable - "Validate server certificate" (note: do NOT disable this in a real world scenario!)
![TLS Client profile](/images/TLSC-2.png)
5. Click Apply.

## Configure the Application Security Policy
The Application Security Policy configures how the DataPower WAF should handle incoming requests. For the Developer Portal, we must simply pass through all requests unmodified, so we are going to create a policy which does that. However, this would be a good place to e.g. block specific known bad URL patterns, perform further verification of requests, send payloads to an ICAP server, etc.
1. Log into DataPower
2. Go to the  domain that will contain your Web Application Firewall
3. Go to Application Security Policy and click Add
4. Set the following in Main
  - Name - "Developer Portal WAF ASP"
5. Set the following in Request Maps after clicking Add
![ASP](/images/asp-1.png)
  Create a new Matching Rule where the rule is of
  - Matching Type - URL
  - URL Match - *
![ASP](/images/asp-2.png)
  Click Apply to save the Web Request Map  
  Create a new Web Request Profile
  - Set Name to "Developer Portal WAF WRP"
  Click Apply to save the Web Request Profile  
6. Set the following in Response Maps after clicking Add
  - Select the previously created Matching Rule.
  Create a new Web Response Profile
  - Set Name to "Developer Portal WAF WRespP"
  Click Apply to save the Web Response Profile  
7. Click Apply to save the Application Security Profile

## Configure the Web Application Firewall
The WAF handles the requests. WAFs have numerous configuration options which we will not cover here. This section will cover the basics to allow the WAF to function. If more advanced configuration is required please contact your local IBM Expert Labs team.
1. Log into DataPower
2. Go to the  domain that will contain your Web Application Firewall
3. Go to Web Application Firewall
4. New
5. Set the following in Main
![WAF](/images/waf-1.png)
  - Name - "Developer Portal WAF"
  - Remote Host - IBM Developer Portal hostname used when deploying the IBM Developer Portal site.
  - Remote Port - 443
  - TLS Type - Sever profile
  - TLS Server Profile - As configured in previous section
  - TLS Client Profile - As configured in previous section
  - Security Profile - As configured in previous section
  - XML Manager  - Set to default
6. Set the following in Source Address, after clicking Add
![WAF](/images/waf-2.png)
  - Local IP Address - 0.0.0.0 (Please note this will allow connections from any interface and may not be desired)
  - Local Port - Desired Port to listen to requests from, often 443.
  - Enable TLS
  Click Apply to save the Source Address configuration
7. Click Apply at the top of the screen to save the WAF
