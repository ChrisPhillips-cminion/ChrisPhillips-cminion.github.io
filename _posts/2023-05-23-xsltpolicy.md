---
layout: post
date: 2023-05-23 00:01:00
categories: APIConnect
title: "Custom Policy with xslt"
---

Recently I was asked to provide a sample custom policy for APIC that contained an XSLT.

<!--more-->

The policy below is a very basic sample. The XSLT can be updated and parameters added.

```yaml
policy: 1.0.0
info:
  title: SampleXLST Custom Policy
  name: sample-xslt-udp
  version: 1.0.0
  description: Example policy with an xslt policy
  contact:
    name: Chris Phillips
    url: 'https://chrisphillips-cminion.github.io/'
    email: chris.phillips@uk.ibm.com
attach:
  - rest
  - soap
gateways:
  - datapower-api-gateway
assembly:
  execute:
    - xslt:
        version: 2.1.0
        title: xslt
        input: false
        serialize-output: true
        source: |2-
              <xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
                <xsl:template match="/">
                  <Hello>World!</Hello>
                </xsl:template>
              </xsl:stylesheet>
```

Once this policy is created you need to zip up the yaml file and load it into APIC. This is loaded in the UI by going to the `Catalog(or space)->Settings->Gateway Serviecs->View Policies`

![image](/images/xslta)

Click on Upload

Drag and Drop the zip file into the first field.

![image](/images/xsltb)

The policy will now be listed in the Policy List.

![image](/images/xsltc)

If you have added this to the sandbox catalog when you go to drafts you will see the custom policy on the canvas.

![image](/images/xsltd)

A video on how to do this with a different policy will be published soon.
