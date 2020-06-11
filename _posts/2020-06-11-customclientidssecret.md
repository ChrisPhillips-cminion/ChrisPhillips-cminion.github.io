---
layout: post
date: 2020-6-11 00:01:00
categories: APIConnect
title: "Custom Client ID and Client Secret values"
---

From API Connect V5 and onwards users have been able to customise the Client ID and Client Secret values on applications. But this is a rarely known gem.  This article will explains the API calls required to do this.

<!--more-->


In order to use custom Client ID and Secrets the following API calls need to be done.

1. Log into to the provider or consumer realm to get the TOKEN

2. Create the application payload
*Note redirect_endpoints and  application_public_certificate_entry are optional*
```json
{
  "type": "app",
  "api_version": "2.0.0",
  "name": "tate",
  "title": "tesid",
  "summary": "Lu babahjo ufatap lih fargisso imsih porkumhaw mumadmuh votupoafa pec kudiri huibwud puuc fahenol ari mov.",
  "client_id": "836505056575488",
  "client_secret": "hopi",
  "redirect_endpoints": [
    "http://hinkidun.lt/kitawuja"
  ],
  "application_public_certificate_entry": "-----BEGIN CERTIFICATE-----xxxEXAMPLExxxxxxxxxEXAMPLExxxxxxxxxxEXAMPLExxxxxxxxxxEXAMPLExxxxxxxEXAMPLExxxxxxxxxEXAMPLExxxxxxxxxxEXAMPLExxxxxxxxxxEXAMPLExxxxxxxEXAMPLExxxxxxxxxEXAMPLExxxxxxxxxxEXAMPLExxxxxxxxxxEXAMPLExxxxxxxEXAMPLExxxxxxxxxEXAMPLExxxxxxxxxxEXAMPLExxxxxxxxxxEXAMPLExxxx-----END CERTIFICATE-----"
}
```

3. Create  the Application
```shell
curl --request POST \
  --url https://<API MANGER API ENDPOINT>/api/consumer-orgs/<PROVIDER ORG>/<CATALOG>/<CONSUMER ORG>/apps \
  --header 'accept: application/json' \
  --header 'content-type: application/json' \
-H 'Authorization: Bearer <TOKEN FROM STEP 1>' \
  --data '<PAYLOAD FROM STEP 2>'
```

This will return something similar to the below
```json
{
    "type": "app",
    "api_version": "2.0.0",
    "id": "c7cfde02-7d37-48e5-bffe-784b6b38c045",
    "name": "tate",
    "title": "tesid",
    "summary": "Lu babahjo ufatap lih fargisso imsih porkumhaw mumadmuh votupoafa pec kudiri huibwud puuc fahenol ari mov.",
    "state": "enabled",
    "lifecycle_state": "production",
    "lifecycle_state_pending": "production",
    "redirect_endpoints": [
        "http://hinkidun.lt/kitawuja"
    ],
    "application_public_certificate_entry": "-----BEGIN CERTIFICATE-----xxxEXAMPLExxxxxxxxxEXAMPLExxxxxxxxxxEXAMPLExxxxxxxxxxEXAMPLExxxxxxxEXAMPLExxxxxxxxxEXAMPLExxxxxxxxxxEXAMPLExxxxxxxxxxEXAMPLExxxxxxxEXAMPLExxxxxxxxxEXAMPLExxxxxxxxxxEXAMPLExxxxxxxxxxEXAMPLExxxxxxxEXAMPLExxxxxxxxxEXAMPLExxxxxxxxxxEXAMPLExxxxxxxxxxEXAMPLExxxx-----END CERTIFICATE-----",
    "image_endpoint": "http://gunnoka.ag/se",
    "application_type_url": "https://apim.ibmcp4i.com/isratco",
    "task_urls": [
        "https://apim.ibmcp4i.com/ade"
    ],
    "created_at": "2020-06-11T09:35:48.015Z",
    "updated_at": "2020-06-11T09:35:48.015Z",
    "org_url": "https://apim.ibmcp4i.com/api/orgs/26abb389-bc29-450d-921e-971c91306d05",
    "catalog_url": "https://apim.ibmcp4i.com/api/catalogs/26abb389-bc29-450d-921e-971c91306d05/e51f536f-c9b1-48a1-a46b-9dcd581558c6",
    "consumer_org_url": "https://apim.ibmcp4i.com/api/consumer-orgs/26abb389-bc29-450d-921e-971c91306d05/e51f536f-c9b1-48a1-a46b-9dcd581558c6/71893d8d-c22b-44ab-82be-e46df0e8de38",
    "url": "https://apim.ibmcp4i.com/api/apps/26abb389-bc29-450d-921e-971c91306d05/e51f536f-c9b1-48a1-a46b-9dcd581558c6/71893d8d-c22b-44ab-82be-e46df0e8de38/c7cfde02-7d37-48e5-bffe-784b6b38c045",
    "app_credential_urls": [
        "https://apim.ibmcp4i.com/api/apps/26abb389-bc29-450d-921e-971c91306d05/e51f536f-c9b1-48a1-a46b-9dcd581558c6/71893d8d-c22b-44ab-82be-e46df0e8de38/c7cfde02-7d37-48e5-bffe-784b6b38c045/credentials/af22ce87-3d80-4e1b-9bff-b9e3e09dcd3f"
    ],
    "client_secret": "hopi",
    "client_id": "836505056575488"
}
```
