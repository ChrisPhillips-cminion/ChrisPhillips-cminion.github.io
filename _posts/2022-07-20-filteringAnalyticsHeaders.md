---
layout: post
categories: APIConnect
date: 2022-07-20 00:14:00
title: Filtering headers from the Analytics data on ingestion.
author: ["thomaswilkinson","chrisphillips"]
---

If header logging is enabled all headers are logged into Analytics. However clients usualy do not want to have the client secret stored.

<!--more-->

By applying the sample below into the Analytics Cluster CR it will filter any headers that contain `X-IBM-Client-Secret` or `X-Also-Hide-This`

```yaml
spec:
  ingestion:
    filter: |
      if [request_http_headers] {
        ruby {
          code => "headers=['X-ibm-client-secret','X-Also-Hide-This']; newHeaders = event.get('[request_http_headers]').collect {|i| headers.each {|header| i[header] = '********sanitized********' if i.has_key?(header)}; i}; event.set('[request_http_headers]', newHeaders)"
        }
      }
```
