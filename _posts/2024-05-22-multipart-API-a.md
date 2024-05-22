---
layout: post
date: 2024-05-22 21:00:00
categories: APIConnect
title: "MultiPart APIs - Part 1 - What are they? How can I access the elements in API Connect."

draft: true
---

MultiPart API calls allow multiple set of data to be set to an API as individual items. If you have a series of images and text you need to upload you could write a curl command similar to

`curl -vk -F 'name=fred' -F "name2=@image.png" https://APIURL/ -H "content-type: multipart/related"`


<!--more-->
This would generate a payload similar to

```
--------------------------HonVo683Z8qiA5OPd5X6DU
Content-Disposition: attachment; name="name"
Content-Type: text/plain
Content-Transfer-Encoding: binary

fred
--------------------------HonVo683Z8qiA5OPd5X6DU
Content-Disposition: attachment; name="name2"; filename="image.png"
Content-Type: image/png

�PNG BINARY DATA


--------------------------HonVo683Z8qiA5OPd5X6DU--
```


In API Connect you can handle these kind of requests.

In the Assembly we first must add a Parse policy. This will take in the payload and set the first entry to be the `message.body` and `message.headers`. Each subsequent part added to the attachment array on the message object.

An example of the message object is below.
```json
{
  "variables": {},
  "headers": {
    "Content-Disposition": "attachment; name=\"name\"",
    "Content-Type": "text/plain"
  },
  "original": {
    "headers": {
      "Host": "small-host.cloud",
      "user-agent": "curl/8.4.0",
      "accept": "*/*",
      "content-length": "764184",
      "content-type": "multipart/related; boundary=------------------------IahqzsqopMSgmN4Z0O9adR"
    }
  },
  "status": {},
  "body": "fred",
  "attributes": {
    "fromClient": true
  },
  "package": {
    "headers": {
      "user-agent": "curl/8.4.0",
      "accept": "*/*",
      "content-length": "764184",
      "content-type": "multipart/related; boundary=------------------------IahqzsqopMSgmN4Z0O9adR",
      "X-Client-IP": "172.30.138.5",
      "X-Global-Transaction-ID": "a1ab7cdb664d1d9f00009760"
    },
    "boundary": "------------------------IahqzsqopMSgmN4Z0O9adR"
  },
  "attachments": [
    {
      "headers": {
        "Content-Disposition": "attachment; name=\"name2\"; filename=\"image.png\"",
        "Content-Type": "image/png"
      },
      "body": "�PNG\r\n\u001a\n"
    }
  ]
}
```


So we can access these fields in gateway script and validate the data - see Part 2 for an example.
