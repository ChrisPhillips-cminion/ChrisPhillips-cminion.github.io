---
layout: post
date: 2019-09-20 01:00:00
categories: APIConnect
title: "Getting a Client ID and Secret to control the API Connect Management REST Interface"  
author: ["ChrisPhillips","JPSchiller"]
---

When using the API Connect REST interface  you need to identify yourself with a bearer token. We produced a [guide on how to get this bearer token a few days ago](https://chrisphillips-cminion.github.io/apiconnect/2019/09/18/GettingoAuthTokenFromAPIC.html. However a common question is how do you get the ClientID and ClientSecret required,

<!--more-->

For each application you have invoking the REST interface for the API Manager should have its own Client ID and Secret.

_Note: This is the REST interface to drive APIConnect not to interact to control the API Manager no the APIs hosted on it._

First of all you need to produce the registration document

```yaml
type: registration
api_version: 2.0.0
name: consumingapplication
client_type: toolkit
title: This is demo application for consuming the API Manager Public APIs
client_id: clientID
client_secret: clientPassword
scopes:
  - 'org:view'
  - 'org:manage'
  - 'published-product:view'
  - 'app:view'
  - 'app:manage'
  - 'app-analytics:view'
  - 'my:view'
  - 'my:manage'
```

Please update the client_id and client_secret with your desired value

After logging into the Cloud Manager (nto API Manager) with the apic tool, the following command is run
```
    apic registrations:create  -s <ServerHost> <path registration document>
```
This returns the following
```
    consumingapplication    [state: enabled]   https://localhost:2000/api/cloud/registrations/bbc547ee-6d8f-4bfa-83f4-907894a6cb57   
```
To test this we run the following payload in the command below

```json
{
  "username": "<username>",
  "password": "<password>",
  "realm": "admin/default-idp-1",
  "client_id": "clientID",
  "client_secret": "clientPassword",
  "grant_type": "password"
}
```

```bash
curl  -k -X POST -d '<PAYLOAD>' -H 'Content-Type: application/json' -H 'Accept: application/json' https://localhost:2000/api/token
```
