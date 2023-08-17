---
layout: post
date: 2023-08-14 01:00:00
categories: APIConnect
title: "API Connect - Rest call to retrieve APIs."
---


API Connect has two Rest Interfaces, one for consumer users the other for provider users. This article will go through how to retrieve applications with the provider (platform) api.

<!--more-->

## APIConnect

## Step 1 - Get an accesstoken
See [https://chrisphillips-cminion.github.io/apiconnect/2019/09/18/GettingoAuthTokenFromAPIC.html
](https://chrisphillips-cminion.github.io/apiconnect/2019/09/18/GettingoAuthTokenFromAPIC.html)

## Step 2 - Remove the Gateway Service from the Catalogs or Spaces
Invoke the following URL with a get  `https://<Platform-API>/api/catalogs/<ProviderOrg>/<CatalogID>/apps?fields=consumer_org,credentials,updated_at&expand=credentials,consumer_org`

e.g.
  `https://small-mgmt-api-manager-apiconnect.mycluster-lon06-m3c-8x64-420eb34f056ae68f3969289d61f61851-0000.eu-gb.containers.appdomain.cloud/api/catalogs/75698862-39ed-45ef-9b52-c10742b8ea08/3567f397-af1e-493e-b5d0-bcc319c77a58/apps?limit=1000&offset=0&fields=consumer_org,credentials,id,lifecycle_state,lifecycle_state_pending,name,state,title,updated_at,url&expand=credentials,consumer_org`

  This will return a payload similar to the below

```json
  {
    "total_results": 2,
    "results": [
        {
            "consumer_org": {
                "id": "9ade68ed-da48-46bf-905f-3b4ec87e0111",
                "title": "libby",
                "name": "libby",
            },
            "credentials": [
                {
                    "id": "ce832228-4114-452c-a161-0c608ae3312d",
                    "name": "Credential-for-test",
                    "title": "Credential for test",
                    "client_id": "0d85e77e32a663cbfebe9c964024723c"
                }
            ],
            "updated_at": "2023-08-17T16:48:34.000Z"
        },
        {
            "consumer_org": {
                "id": "9b66615d-10c6-4238-916a-12545a947f04",
                "title": "Sandbox Test Organization",
                "name": "sandbox-test-org",

            },
            "credentials": [
                {
                    "id": "bc3b99f8-3635-4288-84d0-409733988f24",
                    "name": "sandbox-test-app-credentials",
                    "title": "Sandbox Test App Credentials",
                    "client_id": "9b0b9df5822bd33145c1e36b12cbdce4"
                }
            ],
            "updated_at": "2023-07-19T16:26:20.000Z"
        }
    ]
}
```
