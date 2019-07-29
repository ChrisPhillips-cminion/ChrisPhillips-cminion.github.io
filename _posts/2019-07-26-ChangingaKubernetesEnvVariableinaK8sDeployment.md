---
layout: post
date: 2019-07-26 10:00:00
categories: Kubernetes
title: "Adding or Changing an ENV Variable in a Kubernetes Deployment"
draft: true
---

This is a very simple tasks but not one I do very often and I occasionally get the syntax wrong.

The scenario is  you need to modify the environmental variable of a Kuberentes Pod/Deployment. In order to do this you must edit the Deployment. Once this is saved a new pod is spawned and the old pod is terminated, this is repeated until all pods have been updated. If you create a syntax error k8s does not save the config change.

*Step 1* Run the following
```bash
kubectl edit deploy <deployment name> -n  <namespace>
```

Where deployment name is the name of the deplomyent you wish to change and namespaces is the namespace contianing the deployment.

*Step 2* Go to the env section of the deployment config

```yaml
eample: goes here
```

*Step 3* Add the variable using the following format. Ensure that the number of spaces is correct and it is added after the `env:` line.

```yaml
- name: environment variable name
  value: environment variable value
```

This should look similar to the below.

```yaml
example goes here
```

*Step 4* Save the file

If the file does not exit cleanly it is because kubernetes thinks there was a syntax error and you must go and make your change again.

*Step 5* Check the pods are being replaced, by running the following commmand
```bash
kubectl get po -n <namespace>  -w
```

`-w` triggers the watch function of kubernetes. When you hve finished watching press `ctrl+c` to exit.



Video
