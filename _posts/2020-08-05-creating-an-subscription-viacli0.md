---
layout: post
date: 2020-8-5 00:13:00
categories: APIConnect
title: "Using the APIC CLI to create a subscription"
---

APIC can be fully driven by its CLI and Rest Interface
<!--more-->
To create an subsription you need a payload like

```json
{
  "product_url": "https://<manager url>/api/catalogs/<org>/<catalog>/products/<product id>",
  "plan": "default"
}
```

*The product ID can be retrieved by listing the products*



Then after logging in with the CLI  use the following command to create the application.

```bash
apic-slim subscriptions:create -a <application>  -c <catalog> -o <org> -s <manager url> --consumer-org <consumer org> <path to the payload file>
```
