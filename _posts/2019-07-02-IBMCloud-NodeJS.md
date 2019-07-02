---
layout: post
date: 2019-07-01 01:00:00
categories: IBMCloud
title: "Publishing a NodeJS Application to IBM Cloud"
draft: true
---

This article explains the basics for publishing a Node JS application to the IBM Cloud (Formally Bluemix). It assumes that you are already have an IBM ID that is used on IBM Cloud.

## Pre Reqs

1. Have an IBM ID that is connected to an IBM Cloud account
2. Have an http service Node JS Implementation that starts with npm `start`.


## 1. Manifest file

In the root of the node js application create a manifest.yml

```
applications:
- buildpack: sdk-for-nodejs_v3_27-20190530-0937
  command: npm start
  instances: 1
  memory: 256MB
  name: applicationName
  routes:
  - route: applicationName.us-south.cf.appdomain.cloud
  timeout: 180
```

Note the route must be unique and match the IBM Cloud you are routing to.

ApplicationName should be updated to match the name of your node application.

## 2. Update package.json

Ensure your package.json you have the following section.

```
"engines": {
  "node": "12.x",
  "npm": "6.x"
}
```

This tells the BuildPack which version of node and npm to use. If this is not their it defaults to v6.

## 3. Push

Log into the cloud with
`ibmcloud login --sso`
or
`ibmcloud login`

Then push the application by running the following command in the directory with the manifest.yml file.
`ibmcloud cf push`

## Getting the logs
If you need to get the logs of your application then run the following command.
`bx cf logs ApplicationName --recent`
Remember to update ApplicationName to the name you set in the manifest.
