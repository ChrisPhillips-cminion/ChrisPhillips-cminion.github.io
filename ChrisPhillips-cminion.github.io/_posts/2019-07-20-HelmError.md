---
layout: post
date: 2019-07-20 01:00:00
categories: Kubernetes
title: "Helm ERROR 'User \"system:serviceaccount:kube-system:default\" cannot get namespaces in the namespace '\"default\"'"

---
<!--more-->

Trying to use a new k8s instance with helm deploying to the default namespace to test an idea.

I got this ERROR
```
User "system:serviceaccount:kube-system:default" cannot get namespaces in the namespace "default
```

This means that there is no service account to allow helm (tiller) permission to deploy to the default namespace.

To fix run the following

```
kubectl create serviceaccount --namespace kube-system tiller
kubectl create clusterrolebinding tiller-cluster-rule --clusterrole=cluster-admin --serviceaccount=kube-system:tiller
kubectl patch deploy --namespace kube-system tiller-deploy -p '{"spec":{"template":{"spec":{"serviceAccount":"tiller"}}}}'
```

Thanks to this post for the solution, just reposting it so I can find it quicker next time.

https://github.com/fnproject/fn-helm/issues/21
