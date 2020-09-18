---
layout: post
date: 2020-9-18 00:13:00
categories: APIConnect
title: "Pipelines :: How and why to use them to deploy Products and APIs into API Connect "
---

_*Pipelines are an in fashion*._ They provide an important part of a modern development approach. A typical pipeline takes artefacts from git, builds and then deploys them.  Customers often ask for advice on how to create nd build pipeline for API Connect.  Pipelines combine the stages of automated build, linting/syntax testing, continuous/automated deploy and continuous/automated testing.  I will go through each of these stages and explain how to apply them to API Connect
​

<!--more-->
_This article is about API Connect, however it does not specify any particular pipeline technolgy._
​
## Automated Build
​
API Connect publishes products that encapsulate one or more APIs. Products and APIs are each represented as a YAML file. These YAML files can be published directly and do not need to be built.
​
However, some users like to augment environment variables in hte yaml files during the build process. For example updating target endpoints for different environments.  Even then, this is not essential because this can also be done using catalog level properties which may be more appropriate depending on the use case.
​
If this behaviour is required at the build stage it can be achieved using a simple script to replace key words in the YAML.
​
## Linting / Syntax Testing
​
The initial purpose of Linting is check what we are trynig to load into API connect is valid. There purpose has grown from just validating the sturcture to ensuring that business  governance standards are met.

Linting is the process of validating the YAML files prior to deploying them into API Connect. Linting does two main functions:
​
*Syntactically:*

​* Is it valid YAML/JSON?
* Is it valid OpenAPI 2/3/3.1?

*Governance:*
Additional rules can be written to validate the files in any way necessary e.g.
​
* Validate examples are set
* Validated paths fit the corporate guidelines
* Validate that descriptions are populated, and free of spelling mistakes
​
A future article will provide more detail on this topic and examples.
​
​
## Continuous or Automated Deployment
​
Once the YAML is validated it can be deployed into API Connect. API Connect provides both a REST interface and a command line utility for loading YAML files into into API Connect.
​
To use the CLI you must first login with:
​
```
apic login -s <server> -u <user> -p <password> --realm <realm>
```
​
​
Then the product can be published to a catalog with the following:
​
```
apic  publish:create <path to product yaml file> -s <server> -o <provider org> -c <catalog>  
```
​
Or to a space in side a catalog with :
​
```
apic  publish:create <path to product yaml file> -s <server> -o <provider org> -c <catalog> --scope space --space <space>
```

To use the REST interface see the following articles.
* [https://chrisphillips-cminion.github.io/apiconnect/2019/09/20/RegistringAppsToUseTheAPICCLI.html](https://chrisphillips-cminion.github.io/apiconnect/2019/09/20/RegistringAppsToUseTheAPICCLI.html)
* [https://chrisphillips-cminion.github.io/apiconnect/2019/09/18/GettingoAuthTokenFromAPIC.html](https://chrisphillips-cminion.github.io/apiconnect/2019/09/18/GettingoAuthTokenFromAPIC.html)
* [https://chrisphillips-cminion.github.io/apiconnect/2019/09/26/APIConnect-PublishAPIRestStaging.html](https://chrisphillips-cminion.github.io/apiconnect/2019/09/26/APIConnect-PublishAPIRestStaging.html)
​
​
## Continuous or automated testing.
​
This phase of testing should validate that the messages being sent to and the responses received from the API are correct. There are several strategies for testing on the context of continuous delivery which are widely documented and are beyond the scope of this document. The key principle to follow is the testing should not require human intervention, and test failures as well as the golden path.
​
## Conclusion
​
In this article we cover the key parts of a pipeline in a tool-agnostic way. Though pipelines will not contain all of these sections in their first version, in order to get the most from pipeline delivery all of these steps should be implemented.
