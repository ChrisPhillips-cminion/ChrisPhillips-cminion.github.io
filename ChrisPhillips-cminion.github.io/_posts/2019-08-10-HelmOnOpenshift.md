---
layout: post
date: 2019-08-10 12:00:00
categories: OpenShift
title: "Setting up Helm v2.x on OpenShift"
---

Helm is the de facto standard for deploying to Kubernetes. OpenShift does not ship with helm but instead provides their own system called Templates. Thus far I have never used OpenShift Templates and so I focus on helm. This article does not go through the differences but just shows how to get helm v2 up and running.

<!--more-->

These instructions assume that the worker node can reach docker hub.

1. Download from github [https://github.com/helm/helm/releases](https://github.com/helm/helm/releases)
2. Extract the tar `tar zxvf helm-v2*gz`
3. Move helm to the usr local bin `cp */helm /usr/local/bin`
4. Change permissions on the executable `chmod 755 /usr/local/bin/helm`
5. run `helm vesion`  to check that it is installed correctly. A sample response is below
```yaml
Client: &version.Version{SemVer:"v2.14.3", GitCommit:"0e7f3b6637f7af8fcfddb3d2941fcc7cbebb0085", GitTreeState:"clean"}
Error: Get http://localhost:8080/api/v1/namespaces/kube-system/pods?labelSelector=app%3Dhelm%2Cname%3Dtiller: dial tcp [::1]:8080: connect: connection refused
```
The error is because there is no server side component installed yet.
6.  Log into the OpenShift via the Cli `oc login https://<webconsole host and port> ` if this works correctly it will display a list of projects
9. Run `helm init` this deploys the tiller pods to the kube-system namespace.
10. Running  `helm ls` will get an error message similar to the below if you have not configured the user role.
```
Error: configmaps is forbidden: User "system:serviceaccount:kube-system:default" cannot list configmaps in the namespace "kube-system": no RBAC policy matched
```
11. I have already blogged how to fix this issue [https://chrisphillips-cminion.github.io/kubernetes/2019/07/20/HelmError.html](https://chrisphillips-cminion.github.io/kubernetes/2019/07/20/HelmError.html)

*TLDR*
```bash
kubectl create serviceaccount --namespace kube-system tiller
kubectl create clusterrolebinding tiller-cluster-rule --clusterrole=cluster-admin --serviceaccount=kube-system:tiller
kubectl patch deploy --namespace kube-system tiller-deploy -p '{"spec":{"template":{"spec":{"serviceAccount":"tiller"}}}}'
```
Please note you may want to consider a different role to bind then cluster-admin for production systems .

12. Now to test it run `helm version` and you should got a response similar to the below
```yaml
Client: &version.Version{SemVer:"v2.14.3", GitCommit:"0e7f3b6637f7af8fcfddb3d2941fcc7cbebb0085", GitTreeState:"clean"}
Server: &version.Version{SemVer:"v2.14.3", GitCommit:"0e7f3b6637f7af8fcfddb3d2941fcc7cbebb0085", GitTreeState:"clean"}
```
