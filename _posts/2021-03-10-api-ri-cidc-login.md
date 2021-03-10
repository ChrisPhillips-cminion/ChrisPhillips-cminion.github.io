---
layout: post
categories: APIConnect
date: 2021-03-10 00:15:00
title: Logging in via the CLI when using an OIDC registry in IBM Cloud

---
API Connect has a managed service offering call API Connect Reserved Instance. This uses the OIDC user registry provided by IBM Cloud to provide access.

<!--more-->

When logging in via the API Connect CLI to an instance using ODIC requires a the user getting token, normally this is done by a pop up asking for authorization.  However with a headless setup a pop up is not convenient. Ricky Moorhouse has written this great article on how to handle this with an OIDC registry on IBM Cloud.

[https://rickymoorhouse.uk/blog/2021/cicd-workaround/](https://rickymoorhouse.uk/blog/2021/cicd-workaround/)
