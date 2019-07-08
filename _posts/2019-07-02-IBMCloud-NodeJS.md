---
layout: post
date: 2019-07-02 01:00:00
categories: IBMCloud
title: "Publishing a NodeJS Application to IBM Cloud"
---

This article explains the basics for publishing a Node JS application to the IBM Cloud (Formally Bluemix). It assumes that you are already have an IBM ID that is used on IBM Cloud.

## Pre Reqs

1. An IBM ID that is connected to an IBM Cloud account
2. A Node JS Application exposing an HTTP(s) Interface
3. The package.json of the NodeJS Application includes the following
```javascript
"scripts": {
  "start": "node index.js"
}
```

## 1. Manifest file

In the root of the node js application create a manifest.yml

```yaml
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

The terms in the manifest are as explained below

| **Term**   | **Definition**  |
| buildpack |  The IBM Cloud buildpack to pull in |
| command   | The Shell command to execute the nodejs application   |
| instances   |   The number of instances to spin up |
| memory   | The amount of memory each instance should have.    |
| name   | The name of  your application. This is used to identify the application in the IBM Cloud interfaces  |
| routes   | The URL to access the application. Note the route must be unique and match the IBM Cloud you are routing to. |
|  Timeout | How long to wait for the applciation to start.  |


## 2. Update package.json

Ensure your package.json you have the following section.

```javascript
"engines": {
  "node": "12.x",
  "npm": "6.x"
}
```

This tells the BuildPack which version of node and npm to use. If this is not their it defaults to v6.

## 3. Push

Log into the cloud with
`ibmcloud login --sso` if you require logging in through your organization
or
`ibmcloud login`

Then push the application by running the following command in the directory with the manifest.yml file.
`ibmcloud cf push`

## Getting the logs
If you need to get the logs of your application then run the following command.
`ibmcloud cf logs ApplicationName --recent`
Remember to update ApplicationName to the name you set in the manifest.
