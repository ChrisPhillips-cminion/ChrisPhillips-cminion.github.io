---
layout: post
date: 2019-09-18 01:00:00
categories: API Connect
title: "Getting an OAuth Token to invoke the API Connect Rest interface"  
author: ["ChrisPhillips","sachinkj"]
---
When using the API Connect REST interface  you need to identify yourself with a bearer token. This guide quickly walks through the commands needed.


<!--more-->


### What do you needed
In order to get an access token you require the realm (identity provider) and a set of user credentials with the required permissions. This article assumes that you have a user with the correct permissions.



### Getting the realm (Identity Provider)

In order to programatically get the realm you need to do a GET on `/api/cloud/provider/identity-providers` or `/api/cloud/admin/identity-providers`. If you are wanting to run operations on the Cloud Manager you need use `admin` if you want to use the API Manager use `provider`.

*Curl Sample to get the provider Realms*

```bash
curl -k -H "Accept: application/json" https://<APIMHOST>/api/cloud/provider/identity-providers
```
This returns something similar to the below.
```json
{
    "total_results": 1,
    "results": [
        {
            "name": "default-idp-2",
            "title": "API Manager User Registry",
            "default": true,
            "registry_type": "lur"
        }
    ]
  }
```


*Please note that this only needs to be run once as the value will not change, unless you change the user registry.*

### Getting access token

To request a token you generate the following payload.
```json
{
  "username": "<username>",
  "password": "<password>",
  "realm": "<admin/provider>/<realm>",
  "client_id": "caa87d9a-8cd7-4686-8b6e-ee2cdc5ee267",
  "client_secret": "3ecff363-7eb3-44be-9e07-6d4386c48b0b",
  "grant_type": "password"
}
````
The `username` and `password` are the credentials for the user. The realm value is made up of the `realm` name prefixed with `provider` or `admin`. The `client_id` and the `client_secret` are at this time hard coded to this value.
e.g.
```json
{
  "username": "chrisp",
  "password": "password",
  "realm": "provider/default-idp-2",
  "client_id": "caa87d9a-8cd7-4686-8b6e-ee2cdc5ee267",
  "client_secret": "3ecff363-7eb3-44be-9e07-6d4386c48b0b",
  "grant_type": "password"
}
```


This Payload is POSTed to `https://<APIMHOST>/api/token`

*Curl Sample to get the provider Realms*
```bash
curl  -k -X POST -d '{"username": "<userid>", "password": "<pwd>", "realm": "<admin/provider>/<realm>", "client_id": "599b7aef-8841-4ee2-88a0-84d49c4d6ff", "client_secret": "0ea28423-e73b-47d4-b40e-ddb45c48bb0", "grant_type": "password"}' -H 'Content-Type: application/json' -H 'Accept: application/json' https://<APIMHOST>/api/token
```

*Sample response*
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJjOTg2ZGUzOC0zYmM3LTRmZTItOGUwYy1kZWU0OWFkNjYyMmEiLCJuYW1lc3BhY2UiOiJmNDFhNTM5ZS1hNzIxLTRlN2MtYTA4Yi05NWZkMzRkZDJjN2I6YzIwYWNhOWMtYjEwNS00MGQ4LThmNGYtMzBlOGQxYWRjYTE5OjRhYzQzMWY1LTE2ZmQtNGVkOC04MzQyLTQ2MGJhYTFjMzliYyIsImF1ZCI6Ii9hcGkvY2xvdWQvcmVnaXN0cmF0aW9ucy82ZWNkZTA5OS04NzdmLTQxMTgtYWFjYy0yYTE5ZmU4MzBkMDQiLCJzdWIiOiIvYXBpL3VzZXItcmVnaXN0cmllcy9mNDFhNTM5ZS1hNzIxLTRlN2MtYTA4Yi05NWZkMzRkZDJjN2IvYzIwYWNhOWMtYjEwNS00MGQ4LThmNGYtMzBlOGQxYWRjYTE5L3VzZXJzLzRhYzQzMWY1LTE2ZmQtNGVkOC04MzQyLTQ2MGJhYTFjMzliYyIsImlzcyI6IklCTSBBUEkgQ29ubmVjdCIsImV4cCI6MTU2ODY3MDI1NiwiaWF0IjoxNTY4NjQxNDU2LCJndmFudF90eXBlIjoicGFzc3dvcmQiLCJ1c2VyX3JlZ2lzdHJ5X3VybCI6Ii9hcGkvdXNlci1yZWdpc3RyaWVzL2Y0MWE1MzllLWE3MjEtNGU3Yy1hMDhiLTk1ZmQzNGRkMmM3Yi9jMjBhY2E5Yy1iMTA1LTQwZDgtOGY0Zi0zMGU4ZDFhZGNhMTkiLCJyZWFsbSI6InByb3ZpZGVyL2RlZmF1bHQtaWRwLTIiLCJ1c2VybmFtZSI6ImNocmlzcCIsImlkX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5Sm1hWEp6ZEY5dVlXMWxJam9pUTJoeWFYTWlMQ0pzWVhOMFgyNWhiV1VpT2lKUWFHbHNiR2x3Y3lJc0luVnpaWEpmYVdRaU9pSTFNV1F3T0RFNU9DMWhNREppTFRRelptUXRPR0ZqTlMxbFlqYzJZMlprTVRoaFpEVWlMQ0oxYzJWeWJtRnRaU0k2SW1Ob2NtbHpjQ0lzSW1saGRDSTZNVFUyT0RZME1UUTFObjAudlY4TmZLMkZjUVF3bFRGMTBYamttX3Y5RGVQNkJXMEl5QnZNaW45T1B3TSIsInNjb3BlcyI6WyJjbG91ZDp2aWV3IiwiY2xvdWQ6bWFuYWdlIiwicHJvdmlkZXItb3JnOnZpZXciLCJwcm92aWRlci1vcmc6bWFuYWdlIiwib3JnOnZpZXciLCJvcmc6bWFuYWdlIiwiZHJhZnwzOnZpZXciLCJkcmFmdHM6ZWRpdCIsImNoaWxkOnZpZXciLCJjaGlsZDpjcmVhdGUiLCJjaGlsZDptYW5hZ2UiLCJwcm9kdWN0OnZpZXciLCJwcm9kdWN0OnN0YWdlIiwicHJvZHVjdDptYW5hZ2UiLCJhcHByb3ZhbDp2aWV3IiwiYXBwcm92YWw6bWFuYWdlIiwiYXBpLWFuYWx5dGljczp2aWV3IiwiYXBpLWFuYWx5dGljczptYW5hZ2UiLCJjb25zdW1lci1vcmc6dmlldyIsImNvbnN1bWVyLW9yZzptYW5hZ2UiLCJhcHA6dmlldzphbGwiLCJhcHA6bWFuYWdlOmFsbCIsIm15OnZpZXciLCJteTptYW5hZ2UiLCJ3ZWJob29rOnZpZXciXX0.DxjqO00W47De9O9BS0ehTzAubDyxzx2YZvdHvYa4H-o",
    "token_type": "Bearer",
    "expires_in": 28800
}
```
