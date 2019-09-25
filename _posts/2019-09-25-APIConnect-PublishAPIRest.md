---
layout: post
date: 2019-25-12 01:00:00
categories: API Connect
title: "Publishing a product using the APIC Rest interface"
draft: true
author: ["ChrisPhillips","sachinkj"]
---
When using the API Connect REST interface  you need to identify yourself with a bearer token. See the earlier post for steps to generate bearer token.
<!--more-->
### Things you need for this API
1. OpenAPI Product definition for the product you want to publish.
2. OpenAPI API definition for the API included in the product.
3. bearer token
### Sample product yaml file
To request a token you generate the following payload.
```yaml
info:
  name: test1
  title: test1
  version: 1.0.0
gateways:
  - datapower-gateway
plans:
  default-plan:
    rate-limits:
      default:
        value: 100/1hour
    title: Default Plan
    description: Default Plan
    approval: false
apis:
  tests1.0.0:
    name: tests:1.0.0
visibility:
  view:
    type: public
    orgs: []
    enabled: true
  subscribe:
    type: authenticated
    orgs: []
    enabled: true
product: 1.0.0
````
Note that api ref in product defintion is using via  name: <apiname>:<apiversio>  instead of $ref which is added by default when using apic toolkit or api manager  to generate the API.
### Sample api yaml file
To request a token you generate the following payload.
```yaml
swagger: '2.0'
info:
  title: tests
  x-ibm-name: tests
  version: 1.0.0
host: $(catalog.host)
schemes:
  - https
basePath: /debutests
produces:
  - application/json
consumes:
  - application/json
security:
  - {}
securityDefinitions:
  clientSecret:
    type: apiKey
    name: X-IBM-Client-Secret
    in: header
  clientID:
    type: apiKey
    in: header
    name: X-IBM-Client-Id
x-ibm-configuration:
  cors:
    enabled: true
  gateway: datapower-gateway
  type: rest
  phase: realized
  enforced: true
  testable: true
  assembly:
    execute:
      - proxy:
          title: proxy
          version: 1.0.0
          verb: GET
          target-url: $(target-url)
  properties:
    target-url:
      value: 'http://<APIHOST>/api/path'
      description: The URL of the target service
      encoded: false
  application-authentication:
    certificate: false
  catalogs: {}
definitions:
  output-data:
    type: object
    additionalProperties: false
    properties:
      message:
        type: string
        description: sdfsdf
        example: 1ssfs
      cardno:
        type: integer
        description: asdaad
        example: '1312313'
      data:
        $ref: '#/definitions/mydata-list'
        properties: {}
        description: data list
  mydata-list:
    type: array
    items:
      $ref: '#/definitions/mydata'
  mydata:
    type: object
    additionalProperties: false
    properties:
      transactid:
        type: string
        description: Transaction id
        example: PT1231231312312
      otpmessage:
        type: string
        description: otp message
        example: OTP has been send t 412312341
paths:
  /testpath:
    get:
      parameters: []
      responses:
        '200':
          description: aasda
          schema:
            $ref: '#/definitions/output-data'
      consumes: []
      produces: []
````
This Payload is POSTed to `https://<APIMHOST>/api/catalogs/<ORG_NAME>/<CATALOG_NAME>/stage`
*Curl Sample to publish the Product *
```bash
curl -X POST -v -k -H 'Accept: application/json' -H "Authorization: bearer <BEARER_TOKEN>" -H "Content-Type: multipart/form-data" -F "product=@/home/sachin/test_product_1.0.0.yaml;type=application/yaml" -F "openapi=@/home/sachin/test_api_1.0.0.yaml;type=application/yaml" https://<APIMHOST>/api/catalogs/<ORG_NAME>/<CATALOG_NAME>/stage
```
*Sample response*
```json
{
    "type": "product",
    "api_version": "2.0.0",
    "id": "123b78c0-37bb-457c-9bc9-3d91e2b655bb",
    "name": "test1",
    "version": "1.0.0",
    "title": "test1",
    "state": "staged",
    "scope": "catalog",
    "gateway_types": [
        "datapower-gateway"
    ],
    "api_urls": [
        "https://<APIMHOST>/api/catalogs/9B576e07-4c7e-40d2-b9cf-d163ce7bdf45/63c6f8cc-1769-4498-93ed-9e1b96658ea4/apis/dfbdea96-2a54-4f0f-921e-866c935d30a7"
    ],
    "gateway_service_urls": [
        "https://<APIMHOST>/api/catalogs/9b576e07-4c7e-40d2-b9cf-d163ce7bdf45/63c6f8cc-1769-4498-93ed-9e1b96658ea4/configured-gateway-services/f741232a-9a7d-4758-a355-89a6cdd0c4aa"
    ],
    "oauth_provider_urls": [],
    "visibility": {
        "view": {
            "type": "public",
            "enabled": true
        },
        "subscribe": {
            "type": "authenticated",
            "enabled": true
        }
    },
    "task_urls": [],
    "created_at": "2019-09-25T12:43:42.725Z",
    "updated_at": "2019-09-25T12:43:42.725Z",
    "org_url": "https://<APIMHOST>/api/orgs/9b576e07-4c7e-40d2-b9cf-d163ce7bdf45",
    "catalog_url": "https://<APIMHOST>/api/catalogs/9b576e07-4c7e-40d2-b9cf-d163ce7bdf45/64c6f8cc-1769-4498-93ed-9e1b96658ea4",
    "url": "https://<APIMHOST>/api/catalogs/9ba576e07-4c7e-40d2-b9cf-d163ce7bdf45/63c6f8cc-1769-4498-93ed-9e1b96658ea4/products/255b78c0-37bb-457c-9bc9-3d91e2b655bb"
* Connection #0 to host <APIMHOST> left intact
}
```
