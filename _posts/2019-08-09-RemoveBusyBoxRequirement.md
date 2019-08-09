---
layout: post
date: 2019-08-09 02:00:00
categories: APIConnect
title: "Deploying DataPower into Kubernetes without external internet access. "
draft: true
---

This is a work around to a problem I have seen a couple of times. I expect this problem to be fixed in the next release of APIConnect.
<!--more-->

When APICUP (the API Connect Installer) configures a DataPower Gateway to be deployed it internally generates a helm chart. This helm chart includes a stateful set that includes both an init container as well a the main container.  

Out of the box the DataPower init container is set to be a busy box image deployed on docker hub. Therefore if the environment that is being used to host the Kubernetes deployment does not have internet access then it fails.

In order to work around this problem follow these steps, where `<gateway name>` should be replaced by the gateway you are installing.

1. configure the install as normal up until the command `apicup subsys install <gateway name>` .
2. Instead run
```
apicup subsys install <gateway name> --out chart-<gateway name>
```
This generates the Helm chart in the `chart-<gateway name>` directory but does not try and install it.
3. Install the secrets that are needed
```
kubectl apply -f chart-<gateway name>/secrets
```
4. extract the tar files from `chart-<gateway name>/helm` but do not delete the original tar.
```
tar zxvf chart-dp/helm/dynamic-gateway-service-1.0.27.tgz
```
5. grep the values file to retrieve the tag for the DataPower image .
```
cat dynamic-gateway-service/values.yaml  | grep tag
```
A sample response is below
```
tag: 2018.4.1.6-309660-release-prod
tag: 1.29-glibc
```

6. copy the tag line that matches the version of DataPower you wish to install, in this case `tag: 2018.4.1.6-309660-release-prod`

7. edit the `chart-<gateway name>/values/dynamic-gateway-service.yml` and add the copied tag line to the `datapower.busybox` section

8. in `chart-<gateway name>/values/dynamic-gateway-service.yml` values file replace `datapower.busybox.repository` with `datapower.image.repository`
9. Now install DataPower with the following command.
```
helm install <gateway name> chart-<gateway name>/helm/dynamic-gateway-service*.tgz -f chart-<gateway name>/values/dynamic-gateway-service
```

[![asciicast](https://asciinema.org/a/KdpZDyyOEJBauXkXXwbH6gChK.svg)](https://asciinema.org/a/KdpZDyyOEJBauXkXXwbH6gChK)
