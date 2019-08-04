---
layout: post
date: 2019-07-28 01:00:00
categories: Kubernetes
title: "Adding or Changing an ENV Variable in a Kubernetes Deployment"
---

This is a very simple task.  However one I occasionally get the syntax wrong for.

The scenario is you need to modify the environmental variable of a Kubernetes Pod/Deployment. In order to do this you must edit the Deployment. Once this is saved a new pod is spawned and the old pod is terminated. This is repeated until all pods have been updated. When modifying the deployment if you create a syntax error k8s does not save the config change.
<!--more-->

It is recommend to do this at the deploy level not the pod level so the changes are persisted.

*Step 1* Run the following
```bash
kubectl edit deploy <deployment name> -n  <namespace>
```

Where deployment name is the name of the deployment you wish to change and namespaces is the namespace contianing the deployment.

*Step 2* Go to the env section of the deployment config. If there is not an env section you can create one using with the key `env:` in each entry of the containers array.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.7.9
        ports:
        - containerPort: 80
```

*Step 3* Add the variable using the following format. Ensure that the number of spaces is correct and it is added after the `env:` line.

```yaml
- name: DEMO_FAREWELL
  value: "Such a sweet sorrow"
```

This should look similar to the below.

```yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.7.9
        ports:
        - containerPort: 80
        env:
        - name: DEMO_GREETING
          value: "Hello from the environment"
        - name: DEMO_FAREWELL
          value: "Such a sweet sorrow"
```

*Step 4* Save the file

If the file does not exit cleanly it is because Kubernetes thinks there was a syntax error and you must go and make your change again.

*Step 5* Check the pods are being replaced, by running the following command
```bash
kubectl get po -n <namespace>  -w
```

`-w` triggers the watch function of Kubernetes. When you have finished watching press `ctrl + c` to exit.


Samples taken from https://kubernetes.io
