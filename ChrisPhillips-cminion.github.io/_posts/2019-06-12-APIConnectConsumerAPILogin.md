---
layout: post
date: 2019-06-12 1:00:00
categories: APIConnect
title: 'API Connect - Getting the Access token for the Consumer API'
---

*Thanks to Reinhard Heite and Ollie Dineen*

API Connect has two different APIs, the provider API and the consumer API.

The provider API is used to control artefacts from the perspective of the API Provider. The consumer API is used to control artefacts belonging to the developers consuming the APIs.

<!--more-->
To get the access token to call additional systems I use the following curl command.


```
curl -X POST \
  https://<consumer api endpoint>/consumer-api/token \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'X-IBM-Consumer-Context: <provider org name or ID>.<catalog name or id>' \
  -d '{
"realm": "consumer:<provider org name or ID>:<catalog name or id>/<identity provider>",
"username": "<user>",
"password": "<password>",
"client_id": "819a8de7-7204-4adb-918f-391ba39d29d0",
"client_secret": "8dad5699-acbf-40ab-85c1-48361981bc75",
"grant_type": "password"
}'  -kv

```

| **Variable** | **Description** | **Example** |
|--------------|-----------------|-------------|
| consumer api endpoint | The endpoint specified at deploy time for exposign the consumer API | `connsumer.apihost.com` |
| provider org name or id | The name or the uuid for the provider org | `dev` |
| catalog name or id | The name or the uuid for the catalog | `internal` |
| identity provider | The identity provider for the user registry being used | `sandbox-idp` |
| user | The username used to log in | `bob`|
| password | The password for the user  | `password` |
