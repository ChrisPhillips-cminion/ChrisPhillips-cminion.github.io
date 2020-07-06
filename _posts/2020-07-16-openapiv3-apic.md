---
layout: post
date: 2020-6-25 00:13:00
categories: APIConnect
title: "APIConnect v10 - Loading and Publishing an OpenAPI v3 specification. "
---

To publish OpenAPIv3 APIs into API Connect you need to add some IBM tags to add the assembly function and you need a product.



<!--more-->

This *hacky* script was built in order to quickly turn a stock OpenAPIv3 into all the artefacts required to publish into API Connect. This must be loaded via the APIConnect CLI.



```bash
#!/bin/bash
filename=$1

url=$(cat ${filename}.yaml | grep \\-\ url  | sed -e s/.*\\-\ url\://)
name=$(cat ${filename}.yaml | grep title:  | sed -e s/.*\:\ *// | sed s/[^a-zA-Z0-9]+/-/g | sed -e s/\ /-/g | tr A-Z a-z)


cp ${filename}.yaml ${filename}_apic.yaml

cat >>${filename}_apic.yaml <<EOF
x-ibm-configuration:
  testable: true
  enforced: true
  cors:
    enabled: true
  assembly:
    execute:
      - invoke:
          target-url: $url
          header-control:
            type: blacklist
            values: []
          parameter-control:
            type: whitelist
            values: []
          version: 2.0.0
EOF

sed -e 's/info:/info:\'$'\n  x-ibm-name: x-ibm-name-name/g' ${filename}_apic.yaml > ${filename}_apic2.yaml
sed -e "s/x-ibm-name-name/$name/g" ${filename}_apic2.yaml > ${filename}_apic.yaml
rm -rf  ${filename}_apic2.yaml

cat ${filename}_apic.yaml


cat >${filename}_product.yaml<<EOF
info:
  version: 1.0.0
  title: product
  name: product
gateways:
  - datapower-api-gateway
plans:
  default-plan:
    rate-limits:
      default:
        value: 100/1hour
    title: Default Plan
    description: Default Plan
    approval: false
apis:
  ${name}1.0.0:
    \$ref: ${filename}_apic.yaml
visibility:
  view:
    type: public
    orgs: []
    tags: []
    enabled: true
  subscribe:
    type: authenticated
    orgs: []
    tags: []
    enabled: true
product: 1.0.0
EOF
```
