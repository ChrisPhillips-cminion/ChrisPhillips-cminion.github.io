---
layout: post
date: 2023-10-11 01:00:00
categories: APIConnect
title: "API Connect Health Check Endpoints to monitor system stability"
---
As an API Connect platform management team being able to confirm the API Manager and Gateway are working as expected is critical. The API Manager and the Gateway both have key endpoints that should be monitored to determine platform health.
<!--more-->

## API Gateway
When the API Gateway comes up the network interfaces are enabled before the API Content is available. To detect when the APIs are available it is best to health check `https://apigw:9443/webapi-init-check` as this will respond with a 200 when APIs are ready to be served.

For more info
[https://www.ibm.com/support/pages/how-properly-health-check-api-connect-gateway](https://www.ibm.com/support/pages/how-properly-health-check-api-connect-gateway)

## API Management
To do a deep health check against the API Manager you need to validate the database is working. The API Manager exposes a single API that queries the database without requiring login credentials to be provided.
`https://platformapi.apic/api/cloud/admin/identity-providers`

For more info
[https://chrisphillips-cminion.github.io/apiconnect/2023/06/29/deephealthcheck.html](https://chrisphillips-cminion.github.io/apiconnect/2023/06/29/deephealthcheck.html)

## Errors
When reviewing pods for errors the most important pod to look in is the API Connect Operator. Look at the log for messages published with the error level. Please note benign errors will appear in here during the install, and this is expected. Not every error is a reason for a PMR.
