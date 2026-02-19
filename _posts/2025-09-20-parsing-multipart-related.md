---
layout: post
date: 2025-09-19 09:00:00
categories: APIConnect
title: "Parsing multipart/related without gateway script"
author: ["ChrisPhillips"]
description: "Learn how to parse multipart/related content in IBM API Connect without using GatewayScript. Includes practical examples and alternative approaches for handling complex MIME types."
tags: [APIConnect, DataPower, MIME, multipart, API Gateway, Integration, HTTP]
---

It is possible to parse an API request that has a `multipart/related` content type without using gateway script.

The key thing here is having two parses.

![alt text](/images/two-parse-json-xml.png)
<!--more-->

The first parse extracts the multipart data and puts each entry into an array called message.attachment.

In a second parse we tell the assembly to parse the contents of one of the attachments.
```
      - parse:
          version: 2.2.0
          title: parse
          parse-settings-reference:
            default: apic-default-parsesettings
          use-content-type: false
          input: message.attachments[0]
```

`message.attachments[0]` will now be parsed. This can be referenced like below in other policies.

```
      - json-to-xml:
          version: 2.0.0
          title: json-to-xml
          root-element-name: json
          always-output-root-element: false
          unnamed-element-name: element
          input: message.attachments[0]
          output: message.attachments[0]
```

**Full Sample API**
```yaml
swagger: '2.0'
info:
  version: 1.0.0
  title: multipartparse
  x-ibm-name: multipartparse
basePath: /multipartparse
x-ibm-configuration:
  cors:
    enabled: true
  gateway: datapower-api-gateway
  type: rest
  phase: realized
  enforced: true
  testable: true
  assembly:
    execute:
      - parse:
          version: 2.2.0
          title: parse
          parse-settings-reference:
            default: apic-default-parsesettings
          use-content-type: false
      - parse:
          version: 2.2.0
          title: parse
          parse-settings-reference:
            default: apic-default-parsesettings
          use-content-type: false
          input: message.attachments[0]
      - json-to-xml:
          version: 2.0.0
          title: json-to-xml
          root-element-name: json
          always-output-root-element: false
          unnamed-element-name: element
          input: message.attachments[0]
          output: message.attachments[0]
  activity-log:
    enabled: true
    success-content: activity
    error-content: payload
paths:
  /:
    get:
      responses:
        '200':
          description: success
          schema:
            type: string
      consumes: []
      produces: []
    put:
      responses:
        '200':
          description: success
          schema:
            type: string
      consumes: []
      produces: []
    post:
      responses:
        '200':
          description: success
          schema:
            type: string
      consumes: []
      produces: []
    delete:
      responses:
        '200':
          description: success
          schema:
            type: string
      consumes: []
      produces: []
    head:
      responses:
        '200':
          description: success
          schema:
            type: string
      consumes: []
      produces: []
    patch:
      responses:
        '200':
          description: success
          schema:
            type: string
      consumes: []
      produces: []
securityDefinitions: {}
security:
  - {}
schemes:
  - https
```

**Sample Curl Command**
```
curl -v -F key1=@manifest.json -F upload=@dotdot.json   https://mydatapower/dev/sandbox/multipartparse/ -k -H "content-type: multipart/related"
```