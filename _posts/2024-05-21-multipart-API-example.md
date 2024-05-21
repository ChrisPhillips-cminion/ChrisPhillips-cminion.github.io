---
layout: post
date: 2024-05-21 21:00:00
categories: APIConnect
title: "MultiPart APIs - Part 2 - Example use "
draft: true
---

In Part 1 we discussed what a multipart API was and how it can be parsed in API Connect. In this part we will take that knowledge and apply it to a real situation.


*Scenario*: I want to upload two images, validate that the images are png and that the size is less then 1MB.

<!--more-->


IMAGE OF ASSSEMBY

In the Gatewayscript we can use the following
```javascript
var data  = context.get('message')
if (data.attachments[0].headers['Content-Type'] != 'image/png')
{
  context.reject('ImageTypeError', 'Invalid image type for first image');
  context.message.statusCode = '400 BadData';
}
else if  (data.attachments[0].body.length > 1024000) {
    context.reject('ImageSizeError', 'Invalid image size for first image, image larger then 1mb');
    context.message.statusCode = '400 BadData';    
}
else if (data.attachments[1].headers['Content-Type'] != 'image/png')
{
  context.reject('ImageTypeError', 'Invalid image type for second image');
  context.message.statusCode = '400 BadData';
}
else if  (data.attachments[1].body.length > 1024000) {
    context.reject('ImageSizeError', 'Invalid image size for second image, image larger then 1mb');
    context.message.statusCode = '400 BadData';    
}

```

We have two if statements to check both of the content types of the second file to be uploaded. We also have two if statements to validate the size of the image.

If any of those checks fail we reject the transaction otherwise it continues.

For a full sample please see the api below.

```yaml
swagger: '2.0'
info:
  title: ImageUploadtest
  x-ibm-name: imageuploadtest
  version: 1.0.0
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
          use-content-type: true
      - gatewayscript:
          version: 2.0.0
          title: gatewayscript
          source: >
            var data  = context.get('message')
            if (data.attachments[0].headers['Content-Type'] != 'image/png')
            {
              context.reject('ImageTypeError', 'Invalid image type for first image');
              context.message.statusCode = '400 BadData';
            }
            else if  (data.attachments[0].body.length > 1024000) {
                context.reject('ImageSizeError', 'Invalid image size for first image, image larger then 1mb');
                context.message.statusCode = '400 BadData';    
            }
            else if (data.attachments[1].headers['Content-Type'] != 'image/png')
            {
              context.reject('ImageTypeError', 'Invalid image type for second image');
              context.message.statusCode = '400 BadData';
            }
            else if  (data.attachments[1].body.length > 1024000) {
                context.reject('ImageSizeError', 'Invalid image size for second image, image larger then 1mb');
                context.message.statusCode = '400 BadData';    
            }
            context.clear('message.attachments');
  properties:
    target-url:
      value: http://example.com/operation-name
      description: The URL of the target service
      encoded: false
  activity-log:
    enabled: false
    success-content: activity
    error-content: payload
basePath: /imageuploadtest
paths:
  /:
    post:
      responses:
        '200':
          description: success
          schema:
            type: string
      consumes: []
      produces: []
schemes:
  - https

```
