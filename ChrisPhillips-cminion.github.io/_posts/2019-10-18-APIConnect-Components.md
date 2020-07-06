---
layout: post
date: 2019-10-17 00:01:00
categories: APIConnect
title: APIConnect Component Interactions
---

API Connect has four core components.

-   API Manager
-   API Gateway (DataPower)
-   Developer Portal
-   Analytics
    <!--more-->

For information on each component please read my API Connect Deployment WhitePaper (https://www.ibm.com/downloads/cas/30YERA2R)[https://www.ibm.com/downloads/cas/30YERA2R]

The table below describes which components communicate and how the communiation is secured.

| From                    | To                      |     | Mutual TLS (SSL) | Single TLS  (SSL) | Oauth |     |
| ----------------------- | ----------------------- | --- | ---------------- | ----------------- | ----- | --- |
| API Manager             | Analytics               |     | Y                |                   |       |     |
| API Manager             | API Gateway (DataPower) |     | Configurable     |                   |       |     |
| API Manager             | Portal                  |     | Y                |                   |       |     |
| API Gateway (DataPower) | API Manager             |     |                  | Y                 | Y     |     |
| API Gateway (DataPower) | Analytics               |     | Y                |                   |       |     |
| Developer Portal        | API Manager             |     |                  | Y                 | Y     |     |

Inside each component the communication is secured with with mtls.
