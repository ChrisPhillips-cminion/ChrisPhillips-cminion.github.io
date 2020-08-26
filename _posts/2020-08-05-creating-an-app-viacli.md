---
layout: post
date: 2020-8-5 00:12:00
categories: APIConnect
title: "Using the APIC CLI to create an application"
---

APIC can be fully driven by its CLI and Rest Interface
<!--more-->
To create an application you need a payload like

```json
{"title":"Jessica's Store","name":"store","redirect_endpoints":[]}
```

Then after logging in with the CLI  use the following command to create the application.

```bash
apic-slim apps:create -s <manager endpoint> -o <org> -c <ctalog> --consumer-org <consumer-org>  --debug
```

Please note that you need the `--debug` flag to retrieve the Client ID and Secret
